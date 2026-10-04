# C语言Socket系统调用实现详解

## 1. Socket数据传输的完整流程

### 1.1 服务端完整实现
```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>

int main() {
    // 1. 创建Socket
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    // 2. 绑定地址
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);
    bind(server_fd, (struct sockaddr*)&address, sizeof(address));
    
    // 3. 监听连接
    listen(server_fd, 3);
    
    // 4. 接受连接
    int client_fd = accept(server_fd, NULL, NULL);
    
    // 5. 数据传输
    char buffer[1024] = {0};
    
    // 接收数据
    int bytes_received = recv(client_fd, buffer, 1024, 0);
    printf("Received: %s\n", buffer);
    
    // 发送响应
    char *response = "Hello from server";
    send(client_fd, response, strlen(response), 0);
    
    // 6. 关闭连接
    close(client_fd);
    close(server_fd);
    
    return 0;
}
```

### 1.2 客户端完整实现
```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

int main() {
    // 1. 创建Socket
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    
    // 2. 连接服务器
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
    
    connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    
    // 3. 发送数据
    char *message = "Hello from client";
    send(sock, message, strlen(message), 0);
    
    // 4. 接收响应
    char buffer[1024] = {0};
    recv(sock, buffer, 1024, 0);
    printf("Server response: %s\n", buffer);
    
    // 5. 关闭连接
    close(sock);
    
    return 0;
}
```

## 2. 数据发送的底层机制

### 2.1 发送数据流程
```c
// 用户调用send()
int bytes_sent = send(sockfd, data, len, flags);

// 底层流程：
// 1. 用户空间 -> 内核空间数据拷贝
// 2. 数据放入Socket发送缓冲区
// 3. TCP层处理（分段、序列号、校验和）
// 4. IP层处理（路由、分片）
// 5. 网络接口层处理
// 6. 物理传输
```

### 2.2 发送缓冲区管理
```c
// 设置发送缓冲区大小
int send_buffer_size = 65536;
setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, 
           &send_buffer_size, sizeof(send_buffer_size));

// 获取当前缓冲区大小
int current_size;
socklen_t size_len = sizeof(current_size);
getsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, 
           &current_size, &size_len);
```

## 3. 数据接收的底层机制

### 3.1 接收数据流程
```c
// 用户调用recv()
int bytes_received = recv(sockfd, buffer, len, flags);

// 底层流程：
// 1. 网络数据包到达网卡
// 2. 网卡触发中断
// 3. 内核协议栈处理
// 4. 数据放入Socket接收缓冲区
// 5. 内核空间 -> 用户空间数据拷贝
```

### 3.2 接收缓冲区管理
```c
// 设置接收缓冲区大小
int recv_buffer_size = 65536;
setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, 
           &recv_buffer_size, sizeof(recv_buffer_size));

// 非阻塞接收
int flags = fcntl(sockfd, F_GETFL, 0);
fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);

int result = recv(sockfd, buffer, len, MSG_DONTWAIT);
if (result == -1 && errno == EAGAIN) {
    // 没有数据可读
}
```

## 4. 内核Socket数据结构

### 4.1 简化的Socket结构
```c
struct socket {
    struct sock *sk;           // 指向具体协议的sock结构
    struct proto_ops *ops;     // 协议操作函数表
    struct file *file;         // 关联的文件描述符
    unsigned short type;       // Socket类型 (SOCK_STREAM, SOCK_DGRAM)
    unsigned short family;     // 协议族 (AF_INET, AF_INET6)
};

struct sock {
    struct sk_buff_head sk_receive_queue;  // 接收队列
    struct sk_buff_head sk_write_queue;    // 发送队列
    int sk_rcvbuf;                         // 接收缓冲区大小
    int sk_sndbuf;                         // 发送缓冲区大小
    struct sockaddr_in sk_daddr;           // 目标地址
    struct sockaddr_in sk_saddr;           // 源地址
};
```

### 4.2 网络数据包结构 (sk_buff)
```c
struct sk_buff {
    struct sk_buff *next;      // 链表指针
    struct sk_buff *prev;
    
    unsigned char *head;       // 缓冲区开始
    unsigned char *data;       // 数据开始
    unsigned char *tail;       // 数据结束
    unsigned char *end;        // 缓冲区结束
    
    unsigned int len;          // 数据长度
    unsigned int data_len;     // 分片数据长度
    
    struct net_device *dev;    // 网络设备
    struct sock *sk;           // 关联的Socket
};
```

## 5. 系统调用的内核实现

### 5.1 send()系统调用
```c
// 简化的内核实现
asmlinkage long sys_sendto(int fd, void __user *buff, 
                          size_t len, unsigned flags,
                          struct sockaddr __user *addr,
                          int addr_len) {
    struct socket *sock;
    struct msghdr msg;
    struct iovec iov;
    
    // 1. 根据文件描述符获取socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    
    // 2. 构造消息结构
    iov.iov_base = buff;
    iov.iov_len = len;
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    
    // 3. 调用协议特定的发送函数
    err = sock_sendmsg(sock, &msg, len);
    
    return err;
}
```

