# HTTP/2核心特性与技术优势

## 1. HTTP/2技术架构概览

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP/2 应用层                        │
├─────────────────────────────────────────────────────────┤
│  多路复用层  │  流控制  │  优先级  │  服务器推送        │
├─────────────────────────────────────────────────────────┤
│              二进制分帧层 (Binary Framing)              │
├─────────────────────────────────────────────────────────┤
│                头部压缩层 (HPACK)                       │
├─────────────────────────────────────────────────────────┤
│                    TLS 1.2+ (加密)                     │
├─────────────────────────────────────────────────────────┤
│                      TCP 传输层                        │
└─────────────────────────────────────────────────────────┘
```

### 1.2 核心设计原则

```java
public class Http2DesignPrinciples {
    /*
     * HTTP/2 的设计原则：
     * 
     * 1. 语义兼容性
     *    - 保持HTTP/1.1的语义不变
     *    - 方法、状态码、头部字段含义相同
     * 
     * 2. 性能优先
     *    - 减少延迟
     *    - 提高吞吐量
     *    - 降低资源消耗
     * 
     * 3. 单连接模型
     *    - 一个域名一个TCP连接
     *    - 通过多路复用实现并发
     * 
     * 4. 二进制协议
     *    - 更高效的解析
     *    - 更紧凑的表示
     */
}
```

## 2. 二进制分帧机制

### 2.1 帧结构详解

```java
public class Http2Frame {
    /*
     * HTTP/2 帧格式：
     * 
     *  0                   1                   2                   3
     *  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     * +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     * |                 Length (24)                   |
     * +---------------+---------------+---------------+
     * |   Type (8)    |   Flags (8)   |
     * +-+-------------+---------------+-------------------------------+
     * |R|                 Stream Identifier (31)                      |
     * +=+=============================================================+
     * |                   Frame Payload (0...)                      ...
     * +---------------------------------------------------------------+
     */
    
    public static class FrameHeader {
        int length;      // 24位：载荷长度 (0-16,777,215)
        byte type;       // 8位：帧类型
        byte flags;      // 8位：帧标志
        int streamId;    // 31位：流标识符 (0-2,147,483,647)
    }
    
    // 帧类型定义
    public enum FrameType {
        DATA(0x0),          // 数据帧
        HEADERS(0x1),       // 头部帧
        PRIORITY(0x2),      // 优先级帧
        RST_STREAM(0x3),    // 流重置帧
        SETTINGS(0x4),      // 设置帧
        PUSH_PROMISE(0x5),  // 推送承诺帧
        PING(0x6),          // PING帧
        GOAWAY(0x7),        // GOAWAY帧
        WINDOW_UPDATE(0x8), // 窗口更新帧
        CONTINUATION(0x9);  // 延续帧
        
        private final int value;
        FrameType(int value) { this.value = value; }
    }
}
```

### 2.2 帧处理实现

```java
public class Http2FrameProcessor {
    public void processFrame(ByteBuffer buffer) {
        // 读取帧头部 (9字节)
        int length = readUInt24(buffer);
        byte type = buffer.get();
        byte flags = buffer.get();
        int streamId = buffer.getInt() & 0x7FFFFFFF; // 清除保留位
        
        // 读取载荷
        byte[] payload = new byte[length];
        buffer.get(payload);
        
        // 根据帧类型处理
        switch (type) {
            case 0x0: // DATA
                processDataFrame(streamId, flags, payload);
                break;
            case 0x1: // HEADERS
                processHeadersFrame(streamId, flags, payload);
                break;
            case 0x4: // SETTINGS
                processSettingsFrame(streamId, flags, payload);
                break;
            // ... 其他帧类型
        }
    }
    
