---
source: "http://www.cnblogs.com/tengpan-cn/p/5909596.html"
title: "Java 基于log4j的日志工具类 - 沙中世界 - 博客园"
fetched_at: "2026-10-05 15:36:10"
---

对log4j日志类进行了简单封装，使用该封装类的优势在于以下两点：

1、不必在每个类中去创建对象，直接类名 + 方法即可

2、可以很方便的打印出堆栈信息


    package com.tradeplatform.receiveorder.util;

    import java.io.PrintWriter;
    import java.io.StringWriter;

    import org.apache.log4j.Logger;

    /**
     * @Description 日志记录类
     * @author panteng
     * @version V0.0.1
     * @date 2016-09-08
     */
    public class SysLog {
        public static Logger log = Logger.getLogger(SysLog.class);

        /**
         * 打印警告
         *
         * @param obj
         */
        public static void warn(Object obj) {
            try{
                /*** 获取输出信息的代码的位置 ***/
                String location = "";
                StackTraceElement[] stacks = Thread.currentThread().getStackTrace();
                location = stacks[2].getClassName() + "." + stacks[2].getMethodName()
                        + "(" + stacks[2].getLineNumber() + ")";
                /*** 是否是异常  ***/
                if (obj instanceof Exception) {
                    Exception e = (Exception) obj;
                    StringWriter sw = new StringWriter();
                    e.printStackTrace(new PrintWriter(sw, true));
                    String str = sw.toString();
                    log.warn(location + str);
                } else {
                    log.warn(location + obj.toString());
                }
            }catch (Exception e) {
                // TODO: handle exception
                e.printStackTrace();
            }
        }

        /**
         * 打印信息
         *
         * @param obj
         */
        public static void info(Object obj) {
            try{
                /*** 获取输出信息的代码的位置 ***/
                String location = "";
                StackTraceElement[] stacks = Thread.currentThread().getStackTrace();
                location = stacks[2].getClassName() + "." + stacks[2].getMethodName()
                        + "(" + stacks[2].getLineNumber() + ")";
                /*** 是否是异常  ***/
                if (obj instanceof Exception) {
                    Exception e = (Exception) obj;
                    StringWriter sw = new StringWriter();
                    e.printStackTrace(new PrintWriter(sw, true));
                    String str = sw.toString();
                    log.info(location + str);
                } else {
                    log.info(location + obj.toString());
                }
            }catch (Exception e) {
                // TODO: handle exception
                e.printStackTrace();
            }
        }

        /**
         * 打印错误
         *
         * @param obj
         */
        public static void error(Object obj) {
            try{
                /*** 获取输出信息的代码的位置 ***/
                String location = "";
                StackTraceElement[] stacks = Thread.currentThread().getStackTrace();
                location = stacks[2].getClassName() + "." + stacks[2].getMethodName()
                        + "(" + stacks[2].getLineNumber() + ")";

                /*** 是否是异常  ***/
                if (obj instanceof Exception) {
                    Exception e = (Exception) obj;
                    StringWriter sw = new StringWriter();
                    e.printStackTrace(new PrintWriter(sw, true));
                    String str = sw.toString();
                    log.error(location + str);
                } else {
                    log.error(location + obj.toString());
                }
            }catch (Exception e) {
                // TODO: handle exception
                e.printStackTrace();
            }
        }

        /**
         * 向数据库告警表中插入信息
         * @param obj
         */
        public static void dbWarn(Object obj) {
            try{
                String printInfo = "";
                /*** 获取输出信息的代码的位置 ***/
                String location = "";
                StackTraceElement[] stacks = Thread.currentThread().getStackTrace();
                location = stacks[2].getClassName() + "." + stacks[2].getMethodName()
                        + "(" + stacks[2].getLineNumber() + ")";

                /*** 是否是异常  ***/
                if (obj instanceof Exception) {
                    Exception e = (Exception) obj;
                    printInfo = location + e.getMessage();
                    log.fatal(printInfo.substring(0, printInfo.length() > 512?512:printInfo.length()));
                } else {
                    printInfo = location + obj.toString();
                    log.fatal(printInfo.substring(0, printInfo.length() > 512?512:printInfo.length()));
                }
            }catch (Exception e) {
                // TODO: handle exception
                e.printStackTrace();
            }
        }

        /**
         * 获取调用此函数的代码的位置
         * @return 包名.类名.方法名(行数)
         */
        public static String getCodeLocation(){
            try{
                /*** 获取输出信息的代码的位置 ***/
                String location = "";
                StackTraceElement[] stacks = Thread.currentThread().getStackTrace();
                location = stacks[2].getClassName() + "." + stacks[2].getMethodName()
                        + "(" + stacks[2].getLineNumber() + ")";
                return location;
            }catch (Exception e) {
                // TODO: handle exception
                SysLog.error(e);
                return "";
            }
        }
    }

