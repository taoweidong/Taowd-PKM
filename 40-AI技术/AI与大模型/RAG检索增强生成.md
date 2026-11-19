---
title: RAG检索增强生成
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI/大模型
  - RAG
  - 检索增强生成
  - 向量检索
aliases:
  - RAG
  - 检索增强生成
source: 网络资料整理
---

# RAG检索增强生成

> [!摘要] 摘要
> **RAG（Retrieval-Augmented Generation，检索增强生成）** 是把"外部知识检索"与"大模型生成"结合的经典范式：先从知识库中检索与问题相关的内容，再将其作为上下文交给大模型生成有据可依的回答。本文覆盖 RAG 的**最新生态动态（截至 2026-11）**、基础概念、核心机制、可运行的实践步骤、最佳实践与常见坑，定位为 [[AI与大模型-从入门到精通]] 体系中"知识落地"的关键一环，适合从零搭建知识库问答的开发者。

## 一、最新动态（截至 2026-11）

RAG 框架与底层基础设施迭代极快，以下版本与日期均来自调研文件，生产使用前请以官方仓库当日状态复核。

- **LangChain / LangGraph**：LangChain **v1.0 GA** 以 `create_agent` 作为构建 Agent 的标准方式；**LangChain v1.4.3（2026-09-28 发布）**；**LangGraph v1.1.0（2026-03-10）** 引入 `version="v2"` 的类型安全 stream/invoke，当前最新 1.2.18。RAG 组件随 v1 持续演进，但 v1 重写存在破坏性变更历史，建议**锁定版本**。来源：[LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)
- **LlamaIndex v0.14.23（2026-06-24）** 为当前最新稳定线，以"数据/索引为中心"提供 RAG 的解析、切分、向量索引与查询引擎。来源：[LlamaIndex 版本列表](https://security.snyk.io/package/pip/llama-index/versions)
- **向量数据库**：**Milvus 3.0 于 2026-07-16 官宣 GA**（Apache 2.0，支持 K8s/Docker，提供 Python/Go/Node SDK）；Qdrant 稳定线 1.18.x；Weaviate 稳定线 1.38.x。来源：[Milvus 相关选型资料](https://cloud.vk.ru/blog/vektornie-bazi-dannikh-dlya-rag-kak-vibrat-dvizhok-i-podnyat-odrant-v-vk-cloud/)
- **嵌入模型**：OpenAI `text-embedding-3-small`（1536 维）/ `text-embedding-3-large`（3072 维，支持 Matryoshka 维度裁剪）；Gemini Embedding 2 在 4K–32K 全长度区间评分 1.000；自托管可选 BGE-M3。来源：[选择嵌入模型的 RAG 指南](https://blog.milvus.io/zh-hant/blog/choose-embedding-model-rag-2026.md)
- **推理引擎**：vLLM **v0.34.0（2026-11-15）**、SGLang **v0.5.23（2026-10-30）** 为 RAG 的在线生成阶段提供高吞吐服务，SGLang 的前缀复用（radix cache）尤其适合 RAG 高前缀重叠场景。来源：[vLLM Releases](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)、[SGLang Releases](https://github.com/sgl-project/sglang/releases)

## 二、基础概念

**定义**：RAG 在生成前先检索外部知识，把检索结果注入提示，从而让模型基于"可核实的资料"作答，而非仅依赖参数化记忆。原始论文为 Lewis 等《Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks》（arXiv:2005.11401），首次系统提出该框架。来源：[RAG 原始论文](https://arxiv.org/abs/2005.11401)

**解决的问题**：

- **幻觉**：模型脱离事实时编造内容，检索接地可显著降低虚构。
- **知识时效**：模型权重更新慢，检索可接入实时/最新文档。
- **私有知识**：企业内网、个人笔记无法进入训练语料，检索是天然入口。
- **可溯源**：回答可附带引用来源，便于人工核查。

**与其它方案的边界**：

| 方案 | 作用 | 与 RAG 的关系 |
| --- | --- | --- |
| 微调（LoRA/QLoRA） | 教模型"怎么说、按什么格式" | 适合固化风格与领域表达，不替代知识更新 |
| 长上下文 | 直接把资料塞进提示 | 成本高、注意力稀释，适合短资料；长资料仍优先 RAG |
| 纯 Prompt 工程 | 优化指令与输出约束 | 与 RAG 互补，不解决知识缺失 |

> [!tip] 核心认知
> RAG 的**上限由检索质量决定**：检索不到或排序错误，再好的模型也只能"在错误资料上生成"。

## 三、核心机制

RAG 的完整链路是五步：**切分 → 向量化 → 索引 → 检索 → 生成**。

1. **切分（Chunking）**：把长文档切成语义完整的片段。粒度过粗引入噪声、过细丢失上下文，需按文档类型权衡，并保留重叠（overlap）避免边界截断。
2. **向量化（Embedding）**：用嵌入模型把每个片段编码为稠密向量，语义相近的片段在向量空间中距离更近。
3. **索引（Index）**：将向量写入向量数据库或可检索结构，按规模选择内存型 / 磁盘型 / 云托管。
4. **检索（Retrieval）**：将用户问题编码后在索引中做相似度检索，常叠加以下优化：
   - **混合检索**：向量检索 + BM25 关键词检索互补，再用 **RRF（Reciprocal Rank Fusion）** 融合排序，兼顾语义与精确词匹配。
   - **查询改写**：把口语化问题改写成更利于检索的表述，提升召回。
   - **重排序（Rerank）**：用交叉编码器对召回结果二次精排，提升 Top-k 精度。
5. **生成（Generation）**：把检索到的片段拼入提示，交给大模型生成，并尽量要求**引用来源**。进阶可用**上下文工程**精简注入内容、减少噪声，或用 **Agentic RAG** 先检索再判断是否补充检索，支持多跳问答。

> [!note] 机制要点
> 检索质量（切分、重排、查询改写）与生成质量需**分开评估**，二者是串联关系，不能只看最终回答好坏。

## 四、实践步骤（含代码/命令示例）

**1. 安装依赖**

```bash
python --version        # 建议 Python 3.11+
pip install sentence-transformers numpy
# 使用框架时：
pip install langchain langgraph
pip install llama-index
pip install pymilvus      # 或 qdrant-client、pgvector
```

**2. 最小可运行的 RAG 流程（切分 → 向量化 → 索引 → 检索 → 生成）**

```python
"""最小可运行 RAG：检索 + 组装上下文（生成处替换为你的模型客户端）"""
import numpy as np
from sentence_transformers import SentenceTransformer

# 1) 载入嵌入模型（中文场景可选 BAAI/bge-small-zh-v1.5 或 BGE-M3）
encoder = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# 2) 切分后的文档片段
chunks = [
    "RAG 通过引入外部知识检索，缓解大模型的幻觉问题。",
    "切分粒度过粗会引入噪声，过细则丢失上下文，需要平衡并保留重叠。",
    "向量检索常用余弦相似度，可结合 BM25 做混合检索后再用重排模型精排。",
]

# 3) 向量化并建立索引（归一化后余弦相似度退化为点积）
embeddings = encoder.encode(chunks, normalize_embeddings=True)

# 4) 检索：问题编码 -> 相似度排序 -> 取 Top-k
query = "如何缓解大模型的幻觉？"
q_emb = encoder.encode([query], normalize_embeddings=True)
scores = embeddings @ q_emb.T                       # (n_chunks, 1)
top_k = 2
idx = np.argsort(scores.flatten())[-top_k:][::-1]
retrieved = [chunks[i] for i in idx]

# 5) 组装上下文并生成（这里用占位，实际换成 LLM API / vLLM 接口）
context = "\n\n".join(retrieved)
prompt = (
    f"请根据以下资料回答问题，并标注引用。\n"
    f"资料：\n{context}\n\n问题：{query}\n回答："
)
print(prompt)
# answer = client.chat(prompt)   # 替换为实际调用
```

**3. 典型切分参数（写入配置文件）**

```yaml
# rag_chunking.yaml
chunk_size: 512          # 每个片段的目标长度
chunk_overlap: 64        # 相邻片段重叠，避免语义截断
separator: "\n\n"        # 优先按段落切，尽量不截断句子
min_chunk_length: 40     # 过短碎片合并，减少噪声
max_chunks_per_doc: 200  # 控制单文档检索噪声上限
```

**4. 用向量数据库落地（Milvus 为例）**

```bash
pip install pymilvus
```

```python
from pymilvus import MilvusClient

client = MilvusClient(uri="http://localhost:19530")
client.create_collection(
    collection_name="rag_chunks",
    dimension=1024,          # 与嵌入模型输出维度一致
    metric_type="COSINE",
)
client.insert("rag_chunks", data=[
    {"id": 1, "text": chunks[0], "vector": embeddings[0].tolist()},
])
hits = client.search("rag_chunks", data=[q_emb[0].tolist()], limit=2, output_fields=["text"])
```

## 五、最佳实践与常见坑

**最佳实践**

- **先优化源文档**：源文档结构混乱时，再高级的检索算法也救不回质量。优先保证文档结构清晰、语义自洽。
- **为检索设定独立 SLO**：建议定义 p95 检索延迟、**recall@k** 等指标，而非只盯最终回答质量，便于定位是检索还是生成的问题。
- **检索与生成分开评估**：建立测试集、指标与基线，每次改动可量化对照，避免"感觉变好了"。
- **引用可溯源**：要求模型标注引用片段，便于核查与追责。
- **框架选型匹配场景**：以数据/索引为中心选 LlamaIndex；偏 Agent 编排选 LangChain/LangGraph；大规模向量选 Milvus，轻量嵌入式选 LanceDB，PostgreSQL 生态选 pgvector。

**常见坑**

| 现象 | 可能原因 | 对策 |
| --- | --- | --- |
| 检索不到 / 不准 | 切分粒度不当、单一检索方式 | 调整切分，启用向量 + BM25 混合检索，再加 rerank |
| 召回内容冗余、噪声大 | 片段过粗、overlap 过大 | 缩小 `chunk_size`、调低 overlap，过滤过短碎片 |
| 回答仍幻觉 | 检索未命中、引用缺失 | 检查 recall@k，强制引用溯源与事实校验 |
| 延迟高 | 检索链路慢、生成未批处理 | 排查检索 SLO，生成侧用 vLLM 连续批处理与前缀缓存 |
| 版本不兼容 | LangChain/LangGraph/嵌入模型升级 | 锁定版本，升级前核对破坏性变更 |
| 维度不匹配 | 嵌入模型与向量库 `dimension` 不一致 | 建库时以嵌入模型输出维度为准，勿随意改动模型 |

> [!warning] 版本风险
> RAG 相关框架迭代极快，本文版本号为 2026-11 检索时点数据。生产环境务必**以官方仓库/文档当日状态复核**，LangChain v1 重写等破坏性变更需提前验证调用方兼容性。

## 六、核心要点速查

1. RAG = **检索外部知识 + 生成**，原始论文为 arXiv:2005.11401。
2. 五步链路：**切分 → 向量化 → 索引 → 检索 → 生成**，检索质量决定生成上限。
3. 核心动机：缓解幻觉、接入实时/私有知识、实现可溯源回答。
4. 检索优化三板斧：**混合检索（向量 + BM25）+ 查询改写 + 重排序（RRF/交叉编码器）**。
5. 生成阶段用**上下文工程**精简注入内容，进阶可用 **Agentic RAG** 支持多跳问答。
6. 评估要**分离检索与生成**，为检索设定 p95 延迟与 recall@k 等独立 SLO。
7. 切分是地基：`chunk_size`、`overlap`、分隔符需按文档类型调，先优化源文档再调检索。
8. 落地选型：索引用 LlamaIndex、编排用 LangChain/LangGraph、向量库按规模选 Milvus/LanceDB/pgvector。
9. 截至 2026-11：LlamaIndex v0.14.23、LangChain v1.4.3、Milvus 3.0 GA，版本号以官方仓库为准。

## 七、学习资源

1. [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（原始论文）](https://arxiv.org/abs/2005.11401)
2. [选择嵌入模型的 RAG 指南（Milvus 博客）](https://blog.milvus.io/zh-hant/blog/choose-embedding-model-rag-2026.md)
3. [RAG 最佳实践（工程要点）](https://redwerk.com/blog/rag-best-practices/)
4. [编写优化 RAG 应用程序的最佳实践（AWS 官方指南）](https://docs.aws.amazon.com/zh_cn/prescriptive-guidance/latest/writing-best-practices-rag/writing-best-practices-rag.pdf)
5. [LlamaIndex Releases / 版本列表](https://security.snyk.io/package/pip/llama-index/versions)
6. [LangChain Changelog](https://docs.langchain.org/oss/javascript/releases/changelog)
7. [Model Context Protocol Specification 2026-07-28（Agent 连接工具与数据的事实标准）](https://modelcontextprotocol.io/specification/2026-07-28/index)
8. [vLLM Releases（RAG 在线生成阶段的推理引擎）](https://github.com/vllm-project/vllm/releases)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]

## 九、变更记录

- 2026-11-19：首次创建。