    private void processDataFrame(int streamId, byte flags, byte[] payload) {
        boolean endStream = (flags & 0x1) != 0;
        boolean padded = (flags & 0x8) != 0;
        
        // 处理填充
        int dataStart = 0;
        int dataLength = payload.length;
        if (padded) {
            int padLength = payload[0] & 0xFF;
            dataStart = 1;
            dataLength -= (1 + padLength);
        }
        
        // 提取实际数据
        byte[] data = Arrays.copyOfRange(payload, dataStart, dataStart + dataLength);
        
        // 更新流状态
        Stream stream = getStream(streamId);
        stream.receiveData(data);
        
        if (endStream) {
            stream.closeRemote();
        }
    }
}
```

### 2.3 二进制vs文本协议对比

```java
public class BinaryVsTextComparison {
    /*
     * HTTP/1.1 文本格式：
     * "GET /api/users HTTP/1.1\r\n"
     * "Host: api.example.com\r\n"
     * "Accept: application/json\r\n"
     * "\r\n"
     * 
     * 解析过程：
     * 1. 逐字符扫描
     * 2. 查找分隔符 (\r\n)
     * 3. 字符串分割和解析
     * 4. 类型转换
     * 
     * HTTP/2 二进制格式：
     * [Length][Type][Flags][StreamId][Payload]
     * 
     * 解析过程：
     * 1. 直接读取固定长度字段
     * 2. 无需字符串解析
     * 3. 直接获得数值
     * 
     * 性能提升：
     * - 解析速度：3-5倍提升
     * - 内存使用：减少30-50%
     * - CPU使用：减少20-40%
     */
}
```

## 3. 多路复用技术

### 3.1 流的概念和管理

```java
public class Http2Stream {
    public enum StreamState {
        IDLE,                    // 空闲
        RESERVED_LOCAL,          // 本地保留
        RESERVED_REMOTE,         // 远程保留
        OPEN,                    // 打开
        HALF_CLOSED_LOCAL,       // 本地半关闭
        HALF_CLOSED_REMOTE,      // 远程半关闭
        CLOSED                   // 关闭
    }
    
    private final int streamId;
    private StreamState state;
    private final Queue<Frame> incomingFrames;
    private final Queue<Frame> outgoingFrames;
    private int windowSize;
    private int priority;
    
    public Http2Stream(int streamId) {
        this.streamId = streamId;
        this.state = StreamState.IDLE;
        this.incomingFrames = new ConcurrentLinkedQueue<>();
        this.outgoingFrames = new ConcurrentLinkedQueue<>();
        this.windowSize = 65535; // 默认窗口大小
        this.priority = 16; // 默认优先级
    }
    
    public void sendHeaders(Map<String, String> headers, boolean endStream) {
        HeadersFrame frame = new HeadersFrame();
        frame.streamId = this.streamId;
        frame.headers = headers;
        frame.endStream = endStream;
        
        outgoingFrames.offer(frame);
        
        if (state == StreamState.IDLE) {
            state = endStream ? StreamState.HALF_CLOSED_LOCAL : StreamState.OPEN;
        }
    }
    
    public void sendData(byte[] data, boolean endStream) {
        DataFrame frame = new DataFrame();
        frame.streamId = this.streamId;
        frame.data = data;
        frame.endStream = endStream;
        
        outgoingFrames.offer(frame);
        
        if (endStream && state == StreamState.OPEN) {
            state = StreamState.HALF_CLOSED_LOCAL;
        }
    }
}
```

### 3.2 连接级别的多路复用管理

```java
public class Http2Connection {
    private final Map<Integer, Http2Stream> streams;
    private final AtomicInteger nextStreamId;
    private final boolean isClient;
    private int connectionWindowSize;
    
    public Http2Connection(boolean isClient) {
        this.streams = new ConcurrentHashMap<>();
        this.isClient = isClient;
        this.nextStreamId = new AtomicInteger(isClient ? 1 : 2); // 客户端奇数，服务器偶数
        this.connectionWindowSize = 65535;
    }
    
    public Http2Stream createStream() {
        int streamId = nextStreamId.getAndAdd(2);
        Http2Stream stream = new Http2Stream(streamId);
        streams.put(streamId, stream);
        return stream;
    }
    
