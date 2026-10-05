---
source: "https://blog.csdn.net/s573626822/article/details/83180567"
title: "springboot2.x之spring-cloud-starter-netflix-zuul-CSDN博客"
fetched_at: "2026-10-05 15:32:30"
---

## [spring cloud连载第三篇补充之Zuul](https://www.cnblogs.com/CLAYJJ/p/9673204.html)

### 由于Zuul的内容较多所以单独列出一篇来讲。全是干货，如果学到东西的，动动小手给点个推荐^_^ 谢谢！

### 1\. Router and Filter: Zuul（路由和过滤：Zuul）

路由是微服务架构不缺少的一部分。例如“/”可能映射到web服务，“/api/users”映射到用户管理服务，而“/api/shop”映射到采购服务。Zuul是Netflix中的一个基于JVM的路由器，也是一个服务端负载均衡器。

zuul有下列用途：

  * Authentication（权限验证）
  * Insights
  * Stress Testing（压力测试）
  * Canary Testing（金丝雀测试）
  * Dynamic Routing（动态路由）
  * Service Migration（服务迁移）
  * Load Shedding（负载削减）
  * Security（安全机制）
  * Static Response handling（静态响应处理）
  * Active/Active traffic management（流量管理）

注意：

1）zuul.max.host.connections已经被zuul.host.maxTotalConnections（默认值200）和zuul.host.maxPerRouteConnections（默认值20）代替了。

2）Hystrix对所有理由的默认隔离模式是SEMAPHORE，可以通过zuul.ribbonIsolationStrategy改为THREAD。

### 1.1 How to Include Zuul（依赖）


    1         <dependency>
    2             <groupId>org.springframework.cloud</groupId>
    3             <artifactId>spring-cloud-starter-netflix-zuul</artifactId>
    4         </dependency>

### 1.2 Embedded Zuul Reverse Proxy（反向代理）

Spring Cloud创建了一个内置Zuul代理来简化开发，比如有一个UI应用想要使用代理调用后端的一个或者多个服务。这可以避免为后台每个服务都配置CORS和权限系统。

