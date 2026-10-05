---
source: "http://www.cnblogs.com/yichenlei/p/5326040.html"
title: "log4j的终极封装 - yichenlei - 博客园"
fetched_at: "2026-10-05 15:36:14"
---

本人在使用log4j的时候最讨厌的就是各种new logger对象了。由于出于偷懒的目的封装了以下这个Log类。今天发布出来给大家分享一下。

共8个日志输出方法，具体如下：


    Log.debug("hello log4j");  //debug输出


    Log.debug("自定义Tag","hello log4j");  //debug输出，带自定义tag


    Log.info("hello info");  //info输出


    Log.info("自定义Tag","hello info");  //info输出，带自定义tag


    Log.warn("hello warn");  //warn输出


    Log.warn("自定义Tag","hello warn");  //warn输出，带自定义tag


    Log.error("hello error");  //error输出


    Log.error("自定义Tag","hello error");  //error输出，带自定义tag

    以下是封装类的源代码：




    package com.ycl.core.common;

    import java.util.HashMap;
    import java.util.Map;

    import org.apache.log4j.Logger;

    public class Log {

        private static Map<String,Logger> loggerMap = new HashMap<String,Logger>();

        public static void main(String[] args) throws ClassNotFoundException {
            Log.error("自定义LOG","sss444444");
        }

        public static void debug(Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            if(log.isDebugEnabled()){
                log.debug(message);
            }
        }

        public static void debug(String tag, Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            if(log.isDebugEnabled()){
                log.debug(new StringBuffer().append("【").append(tag).append("】").append(message).toString());
            }
        }

        public static void info(Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            if(log.isInfoEnabled()){
                log.info(message);
            }
        }

        public static void info(String tag, Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            if(log.isInfoEnabled()){
                log.info(new StringBuffer().append("【").append(tag).append("】").append(message).toString());
            }
        }

        public static void warn(Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            log.warn(message);
        }

        public static void warn(String tag, Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            log.warn(new StringBuffer().append("【").append(tag).append("】").append(message).toString());
        }

        public static void error(Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            log.error(message);
        }

        public static void error(String tag, Object message){
            String className = getClassName();
            Logger log = getLogger(className);
            log.error(new StringBuffer().append("【").append(tag).append("】").append(message).toString());
        }

        /**
         * 获取最开始的调用者所在类
         * @return
         */
        private static String getClassName(){
            Throwable th = new Throwable();
            StackTraceElement[] stes = th.getStackTrace();
            StackTraceElement ste = stes[2];
            return ste.getClassName();
        }
        /**
         * 根据类名获得logger对象
         * @param className
         * @return
         */
        private static Logger getLogger(String className){
            Logger log = null;
            if(loggerMap.containsKey(className)){
                log = loggerMap.get(className);
            }else{
                try {
                    log = Logger.getLogger(Class.forName(className));
                    loggerMap.put(className, log);
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                }
            }
            return log;
        }
    }
