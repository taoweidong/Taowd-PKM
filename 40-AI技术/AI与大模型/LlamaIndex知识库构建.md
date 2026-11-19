---
title: LlamaIndex知识库构建
date: 2026-11-19
updated: 2026-11-19
tags:
  - AI/大模型
  - AI/LLM
  - LlamaIndex
  - RAG
  - 知识库
aliases:
  - LlamaIndex
  - LlamaIndex RAG 知识库
source: 网络资料整理
---

# LlamaIndex知识库构建

> [!摘要] 摘要
> 本文系统讲解用 **LlamaIndex** 构建文档型知识库的完整路径：从版本现状与框架定位出发，讲清「解析 → 切分 → 向量化 → 索引 → 检索 → 生成」的链路，以及 Ingestion Pipeline、VectorStoreIndex、Retriever、Reader 等核心组件，并给出可直接运行的安装、构建与查询代码。适合想用 LlamaIndex 落地企业知识库与 RAG 问答的开发者；与之互补的 Agent 编排侧能力见 [[AI与大模型-从入门到精通]]。

## 一、最新动态（截至 2026-11）

> [!info] 说明
> 以下版本号均来自 2026 年 11 月检索时点的官方仓库与版本列表，框架迭代极快，定稿前请以官方仓库当日状态复核。