### 5.2 recv()系统调用
```c
// 简化的内核实现
asmlinkage long sys_recvfrom(int fd, void __user *ubuf, 
                            size_t size, unsigned flags,
                            struct sockaddr __user *addr,
                            int __user *addr_len) {
    struct socket *sock;
    struct msghdr msg;
    struct iovec iov;
    
    // 1. 根据文件描述符获取socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    
    // 2. 构造消息结构
    iov.iov_base = ubuf;
    iov.iov_len = size;
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    
    // 3. 调用协议特定的接收函数
    err = sock_recvmsg(sock, &msg, size, flags);
    
    return err;
}
```

## 6. 内存管理和数据拷贝

### 6.1 用户空间到内核空间拷贝
```c
// copy_from_user - 安全的数据拷贝
static inline unsigned long copy_from_user(void *to, 
                                          const void __user *from, 
                                          unsigned long n) {
    // 检查用户空间地址有效性
    if (access_ok(VERIFY_READ, from, n))
        return __copy_from_user(to, from, n);
    return n;  // 拷贝失败返回未拷贝字节数
}

// copy_to_user - 内核空间到用户空间拷贝
static inline unsigned long copy_to_user(void __user *to, 
                                        const void *from, 
                                        unsigned long n) {
    if (access_ok(VERIFY_WRITE, to, n))
        return __copy_to_user(to, from, n);
    return n;
}
```

### 6.2 sk_buff内存分配
```c
// 分配网络数据包缓冲区
struct sk_buff *alloc_skb(unsigned int size, gfp_t priority) {
    struct sk_buff *skb;
    u8 *data;
    
    // 分配sk_buff结构
    skb = kmem_cache_alloc(skbuff_head_cache, priority);
    if (!skb)
        return NULL;
    
    // 分配数据缓冲区
    size = SKB_DATA_ALIGN(size);
    data = kmalloc(size + sizeof(struct skb_shared_info), priority);
    if (!data) {
        kmem_cache_free(skbuff_head_cache, skb);
        return NULL;
    }
    
    // 初始化sk_buff
    skb->head = data;
    skb->data = data;
    skb->tail = data;
    skb->end = data + size;
    skb->len = 0;
    
    return skb;
}
```

## 7. 错误处理和异常情况

### 7.1 常见错误码
```c
// Socket操作常见错误
switch (errno) {
    case ECONNREFUSED:
        printf("Connection refused\n");
        break;
    case ETIMEDOUT:
        printf("Connection timeout\n");
        break;
    case EWOULDBLOCK:
        printf("Operation would block\n");
        break;
    case EPIPE:
        printf("Broken pipe\n");
        break;
    case ECONNRESET:
        printf("Connection reset by peer\n");
        break;
}
```

### 7.2 缓冲区满处理
```c
// 发送缓冲区满的处理
int send_all(int sockfd, const char *data, size_t len) {
    size_t total_sent = 0;
    
    while (total_sent < len) {
        int sent = send(sockfd, data + total_sent, 
                       len - total_sent, MSG_NOSIGNAL);
        
        if (sent == -1) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                // 缓冲区满，等待后重试
                usleep(1000);
                continue;
            }
            return -1;  // 其他错误
        }
        
        total_sent += sent;
    }
    
    return total_sent;
}
```

## 8. 性能优化技巧

### 8.1 零拷贝技术
```c
// sendfile() - 零拷贝文件传输
#include <sys/sendfile.h>

int send_file(int out_fd, int in_fd, off_t offset, size_t count) {
    return sendfile(out_fd, in_fd, &offset, count);
}

// splice() - 管道零拷贝
ssize_t splice(int fd_in, loff_t *off_in, int fd_out,
               loff_t *off_out, size_t len, unsigned int flags);
```

### 8.2 批量操作
```c
// sendmsg() - 批量发送
struct msghdr msg;
struct iovec iov[3];

iov[0].iov_base = header;
iov[0].iov_len = header_len;
iov[1].iov_base = body;
iov[1].iov_len = body_len;
iov[2].iov_base = footer;
iov[2].iov_len = footer_len;

msg.msg_iov = iov;
msg.msg_iovlen = 3;

sendmsg(sockfd, &msg, 0);
```

## 9. 总结

C语言Socket系统调用的底层实现涉及：

1. **系统调用层**：用户程序与内核的接口
2. **内核Socket层**：Socket数据结构和缓冲区管理
3. **协议栈层**：TCP/IP协议处理
4. **网络设备层**：硬件接口和驱动
5. **内存管理层**：用户态与内核态数据拷贝

关键理解点：
- 数据传输需要多次内存拷贝
- 协议栈的分层处理
- 缓冲区管理的复杂性
- 错误处理的重要性