    public void processIncomingFrame(Frame frame) {
        if (frame.streamId == 0) {
            // 连接级别的帧
            processConnectionFrame(frame);
        } else {
            // 流级别的帧
            Http2Stream stream = streams.get(frame.streamId);
            if (stream != null) {
                stream.processFrame(frame);
            }
        }
    }
    
    // 并发处理多个流
    public void handleConcurrentStreams() {
        ExecutorService executor = Executors.newCachedThreadPool();
        
        for (Http2Stream stream : streams.values()) {
            executor.submit(() -> {
                while (!stream.isClosed()) {
                    Frame frame = stream.getNextOutgoingFrame();
                    if (frame != null) {
                        sendFrame(frame);
                    }
                }
            });
        }
    }
}
```

### 3.3 多路复用的性能优势

```java
public class MultiplexingPerformance {
    /*
     * 性能对比分析：
     * 
     * 场景：加载包含50个资源的网页
     * 
     * HTTP/1.1 (6个并发连接)：
     * ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
     * │ Conn 1  │ Conn 2  │ Conn 3  │ Conn 4  │ Conn 5  │ Conn 6  │
     * ├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
     * │ Res 1   │ Res 2   │ Res 3   │ Res 4   │ Res 5   │ Res 6   │
     * │ Res 7   │ Res 8   │ Res 9   │ Res 10  │ Res 11  │ Res 12  │
     * │ Res 13  │ Res 14  │ Res 15  │ Res 16  │ Res 17  │ Res 18  │
     * │   ...   │   ...   │   ...   │   ...   │   ...   │   ...   │
     * └─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
     * 
     * 总时间 = ceil(50/6) × 平均资源加载时间 = 9 × 100ms = 900ms
     * 
     * HTTP/2 (1个连接，多路复用)：
     * ┌─────────────────────────────────────────────────────────────┐
     * │                        Single Connection                     │
     * ├─────────────────────────────────────────────────────────────┤
     * │ Stream1 │ Stream3 │ Stream5 │ ... │ Stream97 │ Stream99      │
     * │ Res 1   │ Res 2   │ Res 3   │ ... │ Res 49   │ Res 50        │
     * └─────────────────────────────────────────────────────────────┘
     * 
     * 总时间 = max(所有资源加载时间) ≈ 150ms (考虑带宽限制)
     * 
     * 性能提升：900ms → 150ms = 83% 提升
     */
    
    public class PerformanceMetrics {
        // TCP连接建立时间
        int tcpHandshakeTime = 50; // ms
        
        // HTTP/1.1 总时间
        int http11TotalTime = 6 * tcpHandshakeTime + 900; // 6个连接 + 传输时间
        
        // HTTP/2 总时间  
        int http2TotalTime = 1 * tcpHandshakeTime + 150; // 1个连接 + 传输时间
        
        // 性能提升
        double improvement = (double)(http11TotalTime - http2TotalTime) / http11TotalTime;
        // improvement ≈ 0.84 (84% 提升)
    }
}
```

## 4. 头部压缩（HPACK）

### 4.1 HPACK算法原理

```java
public class HpackCompression {
    /*
     * HPACK 压缩机制：
     * 
     * 1. 静态表 (Static Table)
     *    - 预定义的常用头部字段
     *    - 索引 1-61
     * 
     * 2. 动态表 (Dynamic Table)  
     *    - 连接期间缓存的头部字段
     *    - FIFO 队列，有大小限制
     * 
     * 3. 霍夫曼编码 (Huffman Coding)
     *    - 对字符串进行压缩
     *    - 常用字符用更短的编码
     */
    
    // 静态表（部分）
    private static final Map<Integer, HeaderField> STATIC_TABLE = Map.of(
        1, new HeaderField(":authority", ""),
        2, new HeaderField(":method", "GET"),
        3, new HeaderField(":method", "POST"),
        4, new HeaderField(":path", "/"),
        5, new HeaderField(":path", "/index.html"),
        6, new HeaderField(":scheme", "http"),
        7, new HeaderField(":scheme", "https"),
        8, new HeaderField(":status", "200"),
        9, new HeaderField(":status", "204"),
        10, new HeaderField(":status", "206"),
        // ... 更多条目
        15, new HeaderField("accept-encoding", "gzip, deflate")
    );
    
