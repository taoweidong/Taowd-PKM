---
source: "http://www.jianshu.com/p/e8fcdedbfabe"
title: "Activiti + Spring开发环境搭建 - 简书"
fetched_at: "2026-10-05 15:32:34"
---

# Spring + Spring MVC + Activiti + MyBatis

## 开发环境

  * Eclipse Luna (4.4.2)
  * JDK 1.7.0_68
  * Maven 3.3.3
  * Tomcat 7.0
  * Activiti 5.17.0
  * 其他
    * eclipse插件: activiti designer(activiti流程设计工具)

## 使用maven搭建web工程


    (略)


## 编写pom.xml



        <modelVersion>4.0.0</modelVersion>
        <groupId>org.homeway</groupId>
        <artifactId>activitiDemo</artifactId>
         war
        <version>0.0.1-SNAPSHOT</version>
        <name>activitiDemo Maven Webapp</name>
        <url>http://maven.apache.org</url>


            <spring.version>4.1.4.RELEASE</spring.version>
            <mybatis.version>3.2.8</mybatis.version>
            <mybatis-spring.version>1.2.2</mybatis-spring.version>
            <junit.version>4.12</junit.version>
            <activiti.version>5.17.0</activiti.version>
            <log4j.version>2.2</log4j.version>
            <h2database.version>1.4.187</h2database.version>



        <dependencies>
            <!-- JUnit -->
            <dependency>
                <groupId>junit</groupId>
                <artifactId>junit</artifactId>
                <version>${junit.version}</version>
                <scope>test</scope>
            </dependency>
            <!-- Spring -->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-context-support</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-aop</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-aspects</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-core</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-orm</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-tx</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-test</artifactId>
                <version>${spring.version}</version>
            </dependency>
            <!-- log4j -->
            <dependency>
                <groupId>org.apache.logging.log4j</groupId>
                <artifactId>log4j-api</artifactId>
                <version>${log4j.version}</version>
            </dependency>
            <dependency>
                <groupId>org.apache.logging.log4j</groupId>
                <artifactId>log4j-core</artifactId>
                <version>${log4j.version}</version>
            </dependency>
            <!-- mybatis -->
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis</artifactId>
                <version>${mybatis.version}</version>
            </dependency>
            <dependency>
                <groupId>org.mybatis</groupId>
                <artifactId>mybatis-spring</artifactId>
                <version>${mybatis-spring.version}</version>
            </dependency>
            <!-- activiti -->
            <dependency>
                <groupId>org.activiti</groupId>
                <artifactId>activiti-engine</artifactId>
                <version>${activiti.version}</version>
            </dependency>
            <dependency>
                <groupId>org.activiti</groupId>
                <artifactId>activiti-spring</artifactId>
                <version>${activiti.version}</version>
            </dependency>
            <dependency>
                <groupId>org.activiti</groupId>
                <artifactId>activiti-rest</artifactId>
                <version>${activiti.version}</version>
            </dependency>
            <!-- h2 database -->
            <dependency>
                <groupId>com.h2database</groupId>
                <artifactId>h2</artifactId>
                <version>${h2database.version}</version>
            </dependency>
        </dependencies>


        <build>
            <finalName>activitiDemo</finalName>


                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.2</version>
                    <configuration>
                        <source>1.7</source>
                        <target>1.7</target>
                    </configuration>


        </build>



