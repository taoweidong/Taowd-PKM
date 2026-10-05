---
source: "http://www.cnblogs.com/nick-huang/p/4848843.html"
title: "【Quartz】Quartz的搭建、应用（单独使用Quartz） - nick_huang - 博客园"
fetched_at: "2026-10-05 15:30:59"
---

Quartz在Java构建的系统中，是十分常用的定时任务框架。

本文记录和介绍Quartz的简单入门的单独搭建。

注：本文以入门学习Quartz为主，并非基于Spring托管形式。其中有另一篇关于Spring Boot与Quartz集成的博文《[Quartz与Spring Boot集成使用](http://www.cnblogs.com/nick-huang/p/8456272.html)》。

## 版本说明

除了Quartz，还引入logback（为了看详细的日志嘛！）

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


        <dependencies>
            <dependency>
                <groupId>org.quartz-scheduler</groupId>
                <artifactId>quartz</artifactId>
                <version>2.2.0</version>
            </dependency>

            <dependency>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-classic</artifactId>
                <version>1.1.0</version>
            </dependency>
        </dependencies>

View Code

![](data:image/png;base64,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)

## 简单的搭建

jar包的引入参考上述的pom文件。

quartz.properties，配置quartz的设置。

**注** ，org.quartz.threadPool.threadCount，配置线程池的容量，即表示同时最多可运行的线程数量。在生产环境，此参数应根据实际情况配置。

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    org.quartz.scheduler.instanceName = MyScheduler
    org.quartz.threadPool.threadCount = 3
    org.quartz.jobStore.class = org.quartz.simpl.RAMJobStore

View Code

logback.xml，日志框架logback的配置。这里只简单地配置了控制台和日志文件的输出哦(>_<)

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    <configuration>

        <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
            <!-- encoders are assigned the type ch.qos.logback.classic.encoder.PatternLayoutEncoder
                by default -->
            <encoder>
                 %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n

            </encoder>
        </appender>

        <appender name="FILE" class="ch.qos.logback.core.FileAppender">
            <file>D:/logs/quartz_task_application.log</file>
            <encoder>
                 %d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n

            </encoder>
        </appender>

        <root level="debug">
            <appender-ref ref="STDOUT" />
            <appender-ref ref="FILE" />
        </root>

    </configuration>

View Code

HelloJob.java，具体执行的任务

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    package No01简单的定时任务;

    import org.quartz.Job;
    import org.quartz.JobExecutionContext;
    import org.quartz.JobExecutionException;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;

    public class HelloJob implements Job {

        Logger logger = LoggerFactory.getLogger(this.getClass());

        @Override
        public void execute(JobExecutionContext arg0) throws JobExecutionException {
            // 此任务仅打印日志便于调试、观察
            this.logger.debug(this.getClass().getName() + " trigger...");
        }

    }

View Code

那么，在哪里定义“在什么时候执行什么任务呢？”

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    package No01简单的定时任务;

    import java.util.concurrent.TimeUnit;

    import org.quartz.JobBuilder;
    import org.quartz.JobDetail;
    import org.quartz.Scheduler;
    import org.quartz.SchedulerException;
    import org.quartz.SimpleScheduleBuilder;
    import org.quartz.Trigger;
    import org.quartz.TriggerBuilder;
    import org.quartz.impl.StdSchedulerFactory;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;


    public class Bootstrap {
        private static Logger logger = LoggerFactory.getLogger(Bootstrap.class);

        public static void main(String[] args) {

            try {
                // 获取Scheduler实例
                Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
                scheduler.start();

                // 具体任务
                JobDetail job = JobBuilder.newJob(HelloJob.class).withIdentity("job1", "group1").build();

                // 触发时间点
                SimpleScheduleBuilder simpleScheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
                        .withIntervalInSeconds(5).repeatForever();
                Trigger trigger = TriggerBuilder.newTrigger().withIdentity("trigger1", "group1")
                        .startNow().withSchedule(simpleScheduleBuilder).build();

                // 交由Scheduler安排触发
                scheduler.scheduleJob(job, trigger);

                /* 为观察程序运行，此设置主程序睡眠3分钟才继续往下运行（因下一个步骤是“关闭Scheduler”） */
                try {
                    TimeUnit.MINUTES.sleep(3);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                // 关闭Scheduler
                scheduler.shutdown();

            } catch (SchedulerException se) {
                logger.error(se.getMessage(), se);
            }
        }

    }

View Code

## 在Web应用中使用Quartz

Quartz也常用在Web应用中，常见的是交由Spring托管的形式，但这里并非介绍这个。这里介绍Quartz在Web应用中单独使用。

一般来说，Web应用启动时，应注册已经确定的定时任务；一些动态的、未确定触发时间的定时任务，后续可通过静态的Scheduler注册。

这里使用监听器在应用启动时注册，记得在web.xml注册这个监听器哦(>_<)；在关闭Web应用时，也要相应的注销定时任务。

其他配置文件、Java类与上例子相同，这里只是注册定时任务的地方换成此监听器了。

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    package No02Web应用使用Quartz;

    import javax.servlet.ServletContextEvent;
    import javax.servlet.ServletContextListener;

    import org.quartz.JobBuilder;
    import org.quartz.JobDetail;
    import org.quartz.Scheduler;
    import org.quartz.SchedulerException;
    import org.quartz.SimpleScheduleBuilder;
    import org.quartz.Trigger;
    import org.quartz.TriggerBuilder;
    import org.quartz.impl.StdSchedulerFactory;
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;

    import No01简单的定时任务.HelloJob;

    /**
     * Application Lifecycle Listener implementation class AListener
     *
     */
    public class ApplicationContextListener implements ServletContextListener {

        private Logger logger = LoggerFactory.getLogger(this.getClass());

        public static Scheduler scheduler = null;

        @Override
        public void contextInitialized(ServletContextEvent arg0) {
            this.logger.info("The application start...");

            /* 注册定时任务 */
            try {
                // 获取Scheduler实例
                scheduler = StdSchedulerFactory.getDefaultScheduler();
                scheduler.start();

                // 具体任务
                JobDetail job = JobBuilder.newJob(HelloJob.class).withIdentity("job1", "group1").build();

                // 触发时间点
                SimpleScheduleBuilder simpleScheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
                        .withIntervalInSeconds(5).repeatForever();
                Trigger trigger = TriggerBuilder.newTrigger().withIdentity("trigger1", "group1")
                        .startNow().withSchedule(simpleScheduleBuilder).build();

                // 交由Scheduler安排触发
                scheduler.scheduleJob(job, trigger);

                this.logger.info("The scheduler register...");
            } catch (SchedulerException se) {
                logger.error(se.getMessage(), se);
            }
        }

        @Override
        public void contextDestroyed(ServletContextEvent arg0) {
            this.logger.info("The application stop...");

            /* 注销定时任务 */
            try {
                // 关闭Scheduler
                scheduler.shutdown();

                this.logger.info("The scheduler shutdown...");
            } catch (SchedulerException se) {
                logger.error(se.getMessage(), se);
            }
        }

    }

View Code

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


        <listener>
            <listener-class>No02Web应用使用Quartz.ApplicationContextListener</listener-class>
        </listener>

View Code

**注** ，如果你在Eclipse中调试，可能发现无法看到contextDestroyed方法的执行，请注意用Stop方式（图一）关闭应用，而不是Terminate（图二）。

图一

![](data:image/png;base64,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)

图二

![](data:image/png;base64,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)

## 常用的Cron Schedule

相对于其他方式定义定时任务的触发时间，我们较常用Cron Schedule，小伙伴们也是吧？

Cron Schedule的使用

![](https://images.cnblogs.com/OutliningIndicators/ContractedBlock.gif)![](https://images.cnblogs.com/OutliningIndicators/ExpandedBlockStart.gif)


    // 具体任务
    JobDetail job = JobBuilder.newJob(HelloJob.class).withIdentity("job1", "group1").build();

    // 触发时间点
    CronScheduleBuilder cronScheduleBuilder = CronScheduleBuilder.cronSchedule("0 * * * * ? *");
    Trigger trigger = TriggerBuilder.newTrigger().withIdentity("trigger1", "group1")
            .withSchedule(cronScheduleBuilder).build();

    // 交由Scheduler安排触发
    scheduler.scheduleJob(job, trigger);

View Code

而Cron Expression的学习可参考下列优秀的文章：

[Tutorial - Lesson 6: CronTrigger](http://quartz-scheduler.org/documentation/quartz-2.2.x/tutorials/tutorial-lesson-06)

[Spring - Quartz - cronExpression中问号(?)的解释](http://blog.csdn.net/chh_jiang/article/details/4603529)

## 参考的优秀资料

[Quartz Quick Start Guide](http://quartz-scheduler.org/documentation/quartz-2.2.x/quick-start)

[Chapter 3: Logback configuration](http://logback.qos.ch/manual/configuration.html)