    // 动态表
    private final Deque<HeaderField> dynamicTable = new ArrayDeque<>();
    private int dynamicTableSize = 0;
    private int maxDynamicTableSize = 4096; // 默认4KB
    
    public byte[] encodeHeaders(List<HeaderField> headers) {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        
        for (HeaderField header : headers) {
            // 1. 查找完全匹配（名称+值）
            Integer index = findFullMatch(header);
            if (index != null) {
                writeIndexedHeader(output, index);
                continue;
            }
            
            // 2. 查找名称匹配
            Integer nameIndex = findNameMatch(header.name);
            if (nameIndex != null) {
                writeLiteralHeaderWithIncrementalIndexing(output, nameIndex, header.value);
                addToDynamicTable(header);
                continue;
            }
            
            // 3. 新的头部字段
            writeLiteralHeaderWithIncrementalIndexing(output, header.name, header.value);
            addToDynamicTable(header);
        }
        
        return output.toByteArray();
    }
    
    private void addToDynamicTable(HeaderField header) {
        int headerSize = header.size(); // name.length + value.length + 32
        
        // 确保有足够空间
        while (dynamicTableSize + headerSize > maxDynamicTableSize && !dynamicTable.isEmpty()) {
            HeaderField removed = dynamicTable.removeLast();
            dynamicTableSize -= removed.size();
        }
        
        // 添加到表头
        dynamicTable.addFirst(header);
        dynamicTableSize += headerSize;
    }
}
```

### 4.2 霍夫曼编码实现

```java
public class HuffmanCoding {
    /*
     * HTTP/2 霍夫曼编码表（部分）：
     * 
     * 字符 | 频率 | 编码
     * -----|------|--------
     * ' '  | 高   | 010100
     * 'e'  | 高   | 0100
     * 't'  | 高   | 0101
     * 'a'  | 高   | 1000
     * 'o'  | 高   | 1001
     * 'i'  | 高   | 1010
     * 'n'  | 高   | 1011
     * 's'  | 高   | 1100
     * 'h'  | 高   | 1101
     * 'r'  | 高   | 1110
     * ...  | ...  | ...
     */
    
    private static final Map<Character, String> HUFFMAN_CODES = Map.of(
        ' ', "010100",
        'e', "0100",
        't', "0101",
        'a', "1000",
        'o', "1001",
        'i', "1010",
        'n', "1011",
        's', "1100",
        'h', "1101",
        'r', "1110"
        // ... 完整的256个字符编码
    );
    
    public byte[] encode(String text) {
        StringBuilder bits = new StringBuilder();
        
        for (char c : text.toCharArray()) {
            String code = HUFFMAN_CODES.get(c);
            if (code != null) {
                bits.append(code);
            } else {
                // 未找到编码，使用原始8位表示
                bits.append(String.format("%8s", Integer.toBinaryString(c)).replace(' ', '0'));
            }
        }
        
        // 填充到字节边界
        while (bits.length() % 8 != 0) {
            bits.append('1'); // EOS符号
        }
        
        // 转换为字节数组
        byte[] result = new byte[bits.length() / 8];
        for (int i = 0; i < result.length; i++) {
            String byteStr = bits.substring(i * 8, (i + 1) * 8);
            result[i] = (byte) Integer.parseInt(byteStr, 2);
        }
        
        return result;
    }
}
```

### 4.3 压缩效果分析

```java
public class CompressionAnalysis {
    /*
     * 真实场景压缩效果：
     * 
     * 原始HTTP头部：
     * GET /api/users/123 HTTP/1.1
     * Host: api.example.com
     * User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
     * Accept: application/json, text/plain, */*
     * Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
     * Accept-Encoding: gzip, deflate, br
     * Connection: keep-alive
     * Cookie: sessionid=abc123def456ghi789; userid=987654321; preferences=theme:dark,lang:en
     * Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
     * 
     * 原始大小：约 1200 字节
     * 
     * HPACK压缩后：
     * 1. 静态表匹配：:method GET (索引2) → 1字节
     * 2. 动态表缓存：Host, User-Agent等常用头部
     * 3. 霍夫曼编码：字符串压缩30-40%
     * 
     * 压缩后大小：约 300 字节
     * 压缩率：75%
     * 
     * 后续请求（动态表生效）：
     * 压缩后大小：约 150 字节
     * 压缩率：87.5%
     */
    
