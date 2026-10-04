# HTTP协议演进历程

## 1. HTTP协议发展时间线

```
1989年 ──→ HTTP/0.9 ──→ 1996年 ──→ HTTP/1.0 ──→ 1997年 ──→ HTTP/1.1 ──→ 2015年 ──→ HTTP/2
   │           │            │           │            │           │            │           │
 万维网      极简协议      标准化      长连接       主流协议     性能优化     二进制协议   现代Web
 诞生                                  引入                     完善                     需求
```

## 2. HTTP/0.9 - 极简时代（1989年）

### 2.1 基本特性

HTTP/0.9是最原始的HTTP版本，极其简单：

```
请求格式：
GET /path

响应格式：
<html>
  <body>Hello World</body>
</html>
```

### 2.2 技术特点

- **只支持GET方法**
- **没有HTTP头部**
- **只能传输HTML**
- **连接立即关闭**

### 2.3 局限性

```java
// HTTP/0.9 的简单实现
public class Http09Server {
    public void handleRequest(Socket socket) throws IOException {
        BufferedReader in = new BufferedReader(
            new InputStreamReader(socket.getInputStream()));
        PrintWriter out = new PrintWriter(socket.getOutputStream());
        
        String request = in.readLine(); // 只有一行：GET /path
        String path = request.split(" ")[1];
        
        // 直接返回HTML，没有状态码，没有头部
        out.println("<html><body>Content for " + path + "</body></html>");
        
        socket.close(); // 立即关闭连接
    }
}
```

## 3. HTTP/1.0 - 标准化时代（1996年）

### 3.1 重大改进

HTTP/1.0引入了现代HTTP的基础概念：

```
请求格式：
GET /path HTTP/1.0
Host: www.example.com
User-Agent: Mozilla/4.0

响应格式：
HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

### 3.2 新增特性

#### 3.2.1 HTTP头部机制

```java
public class Http10Headers {
    // 请求头
    Map<String, String> requestHeaders = Map.of(
        "Host", "www.example.com",
        "User-Agent", "Mozilla/4.0",
        "Accept", "text/html,application/xhtml+xml",
        "Accept-Language", "en-US,en;q=0.9"
    );
    
    // 响应头
    Map<String, String> responseHeaders = Map.of(
        "Content-Type", "text/html; charset=UTF-8",
        "Content-Length", "1234",
        "Server", "Apache/2.4.41",
        "Date", "Wed, 21 Oct 2015 07:28:00 GMT"
    );
}
```

#### 3.2.2 状态码系统

```java
public enum HttpStatusCode {
    // 1xx 信息性状态码
    CONTINUE(100, "Continue"),
    
    // 2xx 成功状态码
    OK(200, "OK"),
    CREATED(201, "Created"),
    
    // 3xx 重定向状态码
    MOVED_PERMANENTLY(301, "Moved Permanently"),
    FOUND(302, "Found"),
    
    // 4xx 客户端错误
    BAD_REQUEST(400, "Bad Request"),
    UNAUTHORIZED(401, "Unauthorized"),
    NOT_FOUND(404, "Not Found"),
    
