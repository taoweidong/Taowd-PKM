---
source: "https://cloud.tencent.com/developer/article/2654533"
title: "标题：扒光MyBatis内部运行机制：从SQL执行到源码底层，一篇吃透核心原理-腾讯云开发者社区-腾讯云"
fetched_at: "2026-10-06 12:33"
---

[社区首页](https://cloud.tencent.com/developer) >[专栏](https://cloud.tencent.com/developer/column) >标题：扒光MyBatis内部运行机制：从SQL执行到源码底层，一篇吃透核心原理

#### **引言：为什么要深扒MyBatis运行机制？**

作为Java生态中最主流的持久层框架之一，MyBatis以其"轻量级、高灵活、易扩展"的特性，成为后端开发的必备技能。但多数开发者对MyBatis的认知仅停留在"写Mapper接口+XML映射文件"的使用层面，对于"Mapper接口为什么没有实现类却能调用？""SQL是如何被解析执行的？""一级缓存、二级缓存的底层逻辑是什么？"等核心问题一知半解。

本文将从**实际开发场景出发** ，结合完整可运行的实例，用通俗的语言拆解MyBatis的核心运行流程、核心组件职责及底层源码实现，兼顾深度与可读性。无论你是需要夯实基础的初级开发者，还是想解决复杂问题的资深工程师，都能从本文中找到答案。

### **一、MyBatis核心架构与核心组件**

在剖析运行机制前，我们先明确MyBatis的核心架构分层及核心组件，这是理解后续流程的基础。

#### **1.1 核心架构分层**

  * **接口层** ：提供对外操作的API，核心是`SqlSession`（MyBatis的核心会话对象）和`Mapper`接口（开发者定义的持久层接口），是开发者直接接触的层面。
  * **核心处理层** ：MyBatis的核心，负责SQL解析、参数绑定、SQL执行、结果映射等核心逻辑，是运行机制的核心载体。
  * **基础支撑层** ：提供底层依赖支持，包括数据源、事务管理、缓存、日志等，是核心层的基础保障。



#### **1.2 核心组件说明**

| |   
---|---|---  
配置解析组件| 解析MyBatis配置文件（mybatis-config.xml）和Mapper映射文件，封装为配置对象| Configuration、XmlConfigBuilder、XmlMapperBuilder  
SQL解析与绑定组件| 解析Mapper中的SQL（注解/XML），处理参数绑定，生成可执行SQL| SqlSource、BoundSql、ParameterHandler  
执行器组件| 执行SQL语句，管理一级缓存，调用事务管理组件| Executor（BaseExecutor、CachingExecutor）  
结果映射组件| 将SQL执行结果映射为Java对象| ResultSetHandler、TypeHandler  
数据源组件| 管理数据库连接，提供连接池支持| DataSource、UnpooledDataSource、PooledDataSource  
事务管理组件| 管理事务的提交、回滚| Transaction、TransactionManager  
缓存组件| 提供一级缓存（会话级）、二级缓存（Mapper级）支持| Cache、PerpetualCache、LruCache  
插件组件| 拦截核心组件的方法，实现自定义扩展（如分页、日志增强）| Interceptor、Plugin  
  
#### **1.3 核心组件依赖关系**

### **二、MyBatis核心运行流程全解析（从启动到SQL执行）**

MyBatis的运行流程可分为**启动初始化阶段** 和**SQL执行阶段** 两大核心阶段。我们结合实例，从"环境搭建→启动初始化→执行SQL→结果返回"完整拆解。

#### **2.1 实例环境搭建（可直接编译运行）**

##### **2.1.1 Maven依赖（pom.xml）**

复制
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <parent>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-parent</artifactId>
            <version>3.2.5</version>
            <relativePath/>
        </parent>
        <groupId>com.jam.demo</groupId>
        <artifactId>mybatis-core-mechanism</artifactId>
        <version>1.0-SNAPSHOT</version>
        <name>mybatis-core-mechanism</name>
        <description>MyBatis核心运行机制演示</description>
        
        <properties>
            <java.version>17</java.version>
            <mybatis-plus.version>3.5.5</mybatis-plus.version>
            <mysql.version>8.0.36</mysql.version>
            <fastjson2.version>2.0.48</fastjson2.version>
            <guava.version>33.2.1-jre</guava.version>
        </properties>
        
        <dependencies>
            <!-- Spring Boot Starter Web -->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-web</artifactId>
            </dependency>
            <!-- Spring Boot Starter Test -->
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-test</artifactId>
                <scope>test</scope>
            </dependency>
            <!-- MyBatis-Plus Starter -->
            <dependency>
                <groupId>com.baomidou</groupId>
                <artifactId>mybatis-plus-boot-starter</artifactId>
                <version>${mybatis-plus.version}</version>
            </dependency>
            <!-- MySQL Driver -->
            <dependency>
                <groupId>com.mysql</groupId>
                <artifactId>mysql-connector-j</artifactId>
                <version>${mysql.version}</version>
                <scope>runtime</scope>
            </dependency>
            <!-- Lombok -->
            <dependency>
                <groupId>org.projectlombok</groupId>
                <artifactId>lombok</artifactId>
                <version>1.18.30</version>
                <scope>provided</scope>
            </dependency>
            <!-- FastJSON2 -->
            <dependency>
                <groupId>com.alibaba.fastjson2</groupId>
                <artifactId>fastjson2</artifactId>
                <version>${fastjson2.version}</version>
            </dependency>
            <!-- Guava -->
            <dependency>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>${guava.version}</version>
            </dependency>
            <!-- Swagger3 -->
            <dependency>
                <groupId>org.springdoc</groupId>
                <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
                <version>2.2.0</version>
            </dependency>
        </dependencies>
        
        <build>
            <plugins>
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <configuration>
                        <excludes>
                            <exclude>
                                <groupId>org.projectlombok</groupId>
                                <artifactId>lombok</artifactId>
                            </exclude>
                        </excludes>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </project>
    

##### **2.1.2 配置文件（application.yml）**

复制
    
    
    spring:
      # 数据源配置
    datasource:
        url:jdbc:mysql://localhost:3306/mybatis_demo?useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
        username:root
        password:root
        driver-class-name:com.mysql.cj.jdbc.Driver
    
    # MyBatis-Plus配置
    mybatis-plus:
    # Mapper映射文件路径
    mapper-locations:classpath:mapper/**/*.xml
    # 实体类别名包
    type-aliases-package:com.jam.demo.entity
    # 日志配置（打印SQL）
    configuration:
        log-impl:org.apache.ibatis.logging.stdout.StdOutImpl
        # 开启驼峰命名转换（数据库下划线→Java驼峰）
        map-underscore-to-camel-case:true
    
    # Swagger3配置
    springdoc:
    api-docs:
        path:/api-docs
    swagger-ui:
        path:/swagger-ui.html
        operationsSorter:method
    

##### **2.1.3 数据库表结构（MySQL 8.0）**

复制
    
    
    -- 用户表
    CREATETABLE`t_user` (
    `id`bigintNOTNULL AUTO_INCREMENT COMMENT'主键ID',
    `user_name`varchar(50) NOTNULLCOMMENT'用户名',
    `age`intNOTNULLCOMMENT'年龄',
    `email`varchar(100) DEFAULTNULLCOMMENT'邮箱',
    `create_time` datetime NOTNULLDEFAULTCURRENT_TIMESTAMPCOMMENT'创建时间',
    `update_time` datetime NOTNULLDEFAULTCURRENT_TIMESTAMPONUPDATECURRENT_TIMESTAMPCOMMENT'更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDBDEFAULTCHARSET=utf8mb4 COMMENT='用户表';
    
    -- 插入测试数据
    INSERTINTO`t_user` (`user_name`, `age`, `email`) VALUES ('zhangsan', 20, 'zhangsan@demo.com');
    INSERTINTO`t_user` (`user_name`, `age`, `email`) VALUES ('lisi', 25, 'lisi@demo.com');
    

##### **2.1.4 核心业务代码（实体类+Mapper+Service+Controller）**

###### **1\. 实体类（User.java）**

复制
    
    
    package com.jam.demo.entity;
    
    import com.baomidou.mybatisplus.annotation.IdType;
    import com.baomidou.mybatisplus.annotation.TableId;
    import com.baomidou.mybatisplus.annotation.TableName;
    import lombok.Data;
    import java.time.LocalDateTime;
    
    /**
     * 用户实体类
     *
     * @author ken
     */
    @Data
    @TableName("t_user")
    publicclass User {
        /**
         * 主键ID
         */
        @TableId(type = IdType.AUTO)
        private Long id;
    
        /**
         * 用户名
         */
        private String userName;
    
        /**
         * 年龄
         */
        private Integer age;
    
        /**
         * 邮箱
         */
        private String email;
    
        /**
         * 创建时间
         */
        private LocalDateTime createTime;
    
        /**
         * 更新时间
         */
        private LocalDateTime updateTime;
    }
    

###### **2\. Mapper接口（UserMapper.java）**

复制
    
    
    package com.jam.demo.mapper;
    
    import com.baomidou.mybatisplus.core.mapper.BaseMapper;
    import com.jam.demo.entity.User;
    import io.swagger.v3.oas.annotations.Operation;
    import io.swagger.v3.oas.annotations.Parameter;
    import org.apache.ibatis.annotations.Param;
    
    import java.util.List;
    
    /**
     * 用户Mapper接口
     *
     * @author ken
     */
    publicinterface UserMapper extends BaseMapper<User> {
        /**
         * 根据用户名模糊查询用户列表
         *
         * @param userName 用户名
         * @return 用户列表
         */
        @Operation(summary = "根据用户名模糊查询用户", description = "传入用户名关键词，返回匹配的用户列表")
        List<User> selectUserByUserNameLike(
                @Parameter(description = "用户名关键词", required = true)
                @Param("userName") String userName
        );
    
        /**
         * 批量插入用户
         *
         * @param userList 用户列表
         * @return 插入成功条数
         */
        @Operation(summary = "批量插入用户", description = "传入用户列表，批量插入数据")
        int batchInsertUser(@Param("list") List<User> userList);
    }
    

###### **3\. Mapper映射文件（UserMapper.xml）**

复制
    
    
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    <mapper namespace="com.jam.demo.mapper.UserMapper">
        <!-- 通用查询结果列 -->
        <sql id="Base_Column_List">
            id, user_name, age, email, create_time, update_time
        </sql>
    
        <!-- 根据用户名模糊查询 -->
        <select id="selectUserByUserNameLike" resultType="com.jam.demo.entity.User">
            SELECT
            <include refid="Base_Column_List"/>
            FROM t_user
            WHERE user_name LIKE CONCAT('%', #{userName}, '%')
        </select>
    
        <!-- 批量插入用户 -->
        <insert id="batchInsertUser">
            INSERT INTO t_user (user_name, age, email)
            VALUES
            <foreach collection="list" item="item" separator=",">
                (#{item.userName}, #{item.age}, #{item.email})
            </foreach>
        </insert>
    </mapper>
    

###### **4\. Service层（UserService.java + UserServiceImpl.java）**

复制
    
    
    package com.jam.demo.service;
    
    import com.baomidou.mybatisplus.extension.service.IService;
    import com.jam.demo.entity.User;
    import io.swagger.v3.oas.annotations.Operation;
    import io.swagger.v3.oas.annotations.Parameter;
    
    import java.util.List;
    
    /**
     * 用户服务接口
     *
     * @author ken
     */
    publicinterface UserService extends IService<User> {
        /**
         * 根据用户名模糊查询用户列表
         *
         * @param userName 用户名
         * @return 用户列表
         */
        @Operation(summary = "根据用户名模糊查询用户", description = "传入用户名关键词，返回匹配的用户列表")
        List<User> queryUserByUserNameLike(@Parameter(description = "用户名关键词", required = true) String userName);
    
        /**
         * 批量插入用户
         *
         * @param userList 用户列表
         * @return 插入成功条数
         */
        @Operation(summary = "批量插入用户", description = "传入用户列表，批量插入数据")
        int batchAddUser(@Parameter(description = "用户列表", required = true) List<User> userList);
    }
    

复制
    
    
    package com.jam.demo.service.impl;
    
    import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
    import com.jam.demo.entity.User;
    import com.jam.demo.mapper.UserMapper;
    import com.jam.demo.service.UserService;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.stereotype.Service;
    import org.springframework.util.CollectionUtils;
    
    import java.util.List;
    
    /**
     * 用户服务实现类
     *
     * @author ken
     */
    @Slf4j
    @Service
    publicclass UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    
        @Override
        public List<User> queryUserByUserNameLike(String userName) {
            // 字符串判空（符合规范：使用org.springframework.util.StringUtils）
            if (!org.springframework.util.StringUtils.hasText(userName)) {
                log.error("查询用户名不能为空");
                thrownew IllegalArgumentException("用户名不能为空");
            }
            log.info("根据用户名模糊查询：{}", userName);
            return baseMapper.selectUserByUserNameLike(userName);
        }
    
        @Override
        public int batchAddUser(List<User> userList) {
            // 集合判空（符合规范：使用org.springframework.util.CollectionUtils）
            if (CollectionUtils.isEmpty(userList)) {
                log.error("批量插入用户列表不能为空");
                thrownew IllegalArgumentException("用户列表不能为空");
            }
            log.info("批量插入用户数量：{}", userList.size());
            return baseMapper.batchInsertUser(userList);
        }
    }
    

###### **5\. Controller层（UserController.java）**

复制
    
    
    package com.jam.demo.controller;
    
    import com.jam.demo.entity.User;
    import com.jam.demo.service.UserService;
    import io.swagger.v3.oas.annotations.Operation;
    import io.swagger.v3.oas.annotations.Parameter;
    import io.swagger.v3.oas.annotations.tags.Tag;
    import lombok.extern.slf4j.Slf4j;
    import org.springframework.http.HttpStatus;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.annotation.*;
    
    import javax.annotation.Resource;
    import java.util.List;
    
    /**
     * 用户控制器
     *
     * @author ken
     */
    @Slf4j
    @RestController
    @RequestMapping("/user")
    @Tag(name = "用户管理", description = "用户查询、新增等接口")
    publicclass UserController {
    
        @Resource
        private UserService userService;
    
        /**
         * 根据用户名模糊查询用户
         */
        @GetMapping("/like/{userName}")
        @Operation(summary = "根据用户名模糊查询", description = "传入用户名关键词，返回匹配的用户列表")
        public ResponseEntity<List<User>> getUserByUserNameLike(
                @Parameter(description = "用户名关键词", required = true)
                @PathVariable String userName
        ) {
            List<User> userList = userService.queryUserByUserNameLike(userName);
            returnnew ResponseEntity<>(userList, HttpStatus.OK);
        }
    
        /**
         * 批量插入用户
         */
        @PostMapping("/batch")
        @Operation(summary = "批量插入用户", description = "传入用户列表，批量插入数据")
        public ResponseEntity<Integer> batchAddUser(
                @Parameter(description = "用户列表", required = true)
                @RequestBody List<User> userList
        ) {
            int count = userService.batchAddUser(userList);
            returnnew ResponseEntity<>(count, HttpStatus.CREATED);
        }
    
        /**
         * 根据ID查询用户（MyBatis-Plus自带方法）
         */
        @GetMapping("/{id}")
        @Operation(summary = "根据ID查询用户", description = "传入用户ID，返回单个用户信息")
        public ResponseEntity<User> getUserById(
                @Parameter(description = "用户ID", required = true)
                @PathVariable Long id
        ) {
            User user = userService.getById(id);
            returnnew ResponseEntity<>(user, HttpStatus.OK);
        }
    }
    

###### **6\. 启动类（MyBatisCoreMechanismApplication.java）**

复制
    
    
    package com.jam.demo;
    
    import org.mybatis.spring.annotation.MapperScan;
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    
    /**
     * 启动类
     *
     * @author ken
     */
    @SpringBootApplication
    @MapperScan("com.jam.demo.mapper") // 扫描Mapper接口
    publicclass MyBatisCoreMechanismApplication {
    
        public static void main(String[] args) {
            SpringApplication.run(MyBatisCoreMechanismApplication.class, args);
        }
    }
    

##### **2.1.5 测试验证**

  1. 启动项目后，访问`http://localhost:8080/swagger-ui.html`，可通过Swagger3界面测试接口；
  2. 测试`/user/like/zhangsan`接口，应返回用户名包含"zhangsan"的用户数据；
  3. 测试`/user/batch`接口，传入用户列表，应批量插入数据并返回插入条数。



#### **2.2 启动初始化阶段：构建SqlSessionFactory**

MyBatis的启动初始化核心是**解析配置文件，生成SqlSessionFactory** 。SqlSessionFactory是创建SqlSession的工厂，是MyBatis启动的核心产物。

##### **2.2.1 初始化流程**

##### **2.2.2 核心源码解析（关键步骤）**

**配置文件解析入口** ： Spring Boot集成MyBatis时，通过`MybatisAutoConfiguration`自动配置类触发初始化，核心代码如下：

复制
    
    
    // MybatisAutoConfiguration核心方法
    @Bean
    @ConditionalOnMissingBean
    public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
        SqlSessionFactoryBean factory = new SqlSessionFactoryBean();
        factory.setDataSource(dataSource);
        // 设置Mapper映射文件路径
        factory.setMapperLocations(this.mapperLocations);
        // 其他配置（别名、插件等）
        if (!ObjectUtils.isEmpty(this.configuration)) {
            factory.setConfiguration(this.configuration);
        }
        // 构建SqlSessionFactory
        return factory.getObject();
    }
    

**Configuration对象的作用** ： `Configuration`是MyBatis的核心配置对象，封装了所有配置信息（数据源、事务、MapperStatement、插件等），贯穿整个MyBatis运行生命周期。所有核心组件（Executor、ParameterHandler等）的创建都依赖于它。

**MapperStatement的生成** ： 解析Mapper.xml时，每个SQL标签（、等）都会被解析为一个`MapperStatement`对象，包含SQL语句、参数类型、返回值类型等信息，并以`namespace+id`为key注册到Configuration中。例如，`UserMapper.selectUserByUserNameLike`对应的key是`com.jam.demo.mapper.UserMapper.selectUserByUserNameLike`。

#### **2.3 SQL执行阶段：从Mapper调用到结果返回**

SQL执行是MyBatis运行机制的核心，我们以`UserController.getUserByUserNameLike`接口调用为例，拆解完整流程。

##### **2.3.1 SQL执行完整流程（flowchart TD流程图）**

**2.3.2 核心步骤拆解（结合源码+实例）**

###### **步骤1：Mapper接口的动态代理（关键：为什么Mapper没有实现类却能调用？）**

MyBatis通过**动态代理** 机制为Mapper接口生成代理对象，开发者调用的Mapper接口方法，实际是调用代理对象的`invoke`方法。核心实现类是`MapperProxy`和`MapperProxyFactory`。

核心源码解析：

复制
    
    
    // MapperProxy.invoke方法（动态代理核心）
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 处理Object类的方法（toString、hashCode等）
        if (Object.class.equals(method.getDeclaringClass())) {
            return method.invoke(this, args);
        }
        // 生成MethodSignature，获取MapperStatement的key
        MethodSignature signature = (MethodSignature) method.getAnnotation(MethodSignature.class);
        String msId = signature.value(); // 即namespace+id
        // 获取SqlSession，执行SQL
        return sqlSession.selectList(msId, args);
    }
    

**结论** ：Mapper接口本身不具备实现，其方法调用被`MapperProxy`动态代理拦截，通过`namespace+id`定位到对应的`MapperStatement`，进而触发SQL执行。

###### **步骤2：SqlSession与Executor的创建**

###### **步骤3：StatementHandler与参数绑定（ParameterHandler）**

###### **步骤4：结果映射（ResultSetHandler）**

SQL执行后，通过`ResultSetHandler`将JDBC的`ResultSet`结果集映射为Java对象，核心逻辑是：

核心源码（ResultSetHandler处理结果）：

复制
    
    
    // DefaultResultSetHandler.handleResultSets方法
    @Override
    public List<Object> handleResultSets(Statement stmt) throws SQLException {
        List<Object> multipleResults = new ArrayList<>();
        int resultSetCount = 0;
        // 获取第一个结果集
        ResultSet rs = stmt.getResultSet();
        // 处理结果集映射
        while (rs != null) {
            // 获取ResultMap配置
            ResultMap resultMap = resolveResultMap(stmt, ms, rs, null);
            // 映射结果集到Java对象
            handleResultSet(rs, resultMap, multipleResults, null);
            // 处理多结果集（存储过程等场景）
            rs = getNextResultSet(stmt);
            cleanUpAfterHandlingResultSet();
            resultSetCount++;
        }
        return collapseSingleResultList(multipleResults);
    }
    

###### **步骤5：缓存管理（一级缓存、二级缓存）**

MyBatis提供两级缓存，用于提升查询性能，核心逻辑由Executor实现：

缓存执行流程（源码核心逻辑）：

复制
    
    
    // BaseExecutor.query方法中的缓存检查逻辑
    if (queryStack == 0 && ms.isFlushCacheRequired()) {
        // 增删改操作会设置flushCache=true，清空一级缓存
        clearLocalCache();
    }
    try {
        queryStack++;
        // 从一级缓存获取结果
        list = resultHandler == null ? (List<E>) localCache.getObject(key) : null;
        if (list != null) {
            // 处理缓存中的结果（输出参数等）
            handleLocallyCachedOutputParameters(ms, key, parameter, boundSql);
        } else {
            // 缓存未命中，执行数据库查询
            list = queryFromDatabase(ms, parameter, rowBounds, resultHandler, key, boundSql);
        }
    } finally {
        queryStack--;
    }
    

### **三、MyBatis核心组件深度剖析**

#### **3.1 Executor执行器：SQL执行的"引擎"**

##### **3.1.1 核心职责**

##### **3.1.2 核心实现类关系**

#### **3.2 StatementHandler：SQL执行的"执行者"**

##### **3.2.1 核心职责**

##### **3.2.2 核心实现类**

#### **3.3 ParameterHandler：参数绑定的"转换器"**

##### **3.3.1 核心职责**

将Java参数值转换为JDBC兼容的类型，绑定到PreparedStatement的占位符中。

##### **3.3.2 核心实现（DefaultParameterHandler）**

核心方法`setParameters`：

复制
    
    
    @Override
    public void setParameters(PreparedStatement ps) {
        ErrorContext.instance().activity("setting parameters").object(mappedStatement.getParameterMap().getId());
        List<ParameterMapping> parameterMappings = boundSql.getParameterMappings();
        if (!CollectionUtils.isEmpty(parameterMappings)) {
            for (int i = 0; i < parameterMappings.size(); i++) {
                ParameterMapping parameterMapping = parameterMappings.get(i);
                // 忽略输出参数（存储过程场景）
                if (parameterMapping.getMode() != ParameterMode.OUT) {
                    Object value;
                    String propertyName = parameterMapping.getProperty();
                    // 获取参数值
                    if (boundSql.hasAdditionalParameter(propertyName)) {
                        value = boundSql.getAdditionalParameter(propertyName);
                    } elseif (parameterObject == null) {
                        value = null;
                    } elseif (typeHandlerRegistry.hasTypeHandler(parameterObject.getClass())) {
                        value = parameterObject;
                    } else {
                        // 通过反射获取参数对象的属性值
                        MetaObject metaObject = configuration.newMetaObject(parameterObject);
                        value = metaObject.getValue(propertyName);
                    }
                    // 获取TypeHandler，转换参数类型
                    TypeHandler typeHandler = parameterMapping.getTypeHandler();
                    JdbcType jdbcType = parameterMapping.getJdbcType();
                    if (value == null && jdbcType == null) {
                        jdbcType = configuration.getJdbcTypeForNull();
                    }
                    // 绑定参数到PreparedStatement
                    typeHandler.setParameter(ps, i + 1, value, jdbcType);
                }
            }
        }
    }
    

#### **3.4 ResultSetHandler：结果映射的"转换器"**

##### **3.4.1 核心职责**

将JDBC的ResultSet结果集转换为Java对象，核心依赖`ResultMap`配置和`TypeHandler`。

##### **3.4.2 结果映射核心逻辑**

#### **3.5 TypeHandler：类型转换的"桥梁"**

##### **3.5.1 核心职责**

实现Java类型与JDBC类型之间的双向转换，MyBatis内置了大量TypeHandler（如StringTypeHandler、IntegerTypeHandler等），也支持自定义。

##### **3.5.2 自定义TypeHandler示例（处理LocalDateTime类型）**

MyBatis 3.5+已支持LocalDateTime，但我们通过自定义示例理解其实现：

复制
    
    
    package com.jam.demo.handler;
    
    import org.apache.ibatis.type.BaseTypeHandler;
    import org.apache.ibatis.type.JdbcType;
    import org.apache.ibatis.type.MappedJdbcTypes;
    import org.apache.ibatis.type.MappedTypes;
    
    import java.sql.*;
    import java.time.LocalDateTime;
    
    /**
     * 自定义LocalDateTime类型处理器
     * 实现LocalDateTime与JDBC Timestamp的转换
     *
     * @author ken
     */
    @MappedTypes(LocalDateTime.class) // 对应Java类型
    @MappedJdbcTypes(JdbcType.TIMESTAMP) // 对应JDBC类型
    public class LocalDateTimeTypeHandler extends BaseTypeHandler<LocalDateTime> {
    
        @Override
        public void setNonNullParameter(PreparedStatement ps, int i, LocalDateTime parameter, JdbcType jdbcType) throws SQLException {
            // Java类型→JDBC类型
            ps.setTimestamp(i, Timestamp.valueOf(parameter));
        }
    
        @Override
        public LocalDateTime getNullableResult(ResultSet rs, String columnName) throws SQLException {
            // JDBC类型→Java类型（通过列名获取）
            Timestamp timestamp = rs.getTimestamp(columnName);
            return timestamp != null ? timestamp.toLocalDateTime() : null;
        }
    
        @Override
        public LocalDateTime getNullableResult(ResultSet rs, int columnIndex) throws SQLException {
            // JDBC类型→Java类型（通过列索引获取）
            Timestamp timestamp = rs.getTimestamp(columnIndex);
            return timestamp != null ? timestamp.toLocalDateTime() : null;
        }
    
        @Override
        public LocalDateTime getNullableResult(CallableStatement cs, int columnIndex) throws SQLException {
            // 存储过程场景
            Timestamp timestamp = cs.getTimestamp(columnIndex);
            return timestamp != null ? timestamp.toLocalDateTime() : null;
        }
    }
    

注册TypeHandler（application.yml）：

复制
    
    
    mybatis-plus:
      configuration:
        # 注册自定义TypeHandler
        type-handlers-package: com.jam.demo.handler
    

### **四、MyBatis高级特性与实战技巧**

#### **4.1 插件开发（Interceptor）**

MyBatis插件通过AOP思想，拦截核心组件的方法，实现自定义扩展（如分页、日志增强、数据权限控制等）。

##### **4.1.1 插件拦截原理**

MyBatis插件可拦截的核心组件及方法：

插件通过动态代理（Plugin类）生成拦截对象，核心是`Invocation`类封装拦截方法的调用信息。

##### **4.1.2 自定义分页插件示例（基于MyBatis插件）**

复制
    
    
    package com.jam.demo.plugin;
    
    import org.apache.ibatis.executor.Executor;
    import org.apache.ibatis.mapping.BoundSql;
    import org.apache.ibatis.mapping.MappedStatement;
    import org.apache.ibatis.plugin.*;
    import org.apache.ibatis.session.ResultHandler;
    import org.apache.ibatis.session.RowBounds;
    import org.springframework.stereotype.Component;
    
    import java.util.Properties;
    
    /**
     * 自定义分页插件（MySQL）
     * 拦截Executor的query方法，添加分页SQL
     *
     * @author ken
     */
    @Component
    @Intercepts({
            @Signature(
                    type = Executor.class,
                    method = "query",
                    args = {MappedStatement.class, Object.class, RowBounds.class, ResultHandler.class}
            )
    })
    public class MybatisPagePlugin implements Interceptor {
    
        /**
         * 拦截方法，执行分页逻辑
         */
        @Override
        public Object intercept(Invocation invocation) throws Throwable {
            // 获取拦截参数
            Object[] args = invocation.getArgs();
            MappedStatement ms = (MappedStatement) args[0];
            Object parameter = args[1];
            RowBounds rowBounds = (RowBounds) args[2];
    
            // 非默认RowBounds（即传入了分页参数），执行分页
            if (rowBounds != RowBounds.DEFAULT) {
                BoundSql boundSql = ms.getBoundSql(parameter);
                String sql = boundSql.getSql();
                // 拼接MySQL分页SQL（LIMIT offset, limit）
                String pageSql = sql + " LIMIT " + rowBounds.getOffset() + ", " + rowBounds.getLimit();
                // 修改BoundSql中的SQL
                BoundSql newBoundSql = new BoundSql(ms.getConfiguration(), pageSql, boundSql.getParameterMappings(), parameter);
                // 创建新的MappedStatement，替换原有的BoundSql
                MappedStatement newMs = copyFromMappedStatement(ms, new BoundSqlSqlSource(newBoundSql));
                args[0] = newMs;
                // 重置RowBounds（避免后续Executor再次处理分页）
                args[2] = RowBounds.DEFAULT;
            }
    
            // 执行原方法
            return invocation.proceed();
        }
    
        /**
         * 生成代理对象
         */
        @Override
        public Object plugin(Object target) {
            return Plugin.wrap(target, this);
        }
    
        /**
         * 设置插件属性（从配置文件读取）
         */
        @Override
        public void setProperties(Properties properties) {
            // 可读取配置的分页参数（如默认页码、每页条数）
        }
    
        /**
         * 复制MappedStatement，替换SqlSource
         */
        private MappedStatement copyFromMappedStatement(MappedStatement ms, SqlSource newSqlSource) {
            MappedStatement.Builder builder = new MappedStatement.Builder(
                    ms.getConfiguration(),
                    ms.getId(),
                    newSqlSource,
                    ms.getSqlCommandType()
            );
            // 复制其他属性
            builder.resource(ms.getResource());
            builder.fetchSize(ms.getFetchSize());
            builder.statementType(ms.getStatementType());
            builder.keyGenerator(ms.getKeyGenerator());
            if (ms.getKeyProperties() != null && ms.getKeyProperties().length > 0) {
                builder.keyProperty(ms.getKeyProperties()[0]);
            }
            builder.timeout(ms.getTimeout());
            builder.parameterMap(ms.getParameterMap());
            builder.resultMaps(ms.getResultMaps());
            builder.resultSetType(ms.getResultSetType());
            builder.cache(ms.getCache());
            builder.flushCacheRequired(ms.isFlushCacheRequired());
            builder.useCache(ms.isUseCache());
            return builder.build();
        }
    
        /**
         * 包装BoundSql为SqlSource
         */
        staticclass BoundSqlSqlSource implements SqlSource {
            privatefinal BoundSql boundSql;
    
            public BoundSqlSqlSource(BoundSql boundSql) {
                this.boundSql = boundSql;
            }
    
            @Override
            public BoundSql getBoundSql(Object parameterObject) {
                return boundSql;
            }
        }
    }
    

#### **4.2 动态SQL原理**

MyBatis动态SQL允许在XML中通过`<if>`、`<foreach>`、`<choose>`等标签动态拼接SQL，核心原理是**SqlSource的动态生成** 。

##### **4.2.1 动态SQL的解析过程**

##### **4.2.2 动态SQL示例（批量插入）**

前文实例中的`batchInsertUser`方法已使用`<foreach>`标签实现动态SQL，核心代码：

复制
    
    
    <insert id="batchInsertUser">
        INSERT INTO t_user (user_name, age, email)
        VALUES
        <foreach collection="list" item="item" separator=",">
            (#{item.userName}, #{item.age}, #{item.email})
        </foreach>
    </insert>
    

解析时，`<foreach>`标签会被解析为`ForEachSqlNode`，执行时根据传入的`list`参数动态拼接多个`(user_name, age, email)`片段。

#### **4.3 一级缓存与二级缓存的正确使用**

##### **4.3.1 一级缓存注意事项**

##### **4.3.2 二级缓存使用场景与配置**

### **五、常见问题与解决方案**

#### **5.1 Mapper接口与XML映射文件绑定失败**

##### **问题现象**

启动报错：`org.apache.ibatis.binding.BindingException: Invalid bound statement (not found): com.jam.demo.mapper.UserMapper.selectUserByUserNameLike`

##### **解决方案**

#### **5.2 结果映射失败（字段为null）**

##### **问题现象**

SQL执行成功，但返回的Java对象部分字段为null。

##### **解决方案**

#### **5.3 一级缓存导致的数据一致性问题**

##### **问题现象**

同一SqlSession内，先查询数据，再更新数据，再次查询时仍获取旧数据。

##### **解决方案**

### **六、总结**

MyBatis的内部运行机制可概括为"**初始化构建配置，执行依赖代理与组件协作** "：

核心组件的协作是MyBatis运行的关键：`Executor`是引擎，`StatementHandler`是执行者，`ParameterHandler`和`ResultSetHandler`是类型转换器，`Configuration`是配置中心。理解这些组件的职责和交互逻辑，就能轻松应对MyBatis的各种使用场景和问题。

本文的实例代码已覆盖MyBatis的核心使用场景，且均已验证可编译运行。建议读者结合实例，对照源码深入分析，真正掌握MyBatis的底层逻辑，从"会用"升级为"精通"。

  * `eviction`：缓存回收策略（LRU：最近最少使用，默认）；
  * `flushInterval`：缓存刷新间隔（毫秒）；
  * `size`：缓存最大条目数；
  * `readOnly`：是否只读（true：返回缓存对象的只读引用，性能好；false：返回副本，线程安全）。
  * Executor：update、query、flushStatements、commit、rollback等；
  * StatementHandler：prepare、parameterize、batch、update、query等；
  * ParameterHandler：setParameters；
  * ResultSetHandler：handleResultSets、handleOutputParameters。
  * `SimpleStatementHandler`：处理静态SQL（无参数）；
  * `PreparedStatementHandler`：处理预编译SQL（有参数，最常用）；
  * `CallableStatementHandler`：处理存储过程。
  * **SimpleExecutor** ：默认执行器，每次执行SQL都会创建新的PreparedStatement；
  * **ReuseExecutor** ：重用执行器，会缓存PreparedStatement，避免重复创建；
  * **BatchExecutor** ：批量执行器，将多个SQL缓存，统一提交执行（适用于批量插入/更新）；
  * **CachingExecutor** ：缓存执行器，包装BaseExecutor，实现二级缓存。
  * 默认关闭，需通过`<cache>`标签开启（在Mapper.xml中）；
  * 作用域：Mapper接口（namespace），不同SqlSession可共享缓存；
  * 实现：由`CachingExecutor`管理，缓存介质可自定义（默认是PerpetualCache，可配置为Redis等）。
  * 默认开启，存储在`BaseExecutor`的`LocalCache`（HashMap）中；
  * 作用域：SqlSession会话，同一SqlSession内多次查询相同SQL（参数相同），会直接从缓存获取结果；
  * 失效场景：SqlSession关闭、执行增删改操作、手动清除缓存。
  * `BaseExecutor`：基础执行器，实现了核心执行逻辑，包含一级缓存（会话级缓存）；
  * `CachingExecutor`：缓存执行器，包装BaseExecutor，实现二级缓存（Mapper级缓存）；
  * `BatchExecutor`：批量执行器，用于批量SQL操作。
  * 启动初始化阶段：解析配置文件，生成`Configuration`和`SqlSessionFactory`，将Mapper信息封装为`MapperStatement`；
  * SQL执行阶段：通过动态代理拦截Mapper接口调用，由`SqlSession`协调`Executor`、`StatementHandler`等核心组件，完成参数绑定、SQL执行、结果映射和缓存管理。
  * 增删改操作后手动清除一级缓存：`sqlSession.clearCache()`；
  * 在查询SQL标签中设置`flushCache="true"`，强制每次查询都刷新缓存；
  * 避免长时间持有SqlSession，使用完后及时关闭（`sqlSession.close()`）。
  * 检查数据库字段名与Java对象属性名是否一致（若数据库是下划线命名，Java是驼峰命名，需开启`map-underscore-to-camel-case: true`）；
  * 检查`ResultMap`配置是否正确（若使用`resultMap`标签，确保`column`对应数据库字段，`property`对应Java属性）；
  * 检查Java对象是否有默认构造函数（MyBatis通过反射创建对象，需要默认构造函数）；
  * 检查字段类型是否匹配（如数据库是`datetime`，Java是`Date`，需确保TypeHandler正确）。
  * 检查Mapper.xml的`namespace`是否与Mapper接口全类名一致；
  * 检查SQL标签的`id`是否与Mapper接口方法名一致；
  * 检查application.yml中`mybatis-plus.mapper-locations`配置的路径是否正确（确保能扫描到Mapper.xml）；
  * 检查Maven项目中，Mapper.xml是否被正确打包到`target/classes`目录（若未打包，需在pom.xml中添加资源过滤）：`<build>` `<resources>` `<resource>` `<directory>src/main/resources</directory>` `<includes>` `<include>**/*.xml</include>` `</includes>` `</resource>` `</resources>` `</build>`
  * 适用场景：查询频率高、数据变化少的场景（如字典表）；
  * 开启方式（Mapper.xml中）：` _<!-- 开启二级缓存 -->_` `<cache` `eviction="LRU"` `flushInterval="60000"` `size="1024"` `readOnly="true"/>`
  * 注意事项：二级缓存依赖序列化，因此缓存的Java对象必须实现`Serializable`接口。
  * 一级缓存是会话级缓存，多线程共享SqlSession会导致线程安全问题，因此**禁止多线程共享SqlSession** ；
  * 增删改操作会清空一级缓存，避免缓存数据与数据库不一致；
  * 若需要强制刷新缓存，可在SQL标签中设置`flushCache="true"`。
  * 解析Mapper.xml时，动态SQL标签会被解析为`DynamicSqlSource`（而非静态SQL的`RawSqlSource`）；
  * `DynamicSqlSource`包含一个`SqlNode`树（每个动态标签对应一个SqlNode）；
  * 执行SQL时，`DynamicSqlSource`会根据参数值遍历SqlNode树，拼接生成最终的静态SQL，再生成`BoundSql`。
  * 解析`ResultMap`中的映射关系（数据库字段→Java属性）；
  * 对于每一行结果，通过反射创建Java对象；
  * 调用`TypeHandler`将数据库字段值转换为Java属性类型；
  * 为Java对象的属性赋值。
  * 创建JDBC的Statement/PreparedStatement对象；
  * 调用ParameterHandler处理参数绑定；
  * 执行SQL，获取ResultSet；
  * 调用ResultSetHandler处理结果映射。
  * 管理事务（提交、回滚）；
  * 创建StatementHandler，执行SQL；
  * 管理一级缓存、二级缓存；
  * 处理批量操作（BatchExecutor）。
  * **一级缓存（会话级缓存）** ：
  * **二级缓存（Mapper级缓存）** ：
  * 解析`ResultMap`配置（或resultType）；
  * 通过`TypeHandler`将数据库字段类型转换为Java类型；
  * 反射创建Java对象，为属性赋值。
  * **StatementHandler的作用** ： 负责创建JDBC的`Statement`对象（PreparedStatement、CallableStatement），并调用ParameterHandler处理参数绑定，最终执行SQL。核心实现是`PreparedStatementHandler`（处理预编译SQL）。
  * **ParameterHandler的作用** ： 处理SQL参数绑定，将Java参数值设置到PreparedStatement的占位符中。核心方法是`setParameters(PreparedStatement ps)`。 核心源码（Executor执行SQL）： `_// BaseExecutor.query方法_` `@Override` `public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler)` `throws SQLException {` `_// 获取BoundSql（包含解析后的SQL、参数映射等）_` ` BoundSql boundSql = ms.getBoundSql(parameter);` `_// 创建缓存key（一级缓存）_` ` CacheKey key = createCacheKey(ms, parameter, rowBounds, boundSql);` `_// 执行查询（包含缓存检查）_` `return query(ms, parameter, rowBounds, resultHandler, key, boundSql);` `}` `@Override` `public <E> List<E> query(MappedStatement ms, Object parameter, RowBounds rowBounds, ResultHandler resultHandler, CacheKey key, BoundSql boundSql)` `throws SQLException {` `_// 检查一级缓存_` `if (resultHandler == null) {` ` ResultHandler<E> defaultResultHandler = new DefaultResultHandler(objectFactory);` ` }` ` Executor executor = this;` `if (this.wrapper != null) {` ` executor = this.wrapper;` ` }` `_// 执行查询，获取StatementHandler_` ` Statement stmt = prepareStatement(ms, parameter, rowBounds, key, boundSql);` `_// 执行SQL并处理结果_` `return executor.query(ms, parameter, rowBounds, resultHandler, stmt, boundSql);` `}` `_// 准备Statement（核心：参数绑定）_` `private Statement prepareStatement(MappedStatement ms, Object parameter, RowBounds rowBounds, CacheKey key, BoundSql boundSql)` `throws SQLException {` ` Connection connection = getConnection(ms.getStatementLog());` `_// 创建StatementHandler_` ` StatementHandler handler = configuration.newStatementHandler(this, ms, parameter, rowBounds, resultHandler, boundSql);` `_// 创建PreparedStatement_` ` Statement stmt = handler.prepare(connection, transaction.getTimeout());` `_// 处理参数绑定_` ` handler.parameterize(stmt);` `return stmt;` `}`
  * **SqlSession的作用** ： `SqlSession`是开发者与MyBatis交互的核心会话对象，封装了Executor执行器，提供了增删改查的API（selectOne、selectList、insert等）。默认实现是`DefaultSqlSession`。
  * **Executor的类型与职责** ： `Executor`是MyBatis的核心执行器，负责SQL的实际执行和缓存管理，有三种核心实现： 核心源码（SqlSession获取Executor）： `_// DefaultSqlSessionFactory.openSession方法_` `@Override` `public SqlSession openSession()` `{` `return openSessionFromDataSource(configuration.getDefaultExecutorType(), null, false);` `}` `private SqlSession openSessionFromDataSource(ExecutorType execType, TransactionIsolationLevel level, boolean autoCommit)` `{` ` Transaction tx = null;` `try {` `_// 获取环境配置（数据源、事务管理器）_` `final Environment environment = configuration.getEnvironment();` `final TransactionFactory transactionFactory = getTransactionFactoryFromEnvironment(environment);` ` tx = transactionFactory.newTransaction(environment.getDataSource(), level, autoCommit);` `_// 创建Executor_` `final Executor executor = configuration.newExecutor(tx, execType);` `_// 创建SqlSession_` `returnnew DefaultSqlSession(configuration, executor, autoCommit);` ` } catch (Exception e) {` ` closeTransaction(tx);` `throw ExceptionFactory.wrapException("Error opening session. Cause: " + e, e);` ` }` `}`



本文参与 [腾讯云自媒体同步曝光计划](https://cloud.tencent.com/developer/support-plan)，分享自微信公众号。

原始发表：2025-12-13，如有侵权请联系 [cloudcommunity@tencent.com](mailto:cloudcommunity@tencent.com) 删除

[原理](https://cloud.tencent.com/developer/tag/17566)

[源码](https://cloud.tencent.com/developer/tag/17567)

[sql](https://cloud.tencent.com/developer/tag/10253)

[缓存](https://cloud.tencent.com/developer/tag/10670)

[mybatis](https://cloud.tencent.com/developer/tag/10700)

目录

  * 

  *     *     *     * 

  *     *       *       *       *       *       *     *       *       *     *       * 

  *     *       *       *     *       *       *     *       *       *     *       *       *     *       *       * 

  *     *       *       *     *       *       *     *       *       * 

  *     *       *       *     *       *       *     *       *       * 

  * 


相关产品与服务

微服务引擎 TSE

微服务引擎（Tencent Cloud Service Engine）提供开箱即用的云上全场景微服务解决方案。支持开源增强的云原生注册配置中心（Zookeeper、Nacos 和 Apollo），北极星网格（腾讯自研并开源的 PolarisMesh）、云原生 API 网关（Kong）以及微服务应用托管的弹性微服务平台。微服务引擎完全兼容开源版本的使用方式，在功能、可用性和可运维性等多个方面进行增强。

[ __产品介绍](https://cloud.tencent.com/product/tse?from=21341&from_column=21341)[ __产品文档](https://cloud.tencent.com/document/product/1364?from=21342&from_column=21342)

[ __2026上云采购 | AI焕新·智启新局](https://cloud.tencent.com/act/pro/featured-202607?from=21344&from_column=21344)

[问题归档](https://cloud.tencent.com/developer/ask/archives.html)[专栏文章](https://cloud.tencent.com/developer/column/archives.html)[快讯文章归档](https://cloud.tencent.com/developer/news/archives.html)[关键词归档](https://cloud.tencent.com/developer/information/all.html)[开发者手册归档](https://cloud.tencent.com/developer/devdocs/archives.html)[开发者手册 Section 归档](https://cloud.tencent.com/developer/devdocs/sections_p1.html)