    public void demonstrateCompression() {
        Map<String, String> headers = Map.of(
            ":method", "GET",
            ":path", "/api/users/123",
            ":scheme", "https",
            ":authority", "api.example.com",
            "user-agent", "Mozilla/5.0...",
            "accept", "application/json",
            "cookie", "sessionid=abc123..."
        );
        
        // 第一次请求
        byte[] firstRequest = hpackEncoder.encode(headers);
        System.out.println("第一次请求压缩后大小: " + firstRequest.length);
        
        // 第二次请求（相同头部）
        byte[] secondRequest = hpackEncoder.encode(headers);
        System.out.println("第二次请求压缩后大小: " + secondRequest.length);
        
        // 压缩率提升明显
    }
}
```

## 5. 服务器推送

### 5.1 推送机制原理

```java
public class ServerPush {
    /*
     * 服务器推送流程：
     * 
     * 1. 客户端请求 /index.html
     * 2. 服务器分析依赖：style.css, script.js
     * 3. 服务器发送 PUSH_PROMISE 帧
     * 4. 服务器推送资源
     * 5. 客户端接收并缓存
     * 
     * 时序图：
     * 客户端                    服务器
     *    │                        │
     *    │──── GET /index.html ──→│
     *    │                        │
     *    │←── PUSH_PROMISE ───────│ (承诺推送 style.css)
     *    │    (Stream 2)          │
     *    │                        │
     *    │←── PUSH_PROMISE ───────│ (承诺推送 script.js)
     *    │    (Stream 4)          │
     *    │                        │
     *    │←── HEADERS + DATA ─────│ (index.html 响应)
     *    │    (Stream 1)          │
     *    │                        │
     *    │←── HEADERS + DATA ─────│ (style.css 推送)
     *    │    (Stream 2)          │
     *    │                        │
     *    │←── HEADERS + DATA ─────│ (script.js 推送)
     *    │    (Stream 4)          │
     */
    
    public void handleIndexRequest(Http2Stream requestStream) {
        // 分析请求的资源依赖
        List<String> dependencies = analyzeDependencies("/index.html");
        
        for (String resource : dependencies) {
            if (shouldPush(resource)) {
                // 创建推送流
                Http2Stream pushStream = connection.createStream();
                
                // 发送 PUSH_PROMISE 帧
                PushPromiseFrame pushPromise = new PushPromiseFrame();
                pushPromise.streamId = requestStream.getId();
                pushPromise.promisedStreamId = pushStream.getId();
                pushPromise.headers = Map.of(
                    ":method", "GET",
                    ":path", resource,
                    ":scheme", "https",
                    ":authority", "example.com"
                );
                
                connection.sendFrame(pushPromise);
                
                // 异步推送资源
                CompletableFuture.runAsync(() -> {
                    pushResource(pushStream, resource);
                });
            }
        }
        
        // 发送原始请求的响应
        sendResponse(requestStream, "/index.html");
    }
    
    private boolean shouldPush(String resource) {
        // 推送策略
        return resource.endsWith(".css") || 
               resource.endsWith(".js") ||
               (resource.endsWith(".png") && getFileSize(resource) < 10240); // 小于10KB的图片
    }
}
```

### 5.2 推送缓存管理

```java
public class PushCache {
    /*
     * 客户端推送缓存管理：
     * 
     * 1. 接收推送资源
     * 2. 验证推送合法性
     * 3. 缓存推送资源
     * 4. 处理缓存失效
     */
    