    // 5xx 服务器错误
    INTERNAL_SERVER_ERROR(500, "Internal Server Error"),
    BAD_GATEWAY(502, "Bad Gateway");
}
```

#### 3.2.3 多种HTTP方法

```java
public enum HttpMethod {
    GET,     // 获取资源
    POST,    // 提交数据
    PUT,     // 更新资源
    DELETE,  // 删除资源
    HEAD,    // 获取头部信息
    OPTIONS  // 获取支持的方法
}
```

### 3.3 HTTP/1.0的局限性

```java
// HTTP/1.0 的连接模型
public class Http10Connection {
    public void handleRequest() throws IOException {
        Socket socket = new Socket("www.example.com", 80);
        
        // 发送请求
        PrintWriter out = new PrintWriter(socket.getOutputStream());
        out.println("GET /index.html HTTP/1.0");
        out.println("Host: www.example.com");
        out.println(); // 空行表示请求结束
        
        // 接收响应
        BufferedReader in = new BufferedReader(
            new InputStreamReader(socket.getInputStream()));
        String response = in.readLine();
        
        socket.close(); // 每次请求后都要关闭连接
        
        // 如果需要请求另一个资源，必须重新建立连接
        // 这导致了严重的性能问题
    }
}
```

**主要问题：**
- **连接无法复用**：每个请求都需要新的TCP连接
- **TCP握手开销**：每次都要经历三次握手
- **服务器资源浪费**：大量的连接建立和关闭

## 4. HTTP/1.1 - 优化时代（1997年）

### 4.1 核心改进

HTTP/1.1解决了HTTP/1.0的主要性能问题：

#### 4.1.1 持久连接（Keep-Alive）

```java
public class Http11PersistentConnection {
    public void handleMultipleRequests() throws IOException {
        Socket socket = new Socket("www.example.com", 80);
        PrintWriter out = new PrintWriter(socket.getOutputStream());
        BufferedReader in = new BufferedReader(
            new InputStreamReader(socket.getInputStream()));
        
        // 第一个请求
        out.println("GET /index.html HTTP/1.1");
        out.println("Host: www.example.com");
        out.println("Connection: keep-alive"); // 保持连接
        out.println();
        
        String response1 = readResponse(in);
        
        // 第二个请求（复用同一个连接）
        out.println("GET /style.css HTTP/1.1");
        out.println("Host: www.example.com");
        out.println("Connection: keep-alive");
        out.println();
        
        String response2 = readResponse(in);
        
        // 最后一个请求
        out.println("GET /script.js HTTP/1.1");
        out.println("Host: www.example.com");
        out.println("Connection: close"); // 关闭连接
        out.println();
        
        String response3 = readResponse(in);
        socket.close();
    }
}
```

#### 4.1.2 管道化（Pipelining）

```java
public class Http11Pipelining {
    public void pipelineRequests() throws IOException {
        Socket socket = new Socket("www.example.com", 80);
        PrintWriter out = new PrintWriter(socket.getOutputStream());
        
        // 连续发送多个请求，不等待响应
        out.println("GET /page1.html HTTP/1.1");
        out.println("Host: www.example.com");
        out.println();
        
        out.println("GET /page2.html HTTP/1.1");
        out.println("Host: www.example.com");
        out.println();
        
        out.println("GET /page3.html HTTP/1.1");
        out.println("Host: www.example.com");
        out.println("Connection: close");
        out.println();
        
        // 然后按顺序接收响应
        BufferedReader in = new BufferedReader(
            new InputStreamReader(socket.getInputStream()));
        String response1 = readResponse(in);
        String response2 = readResponse(in);
        String response3 = readResponse(in);
    }
}
```

#### 4.1.3 分块传输编码

```java
public class Http11ChunkedTransfer {
    public void sendChunkedResponse(PrintWriter out) {
        out.println("HTTP/1.1 200 OK");
        out.println("Transfer-Encoding: chunked");
        out.println("Content-Type: text/html");
        out.println();
        
        // 发送第一个块
        String chunk1 = "<html><body>";
        out.println(Integer.toHexString(chunk1.length()));
        out.println(chunk1);
        
        // 发送第二个块
        String chunk2 = "<h1>Hello World</h1>";
        out.println(Integer.toHexString(chunk2.length()));
        out.println(chunk2);
        
        // 发送最后一个块
        String chunk3 = "</body></html>";
        out.println(Integer.toHexString(chunk3.length()));
        out.println(chunk3);
        
        // 结束标记
        out.println("0");
        out.println();
    }
}
```

### 4.2 HTTP/1.1的问题

尽管HTTP/1.1有很多改进，但仍存在问题：

#### 4.2.1 队头阻塞（Head-of-Line Blocking）

```java
// 管道化的问题示例
public class HeadOfLineBlocking {
    /*
     * 请求顺序：GET /fast.html, GET /slow.html, GET /another.html
     * 
     * 即使 fast.html 和 another.html 很快就能处理完，
     * 但由于 slow.html 处理时间长，后面的响应都必须等待
     * 
     * 时间线：
     * 0ms:  发送 GET /fast.html
     * 1ms:  发送 GET /slow.html  
     * 2ms:  发送 GET /another.html
     * 10ms: 收到 fast.html 响应
     * 5000ms: 收到 slow.html 响应  ← 阻塞点
     * 5001ms: 收到 another.html 响应 ← 被阻塞
     */
}
```

#### 4.2.2 连接数限制

```java
public class ConnectionLimitation {
    /*
     * 浏览器对同一域名的并发连接数有限制：
     * - Chrome: 6个并发连接
     * - Firefox: 6个并发连接
     * - IE: 2-8个并发连接
     * 
     * 这意味着如果一个页面需要加载很多资源，
     * 就会出现资源加载排队的情况
     */
    