在spring boot的入口类上使用@EnableZuulProxy注解来开启代理。代理使用Ribbon通过服务发现来定位后端服务实例。并且所有请求在 [hystrix command](http://cloud.spring.io/spring-cloud-static/Finchley.SR1/single/spring-cloud.html#hystrix-fallbacks-for-routes)中执行。所以当断路器打开时，代理将不会重试连接后端服务。

注意：Zuul starter不包含服务发现客户端，所以想要使用服务发现功能，需要提供一个服务发现客户端（比如Eureka）。

为了防止自动添加服务，可以设置zuul.ignored-services参数来避免。如果一个服务匹配到一个忽略表达式，并且又在路由映射中明确指定了，那么它就不会被忽略。例如（application.yml）：


    1 zuul:
    2   ignoredServices: '*'
    3   routes:
    4     users: /myusers/**

你可以单独指定路径和service ID，例如（application.yml）：


    1  zuul:
    2   routes:
    3     users:
    4       path: /myusers/**
    5       serviceId: users_service

其中path是一个ant风格的表达式，所以/myusers/*仅仅匹配一层目录，而/myusers/**可以匹配任意多层级目录。

其中后端服务的位置既可以使用serviceId也可以使用url（物理位置）指定。如下（application.yml）：


    1  zuul:
    2   routes:
    3     users:
    4       path: /myusers/**
    5       url: http://example.com/users_service

这些简单的url路由不会作为HystrixCommand执行，也不会使用Ribbon负载均衡。如果要使用的话，可以指定一个服务器列表的serviceId，如下：

**application.yml.**

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 zuul:
     2   routes:
     3     echo:
     4       path: /myusers/**
     5       serviceId: myusers-service
     6       stripPrefix: true
     7
     8 hystrix:
     9   command:
    10     myusers-service:
    11       execution:
    12         isolation:
    13           thread:
    14             timeoutInMilliseconds: ...
    15
    16 myusers-service:
    17   ribbon:
    18     NIWSServerListClassName: com.netflix.loadbalancer.ConfigurationBasedServerList
    19     listOfServers: http://example1.com,http://example2.com
    20     ConnectTimeout: 1000
    21     ReadTimeout: 3000
    22     MaxTotalHttpConnections: 500
    23     MaxConnectionsPerHost: 100

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

另一个方法是指定一个服务路由并且为serviceId配置Ribbon客户端（这么做需要在Ribbon中禁用Eureka），如下：

**application.yml.**

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 zuul:
     2   routes:
     3     users:
     4       path: /myusers/**
     5       serviceId: users
     6
     7 ribbon:
     8   eureka:
     9     enabled: false
    10
    11 users:
    12   ribbon:
    13     listOfServers: example.com,google.com

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

可以使用正则表达式来配置路由规则。如下：

**ApplicationConfiguration.java.**


    1 @Bean
    2 public PatternServiceRouteMapper serviceRouteMapper() {
    3     return new PatternServiceRouteMapper(
    4         "(?<name>^.+)-(?<version>v.+$)",
    5         "${version}/${name}");
    6 }

在上面的例子中如果serviceId为myusers-v1那么它将被映射到/v1/myusers/**。如果有一个serviceId不匹配，那么将会使用默认规则。例如，在上面的例子中一个serviceId为myusers的服务将会映射到"/myusers/**"。

给所有映射添加前缀可以使用zuul.prefix。默认情况下，请求被转发前将会去除掉其中的代理前缀（可以使用zuul.stripPrefix=false来改变默认行为）。也可以在单独的一个路由中关闭去除服务指定前缀的行为。如下：

**application.yml.**


    1  zuul:
    2   routes:
    3     users:
    4       path: /myusers/**
    5       stripPrefix: false

注意：zuul.stripPrefix只是针对zuul.prefix，对路由中的路径不起作用。

在上面的例子中/myusers/101请求将会转发为/myusers/101到users服务中。

zuul.routes是绑定在ZuulProperties对象上。在这个类里可以看到retryable属性，将它设置为true，可以在请求失败时使用Ribbon客户端重试。

默认情况下，X-Forwarded-Host将会添加到转发的请求头上，可以设置zuul.addProxyHeaders = false来关闭它。默认情况下，路径中的前缀将会被跳过，转发的请求头中将会有一个X-Forwarded-Prefix头（例如上面例子中的/myusers）。

注意：如果你希望你配置的路由是有序的话，那你应该使用yml配置文件，因为使用properties文件时会丢失排序。

### 1.3 Zuul Http Client（Zuul HTTP客户端）

Zuul的默认HTTP客户端是Apache HTTP客户端而不是已经过时的Ribbon的RestClient。如果要使用RestClient或者okhttp3.OkHttpClient，可以设置`ribbon.restclient.enabled=true` 或者 `ribbon.okhttp.enabled=true。`

如果你想自定义Apache HTTP client 或者 OK HTTP client，那么需要提供一个`ClosableHttpClient` 或者 `OkHttpClient类型的bean。`

### 1.4 Cookies and Sensitive Headers（cookies和敏感头部）

可以在路由配置中指定要忽略的头部，如下：

**application.yml.**


    1 zuul:
    2   routes:
    3     users:
    4       path: /myusers/**
    5       sensitiveHeaders: Cookie,Set-Cookie,Authorization
    6       url: https://downstream

注意：上面的例子是sensitiveHeaders的默认值，这是在Spring Cloud Netflix 1.1版本新增的功能。（在1.0中，不能设置头部并且所有cookie双向流动）。

sensitiveHeaders是一个黑名单，默认不为空。因此要让Zuul发送所有头部的话，需要明确指定sensitiveHeaders为空。如下：

**application.yml.**


    1  zuul:
    2   routes:
    3     users:
    4       path: /myusers/**
    5       sensitiveHeaders:
    6       url: https://downstream

你也可以通过zuul.sensitiveHeader进行全局设置。如果在一个路由上设置sensitiveHeaders的话将会覆盖全局设置。

### 1.5 Ignored Headers（忽略头部）

除了路由敏感头部以外，你还可以设置zuul.ignoredHeaders成那些在与下游服务交互时应该剔除的值。默认，Spring Security不在classpath上时，这些值是空的。否则他们被Spring Security初始化为一些常见的“安全”头部。

这种情况下，下游的服务也可能设置这些头部，但是我们想要的是代理中的值。如果Spring Security在classpath上时，为了不剔除这些安全头部，可以设置zuul.ignoreSecurityHeaders=false。

### 1.6 Management Endpoints（管理端点）

如果你同时使用`@EnableZuulProxy` 和Spring Boot Actuator，那么将会开启两个额外的端点：

  * Routes
  * Filters

#### 1.6.1 Routes Endpoint（路由端点）

get请求/routes：

**GET /routes.**


    1 {
    2   /stores/**: "http://localhost:8081"
    3 }

如果想要得到路由的详细信息，在请求上添加?format=details查询字段。

**GET /routes/details**

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 {
     2   "/stores/**": {
     3     "id": "stores",
     4     "fullPath": "/stores/**",
     5     "location": "http://localhost:8081",
     6     "path": "/**",
     7     "prefix": "/stores",
     8     "retryable": false,
     9     "customSensitiveHeaders": false,
    10     "prefixStripped": true
    11   }
    12 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

/routes的POST方法将会强制刷新路由信息。

可以通过endpoints.routes.enabled=false来禁用这个端点。

注意：路由会自动根据服务目录的改动来更新，但是POST请求/routes是一种立即强制更新的方法。

#### 1.6.2 Filters Endpoint（过滤器端点）

/filters的GET请求将会返回过滤器类型列表。

### 1.7 Strangulation Patterns and Local Forwards（压缩模式和本地转发）

当迁移一个老的应用或者API时，需要慢慢把它的访问端点替换成新的实现。Zuul会是一个很有用的代理，因为你可以使用它处理所有来自客户端老的端点的流量并且重定向一些请求到新的实现上。如下：

**application.yml.**

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1  zuul:
     2   routes:
     3     first:
     4       path: /first/**
     5       url: http://first.example.com
     6     second:
     7       path: /second/**
     8       url: forward:/second
     9     third:
    10       path: /third/**
    11       url: forward:/3rd
    12     legacy:
    13       path: /**
    14       url: http://legacy.example.com

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

其中，forward:开头的url将会转发到本地。

### 1.8 Uploading Files through Zuul（通过Zuul上传文件）

如果你使用@EnableZuulProxy，那么可以通过代理路径来上传一些小文件，对于大文件有一个可以绕过Spring `DispatcherServlet的路径“/zuul/*”，换句话说，如果zuul.routes.customers=/customers/*，那么可以`

通过发送POST请求到/zuul/customers/*。servlet路径是通过zuul.servletPath外部化的。如果代理路由使用Ribbon，尤其大文件需要提高超时时间。如下：

**application.yml.**


    1 hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds: 60000
    2 ribbon:
    3   ConnectTimeout: 3000
    4   ReadTimeout: 60000

### 1.9 Query String Encoding（查询字段编码）

当处理请求时，查询字段将会被解码，这样就可以在Zuul过滤器中修改他们。然后在过滤器中再重新编码后发送请求给后端。如果使用Javascrip的encodeURIComponent()方法，那么结果可能会和原始输入不同。这在大多数情况下不会有问题，但是一些web服务器对于复杂查询字段的编码要求还是很挑剔的。

为了强制查询字符串的原始编码，可以向ZuulProperties传递一个特殊的标志，以便将查询字符串作为HttpServletRequest::getQueryString方法使用。

**application.yml.**


    1  zuul:
    2   forceOriginalQueryStringEncoding: true

注意：这个特殊的标志只对SimpleHostRoutingFilter有效，另外可以通过RequestContext.getCurrentContext().setRequestQueryParams(someOverriddenParameters)来覆盖查询字符串。

### 1.10 Plain Embedded Zuul（纯内置Zuul）

如果使用`@EnableZuulServer` （而不是@EnableZuulProxy），可以启动一个Zuul服务器但是没有任何代理。任何ZuulFilter类型的bean会自动安装，但是没有任何代理过滤器会被自动添加。

这种情况下，Zuul服务器的路由依然可以通过"zuul.routes.*"来配置，但是没有服务发现和代理。因此，"serviceId" 和 "url"会被忽略掉。在下面的例子中所有"/api/**"中的路径都会被映射到Zuul的过滤器链。

**application.yml.**


    1  zuul:
    2   routes:
    3     api: /api/**

### 1.11 Disable Zuul Filters（禁用Zuul过滤器）

在代理和服务器模式，spring cloud Zuul都会默认注册一些ZuulFilter。可以通过zuul.<SimpleClassName>.<filterType>.disable=true来禁用指定的过滤器。

按照惯例，包名中filters的后面就是filterType。例如，如果要禁用org.springframework.cloud.netflix.zuul.filters.post.SendResponseFilter，可以设置zuul.SendResponseFilter.post.disable=true。

### 1.12 Providing Hystrix Fallbacks For Routes（为路由提供Hystrix降级服务）

当Zuul的路由回路出现问题时，可以通过一个FallbackProvider类型的bean来提供降级服务。在这个bean中，需要指定路由的ID，并且提供一个ClientHttpResponse。下面的例子提供了一个相对简单的FallbackProvider的实现。

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 class MyFallbackProvider implements FallbackProvider {
     2
     3     @Override
     4     public String getRoute() {
     5         return "customers";
     6     }
     7
     8     @Override
     9     public ClientHttpResponse fallbackResponse(String route, final Throwable cause) {
    10         if (cause instanceof HystrixTimeoutException) {
    11             return response(HttpStatus.GATEWAY_TIMEOUT);
    12         } else {
    13             return response(HttpStatus.INTERNAL_SERVER_ERROR);
    14         }
    15     }
    16
    17     private ClientHttpResponse response(final HttpStatus status) {
    18         return new ClientHttpResponse() {
    19             @Override
    20             public HttpStatus getStatusCode() throws IOException {
    21                 return status;
    22             }
    23
    24             @Override
    25             public int getRawStatusCode() throws IOException {
    26                 return status.value();
    27             }
    28
    29             @Override
    30             public String getStatusText() throws IOException {
    31                 return status.getReasonPhrase();
    32             }
    33
    34             @Override
    35             public void close() {
    36             }
    37
    38             @Override
    39             public InputStream getBody() throws IOException {
    40                 return new ByteArrayInputStream("fallback".getBytes());
    41             }
    42
    43             @Override
    44             public HttpHeaders getHeaders() {
    45                 HttpHeaders headers = new HttpHeaders();
    46                 headers.setContentType(MediaType.APPLICATION_JSON);
    47                 return headers;
    48             }
    49         };
    50     }
    51 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

下面的例子是对应上面例子的路由配置：


    1 zuul:
    2   routes:
    3     customers: /customers/**

如果要对所有路由提供一个默认降级服务，可以创建一个FallbackProvider类型的bean，然后在getRoute方法中返回“*”或者null。如下：

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 class MyFallbackProvider implements FallbackProvider {
     2     @Override
     3     public String getRoute() {
     4         return "*";
     5     }
     6
     7     @Override
     8     public ClientHttpResponse fallbackResponse(String route, Throwable throwable) {
     9         return new ClientHttpResponse() {
    10             @Override
    11             public HttpStatus getStatusCode() throws IOException {
    12                 return HttpStatus.OK;
    13             }
    14
    15             @Override
    16             public int getRawStatusCode() throws IOException {
    17                 return 200;
    18             }
    19
    20             @Override
    21             public String getStatusText() throws IOException {
    22                 return "OK";
    23             }
    24
    25             @Override
    26             public void close() {
    27
    28             }
    29
    30             @Override
    31             public InputStream getBody() throws IOException {
    32                 return new ByteArrayInputStream("fallback".getBytes());
    33             }
    34
    35             @Override
    36             public HttpHeaders getHeaders() {
    37                 HttpHeaders headers = new HttpHeaders();
    38                 headers.setContentType(MediaType.APPLICATION_JSON);
    39                 return headers;
    40             }
    41         };
    42     }
    43 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

### 1.13 Zuul Timeouts（Zuul的超时时间）

如果想要为通过Zuul代理的请求设置socket超时时间和读取超时时间，你有两个选项，基于配置：

1）如果Zuul使用服务发现，则配置ribbon.ReadTimeout和ribbon.SocketTimeout；

2）如果路由是通过URL指定的，那么需要配置zuul.host.connect-timeout-millis和zuul.host.socket-timeout-millis

### 1.14 Rewriting the `Location` header（重写头部Location字段）

如果Zuul在一个web应用前面，那么你需要重写Location头部当你的web应用通过HTTP状态码3XX重定向。否则，浏览器会重定向到web应用的URL而不是Zuul的URL。

可以通过配置一个LocationRewriteFilter类型的Zuul过滤器来重写Location头部到Zuul的URL。它还恢复了删除的全局前缀和特定于路由的前缀。如下：

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 import org.springframework.cloud.netflix.zuul.filters.post.LocationRewriteFilter;
     2 ...
     3
     4 @Configuration
     5 @EnableZuulProxy
     6 public class ZuulConfig {
     7     @Bean
     8     public LocationRewriteFilter locationRewriteFilter() {
     9         return new LocationRewriteFilter();
    10     }
    11 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

注意：要非常小心使用这个过滤器，因为它会作用于所有响应码为3XX的Location头部，这可能在某些场合不适合。比如要重定向到一个外部地址。

### 1.15 Metrics（度量）

Zuul在Actuator metrics端点下提供metrics，当路由请求出现失败时。可以通过/actuator/metrics端点查看。metrics名称的格式为ZUUL::EXCEPTION:errorCause:statusCode。

### 1.16 Zuul Developer Guide（Zuul开发指南）

#### 1.16.1 The Zuul Servlet

Zuul的实现是一个Servlet。通常情况下，Zuul是嵌入到Spring分发机制中的。Spring MVC会掌控路由。这种情况下，Zuul会缓存请求。如果有一种情况是穿过Zuul但是不要缓存（例如大文件的上传），这时可以使用一种独立于Spring分发器的外部Servlet。默认情况，这个Servlet的地址是/zuul。也可以通过zuul.servlet-path属性来修改。

#### 1.16.2 Zuul RequestContext

Zuul使用`[RequestContext](https://github.com/Netflix/zuul/blob/1.x/zuul-core/src/main/java/com/netflix/zuul/context/RequestContext.java)在不同的过滤器中传递信息。它的数据保存在特定于每个请求的ThreadLocal中.它存储的信息有：路由请求到何处，错误，`HttpServletRequest` 和 `HttpServletResponse。``

RequestContext继承ConcurrentHashMap，所以它可以存储任何信息。`[FilterConstants](https://github.com/spring-cloud/spring-cloud-netflix/blob/master/spring-cloud-netflix-core/src/main/java/org/springframework/cloud/netflix/zuul/filters/support/FilterConstants.java)保存了那些被过滤器使用的key。`

#### `1.16.3 @EnableZuulProxy` vs. `@EnableZuulServer`

Spring Cloud Netflix安装了一系列过滤器，安装了哪些过滤器依赖于你使用哪种注解来开启Zuul的。@EnableZuulProxy是@EnableZuulServer的超集。换句话说，@EnableZuulProxy包含了@EnableZuulServer中的过滤器。

在“proxy”模式中的额外过滤器开启了路由功能。所以如果想要一个“空白”的Zuul，就使用@EnableZuulServer。

#### `1.16.4 @EnableZuulServer` Filters

@EnableZuulServer创建一个SimpleRouteLocator（它从Spring Boot配置文件中加载路由定义）。

安装的过滤器（作为普通的spring bean）：

**1）Pre filters:**

ServletDetectionFilter：检测请求是否是通过Spring Dispatcher，设置FilterConstants.IS_DISPATCHER_SERVLET_REQUEST_KEY的布尔值。

FormBodyWrapperFilter：解析表单数据，并且为下游请求重新编码这些数据。

DebugFilter：如果请求参数中设置了debug，则RequestContext.setDebugRouting()和RequestContext.setDebugRequest()都设置为true。

**2）Route filters：**

SendForwardFilter：使用RequestDispatcher转发请求。转发地址存储在RequestContext的FilterConstants.FORWARD_TO_KEY属性中。

**3）Post filters：**

SendResponseFilter：将代理请求的响应写入到当前的响应中。

**4）Error filters：**

SendErrorFilter：如果RequestContext.getThrowable()不是null，则转发到/error（默认）。也可以error.path设置转发路径。

#### `1.16.5 @EnableZuulProxy` Filters

创建一个 `DiscoveryClientRouteLocator（从DiscoveryClient（例如Eureka）和配置文件中加载路由定义）。为每个服务发现客户端中的serviceId都会创建一个路由。当有新服务添加时，路由就会刷新。`

除了上面的过滤器外，还有额外的过滤器：

**1）Pre filters：**

PreDecorationFilter：根据提供的RouteLocator来决定如何路由，并且路由到何处。并且为下游服务设置了一些代理相关的头部。

**2）Route filters：**

RibbonRoutingFilter：使用Ribbon、Hystrix和可插入的HTTP客户端发送请求。服务ID存储在RequestContext的FilterConstants.SERVICE_ID_KEY键中。

这个过滤器可以使用不同的HTTP客户端：

1️⃣Apache `HttpClient：默认客户端`

2️⃣Squareup `OkHttpClient` v3：添加com.squareup.okhttp3:okhttp依赖，并且设置ribbon.okhttp.enabled=true。

3️⃣Netflix Ribbon HTTP client：设置ribbon.restclient.enabled=true。但是这个客户端有一些限制，它不支持PATCH方法，但是有内建的重试机制。

SimpleHostRoutingFilter：通过Apache HttpClient向预定的url发送请求。URL在RequestContext.getRouteHost()中。

#### 1.16.6 Custom Zuul Filter Examples（自定义Zuul过滤器示例）

下面大多数的例子都包括在[Sample Zuul Filters](https://github.com/spring-cloud-samples/sample-zuul-filters)项目中。这个项目中还包含了一些如果修改请求或者响应的消息体的例子。

How to Write a Pre Filter

Pre filters为在RequestContext中设置数据，给下游的过滤器使用。主要用途就设置一些route过滤器需要的信息。如下：

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 public class QueryParamPreFilter extends ZuulFilter {
     2     @Override
     3     public int filterOrder() {
     4         return PRE_DECORATION_FILTER_ORDER - 1; // run before PreDecoration
     5     }
     6
     7     @Override
     8     public String filterType() {
     9         return PRE_TYPE;
    10     }
    11
    12     @Override
    13     public boolean shouldFilter() {
    14         RequestContext ctx = RequestContext.getCurrentContext();
    15         return !ctx.containsKey(FORWARD_TO_KEY) // a filter has already forwarded
    16                 && !ctx.containsKey(SERVICE_ID_KEY); // a filter has already determined serviceId
    17     }
    18     @Override
    19     public Object run() {
    20         RequestContext ctx = RequestContext.getCurrentContext();
    21         HttpServletRequest request = ctx.getRequest();
    22         if (request.getParameter("sample") != null) {
    23             // put the serviceId in `RequestContext`
    24             ctx.put(SERVICE_ID_KEY, request.getParameter("foo"));
    25         }
    26         return null;
    27     }
    28 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

上面的过滤器使用sample请求参数填充SERVICE_ID_KEY。实际上不应该做这种直接映射，Service ID应该从sample的值中查找。

现在，SERVICE_ID_KEY已经被填充，所以PreDecorationFilter将不会执行，RibbonRoutingFilter会执行。

注意：如果想路由到一个完整的URL，调用ctx.setRouteHost(url)。

要修改路由过滤器转发到的路径，请设置REQUEST_URI_KEY。

How to Write a Route Filter

Route filters在pre filters后执行。它转发请求到其他服务。这里的大部分工作是将请求和响应数据转换到客户机所需的模型。

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 public class OkHttpRoutingFilter extends ZuulFilter {
     2     @Autowired
     3     private ProxyRequestHelper helper;
     4
     5     @Override
     6     public String filterType() {
     7         return ROUTE_TYPE;
     8     }
     9
    10     @Override
    11     public int filterOrder() {
    12         return SIMPLE_HOST_ROUTING_FILTER_ORDER - 1;
    13     }
    14
    15     @Override
    16     public boolean shouldFilter() {
    17         return RequestContext.getCurrentContext().getRouteHost() != null
    18                 && RequestContext.getCurrentContext().sendZuulResponse();
    19     }
    20
    21     @Override
    22     public Object run() {
    23         OkHttpClient httpClient = new OkHttpClient.Builder()
    24                 // customize
    25                 .build();
    26
    27         RequestContext context = RequestContext.getCurrentContext();
    28         HttpServletRequest request = context.getRequest();
    29
    30         String method = request.getMethod();
    31
    32         String uri = this.helper.buildZuulRequestURI(request);
    33
    34         Headers.Builder headers = new Headers.Builder();
    35         Enumeration<String> headerNames = request.getHeaderNames();
    36         while (headerNames.hasMoreElements()) {
    37             String name = headerNames.nextElement();
    38             Enumeration<String> values = request.getHeaders(name);
    39
    40             while (values.hasMoreElements()) {
    41                 String value = values.nextElement();
    42                 headers.add(name, value);
    43             }
    44         }
    45
    46         InputStream inputStream = request.getInputStream();
    47
    48         RequestBody requestBody = null;
    49         if (inputStream != null && HttpMethod.permitsRequestBody(method)) {
    50             MediaType mediaType = null;
    51             if (headers.get("Content-Type") != null) {
    52                 mediaType = MediaType.parse(headers.get("Content-Type"));
    53             }
    54             requestBody = RequestBody.create(mediaType, StreamUtils.copyToByteArray(inputStream));
    55         }
    56
    57         Request.Builder builder = new Request.Builder()
    58                 .headers(headers.build())
    59                 .url(uri)
    60                 .method(method, requestBody);
    61
    62         Response response = httpClient.newCall(builder.build()).execute();
    63
    64         LinkedMultiValueMap<String, String> responseHeaders = new LinkedMultiValueMap<>();
    65
    66         for (Map.Entry<String, List<String>> entry : response.headers().toMultimap().entrySet()) {
    67             responseHeaders.put(entry.getKey(), entry.getValue());
    68         }
    69
    70         this.helper.setResponse(response.code(), response.body().byteStream(),
    71                 responseHeaders);
    72         context.setRouteHost(null); // prevent SimpleHostRoutingFilter from running
    73         return null;
    74     }
    75 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

上面的过滤器将Servlet请求信息转换到OkHttp3请求信息中，并且发送一个HTTP请求，然后将OkHttp3响应信息转换到Servlet响应信息中。

How to Write a Post Filter

Post filters主要是用来修改响应。下面的例子中在响应头中添加一个X-Sample头部并且设置为UUID。

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 public class AddResponseHeaderFilter extends ZuulFilter {
     2     @Override
     3     public String filterType() {
     4         return POST_TYPE;
     5     }
     6
     7     @Override
     8     public int filterOrder() {
     9         return SEND_RESPONSE_FILTER_ORDER - 1;
    10     }
    11
    12     @Override
    13     public boolean shouldFilter() {
    14         return true;
    15     }
    16
    17     @Override
    18     public Object run() {
    19         RequestContext context = RequestContext.getCurrentContext();
    20         HttpServletResponse servletResponse = context.getResponse();
    21         servletResponse.addHeader("X-Sample", UUID.randomUUID().toString());
    22         return null;
    23     }
    24 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

注意：其他操作，比如转换响应体，则要复杂得多，计算量也大得多。

#### 1.16.7 How Zuul Errors Work（Zuul错误）

Zuul过滤器的生命周期的任何阶段出现异常，error过滤器将会执行。当RequestContext.getThrowable()不为null时，SendErrorFilter将会执行。它然后在请求中设置javax.servlet.error.*属性，

然后将请求转发到spring boot的错误页面。

#### 1.16.8 Zuul Eager Application Context Loading

Zuul内部使用Ribbon来请求远程URL。默认，Ribbon客户端在第一次被使用时才被Spring Cloud加载。可以通过下面的配置来改变默认行为。它会在启动时初始化Ribbon相关的上下文。

**application.yml.**


    1 zuul:
    2   ribbon:
    3     eager-load:
    4       enabled: true

### 1.17 Retrying Failed Requests（重试失败请求）

Spring Cloud Netflix提供了许多发送HTTP请求的方法。你可以使用`RestTemplate`, Ribbon, 或者 Feign。无论怎么选择创建HTTP请求，都有可能请求失败。

当请求失败时，你可能想要请求自动重试。当使用Sping Cloud Netflix时，你需要添加[Spring Retry](https://github.com/spring-projects/spring-retry)到classpath上。这样`RestTemplates`, Feign, 和 Zuul会在请求失败时

自动重试。

### 1.17.1 BackOff Policies（补偿政策）

默认，在使用重试机制时是没有补偿政策的。如果你想配置一个补偿政策，则需要创建一个LoadBalancedBackOffPolicyFactory类型的bean。它会为指定的服务创建一个BackOffPolicy。如下：

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)


     1 @Configuration
     2 public class MyConfiguration {
     3     @Bean
     4     LoadBalancedBackOffPolicyFactory backOffPolicyFactory() {
     5         return new LoadBalancedBackOffPolicyFactory() {
     6             @Override
     7             public BackOffPolicy createBackOffPolicy(String service) {
     8                 return new ExponentialBackOffPolicy();
     9             }
    10         };
    11     }
    12 }

![复制代码](https://i-blog.csdnimg.cn/blog_migrate/69c5a8ac3fa60e0848d784a6dd461da6.gif)

### 1.17.2 Configuration（配置）

当你使用Ribbon和Spring Retry时，你可以通过配置某些Ribbon属性来控制重试功能。例如，`client.ribbon.MaxAutoRetries`, `client.ribbon.MaxAutoRetriesNextServer`, 和 `client.ribbon.OkToRetryOnAllOperations。`

注意：开启client.ribbon.OkToRetryOnAllOperations的话将会包括重试POST请求，这样会对服务器资源有些影响，因为它会缓存请求体数据。

另外，你可能希望对某些响应中的状态码进行重试请求。可通过设置clientName.ribbon.retryableStatusCodes。


    1 clientName:
    2   ribbon:
    3     retryableStatusCodes: 404,502

你也可以创建一个LoadBalancedRetryPolicy类型的bean，并且实现retryableStatusCode方法。

#### 1.17.2.1 Zuul

可以通过zuul.retryable设置为false来关闭zuul中的重试机制。也可以设置zuul.routes.routename.retryable为false来关闭某个指定路由上的重试机制。

### 1.18 HTTP Clients

Spring Cloud Netflix 会为Ribbon, Feign, 和 Zuul自动创建HTTP客户端。你也可以提供你自己的HTTP客户端。如果您使用的是Apache Http Cient，那么可以创建类型为ClosableHttpClient的bean，或者如果您使用的是OK Http，则可以创建OkHttpClient。

注意：当您创建自己的HTTP客户机时，您还负责为这些客户机实现正确的连接管理策略。如果没做好会导致资源管理问题。