    private final Map<String, CachedResource> pushCache = new ConcurrentHashMap<>();
    
    public void handlePushPromise(PushPromiseFrame frame) {
        String path = frame.headers.get(":path");
        String authority = frame.headers.get(":authority");
        String cacheKey = authority + path;
        
        // 检查是否已经有该资源的请求
        if (hasPendingRequest(cacheKey)) {
            // 取消推送，使用现有请求
            sendRstStream(frame.promisedStreamId, ErrorCode.CANCEL);
            return;
        }
        
        // 检查缓存策略
        if (!shouldAcceptPush(cacheKey)) {
            sendRstStream(frame.promisedStreamId, ErrorCode.REFUSED_STREAM);
            return;
        }
        
        // 准备接收推送资源
        preparePushReception(frame.promisedStreamId, cacheKey);
    }
    
    public void handlePushedResource(int streamId, byte[] data, Map<String, String> headers) {
        String cacheKey = getCacheKey(streamId);
        
        // 创建缓存条目
        CachedResource resource = new CachedResource();
        resource.data = data;
        resource.headers = headers;
        resource.timestamp = System.currentTimeMillis();
        resource.etag = headers.get("etag");
        
        // 存入缓存
        pushCache.put(cacheKey, resource);
        
        // 通知等待的请求
        notifyWaitingRequests(cacheKey, resource);
    }
    
    public CachedResource getFromPushCache(String url) {
        CachedResource resource = pushCache.get(url);
        
        if (resource != null && !isExpired(resource)) {
            return resource;
        }
        
        return null; // 缓存未命中或已过期
    }
    
    static class CachedResource {
        byte[] data;
        Map<String, String> headers;
        long timestamp;
        String etag;
    }
}
```

### 5.3 推送性能优化

```java
public class PushOptimization {
    /*
     * 推送性能优化策略：
     * 
     * 1. 智能推送决策
     * 2. 推送优先级管理
     * 3. 带宽感知推送
     * 4. 推送效果监控
     */
    
    public class IntelligentPushDecision {
        private final Map<String, PushStatistics> pushStats = new ConcurrentHashMap<>();
        
        public boolean shouldPushResource(String resource, ClientContext context) {
            PushStatistics stats = pushStats.get(resource);
            
            // 基于历史数据决策
            if (stats != null) {
                double hitRate = stats.getHitRate();
                if (hitRate < 0.3) { // 命中率低于30%
                    return false;
                }
            }
            
            // 基于客户端特征
            if (context.isSlowConnection()) {
                return resource.endsWith(".css"); // 只推送关键CSS
            }
            
            // 基于资源大小
            long resourceSize = getResourceSize(resource);
            if (resourceSize > context.getMaxPushSize()) {
                return false;
            }
            
            return true;
        }
        
        public void recordPushResult(String resource, boolean wasUsed) {
            pushStats.computeIfAbsent(resource, k -> new PushStatistics())
                    .recordResult(wasUsed);
        }
    }
    
    public class PushPriorityManager {
        public void setPushPriority(Http2Stream pushStream, String resourceType) {
            switch (resourceType) {
                case "css":
                    pushStream.setPriority(1); // 最高优先级
                    break;
                case "js":
                    pushStream.setPriority(2);
                    break;
                case "image":
                    pushStream.setPriority(3); // 最低优先级
                    break;
            }
        }
    }
    
    static class PushStatistics {
        private int totalPushes = 0;
        private int usedPushes = 0;
        
        public void recordResult(boolean wasUsed) {
            totalPushes++;
            if (wasUsed) {
                usedPushes++;
            }
        }
        