    private static final int MAX_CONNECTIONS_PER_HOST = 6;
    
    public void loadResources(List<String> resources) {
        // 只能同时建立6个连接
        // 其余资源必须等待
        for (int i = 0; i < resources.size(); i += MAX_CONNECTIONS_PER_HOST) {
            List<String> batch = resources.subList(i, 
                Math.min(i + MAX_CONNECTIONS_PER_HOST, resources.size()));
            loadBatch(batch);
        }
    }
}
```

#### 4.2.3 头部冗余

```java
public class HeaderRedundancy {
    /*
     * 每个请求都要发送完整的头部信息：
     * 
     * 请求1：
     * GET /page1.html HTTP/1.1
     * Host: www.example.com
     * User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
     * Accept: text/html,application/xhtml+xml,application/xml;q=0.9...
     * Accept-Language: en-US,en;q=0.5
     * Accept-Encoding: gzip, deflate
     * Cookie: sessionid=abc123; userid=456789
     * 
     * 请求2：
     * GET /style.css HTTP/1.1
     * Host: www.example.com                    ← 重复
     * User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)... ← 重复
     * Accept: text/css,*/*;q=0.1
     * Accept-Language: en-US,en;q=0.5         ← 重复
     * Accept-Encoding: gzip, deflate          ← 重复
     * Cookie: sessionid=abc123; userid=456789 ← 重复
     * 
     * 大量重复信息浪费带宽
     */
}
```

## 5. HTTP/2 - 革命性变化（2015年）

### 5.1 设计目标

HTTP/2的设计目标是解决HTTP/1.1的性能问题：

```java
public class Http2Goals {
    /*
     * 设计目标：
     * 1. 减少延迟 - 通过多路复用、头部压缩
     * 2. 提高吞吐量 - 通过二进制分帧、流优先级
     * 3. 保持兼容性 - 语义层面与HTTP/1.1完全兼容
     * 4. 减少资源消耗 - 单连接、头部压缩
     */
}
```

### 5.2 核心技术创新

#### 5.2.1 二进制分帧

```java
public class Http2BinaryFraming {
    /*
     * HTTP/1.1 文本格式：
     * GET /index.html HTTP/1.1\r\n
     * Host: www.example.com\r\n
     * \r\n
     * 
     * HTTP/2 二进制格式：
     * +-----------------------------------------------+
     * |                 Length (24)                  |
     * +---------------+---------------+---------------+
     * |   Type (8)    |   Flags (8)   |
     * +-+-------------+---------------+-------------------------------+
     * |R|                 Stream Identifier (31)                      |
     * +=+=============================================================+
     * |                   Frame Payload (0...)                      ...
     * +---------------------------------------------------------------+
     */
    
    public class Frame {
        int length;      // 24位：帧载荷长度
        byte type;       // 8位：帧类型
        byte flags;      // 8位：帧标志
        int streamId;    // 31位：流标识符
        byte[] payload;  // 载荷数据
    }
}
```

#### 5.2.2 多路复用

```java
public class Http2Multiplexing {
    /*
     * HTTP/1.1 的串行模式：
     * Connection 1: Request1 → Response1 → Request2 → Response2
     * 
     * HTTP/2 的并行模式：
     * Connection 1: 
     *   Stream 1: Request1 ←→ Response1
     *   Stream 3: Request2 ←→ Response2  
     *   Stream 5: Request3 ←→ Response3
     *   Stream 7: Request4 ←→ Response4
     * 
     * 所有流共享同一个TCP连接，可以并行处理
     */
    