- **LlamaIndex 最新稳定线 v0.14.23（2026-06-24）**；核心包 `llama-index-core` 随版本迭代，**自 v0.14.18 起弃用 Python 3.9**。来源：[LlamaIndex 版本列表（Snyk）](https://security.snyk.io/package/pip/llama-index/versions)、[llama_index v0.14.18 Release](https://github.com/run-llama/llama_index/releases/tag/v0.14.18)
- **框架分工**：LlamaIndex 与 LangChain/LangGraph 同为 RAG 与智能体主流框架，分工是「LlamaIndex 偏数据接入与索引，LangChain 偏 Agent 编排」（[LangChain v1 说明](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)）。
- **向量库格局（2026）**：[Milvus 3.0 于 2026-07-16 官宣 GA](https://cloud.vk.ru/blog/vektornie-bazi-dannikh-dlya-rag-kak-vibrat-dvizhok-i-podnyat-odrant-v-vk-cloud/)（Apache 2.0、支持 K8s/Docker、提供 Python/Go/Node SDK）；Qdrant 稳定线 1.18.x、Weaviate 稳定线 1.38.x，最新小版本号以官方仓库为准。
- **嵌入模型（2026）**：OpenAI `text-embedding-3-small`（1536 维）、`text-embedding-3-large`（3072 维，支持 Matryoshka 维度裁剪）；另有 Gemini Embedding 2、Voyage、Jina v4、Cohere Embed v4 及可自托管的 BGE-M3。来源：[Milvus 博客：为 RAG 选择嵌入模型（2026）](https://blog.milvus.io/zh-hant/blog/choose-embedding-model-rag-2026.md)
- **推理底座**：本地开源模型常经 vLLM 等引擎以 OpenAI 兼容接口暴露，vLLM v0.34.0（2026-11-15）为最新稳定线（[vLLM v0.34.0 Release](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)）。

## 二、基础概念

**LlamaIndex 的定位**：以「数据/索引为中心」构建 RAG 与知识库的框架，围绕**文档接入 → 索引构建 → 检索查询**组织能力，天然适合文档型知识库场景。核心概念：

- **Document / Node**：Document 是原始文档（含文本与元数据）；Node 是切分后的片段，是索引与检索的基本单位。
- **Ingestion Pipeline**：把原始文档加工为可索引节点的流水线，串起解析、切分、嵌入、写入等步骤。
- **VectorStoreIndex**：以向量库为存储的索引，是最常用的索引类型；此外还有 KeywordIndex、SummaryIndex、KnowledgeGraphIndex 等。
- **Retriever / Reader**：Retriever 负责按查询召回相关节点，Reader（或 Query Engine）在召回结果上组织上下文，交给 LLM 生成回答。
- **Settings**：全局配置模型（LLM、嵌入模型、分块参数等）的入口。

**与 LangChain 的分工**：两者都能做 RAG，但 LlamaIndex 更强调「把数据结构化并索引好」，LangChain 更强调「编排 Agent 与工具」。知识库侧重选 LlamaIndex，智能体侧重选 LangChain。

## 三、核心机制

LlamaIndex 知识库的完整链路是 **解析（Parsing）→ 切分（Chunking）→ 向量化（Embedding）→ 索引（Indexing）→ 检索（Retrieval）→ 生成（Generation）**，每一步都可单独配置与评估。

**1. 解析与切分**
解析器按文件类型把 PDF、Word、Markdown、HTML 等转成 Document；切分器把长文档切成语义完整、长度合适的 Node。常用 `SentenceSplitter`，通过 `chunk_size`（如 512–1024）与 `chunk_overlap`（如 20–100）控制粒度。切分过细则语义破碎、检索噪声大；过粗则关键信息被稀释。

**2. 向量化与索引**
每个 Node 经嵌入模型转为向量后写入向量库形成索引。LlamaIndex 用 `VectorStoreIndex` 封装该过程，底层可切换 Milvus、Qdrant、Weaviate、Chroma、pgvector 等。选择时关注数据规模、是否支持过滤与混合检索、部署形态（内存/磁盘/云）。

**3. 检索与生成**
查询时先由 Retriever 召回 Top-K 节点，再由 Reader 把节点拼成上下文交给 LLM 生成。召回策略可选 `similarity`（向量相似度）、`mmr`（最大边际相关，兼顾多样性与相关性）、`similarity_score`（带相似度阈值过滤）等。

**4. 元数据驱动**
为 Document/Node 附加元数据（来源、标题、章节、时间、权限标签等），可在检索时用 `filter` 做权限过滤与结构化筛选，是企业知识库落地的关键。

## 四、实践步骤（含代码/命令示例）

**Step 1 安装依赖**

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "llama-index>=0.14.23"
pip install "llama-index-llms-openai" "llama-index-embeddings-openai"
# 按需选择向量库（示例用 Milvus）
pip install "llama-index-vector-stores-milvus"
```

**Step 2 准备文档与模型**

```bash
mkdir -p ./docs && cp /path/to/*.pdf ./docs
# 本地模型可先启动 OpenAI 兼容服务，供 LlamaIndex 调用
vllm serve Qwen/Qwen3-8B --port 8000
```

**Step 3 构建索引并查询（Python）**

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1) 配置模型（API，或本地 vLLM 的 OpenAI 兼容地址）
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0, api_base="http://127.0.0.1:8000/v1")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# 2) 读取文档（PDF / Markdown / txt 等）
documents = SimpleDirectoryReader("./docs").load_data()

# 3) 构建向量索引（默认自动完成切分与嵌入）
index = VectorStoreIndex.from_documents(documents)

# 4) 查询：召回 Top-K 后交给 LLM 生成回答
query_engine = index.as_query_engine(similarity_top_k=3, retriever_mode="mmr")
response = query_engine.query("LlamaIndex 的核心组件有哪些？")
print(response)
```

**Step 4 用 Ingestion Pipeline 精细控制（Python）**

```python
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.milvus import MilvusVectorStore

splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
pipeline = IngestionPipeline(transformations=[splitter])  # 可叠加元数据抽取、标题提取等

documents = SimpleDirectoryReader("./docs").load_data()
nodes = pipeline.run(documents)

vector_store = MilvusVectorStore(uri="http://localhost:19530", dim=1536, overwrite=True)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex(nodes, storage_context=storage_context)
```

**Step 5 评估与迭代**：为检索与生成分别准备测试集，用检索的 recall@k、回答的准确率与格式合规等指标做回归对照，再调整切分粒度与 Top-K。

## 五、最佳实践与常见坑

**最佳实践**

- **先调源文档结构，再调检索**：源文档结构混乱时，再高级的检索也难救回质量。
- **切分粒度优先**：合理的 `chunk_size` / `chunk_overlap` 是性价比最高的优化；必要时做元数据抽取，用过滤器在检索时精准定位。
- **检索与生成分开评估**：给检索设独立 SLO（如 p95 延迟、recall@k），不要只看回答质量。
- **引用可溯源**：让回答附带来源片段，便于核查，缓解幻觉。
- **锁定版本**：LlamaIndex、向量库、嵌入模型迭代快，生产环境建议固定版本。

**常见坑**

| 现象 | 可能原因 | 对策 |
| --- | --- | --- |
| 检索不到 / 不准 | 切分粒度不当、单一向量检索 | 调整 chunk 参数，引入元数据过滤，必要时上混合检索 + 重排 |
| 回答幻觉 | 召回噪声大、无引用 | 提高召回质量、附来源引用、加事实校验 |
| 召回上下文过长 | Top-K 过大、切分过粗 | 降低 `similarity_top_k`，改用 MMR，压缩上下文 |
| 权限 / 数据越界 | 元数据缺失、未做过滤 | 写入权限标签，检索时用 `filter` 过滤 |
| 环境报错 | Python 版本过低 | v0.14.18 起需 Python 3.10+，建议 3.11+；按官方要求升级 |
| 依赖冲突 | 版本过新或过旧 | 锁定版本，核对 `llama-index-core` 与向量库适配器版本 |

## 六、核心要点速查

1. LlamaIndex 定位「数据/索引为中心」，适合文档型知识库；LangChain 偏 Agent 编排，二者互补。
2. 当前最新稳定线 v0.14.23（2026-06-24），`llama-index-core` 自 v0.14.18 起弃用 Python 3.9。
3. 完整链路：解析 → 切分 → 向量化 → 索引 → 检索 → 生成，检索质量决定生成质量。
4. 核心组件：Ingestion Pipeline、VectorStoreIndex、Retriever、Reader。
5. 切分用 `SentenceSplitter`，`chunk_size` 与 `chunk_overlap` 是首要调参项。
6. 向量库按规模选：轻量用 Chroma/LanceDB，PostgreSQL 生态用 pgvector，大规模用 Milvus。
7. 召回模式：`similarity`、`mmr`、`similarity_score`，需兼顾相关性与多样性。
8. 元数据 + `filter` 实现权限过滤与结构化检索，是生产落地关键。
9. 检索与生成分开评估，为检索设独立 SLO。
10. 生产环境锁定版本，避免依赖漂移。

## 七、学习资源

1. [LlamaIndex 版本列表（Snyk）](https://security.snyk.io/package/pip/llama-index/versions)
2. [llama_index GitHub Releases](https://github.com/run-llama/llama_index/releases)
3. [Announcing Retrieval Harness（LlamaIndex 官方博客）](https://www.llamaindex.ai/blog/announcing-retrieval-harness)
4. [LangChain v1 说明](https://langchain-5e9cc07a.mintlify.app/oss/javascript/releases/langchain-v1)
5. [vLLM v0.34.0 Release Notes](https://github.com/vllm-project/vllm/releases/tag/v0.34.0)
6. [Milvus 博客：为 RAG 选择嵌入模型（2026）](https://blog.milvus.io/zh-hant/blog/choose-embedding-model-rag-2026.md)
7. [RAG 原始论文（arXiv:2005.11401）](https://arxiv.org/abs/2005.11401)
8. [DB-Engines 向量数据库排行](https://db-engines.com/en/ranking/vector+dbms)

## 八、关联笔记

- [[AI与大模型-从入门到精通]]
- [[LLM-RAG检索增强生成]]
- [[Agent智能体开发基础]]
- [[AI工具-LangChain实战]]
- [[大模型基础核心要点]]
- [[40-AI技术]]

## 九、变更记录

- 2026-11-19：首次创建。