        public double getHitRate() {
            return totalPushes > 0 ? (double) usedPushes / totalPushes : 0.0;
        }
    }
}
```

## 6. 流控制机制

### 6.1 流控制原理

```java
public class FlowControl {
    /*
     * HTTP/2 流控制机制：
     * 
     * 1. 连接级别流控制
     *    - 控制整个连接的数据流量
     *    - 防止快速发送方压垮慢速接收方
     * 
     * 2. 流级别流控制
     *    - 控制单个流的数据流量
     *    - 允许不同流有不同的流控策略
     * 
     * 3. 窗口更新机制
     *    - 接收方通过WINDOW_UPDATE帧增加窗口
     *    - 发送方根据窗口大小控制发送速率
     */
    
    public class FlowControlWindow {
        private int windowSize;
        private final int initialWindowSize;
        private final Object lock = new Object();
        
        public FlowControlWindow(int initialSize) {
            this.windowSize = initialSize;
            this.initialWindowSize = initialSize;
        }
        
        public boolean canSend(int dataSize) {
            synchronized (lock) {
                return windowSize >= dataSize;
            }
        }
        
        public void consumeWindow(int dataSize) {
            synchronized (lock) {
                windowSize -= dataSize;
                if (windowSize < 0) {
                    throw new IllegalStateException("Flow control window underflow");
                }
            }
        }
        
        public void updateWindow(int increment) {
            synchronized (lock) {
                long newSize = (long) windowSize + increment;
                if (newSize > Integer.MAX_VALUE) {
                    throw new IllegalArgumentException("Flow control window overflow");
                }
                windowSize = (int) newSize;
                lock.notifyAll(); // 唤醒等待的发送线程
            }
        }
        
        public void waitForWindow(int requiredSize) throws InterruptedException {
            synchronized (lock) {
                while (windowSize < requiredSize) {
                    lock.wait();
                }
            }
        }
    }
}
```

### 6.2 自适应流控制

```java
public class AdaptiveFlowControl {
    /*
     * 自适应流控制策略：
     * 
     * 1. 基于网络状况调整窗口大小
     * 2. 基于应用需求优化流控
     * 3. 动态调整更新频率
     */
    
    public class AdaptiveWindowManager {
        private int currentWindowSize;
        private final int minWindowSize = 32 * 1024;    // 32KB
        private final int maxWindowSize = 16 * 1024 * 1024; // 16MB
        private long lastUpdateTime;
        private int bytesReceived;
        private double averageThroughput;
        
        public void onDataReceived(int dataSize) {
            bytesReceived += dataSize;
            long currentTime = System.currentTimeMillis();
            
            // 每秒计算一次吞吐量
            if (currentTime - lastUpdateTime >= 1000) {
                double throughput = (double) bytesReceived / (currentTime - lastUpdateTime) * 1000;
                updateAverageThroughput(throughput);
                
                // 调整窗口大小
                adjustWindowSize();
                
                // 重置计数器
                bytesReceived = 0;
                lastUpdateTime = currentTime;
            }
        }
        
        private void adjustWindowSize() {
            // 基于吞吐量调整窗口
            if (averageThroughput > getTargetThroughput() * 1.2) {
                // 吞吐量高，增加窗口
                currentWindowSize = Math.min(currentWindowSize * 2, maxWindowSize);
            } else if (averageThroughput < getTargetThroughput() * 0.8) {
                // 吞吐量低，减少窗口
                currentWindowSize = Math.max(currentWindowSize / 2, minWindowSize);
            }
        }
        
        public int getOptimalUpdateThreshold() {
            // 当消费了一半窗口时发送更新
            return currentWindowSize / 2;
        }
    }
}
```

## 7. 性能优化与最佳实践

### 7.1 连接优化

```java
public class ConnectionOptimization {
    /*
     * HTTP/2 连接优化策略：
     * 
     * 1. 连接预热
     * 2. 设置优化
     * 3. 连接复用
     * 4. 优雅关闭
     */
    