    public class Stream {
        int streamId;           // 奇数：客户端发起，偶数：服务器发起
        StreamState state;      // 流状态
        Queue<Frame> frames;    // 帧队列
        int priority;           // 优先级
    }
    
    enum StreamState {
        IDLE, OPEN, HALF_CLOSED_LOCAL, 
        HALF_CLOSED_REMOTE, CLOSED
    }
}
```

#### 5.2.3 头部压缩（HPACK）

```java
public class Http2HeaderCompression {
    /*
     * HPACK 压缩原理：
     * 1. 静态表：预定义常用头部
     * 2. 动态表：缓存之前出现的头部
     * 3. 霍夫曼编码：压缩字符串
     */
    
    // 静态表示例
    Map<Integer, String> staticTable = Map.of(
        1, ":authority",
        2, ":method GET",
        3, ":method POST",
        4, ":path /",
        5, ":path /index.html",
        8, ":status 200",
        14, "accept-charset",
        15, "accept-encoding gzip, deflate"
    );
    
    // 动态表（FIFO队列）
    Queue<String> dynamicTable = new LinkedList<>();
    
    public byte[] compressHeaders(Map<String, String> headers) {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        
        for (Map.Entry<String, String> header : headers.entrySet()) {
            String name = header.getKey();
            String value = header.getValue();
            
            // 查找静态表
            Integer staticIndex = findInStaticTable(name, value);
            if (staticIndex != null) {
                output.write(encodeIndex(staticIndex));
                continue;
            }
            
            // 查找动态表
            Integer dynamicIndex = findInDynamicTable(name, value);
            if (dynamicIndex != null) {
                output.write(encodeIndex(dynamicIndex + staticTable.size()));
                continue;
            }
            
            // 新头部：添加到动态表并编码
            dynamicTable.offer(name + ": " + value);
            output.write(encodeLiteral(name, value));
        }
        
        return output.toByteArray();
    }
}
```

#### 5.2.4 服务器推送

```java
public class Http2ServerPush {
    /*
     * 传统模式：
     * 1. 客户端请求 index.html
     * 2. 服务器返回 index.html
     * 3. 客户端解析发现需要 style.css
     * 4. 客户端请求 style.css
     * 5. 服务器返回 style.css
     * 
     * HTTP/2 服务器推送：
     * 1. 客户端请求 index.html
     * 2. 服务器推送 style.css (PUSH_PROMISE)
     * 3. 服务器返回 index.html
     * 4. 服务器返回 style.css
     */
    