配置文件：


    base.logs.dir=D:/testMycatLog

    log4j.rootLogger = DEBUG, INFO, all_log, stdout ,DB

    log4j.appender.stdout=org.apache.log4j.ConsoleAppender
    log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
    log4j.appender.stdout.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss SSS} %-5p [%-15x] [%t] - %m%n

    log4j.appender.all_log=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.all_log.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.all_log.File=${base.logs.dir}/all_log.log
    log4j.appender.all_log.layout=org.apache.log4j.PatternLayout
    log4j.appender.all_log.layout.ConversionPattern=%d{yyyy-MM-dd HH:mm:ss SSS} %-5p [%-15x] [%t] - %m%n


    log4j.appender.DB = org.apache.log4j.jdbc.JDBCAppender
    log4j.appender.DB.BufferSize=1
    log4j.appender.DB.driver=com.mysql.jdbc.Driver
    log4j.appender.DB.URL=jdbc:mysql://192.168.91.231:8066/CTPDB
    log4j.appender.DB.user=ctp
    log4j.appender.DB.password=ctp
    log4j.appender.DB.Threshold =FATAL
    log4j.appender.DB.layout = org.apache.log4j.PatternLayout
    log4j.appender.DB.sql=insert into syswarn(WARN_LEVEL,WARN_INFO) values("1",'%m');

    #--------------kafka配置----------------#
    log4j.appender.kafkaAppender=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.kafkaAppender.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.kafkaAppender.File=${base.logs.dir}/server.log
    log4j.appender.kafkaAppender.layout=org.apache.log4j.PatternLayout
    log4j.appender.kafkaAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

    log4j.appender.stateChangeAppender=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.stateChangeAppender.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.stateChangeAppender.File=${base.logs.dir}/state-change.log
    log4j.appender.stateChangeAppender.layout=org.apache.log4j.PatternLayout
    log4j.appender.stateChangeAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

    log4j.appender.requestAppender=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.requestAppender.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.requestAppender.File=${base.logs.dir}/kafka-request.log
    log4j.appender.requestAppender.layout=org.apache.log4j.PatternLayout
    log4j.appender.requestAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

    log4j.appender.cleanerAppender=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.cleanerAppender.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.cleanerAppender.File=${base.logs.dir}/log-cleaner.log
    log4j.appender.cleanerAppender.layout=org.apache.log4j.PatternLayout
    log4j.appender.cleanerAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

    log4j.appender.controllerAppender=org.apache.log4j.DailyRollingFileAppender
    log4j.appender.controllerAppender.DatePattern='.'yyyy-MM-dd-HH
    log4j.appender.controllerAppender.File=${base.logs.dir}/controller.log
    log4j.appender.controllerAppender.layout=org.apache.log4j.PatternLayout
    log4j.appender.controllerAppender.layout.ConversionPattern=[%d] %p %m (%c)%n

    # Turn on all our debugging info
    #log4j.logger.kafka.producer.async.DefaultEventHandler=DEBUG, kafkaAppender
    #log4j.logger.kafka.client.ClientUtils=DEBUG, kafkaAppender
    #log4j.logger.kafka.perf=DEBUG, kafkaAppender
    #log4j.logger.kafka.perf.ProducerPerformance$ProducerThread=DEBUG, kafkaAppender
    #log4j.logger.org.I0Itec.zkclient.ZkClient=DEBUG
    log4j.logger.kafka=INFO, kafkaAppender

    log4j.logger.kafka.network.RequestChannel$=WARN, requestAppender
    log4j.additivity.kafka.network.RequestChannel$=false

    #log4j.logger.kafka.network.Processor=TRACE, requestAppender
    #log4j.logger.kafka.server.KafkaApis=TRACE, requestAppender
    #log4j.additivity.kafka.server.KafkaApis=false
    log4j.logger.kafka.request.logger=WARN, requestAppender
    log4j.additivity.kafka.request.logger=false

    log4j.logger.kafka.controller=TRACE, controllerAppender
    log4j.additivity.kafka.controller=false

    log4j.logger.kafka.log.LogCleaner=INFO, cleanerAppender
    log4j.additivity.kafka.log.LogCleaner=false
    log4j.logger.kafka.log.Cleaner=INFO, cleanerAppender
    log4j.additivity.kafka.log.Cleaner=false

    log4j.logger.state.change.logger=TRACE, stateChangeAppender
    log4j.additivity.state.change.logger=false
    #---------------------------------------#