    public void optimizeConnection(Http2Connection connection) {
        // 1. 发送优化的SETTINGS帧
        SettingsFrame settings = new SettingsFrame();
        settings.parameters.put(SETTINGS_HEADER_TABLE_SIZE, 8192);      // 增加头部表大小
        settings.parameters.put(SETTINGS_ENABLE_PUSH, 1);               // 启用服务器推送
        settings.parameters.put(SETTINGS_MAX_CONCURRENT_STREAMS, 100);  // 增加并发流数量
        settings.parameters.put(SETTINGS_INITIAL_WINDOW_SIZE, 1048576); // 1MB初始窗口
        settings.parameters.put(SETTINGS_MAX_FRAME_SIZE, 32768);        // 32KB最大帧大小
        connection.sendFrame(settings);
        
        // 2. 连接级别窗口更新
        WindowUpdateFrame windowUpdate = new WindowUpdateFrame();
        windowUpdate.streamId = 0; // 连接级别
        windowUpdate.increment = 15728640; // 15MB
        connection.sendFrame(windowUpdate);
        
        // 3. 启用连接预热
        warmupConnection(connection);
    }
    
    private void warmupConnection(Http2Connection connection) {
        // 发送PING帧测试连接
        PingFrame ping = new PingFrame();
        ping.data = System.currentTimeMillis();
        connection.sendFrame(ping);
        
        // 预创建一些流对象
        for (int i = 0; i < 10; i++) {
            connection.preCreateStream();
        }
    }
}
```

### 7.2 资源优化策略

```java
public class ResourceOptimization {
    /*
     * 资源优化策略：
     * 
     * 1. 资源优先级设置
     * 2. 关键资源推送
     * 3. 资源合并策略
     * 4. 缓存优化
     */
    
    public class ResourcePriorityManager {
        public void setResourcePriorities(List<Resource> resources) {
            for (Resource resource : resources) {
                int priority = calculatePriority(resource);
                resource.getStream().setPriority(priority);
            }
        }
        
        private int calculatePriority(Resource resource) {
            // 关键渲染路径资源优先级最高
            if (resource.isCriticalRenderingPath()) {
                return 1;
            }
            
            // CSS 文件高优先级
            if (resource.getType().equals("css")) {
                return 2;
            }
            
            // JavaScript 文件中等优先级
            if (resource.getType().equals("js")) {
                return 3;
            }
            
            // 图片等其他资源低优先级
            return 4;
        }
    }
    
    public class CriticalResourcePush {
        public void pushCriticalResources(String requestPath) {
            List<String> criticalResources = identifyCriticalResources(requestPath);
            
            for (String resource : criticalResources) {
                if (shouldPush(resource)) {
                    pushResource(resource, Priority.HIGH);
                }
            }
        }
        
        private List<String> identifyCriticalResources(String path) {
            // 基于页面分析确定关键资源
            if (path.equals("/")) {
                return List.of("/css/critical.css", "/js/above-fold.js");
            } else if (path.startsWith("/product/")) {
                return List.of("/css/product.css", "/js/product-viewer.js");
            }
            
            return Collections.emptyList();
        }
    }
}
```

## 8. 小结

HTTP/2通过以下核心技术实现了显著的性能提升：

### 8.1 技术创新总结

1. **二进制分帧**：提高解析效率，减少错误
2. **多路复用**：解决队头阻塞，提高并发性
3. **头部压缩**：减少带宽消耗，降低延迟
4. **服务器推送**：主动推送资源，减少往返时间
5. **流控制**：防止缓冲区溢出，优化资源利用

### 8.2 性能提升效果

- **延迟降低**：50-70%
- **带宽利用率**：提升30-50%
- **并发处理能力**：提升5-10倍
- **服务器资源消耗**：降低20-40%

### 8.3 适用场景

HTTP/2特别适合：
- 现代Web应用
- 移动应用后端API
- 实时数据传输
- 微服务架构
- CDN和边缘计算

HTTP/2的这些技术创新为现代互联网应用提供了强大的基础设施支持，是Web性能优化的重要里程碑。

---

**相关学习**：[gRPC协议](../gRPC协议/导航.md) - 基于HTTP/2的高性能RPC框架