    public void handleIndexRequest(Http2Connection connection) {
        // 发送 PUSH_PROMISE 帧
        PushPromiseFrame pushPromise = new PushPromiseFrame();
        pushPromise.streamId = 1;  // 原始请求流
        pushPromise.promisedStreamId = 2;  // 推送流
        pushPromise.headers = Map.of(
            ":method", "GET",
            ":path", "/style.css",
            ":authority", "www.example.com"
        );
        connection.sendFrame(pushPromise);
        
        // 发送 index.html 响应
        HeadersFrame indexHeaders = new HeadersFrame();
        indexHeaders.streamId = 1;
        indexHeaders.headers = Map.of(":status", "200");
        connection.sendFrame(indexHeaders);
        
        DataFrame indexData = new DataFrame();
        indexData.streamId = 1;
        indexData.data = loadIndexHtml();
        connection.sendFrame(indexData);
        
        // 发送推送的 style.css
        HeadersFrame cssHeaders = new HeadersFrame();
        cssHeaders.streamId = 2;
        cssHeaders.headers = Map.of(":status", "200");
        connection.sendFrame(cssHeaders);
        
        DataFrame cssData = new DataFrame();
        cssData.streamId = 2;
        cssData.data = loadStyleCss();
        connection.sendFrame(cssData);
    }
}
```

## 6. 性能对比分析

### 6.1 连接建立开销

```java
public class ConnectionOverheadComparison {
    /*
     * HTTP/1.1 (6个并发连接)：
     * - TCP握手：6 × 3 = 18个数据包
     * - TLS握手：6 × 4 = 24个数据包
     * - 总计：42个数据包
     * 
     * HTTP/2 (1个连接)：
     * - TCP握手：1 × 3 = 3个数据包
     * - TLS握手：1 × 4 = 4个数据包
     * - 总计：7个数据包
     * 
     * 减少了 83% 的握手开销
     */
}
```

### 6.2 头部压缩效果

```java
public class HeaderCompressionComparison {
    /*
     * 典型的HTTP请求头部：
     * 
     * HTTP/1.1 原始大小：
     * GET /api/users HTTP/1.1
     * Host: api.example.com
     * User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
     * Accept: application/json, text/plain, */*
     * Accept-Language: en-US,en;q=0.9
     * Accept-Encoding: gzip, deflate, br
     * Cookie: sessionid=abc123def456; userid=789012
     * Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
     * 
     * 总大小：约 800 字节
     * 
     * HTTP/2 HPACK压缩后：约 200 字节
     * 压缩率：75%
     */
}
```

### 6.3 多路复用效果

```java
public class MultiplexingComparison {
    /*
     * 加载包含20个资源的页面：
     * 
     * HTTP/1.1 (6个并发连接)：
     * - 第1批：6个资源并行加载
     * - 第2批：6个资源并行加载  
     * - 第3批：6个资源并行加载
     * - 第4批：2个资源并行加载
     * - 总时间：4个批次的串行时间
     * 
     * HTTP/2 (1个连接，多路复用)：
     * - 所有20个资源可以并行加载
     * - 总时间：最慢资源的加载时间
     * 
     * 性能提升：50-70%
     */
}
```

## 7. 协议演进的启示

### 7.1 技术演进规律

```java
public class ProtocolEvolutionPattern {
    /*
     * 协议演进的一般规律：
     * 
     * 1. 简单起步 (HTTP/0.9)
     *    - 满足基本需求
     *    - 实现简单
     * 
     * 2. 功能完善 (HTTP/1.0)
     *    - 添加必要特性
     *    - 标准化
     * 
     * 3. 性能优化 (HTTP/1.1)
     *    - 解决性能瓶颈
     *    - 向后兼容
     * 
     * 4. 架构革新 (HTTP/2)
     *    - 突破根本限制
     *    - 保持语义兼容
     */
}
```

### 7.2 设计权衡

```java
public class DesignTradeoffs {
    /*
     * 协议设计中的权衡：
     * 
     * 1. 简单性 vs 功能性
     *    - HTTP/0.9: 极简但功能有限
     *    - HTTP/2: 复杂但功能强大
     * 
     * 2. 性能 vs 兼容性
     *    - 二进制格式提升性能但增加复杂度
     *    - 保持语义兼容确保平滑迁移
     * 
     * 3. 灵活性 vs 效率
     *    - 文本协议易于调试
     *    - 二进制协议处理高效
     */
}
```

## 8. 小结

HTTP协议的演进历程展现了网络协议发展的典型模式：

1. **HTTP/0.9**：极简起步，满足基本需求
2. **HTTP/1.0**：标准化，引入现代概念
3. **HTTP/1.1**：性能优化，解决连接问题
4. **HTTP/2**：架构革新，突破根本限制

每个版本都在解决前一版本的主要问题，同时保持向后兼容性。HTTP/2通过二进制分帧、多路复用、头部压缩等技术，彻底解决了HTTP/1.1的性能瓶颈，为现代Web应用提供了强大的基础。

---

**下一步学习**：[HTTP/2核心特性与技术优势](./HTTP2核心特性与技术优势.md) - 深入了解HTTP/2的技术细节