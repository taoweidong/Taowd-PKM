---
source: "https://www.cnblogs.com/linkstar/p/8309039.html"
title: "在SpringBoot中添加Logback日志处理 - LinkinStar - 博客园"
fetched_at: "2026-10-05 15:46:41"
---

## 前言

SpringBoot项目中在官方文档中说明，默认已经依赖了一些日志框架。而其中推荐使用的就是Logback，所以这一次我将在我的模版中加入Logback日志的配置，说明一下，SpringBoot已经依赖了Logback所以不需要手动添加依赖。

已经加入我的github模版中：<https://github.com/LinkinStars/springBootTemplate>

## 如何配置

1、在resources目录下新建logback-spring.xml

只要你的名字是logback-spring.xml的话SpringBoot会自动识别和读取它的，所以你就不需要在application.yml进行其他的配置了。

配置文件具体如下：


    <?xml version="1.0" encoding="UTF-8"?>
    <configuration debug="true">
        <!-- 项目名称 -->


        <!--定义日志文件的存储地址 勿在 LogBack 的配置中使用相对路径-->


        <!-- 控制台输出 -->
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <withJansi>true</withJansi>
            <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
                <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
                 [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%thread] %highlight([%-5level] %logger{50} - %msg%n)
                <charset>UTF-8</charset>
            </encoder>
        </appender>

        <!-- 系统错误日志文件 -->
        <appender name="SYSTEM_FILE"  class="ch.qos.logback.core.rolling.RollingFileAppender">
            <!-- 过滤器，只打印ERROR级别的日志 -->
            <filter class="ch.qos.logback.classic.filter.LevelFilter">
                <level>ERROR</level>
                <onMatch>ACCEPT</onMatch>
                <onMismatch>DENY</onMismatch>
            </filter>
            <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
                <!--日志文件输出的文件名-->
                <FileNamePattern>${LOG_HOME}/${PROJECT_NAME}.system_error.%d{yyyy-MM-dd}.%i.log</FileNamePattern>
                <!--日志文件保留天数-->
                <MaxHistory>15</MaxHistory>
                <!--日志文件最大的大小-->
                <MaxFileSize>10MB</MaxFileSize>
            </rollingPolicy>

            <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
                <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
                 [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%thread] [%-5level] %logger{50} - %msg%n
                <charset>UTF-8</charset>
            </encoder>
        </appender>
        <logger name="system_error" additivity="true">
            <appender-ref ref="SYSTEM_FILE"/>
        </logger>

        <!-- 自己打印的日志文件，用于记录重要日志信息 -->
        <appender name="MY_INFO_FILE"  class="ch.qos.logback.core.rolling.RollingFileAppender">
            <!-- 过滤器，只打印ERROR级别的日志 -->
            <filter class="ch.qos.logback.classic.filter.LevelFilter">
                <level>INFO</level>
                <onMatch>ACCEPT</onMatch>
                <onMismatch>DENY</onMismatch>
            </filter>
            <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
                <!--日志文件输出的文件名-->
                <FileNamePattern>${LOG_HOME}/${PROJECT_NAME}.my_info.%d{yyyy-MM-dd}.%i.log</FileNamePattern>
                <!--日志文件保留天数-->
                <MaxHistory>15</MaxHistory>
                <!--日志文件最大的大小-->
                <MaxFileSize>10MB</MaxFileSize>
            </rollingPolicy>

            <encoder class="ch.qos.logback.classic.encoder.PatternLayoutEncoder">
                <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
                 [%d{yyyy-MM-dd HH:mm:ss.SSS}] [%thread] [%-5level] %logger{50} - %msg%n
                <charset>UTF-8</charset>
            </encoder>
        </appender>
        <logger name="my_info" additivity="true">
            <appender-ref ref="MY_INFO_FILE"/>
        </logger>

        <!-- 开发环境下的日志配置 -->
        <springProfile name="dev">
            <root level="INFO">
                <appender-ref ref="CONSOLE" />
                <appender-ref ref="SYSTEM_FILE" />
            </root>
        </springProfile>

        <!-- 生产环境下的日志配置 -->
        <springProfile name="prod">
            <root level="INFO">
                <appender-ref ref="SYSTEM_FILE" />
            </root>
        </springProfile>
    </configuration>

2、其实至此为止你已经可以正常使用你的日志工具了，但是既然是我的模版，我需要给它添加我使用的工具类，从而方便日志的打印


    package com.linkinstars.springBootTemplate.utils;

    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;

    /**
     * @Description: 日志工具类
     * @Author: LinkinStar
     */
    public class LogUtil {

        /**
         * 将信息打印到自定义日志（my_info.log）中
         * @param message 需要被打印的信息
         */
        public static void printLog(String message){
            Logger logger  =  LoggerFactory.getLogger("my_info");

            StringBuffer logOut = new StringBuffer();
            logOut.append("\n");
            logOut.append(message);
            logOut.append("\n");

            logger.info(logOut.toString());
        }

        /**
         * 将信息打印到自定义日志（system_error.log）中
         * @param e 异常信息
         */
        public static void printLog(Exception e, Class<?> clazz){
            Logger logger  =  LoggerFactory.getLogger(clazz);

            StringBuffer logOut = new StringBuffer();
            logOut.append("\n");
            logOut.append(e.toString());
            logOut.append("\n");

            StackTraceElement[] errorList = e.getStackTrace();
            for (StackTraceElement stackTraceElement : errorList) {
                logOut.append(stackTraceElement.toString());
                logOut.append("\n");
            }

            logOut.append("\n");
            logOut.append("\n");

            logger.error(logOut.toString());
        }

    }

这个工具类会根据之后的情况发生改变暂时只是用例

3、日志打印的说明

首先在配置文件中<springProfile name="prod">

当我们在修改

spring:
# 选择加载不同环境的配置文件
profiles:
active: dev

同样的logback这里的配置文件也会读取相应的配置，比如你使用dev那么就会读取dev下的配置，如果你使用prod就会使用prod下的配置。

也就是说等到项目需要上线的时候，你只需修改springBoot的配置文件就可以了，不需要对logback进行修改，就可以实现在生产环境下和开发环境下打印不同的日志级别

在控制台打印的信息经过处理显示的颜色会有不同的区分，很容易发现问题。

还有是日志文件的分类

通过我的工具类中会分离我打印的日志

我将我所需要的重要日志信息打印在my_info文件中去，而重要的错误信息存放在system_error文件中

其他的配置请参考logback配置文件详解等

## 参考文档

logback官方给出的配置文件说明<https://logback.qos.ch/manual/layouts.html#conversionWord>

所参考的博客配置：<http://blog.csdn.net/tigerd1995/article/details/50845999>