## 编写web.xml


    <web-app xmlns="http://java.sun.com/xml/ns/javaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
              http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd"
        version="3.0">
        <display-name>Servlet 3.0 Web Application</display-name>

        <context-param>
             contextConfigLocation
             classpath*:applicationContext-spring.xml
        </context-param>

        <listener>
            <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
        </listener>

        <filter>
            <filter-name>encodingFilter</filter-name>
            <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
            <init-param>
                 encoding
                 UTF-8
            </init-param>
            <init-param>
                 forceEncoding
                 true
            </init-param>
        </filter>
        <filter-mapping>
            <filter-name>encodingFilter</filter-name>
            <url-pattern>/*</url-pattern>
        </filter-mapping>

        <servlet>
            <servlet-name>dispatcher</servlet-name>
            <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
            <init-param>
                 contextConfigLocation
                 classpath*:spring-mvc.xml
            </init-param>
            <load-on-startup>1</load-on-startup>
        </servlet>
        <servlet-mapping>
            <servlet-name>dispatcher</servlet-name>
            <url-pattern>*.action</url-pattern>
        </servlet-mapping>

    </web-app>


## 编写spring相关的配置文件

### applicationContext-spring.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context"
        xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.1.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.1.xsd
            http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.1.xsd">

        <context:component-scan base-package="org.homeway">
            <context:exclude-filter type="annotation"
                expression="org.springframework.stereotype.Controller" />
        </context:component-scan>

        <tx:annotation-driven transaction-manager="transactionManager" />

        <context:property-placeholder
            ignore-unresolvable="true" location="classpath*:db.properties" />

        <bean id="dataSource"
            class="org.springframework.jdbc.datasource.SimpleDriverDataSource">




        </bean>

        <bean id="transactionManager"
            class="org.springframework.jdbc.datasource.DataSourceTransactionManager">

        </bean>

        <tx:advice id="txAdvice" transaction-manager="transactionManager">
            <tx:attributes>
                <tx:method name="delete*" propagation="REQUIRED" />
                <tx:method name="insert*" propagation="REQUIRED" />
                <tx:method name="update*" propagation="REQUIRED" />
            </tx:attributes>
        </tx:advice>

        <aop:config>
            <aop:pointcut expression="execution(* org.homeway.activiti.demo.service.*.*(..))"
                id="serviceCutPoint" />
            <aop:advisor advice-ref="txAdvice" pointcut-ref="serviceCutPoint" />
        </aop:config>

        <import resource="applicationContext-activiti.xml" />

        <import resource="applicationContext-mybatis.xml" />

    </beans>


### applicationContext-activiti.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context"
        xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.1.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.1.xsd
            http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.1.xsd">

        <bean id="processEngineConfiguration" class="org.activiti.spring.SpringProcessEngineConfiguration">





        </bean>
        <bean id="processEngine" class="org.activiti.spring.ProcessEngineFactoryBean">

        </bean>
        <bean id="repositoryService" factory-bean="processEngine"
            factory-method="getRepositoryService" />
        <bean id="runtimeService" factory-bean="processEngine"
            factory-method="getRuntimeService" />
        <bean id="taskService" factory-bean="processEngine"
            factory-method="getTaskService" />
        <bean id="historyService" factory-bean="processEngine"
            factory-method="getHistoryService" />
        <bean id="managementService" factory-bean="processEngine"
            factory-method="getManagementService" />
        <bean id="IdentityService" factory-bean="processEngine"
            factory-method="getIdentityService" />

    </beans>


### applicationContext-mybatis.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:context="http://www.springframework.org/schema/context"
        xmlns:aop="http://www.springframework.org/schema/aop" xmlns:tx="http://www.springframework.org/schema/tx"
        xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.1.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.1.xsd
            http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.1.xsd">

        <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">



        </bean>

        <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">


        </bean>

    </beans>


### spring-mvc.xml


    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:context="http://www.springframework.org/schema/context"
        xmlns:mvc="http://www.springframework.org/schema/mvc"
        xsi:schemaLocation="http://www.springframework.org/schema/jee http://www.springframework.org/schema/jee/spring-jee-4.1.xsd
            http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc-4.1.xsd
            http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans-4.1.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context-4.1.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop-4.1.xsd
            http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx-4.1.xsd">

        <context:component-scan base-package="org.homeway" use-default-filters="false">
            <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        </context:component-scan>

    </beans>


### mybatis-config.xml


    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE configuration
      PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
      "http://mybatis.org/dtd/mybatis-3-config.dtd">
    <configuration>
        <settings>
            <setting name="logImpl" value="LOG4J" />
        </settings>
    </configuration>


### db.properties


    db.driver=org.h2.Driver
    db.url=jdbc:h2:mem:activiti;DB_CLOSE_DELAY=1000
    db.username=sa
    db.password=


项目结构

demo.webapp.png

## 使用activiti designer绘制流程图


    Eclipse安装activiti designer
    help >> install new sofeware >> add
    name: Activiti BPMN 2.0 designer , location:  http://activiti.org/designer/update/


demo.process.test.png



        <startEvent id="startevent1" name="Start" activiti:initiator="firstPerson"></startEvent>
        <userTask id="usertask1" name="Step 1" activiti:assignee="kermit"></userTask>
        <sequenceFlow id="flow1" sourceRef="startevent1" targetRef="usertask1"></sequenceFlow>
        <userTask id="usertask2" name="Step 2" activiti:assignee="stone"></userTask>
        <sequenceFlow id="flow2" sourceRef="usertask1" targetRef="usertask2"></sequenceFlow>
        <endEvent id="endevent1" name="End"></endEvent>
        <sequenceFlow id="flow3" sourceRef="usertask2" targetRef="endevent1"></sequenceFlow>
        <boundaryEvent id="boundarytimer1" name="Timer" attachedToRef="usertask2" cancelActivity="true">
          <timerEventDefinition>
            <timeDuration>PT5S</timeDuration>
          </timerEventDefinition>
        </boundaryEvent>
        <userTask id="usertask3" name="step 2.1" activiti:assignee="kermit"></userTask>
        <sequenceFlow id="flow5" sourceRef="boundarytimer1" targetRef="usertask3"></sequenceFlow>
        <sequenceFlow id="flow6" sourceRef="usertask3" targetRef="endevent1"></sequenceFlow>



## 使用junit测试


    package org.homeway.activiti.demo.test;


    import java.util.List;

    import org.activiti.engine.HistoryService;
    import org.activiti.engine.IdentityService;
    import org.activiti.engine.RepositoryService;
    import org.activiti.engine.RuntimeService;
    import org.activiti.engine.TaskService;
    import org.activiti.engine.history.HistoricProcessInstance;
    import org.activiti.engine.runtime.ProcessInstance;
    import org.activiti.engine.task.Task;
    import org.activiti.spring.ProcessEngineFactoryBean;
    import org.apache.log4j.Logger;
    import org.junit.Test;
    import org.junit.runner.RunWith;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.test.context.ContextConfiguration;
    import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration("classpath:applicationContext-spring.xml")
    public class WorkFlowTest {

        Logger logger = Logger.getLogger(this.getClass());

        @Autowired
        ProcessEngineFactoryBean processEngine;

        @Autowired
        private RepositoryService repositoryService;

        @Autowired
        private RuntimeService runtimeService;

        @Autowired
        private TaskService taskService;

        @Autowired
        private HistoryService historyService;

        @Autowired
        private IdentityService identityService;

        @Test
        public void testEvent() throws InterruptedException {
            repositoryService.createDeployment()
                .addClasspathResource("org/homeway/activiti/demo/workflow/hello.bpmn")
                .deploy();
            System.out.println("Number of process definitions: " + repositoryService.createProcessDefinitionQuery().count());

            identityService.setAuthenticatedUserId("Jeff Dean");

            ProcessInstance processInstance = runtimeService.startProcessInstanceByKey("helloProcess");
            System.out.println(processInstance.getId());
            System.out.println(processInstance.getProcessDefinitionId());
            System.out.println(processInstance.getProcessDefinitionKey());

            List<Task> tasks = taskService.createTaskQuery().taskAssignee("kermit").list();
            for (Task task : tasks) {
                System.out.println(task.getName() + " : " + task.getAssignee());

                taskService.claim(task.getId(), "kermit");
            }

            tasks = taskService.createTaskQuery().taskAssignee("kermit").list();
            for (Task task : tasks) {

                taskService.complete(task.getId());
                System.out.println(task.getName() + " : " + task.getId() + " completed ");
            }

            Thread.sleep(10 * 1000);

            tasks = taskService.createTaskQuery().taskAssignee("stone").list();
            for (Task task : tasks) {
                System.out.println(task.getName() + " : " + task.getAssignee());
                taskService.claim(task.getId(), "stone");
            }

            tasks = taskService.createTaskQuery().taskAssignee("stone").list();
            for (Task task : tasks) {
                taskService.complete(task.getId());
                System.out.println(task.getName() + " : " + task.getId() + " completed ");
            }

            tasks = taskService.createTaskQuery().taskAssignee("kermit").list();
            for (Task task : tasks) {
                System.out.println(task.getName() + " : " + task.getAssignee());
                taskService.claim(task.getId(), "kermit");
            }


            HistoricProcessInstance hpInstance =
                    historyService.createHistoricProcessInstanceQuery()
                    .processInstanceId(processInstance.getId()).singleResult();
            System.out.println("end time: " + hpInstance.getEndTime());

        }
    }
