---
source: "https://www.cnblogs.com/gccbuaa/p/19287413"
title: "深入解析：MyBatis 源码深度解析：从 Spring Boot 实战到底层原理 - gccbuaa - 博客园"
fetched_at: "2026-10-06 12:33"
---

#  [ 深入解析：MyBatis 源码深度解析：从 Spring Boot 实战到底层原理 ](https://www.cnblogs.com/gccbuaa/p/19287413 "发布于 2025-11-29 20:36")

## MyBatis 源码深度解析：从 Spring Boot 实战到底层原理

作为 Java 生态中最流行的持久层框架之一，MyBatis 以其灵活的 SQL 控制和极简的配置深受开发者喜爱。本文将从 Spring Boot 中的实际用法出发，逐步深入 MyBatis 核心源码，解析其设计思想与运行机制。

### 一、Spring Boot 中 MyBatis 的实战用法

在实际开发中，MyBatis 常与 Spring Boot 结合使用，通过 Starter 快速集成。以下是完整的使用流程：

#### 1\. 环境搭建

**引入依赖** （Maven）：
    
    
    <dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>2.3.0</version>
    </dependency>
    <dependency>
    <groupId>com.mysql</groupId>
    <artifactId>mysql-connector-j</artifactId>
    <scope>runtime</scope>
    </dependency>

**配置数据库连接** （application.yml）：
    
    
    spring:
    datasource:
    url: jdbc:mysql://localhost:3306/test?useSSL=false&serverTimezone=UTC
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
    mybatis:
    mapper-locations: classpath:mapper/*.xml  
    type-aliases-package: com.example.entity  
    configuration:
    map-underscore-to-camel-case: true  
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl  

#### 2\. 核心组件使用

##### （1）实体类（Entity）
    
    
    public class User {
    private Long id;
    private String userName;  
    private Integer age;
    
    }

##### （2）Mapper 接口
    
    
    @Mapper  
    public interface UserMapper {
    
    @Select("SELECT * FROM user WHERE id = #{id}")
    User selectById(Long id);
    
    int insert(User user);
    }

##### （3）Mapper XML 文件（resources/mapper/UserMapper.xml）
    
    
    <?xml version="1.0" encoding="UTF-8"?>
      <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
      "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
        <mapper namespace="com.example.mapper.UserMapper">
          <insert id="insert" parameterType="User">
          INSERT INTO user (user_name, age)
          VALUES (#{userName}, #{age})
        </insert>
      </mapper>

##### （4）Service 层调用
    
    
    @Service
    public class UserService {
    @Autowired
    private UserMapper userMapper;  
    public User getUserById(Long id) {
    return userMapper.selectById(id);
    }
    public void addUser(User user) {
    userMapper.insert(user);
    }
    }

#### 3\. 关键特性应用

  * **分页查询** ：结合 `PageHelper` 插件
        
        PageHelper.startPage(1, 10);  
        List<User> users = userMapper.selectAll();
          Page<User> page = (Page<User>) users;  

  * **动态 SQL** ：在 XML 中使用 `<if>`、`<foreach>` 等标签
        
        <select id="selectByCondition" parameterType="User">
          SELECT * FROM user
          <where>
          <if test="userName != null">AND user_name LIKE CONCAT('%', #{userName}, '%')</if>
          <if test="age != null">AND age = #{age}</if>
          </where>
        </select>




### 二、MyBatis 核心特性解析

MyBatis 的强大源于其独特的设计，以下是工作中最常用的核心特性：

#### 1\. 动态 SQL

动态 SQL 允许根据参数动态生成 SQL 语句，避免了字符串拼接的繁琐和 SQL 注入风险。核心标签包括：

  * `<if>`：条件判断
  * `<where>`/`<set>`：自动处理多余的 `AND`/`,` 符号
  * `<foreach>`：循环遍历（如批量插入 `IN` 条件）
  * `<sql>`/`<include>`：SQL 片段复用



**优势** ：在多条件查询、动态更新等场景中非常实用，例如后台管理系统的复杂搜索功能。

#### 2\. 结果映射（ResultMap）

解决实体类与数据库表字段名不匹配的问题（即使不开启驼峰转换也能通过配置映射）：
    
    
    <resultMap id="UserResultMap" type="User">
      <id column="user_id" property="id"/>  
      <result column="user_name" property="userName"/>  
        <association property="role" javaType="Role">  
        <id column="role_id" property="id"/>
        <result column="role_name" property="name"/>
      </association>
    </resultMap>

**应用场景** ：多表关联查询（一对一、一对多），复杂对象的映射。

#### 3\. 缓存机制

MyBatis 提供两级缓存，减少数据库访问次数：

  * **一级缓存** ：SqlSession 级别（默认开启），同一 SqlSession 内的查询结果会被缓存。
  * **二级缓存** ：Mapper 级别（需手动开启），多个 SqlSession 共享缓存。



**开启二级缓存** ：
    
    
      <cache eviction="LRU" flushInterval="60000" size="1024" readOnly="true"/>

**注意** ：二级缓存适合查询频繁、修改较少的数据（如字典表），避免缓存一致性问题。

#### 4\. 插件机制

MyBatis 允许通过插件拦截四大核心组件的方法，实现自定义功能：

  * Executor：执行器（update、query等方法）
  * ParameterHandler：参数处理器
  * ResultSetHandler：结果集处理器
  * StatementHandler：SQL 语句处理器



**典型应用** ：分页插件（PageHelper）、数据权限控制、SQL 日志打印等。

### 三、MyBatis 源码深度解析

#### 1\. 核心架构概览

MyBatis 核心架构分为三层：

  1. **接口层** ：对外提供 API（如 `SqlSession`、`Mapper` 接口）
  2. **核心处理层** ：处理 SQL 解析、参数映射、结果映射等核心逻辑
  3. **基础支撑层** ：提供数据源、事务管理、缓存等基础服务



#### 2\. 核心流程：一条 SQL 的执行过程

以 `userMapper.selectById(1L)` 为例，解析 MyBatis 执行流程：

##### （1）获取 SqlSession

在 Spring 环境中，`SqlSession` 由 `SqlSessionTemplate` 管理，其本质是对 `SqlSession` 的代理，确保线程安全。
    
    
    private class SqlSessionInterceptor implements InvocationHandler {
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    SqlSession sqlSession = getSqlSession(
    SqlSessionTemplate.this.sqlSessionFactory,
    SqlSessionTemplate.this.executorType,
    SqlSessionTemplate.this.exceptionTranslator);
    try {
    Object result = method.invoke(sqlSession, args);  
    if (!isSqlSessionTransactional(sqlSession, SqlSessionTemplate.this.sqlSessionFactory)) {
    sqlSession.commit(true);  
    }
    return result;
    } catch (Throwable t) {
    
    } finally {
    closeSqlSession(sqlSession, SqlSessionTemplate.this.sqlSessionFactory);
    }
    }
    }

##### （2）Mapper 接口代理

MyBatis 通过 JDK 动态代理为 `UserMapper` 生成实现类（`MapperProxy`），当调用 `selectById` 时，实际执行 `MapperProxy.invoke()` 方法。
    
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
    if (Object.class.equals(method.getDeclaringClass())) {
    return method.invoke(this, args);  
    } else {
    
    return cachedInvoker(method).invoke(proxy, method, args, sqlSession);
    }
    }
    
    private MapperMethodInvoker cachedInvoker(Method method) throws Throwable {
    return methodCache.computeIfAbsent(method, m -> {
    if (m.isDefault()) {
    
    } else {
    return new PlainMethodInvoker(new MapperMethod(mapperInterface, method, sqlSession.getConfiguration()));
    }
    });
    }

##### （3）SQL 解析与执行

`MapperMethod` 将方法调用转换为对 `SqlSession` 的操作（如 `selectOne`），最终由 `Executor` 执行 SQL：
    
    
    @Override
    public <E> List<E> doQuery(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, BoundSql boundSql) throws SQLException {
      Statement stmt = null;
      try {
      Configuration configuration = ms.getConfiguration();
      
      StatementHandler handler = configuration.newStatementHandler(wrapper, ms, parameter, rowBounds, resultHandler, boundSql);
      
      stmt = prepareStatement(handler, ms.getStatementLog());
      
      return handler.query(stmt, resultHandler);
      } finally {
      closeStatement(stmt);
      }
      }

##### （4）结果映射

`ResultSetHandler` 将数据库返回的 `ResultSet` 转换为 Java 对象：
    
    
    @Override
    public List<Object> handleResultSets(Statement stmt) throws SQLException {
      final List<Object> multipleResults = new ArrayList<>();
        int resultSetCount = 0;
        
        ResultSetWrapper rsw = getFirstResultSet(stmt);
        
        List<ResultMap> resultMaps = mappedStatement.getResultMaps();
          int resultMapCount = resultMaps.size();
          
          while (rsw != null && resultMapCount > resultSetCount) {
          ResultMap resultMap = resultMaps.get(resultSetCount);
          
          handleResultSet(rsw, resultMap, multipleResults, null);
          rsw = getNextResultSet(stmt);
          cleanUpAfterHandlingResultSet();
          resultSetCount++;
          }
          
          return collapseSingleResultList(multipleResults);
          }

#### 3\. 动态 SQL 解析原理

动态 SQL 的解析发生在 MyBatis 初始化阶段，通过 `XMLScriptBuilder` 解析 `<if>`、`<where>` 等标签，生成 `SqlNode` 树，最终在执行时动态拼接 SQL。
    
    
    private MixedSqlNode parseDynamicTags(XNode node) {
    List<SqlNode> contents = new ArrayList<>();
      NodeList children = node.getNode().getChildNodes();
      for (int i = 0; i < children.getLength(); i++) {
      XNode child = node.newXNode(children.item(i));
      if (child.getNode().getNodeType() == Node.CDATA_SECTION_NODE || child.getNode().getNodeType() == Node.TEXT_NODE) {
      
      String data = child.getStringBody("");
      TextSqlNode textSqlNode = new TextSqlNode(data);
      if (textSqlNode.isDynamic()) {
      contents.add(textSqlNode);
      isDynamic = true;
      } else {
      contents.add(new StaticTextSqlNode(data));
      }
      } else if (child.getNode().getNodeType() == Node.ELEMENT_NODE) {
      
      String nodeName = child.getNode().getNodeName();
      NodeHandler handler = nodeHandlerMap.get(nodeName);
      if (handler == null) {
      throw new BuilderException("Unknown element <" + nodeName + "> in SQL statement.");
        }
        handler.handleNode(child, contents);
        isDynamic = true;
        }
        }
        return new MixedSqlNode(contents);
        }

执行时，`DynamicSqlSource.getBoundSql()` 会根据参数动态生成最终 SQL：
    
    
    @Override
    public BoundSql getBoundSql(Object parameterObject) {
    DynamicContext context = new DynamicContext(configuration, parameterObject);
    
    rootSqlNode.apply(context);
    SqlSourceBuilder sqlSourceParser = new SqlSourceBuilder(configuration);
    Class<?> parameterType = parameterObject == null ? Object.class : parameterObject.getClass();
      SqlSource sqlSource = sqlSourceParser.parse(context.getSql(), parameterType, context.getBindings());
      BoundSql boundSql = sqlSource.getBoundSql(parameterObject);
      
      context.getBindings().forEach(boundSql::setAdditionalParameter);
      return boundSql;
      }

#### 4\. 一级缓存实现原理

一级缓存（`PerpetualCache`）存储在 `SqlSession` 对应的 `Executor` 中，默认开启，缓存 key 由 `MappedStatement ID + SQL + 参数 + 分页信息` 组成。
    
    
    @Override
    public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler) throws SQLException {
      BoundSql boundSql = ms.getBoundSql(parameter);
      
      CacheKey key = createCacheKey(ms, parameter, rowBounds, boundSql);
      return query(ms, parameter, rowBounds, resultHandler, key, boundSql);
      }
      @Override
      public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, CacheKey key, BoundSql boundSql) throws SQLException {
        
        List<E> list;
          try {
          queryStack++;
          list = resultHandler == null ? (List<E>) localCache.getObject(key) : null;
            if (list != null) {
            
            handleLocallyCachedOutputParameters(ms, key, parameter, boundSql);
            } else {
            
            list = queryFromDatabase(ms, parameter, rowBounds, resultHandler, key, boundSql);
            }
            } finally {
            queryStack--;
            }
            
            if (queryStack == 0) {
            for (DeferredLoad deferredLoad : deferredLoads) {
            deferredLoad.load();
            }
            deferredLoads.clear();
            if (configuration.getLocalCacheScope() == LocalCacheScope.STATEMENT) {
            
            clearLocalCache();
            }
            }
            return list;
            }

### 四、工作中的最佳实践与优化建议

  1. **SQL 优化** ：

     * 避免 `SELECT *`，只查询需要的字段
     * 复杂查询优先使用 XML 方式编写，便于维护
     * 合理使用索引，避免全表扫描
  2. **缓存策略** ：

     * 一级缓存默认开启，但在事务中需注意缓存有效性
     * 二级缓存谨慎使用，建议只在只读表或极少更新的表中开启
     * 分布式环境下，优先使用 Redis 等分布式缓存替代二级缓存
  3. **性能监控** ：

     * 开启 MyBatis 日志，监控 SQL 执行时间
     * 使用 `PageHelper` 分页时，注意 count 查询的性能
     * 避免 N+1 查询问题（可通过 `association` 或 `collection` 的 `fetchType="eager"` 解决）
  4. **安全规范** ：

     * 禁止直接拼接 SQL 字符串，使用 `#{}` 占位符（防止 SQL 注入）
     * 敏感字段加密存储，查询时通过插件解密



### 五、总结

MyBatis 以其灵活的设计和强大的功能，成为 Java 持久层框架的佼佼者。通过本文的分析，我们从 Spring Boot 实战出发，深入理解了 MyBatis 的核心特性和源码实现，包括 SQL 执行流程、动态 SQL 解析、缓存机制等。

**参考资料** ：

  * [MyBatis 官方文档](https://mybatis.org/mybatis-3/zh/index.html)
  * MyBatis 源码（3.5.10 版本）



* * *

> Studying will never be ending.

▲如有纰漏，烦请指正~~

posted @ 2025-11-29 20:36 [gccbuaa](https://www.cnblogs.com/gccbuaa) 阅读(186) 评论(0) [收藏](javascript:void\(0\)) [举报](https://report.cnblogs.com?targetLink=https%3A%2F%2Fwww.cnblogs.com%2Fgccbuaa%2Fp%2F19287413&targetId=19287413&targetType=0)
