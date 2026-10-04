# send/recv系统调用底层机制详解

## 1. 系统调用入口机制

### 1.1 用户态到内核态转换
```c
// 用户程序调用
int result = send(sockfd, data, len, flags);

// 汇编层面的系统调用
// x86_64架构下：
// mov $SYS_sendto, %rax    // 系统调用号
// mov sockfd, %rdi         // 第一个参数
// mov data, %rsi           // 第二个参数
// mov len, %rdx            // 第三个参数
// mov flags, %r10          // 第四个参数
// syscall                  // 触发系统调用
```

### 1.2 系统调用表和分发
```c
// 系统调用表 (简化)
const sys_call_ptr_t sys_call_table[__NR_syscall_max+1] = {
    [__NR_socket] = sys_socket,
    [__NR_bind] = sys_bind,
    [__NR_listen] = sys_listen,
    [__NR_accept] = sys_accept,
    [__NR_sendto] = sys_sendto,
    [__NR_recvfrom] = sys_recvfrom,
    // ... 其他系统调用
};

// 系统调用分发器
asmlinkage long system_call(struct pt_regs *regs) {
    unsigned long nr = regs->orig_ax;
    
    if (nr >= __NR_syscall_max)
        return -ENOSYS;
    
    return sys_call_table[nr](regs->di, regs->si, regs->dx, 
                             regs->r10, regs->r8, regs->r9);
}
```

## 2. send系统调用完整实现

### 2.1 sys_sendto内核实现
```c
SYSCALL_DEFINE6(sendto, int, fd, void __user *, buff, size_t, len,
                unsigned int, flags, struct sockaddr __user *, addr,
                int, addr_len) {
    struct socket *sock;
    struct sockaddr_storage address;
    int err;
    struct msghdr msg;
    struct iovec iov;
    int fput_needed;
    
    // 1. 参数验证
    if (len > INT_MAX)
        len = INT_MAX;
    
    // 2. 根据文件描述符查找socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (!sock)
        goto out;
    
    // 3. 构造消息结构
    iov.iov_base = buff;
    iov.iov_len = len;
    msg.msg_name = NULL;
    msg.msg_iov = &iov;
    msg.msg_iovlen = 1;
    msg.msg_control = NULL;
    msg.msg_controllen = 0;
    msg.msg_namelen = 0;
    
    // 4. 处理目标地址
    if (addr) {
        err = move_addr_to_kernel(addr, addr_len, &address);
        if (err < 0)
            goto out_put;
        msg.msg_name = (struct sockaddr *)&address;
        msg.msg_namelen = addr_len;
    }
    
    // 5. 设置标志
    if (sock->file->f_flags & O_NONBLOCK)
        flags |= MSG_DONTWAIT;
    msg.msg_flags = flags;
    
    // 6. 调用socket层发送函数
    err = sock_sendmsg(sock, &msg, len);
    
out_put:
    fput_light(sock->file, fput_needed);
out:
    return err;
}
```

### 2.2 sockfd_lookup_light实现
```c
static struct socket *sockfd_lookup_light(int fd, int *err, int *fput_needed) {
    struct file *file;
    struct socket *sock;
    
    *err = -EBADF;
    
    // 从文件描述符表获取file结构
    file = fget_light(fd, fput_needed);
    if (file) {
        // 检查是否为socket文件
        sock = sock_from_file(file, err);
        if (sock)
            return sock;
        fput_light(file, *fput_needed);
    }
    return NULL;
}

// 从file结构获取socket
struct socket *sock_from_file(struct file *file, int *err) {
    if (file->f_op == &socket_file_ops)
        return file->private_data;  // socket结构存储在private_data中
    
    *err = -ENOTSOCK;
    return NULL;
}
```

### 2.3 sock_sendmsg实现
```c
int sock_sendmsg(struct socket *sock, struct msghdr *msg, size_t size) {
    struct kiocb iocb;
    struct sock_iocb siocb;
    int ret;
    
    // 初始化异步I/O控制块
    init_sync_kiocb(&iocb, sock->file);
    iocb.private = &siocb;
    siocb.sock = sock;
    siocb.scm = NULL;
    siocb.msg = msg;
    siocb.size = size;
    
    // 调用协议特定的sendmsg函数
    ret = sock->ops->sendmsg(&iocb, sock, msg, size);
    
    return ret;
}
```

## 3. 协议多态机制详解

### 3.1 proto_ops结构体
```c
struct proto_ops {
    int family;
    struct module *owner;
    
    // 函数指针表
    int (*release)(struct socket *sock);
    int (*bind)(struct socket *sock, struct sockaddr *myaddr, int sockaddr_len);
    int (*connect)(struct socket *sock, struct sockaddr *vaddr, int sockaddr_len, int flags);
    int (*socketpair)(struct socket *sock1, struct socket *sock2);
    int (*accept)(struct socket *sock, struct socket *newsock, int flags);
    int (*getname)(struct socket *sock, struct sockaddr *addr, int *sockaddr_len, int peer);
    unsigned int (*poll)(struct file *file, struct socket *sock, struct poll_table_struct *wait);
    int (*ioctl)(struct socket *sock, unsigned int cmd, unsigned long arg);
    int (*listen)(struct socket *sock, int len);
    int (*shutdown)(struct socket *sock, int flags);
    int (*setsockopt)(struct socket *sock, int level, int optname, char __user *optval, unsigned int optlen);
    int (*getsockopt)(struct socket *sock, int level, int optname, char __user *optval, int __user *optlen);
    int (*sendmsg)(struct kiocb *iocb, struct socket *sock, struct msghdr *m, size_t total_len);
    int (*recvmsg)(struct kiocb *iocb, struct socket *sock, struct msghdr *m, size_t total_len, int flags);
    // ... 其他函数指针
};
```

### 3.2 TCP协议的proto_ops实现
```c
const struct proto_ops inet_stream_ops = {
    .family        = PF_INET,
    .owner         = THIS_MODULE,
    .release       = inet_release,
    .bind          = inet_bind,
    .connect       = inet_stream_connect,
    .socketpair    = sock_no_socketpair,
    .accept        = inet_accept,
    .getname       = inet_getname,
    .poll          = tcp_poll,
    .ioctl         = inet_ioctl,
    .listen        = inet_listen,
    .shutdown      = inet_shutdown,
    .setsockopt    = sock_common_setsockopt,
    .getsockopt    = sock_common_getsockopt,
    .sendmsg       = inet_sendmsg,    // TCP发送入口
    .recvmsg       = inet_recvmsg,    // TCP接收入口
    // ... 其他实现
};
```

### 3.3 inet_sendmsg实现
```c
int inet_sendmsg(struct kiocb *iocb, struct socket *sock, 
                 struct msghdr *msg, size_t size) {
    struct sock *sk = sock->sk;
    
    // 调用传输层协议的sendmsg
    return sk->sk_prot->sendmsg(iocb, sk, msg, size);
}
```

### 3.4 TCP协议的proto结构
```c
struct proto tcp_prot = {
    .name            = "TCP",
    .owner           = THIS_MODULE,
    .close           = tcp_close,
    .connect         = tcp_v4_connect,
    .disconnect      = tcp_disconnect,
    .accept          = inet_csk_accept,
    .ioctl           = tcp_ioctl,
    .init            = tcp_v4_init_sock,
    .destroy         = tcp_v4_destroy_sock,
    .shutdown        = tcp_shutdown,
    .setsockopt      = tcp_setsockopt,
    .getsockopt      = tcp_getsockopt,
    .sendmsg         = tcp_sendmsg,    // TCP具体发送实现
    .recvmsg         = tcp_recvmsg,    // TCP具体接收实现
    .sendpage        = tcp_sendpage,
    .backlog_rcv     = tcp_v4_do_rcv,
    // ... 其他TCP特定实现
};
```

## 4. tcp_sendmsg详细实现

### 4.1 tcp_sendmsg核心逻辑
```c
int tcp_sendmsg(struct kiocb *iocb, struct sock *sk, 
                struct msghdr *msg, size_t size) {
    struct tcp_sock *tp = tcp_sk(sk);
    struct sk_buff *skb;
    int flags, err, copied = 0;
    int mss_now = 0, size_goal, copied_syn = 0, offset = 0;
    bool sg;
    long timeo;
    
    // 1. 检查socket状态
    lock_sock(sk);
    
    flags = msg->msg_flags;
    if (flags & MSG_FASTOPEN) {
        err = tcp_sendmsg_fastopen(sk, msg, &copied_syn, size);
        if (err == -EINPROGRESS && copied_syn > 0)
            goto out;
        else if (err)
            goto out_err;
        offset = copied_syn;
    }
    
    timeo = sock_sndtimeo(sk, flags & MSG_DONTWAIT);
    
    // 2. 等待TCP连接建立
    if (((1 << sk->sk_state) & ~(TCPF_ESTABLISHED | TCPF_CLOSE_WAIT)) &&
        !tcp_passive_fastopen(sk)) {
        if ((err = sk_stream_wait_connect(sk, &timeo)) != 0)
            goto do_error;
    }
    
    // 3. 处理紧急数据
    if (unlikely(tp->repair)) {
        if (tp->repair_queue == TCP_RECV_QUEUE) {
            copied = tcp_send_rcvq(sk, msg, size);
            goto out;
        }
        
        err = -EINVAL;
        if (tp->repair_queue == TCP_NO_QUEUE)
            goto out_err;
    }
    
    // 4. 获取MSS和目标大小
    mss_now = tcp_send_mss(sk, &size_goal, flags);
    
    // 5. 主要数据发送循环
    sg = !!(sk->sk_route_caps & NETIF_F_SG);
    
    while (msg_data_left(msg)) {
        int copy = 0;
        int max = size_goal;
        
        // 获取或分配sk_buff
        skb = tcp_write_queue_tail(sk);
        if (tcp_send_head(sk)) {
            if (skb->ip_summed == CHECKSUM_NONE)
                max = mss_now;
            copy = max - skb->len;
        }
        
        if (copy <= 0) {
new_segment:
            // 分配新的sk_buff
            if (!sk_stream_memory_free(sk))
                goto wait_for_sndbuf;
            
            skb = sk_stream_alloc_skb(sk,
                                    select_size(sk, sg),
                                    sk->sk_allocation);
            if (!skb)
                goto wait_for_memory;
            
            // 设置skb属性
            skb_entail(sk, skb);
            copy = size_goal;
            max = size_goal;
        }
        
        // 6. 拷贝数据到sk_buff
        if (copy > msg_data_left(msg))
            copy = msg_data_left(msg);
        
        // 关键：数据拷贝函数
        err = skb_add_data_nocache(sk, skb, &msg->msg_iter, copy);
        if (err)
            goto do_fault;
        
        // 更新统计信息
        if (!copied)
            TCP_SKB_CB(skb)->tcp_flags &= ~TCPHDR_PSH;
        
        tp->write_seq += copy;
        TCP_SKB_CB(skb)->end_seq += copy;
        tcp_skb_pcount_set(skb, 0);
        
        copied += copy;
        if (!msg_data_left(msg)) {
            tcp_tx_timestamp(sk, skb);
            goto out;
        }
        
        // 检查是否需要立即发送
        if (forced_push(tp)) {
            tcp_mark_push(tp, skb);
            __tcp_push_pending_frames(sk, mss_now, TCP_NAGLE_PUSH);
        } else if (skb == tcp_send_head(sk))
            tcp_push_one(sk, mss_now);
        continue;
        
wait_for_sndbuf:
        set_bit(SOCK_NOSPACE, &sk->sk_socket->flags);
wait_for_memory:
        if (copied)
            tcp_push(sk, flags & ~MSG_MORE, mss_now, 
                     TCP_NAGLE_PUSH, size_goal);
        
        if ((err = sk_stream_wait_memory(sk, &timeo)) != 0)
            goto do_error;
        
        mss_now = tcp_send_mss(sk, &size_goal, flags);
    }
    
out:
    // 7. 发送数据
    if (copied && !(flags & MSG_SENDPAGE_NOTLAST))
        tcp_push(sk, flags, mss_now, tp->nonagle, size_goal);
    
    release_sock(sk);
    return copied + copied_syn;
    
do_fault:
    if (!skb->len) {
        tcp_unlink_write_queue(skb, sk);
        sk_wmem_free_skb(sk, skb);
    }
    
do_error:
    if (copied + copied_syn)
        goto out;
out_err:
    err = sk_stream_error(sk, flags, err);
    release_sock(sk);
    return err;
}
```

## 5. 关键函数详解

### 5.1 skb_add_data_nocache实现
```c
static inline int skb_add_data_nocache(struct sock *sk, struct sk_buff *skb,
                                      struct iov_iter *from, int copy) {
    int err, offset = skb->len;
    
    // 扩展skb数据区域
    err = skb_do_copy_data_nocache(sk, skb, from, 
                                  skb_put(skb, copy), copy,
                                  offset);
    if (err)
        __skb_trim(skb, offset);  // 失败时回滚
    
    return err;
}

static int skb_do_copy_data_nocache(struct sock *sk, struct sk_buff *skb,
                                   struct iov_iter *from, char *to,
                                   int copy, int offset) {
    // 检查是否需要计算校验和
    if (skb->ip_summed == CHECKSUM_NONE) {
        __wsum csum = 0;
        // 拷贝数据并计算校验和
        if (csum_and_copy_from_iter(to, copy, &csum, from) != copy)
            return -EFAULT;
        skb->csum = csum_block_add(skb->csum, csum, offset);
    } else {
        // 硬件校验和卸载，直接拷贝
        if (copy_from_iter(to, copy, from) != copy)
            return -EFAULT;
    }
    return 0;
}
```

### 5.2 tcp_push实现
```c
static inline void tcp_push(struct sock *sk, int flags, int mss_now,
                           int nonagle, int size_goal) {
    if (tcp_send_head(sk)) {
        struct tcp_sock *tp = tcp_sk(sk);
        
        // 设置PSH标志
        if (!(flags & MSG_MORE) || forced_push(tp))
            tcp_mark_push(tp, tcp_write_queue_tail(sk));
        
        // 设置紧急指针
        tcp_mark_urg(tp, flags);
        
        // 触发实际发送
        __tcp_push_pending_frames(sk, mss_now, nonagle);
    }
}

void __tcp_push_pending_frames(struct sock *sk, unsigned int cur_mss,
                              int nonagle) {
    if (unlikely(sk->sk_state == TCP_CLOSE))
        return;
    
    if (tcp_write_xmit(sk, cur_mss, nonagle, 0,
                      sk_gfp_atomic(sk, GFP_ATOMIC)))
        tcp_check_probe_timer(sk);
}
```

## 6. recv系统调用实现

### 6.1 sys_recvfrom内核实现
```c
SYSCALL_DEFINE6(recvfrom, int, fd, void __user *, ubuf, size_t, size,
                unsigned int, flags, struct sockaddr __user *, addr,
                int __user *, addr_len) {
    struct socket *sock;
    struct iovec iov;
    struct msghdr msg;
    struct sockaddr_storage address;
    int err, err2;
    int fput_needed;
    
    // 1. 参数验证
    if (size > INT_MAX)
        size = INT_MAX;
    
    // 2. 查找socket
    sock = sockfd_lookup_light(fd, &err, &fput_needed);
    if (!sock)
        goto out;
    
    // 3. 构造消息结构
    msg.msg_control = NULL;
    msg.msg_controllen = 0;
    msg.msg_iovlen = 1;
    msg.msg_iov = &iov;
    iov.iov_len = size;
    iov.iov_base = ubuf;
    msg.msg_name = (struct sockaddr *)&address;
    msg.msg_namelen = sizeof(address);
    
    // 4. 设置标志
    if (sock->file->f_flags & O_NONBLOCK)
        flags |= MSG_DONTWAIT;
    
    // 5. 调用接收函数
    err = sock_recvmsg(sock, &msg, size, flags);
    
    // 6. 拷贝地址信息到用户空间
    if (err >= 0 && addr != NULL) {
        err2 = move_addr_to_user(&address,
                                msg.msg_namelen, addr, addr_len);
        if (err2 < 0)
            err = err2;
    }
    
    fput_light(sock->file, fput_needed);
out:
    return err;
}
```

### 6.2 tcp_recvmsg实现
```c
int tcp_recvmsg(struct kiocb *iocb, struct sock *sk, struct msghdr *msg,
                size_t len, int nonblock, int flags, int *addr_len) {
    struct tcp_sock *tp = tcp_sk(sk);
    int copied = 0;
    u32 peek_seq;
    u32 *seq;
    unsigned long used;
    int err;
    int target;        /* Read at least this many bytes */
    long timeo;
    struct task_struct *user_recv = NULL;
    struct sk_buff *skb;
    u32 urg_hole = 0;
    
    // 1. 参数检查和初始化
    lock_sock(sk);
    
    err = -ENOTCONN;
    if (sk->sk_state == TCP_LISTEN)
        goto out;
    
    timeo = sock_rcvtimeo(sk, nonblock);
    
    // 2. 处理紧急数据
    if (flags & MSG_OOB)
        goto recv_urg;
    
    if (unlikely(tp->repair)) {
        err = -EPERM;
        if (!(flags & MSG_PEEK))
            goto out;
        
        if (tp->repair_queue == TCP_SEND_QUEUE)
            goto recv_sndq;
        
        err = -EINVAL;
        if (tp->repair_queue == TCP_NO_QUEUE)
            goto out;
    }
    
    seq = &tp->copied_seq;
    if (flags & MSG_PEEK) {
        peek_seq = tp->copied_seq;
        seq = &peek_seq;
    }
    
    target = sock_rcvlowat(sk, flags & MSG_WAITALL, len);
    
    // 3. 主接收循环
    do {
        u32 offset;
        
        // 检查接收队列
        skb_queue_walk(&sk->sk_receive_queue, skb) {
            offset = *seq - TCP_SKB_CB(skb)->seq;
            
            // 检查数据是否可用
            if (TCP_SKB_CB(skb)->tcp_flags & TCPHDR_SYN) {
                pr_err_once("%s: found a SYN, please report !\n", __func__);
                offset--;
            }
            if (offset < skb->len)
                goto found_ok_skb;
            
            // 处理FIN
            if (TCP_SKB_CB(skb)->tcp_flags & TCPHDR_FIN)
                goto found_fin_ok;
        }
        
        // 4. 没有数据可读，检查是否需要等待
        if (copied >= target && !sk->sk_backlog.tail)
            break;
        
        if (copied) {
            if (sk->sk_err ||
                sk->sk_state == TCP_CLOSE ||
                (sk->sk_shutdown & RCV_SHUTDOWN) ||
                !timeo ||
                signal_pending(current))
                break;
        } else {
            if (sock_flag(sk, SOCK_DONE))
                break;
            
            if (sk->sk_err) {
                copied = sock_error(sk);
                break;
            }
            
            if (sk->sk_shutdown & RCV_SHUTDOWN)
                break;
            
            if (sk->sk_state == TCP_CLOSE) {
                if (!sock_flag(sk, SOCK_DONE)) {
                    copied = -ENOTCONN;
                    break;
                }
                break;
            }
            
            if (!timeo) {
                copied = -EAGAIN;
                break;
            }
            
            if (signal_pending(current)) {
                copied = sock_intr_errno(timeo);
                break;
            }
        }
        
        // 5. 等待数据到达
        tcp_cleanup_rbuf(sk, copied);
        
        if (!sysctl_tcp_low_latency && tp->ucopy.task == user_recv) {
            if (tp->rcv_nxt == tp->copied_seq &&
                len - copied <= tp->ucopy.len) {
                
                tcp_prequeue_process(sk);
                
                if (tp->rcv_nxt == tp->copied_seq &&
                    len - copied <= tp->ucopy.len) {
                    tp->ucopy.len = len - copied;
                    
                    if (tp->ucopy.len == 0) {
                        tp->ucopy.task = NULL;
                        tp->ucopy.len = 0;
                    } else {
                        sk_wait_data(sk, &timeo);
                    }
                    
                    continue;
                }
            }
        }
        
        sk_wait_data(sk, &timeo);
        continue;
        
    found_ok_skb:
        // 6. 找到可读数据，开始拷贝
        used = skb->len - offset;
        if (len < used)
            used = len;
        
        // 拷贝数据到用户空间
        if (!(flags & MSG_TRUNC)) {
            err = skb_copy_datagram_msg(skb, offset, msg, used);
            if (err) {
                if (!copied)
                    copied = -EFAULT;
                break;
            }
        }
        
        *seq += used;
        copied += used;
        len -= used;
        
        // 检查是否读取完整个skb
        if (used + offset < skb->len)
            continue;
        
        // 处理TCP标志
        if (TCP_SKB_CB(skb)->tcp_flags & TCPHDR_FIN)
            goto found_fin_ok;
        
        // 如果不是peek模式，释放skb
        if (!(flags & MSG_PEEK))
            sk_eat_skb(sk, skb);
        continue;
        
    found_fin_ok:
        ++*seq;
        if (!(flags & MSG_PEEK))
            sk_eat_skb(sk, skb);
        break;
        
    } while (len > 0);
    
    // 7. 清理和返回
    tcp_cleanup_rbuf(sk, copied);
    
    release_sock(sk);
    return copied;
    
out:
    release_sock(sk);
    return err;
    
recv_urg:
    err = tcp_recv_urg(sk, msg, len, flags);
    goto out;
    
recv_sndq:
    err = tcp_peek_sndq(sk, msg, len);
    goto out;
}
```

## 7. 网络中断处理

### 7.1 网络数据包到达处理
```c
// 网络中断处理函数
static irqreturn_t network_interrupt_handler(int irq, void *dev_id) {
    struct net_device *dev = dev_id;
    struct sk_buff *skb;
    
    // 从网卡读取数据包
    while ((skb = dev->netdev_ops->ndo_rx_read(dev)) != NULL) {
        // 设置skb属性
        skb->dev = dev;
        skb->protocol = eth_type_trans(skb, dev);
        
        // 将数据包加入处理队列
        netif_rx(skb);
    }
    
    return IRQ_HANDLED;
}

// 软中断处理网络数据包
static void net_rx_action(struct softirq_action *h) {
    struct list_head *list = &__get_cpu_var(softnet_data).poll_list;
    unsigned long time_limit = jiffies + 2;
    int budget = netdev_budget;
    
    local_irq_disable();
    
    while (!list_empty(list)) {
        struct napi_struct *n;
        int work, weight;
        
        if (unlikely(budget <= 0 || time_after(jiffies, time_limit)))
            goto softnet_break;
        
        local_irq_enable();
        
        n = list_first_entry(list, struct napi_struct, poll_list);
        
        weight = n->weight;
        
        work = 0;
        if (test_bit(NAPI_STATE_SCHED, &n->state)) {
            work = n->poll(n, weight);
            trace_napi_poll(n);
        }
        
        WARN_ON_ONCE(work > weight);
        
        budget -= work;
        
        local_irq_disable();
        
        if (unlikely(work == weight)) {
            if (unlikely(napi_disable_pending(n))) {
                local_irq_enable();
                napi_complete(n);
                local_irq_disable();
            } else {
                if (n->gro_list) {
                    local_irq_enable();
                    napi_gro_flush(n, false);
                    local_irq_disable();
                }
                list_move_tail(&n->poll_list, list);
            }
        }
    }
    
    local_irq_enable();
    
softnet_break:
    __raise_softirq_irqoff(NET_RX_SOFTIRQ);
    
    local_irq_enable();
}
```

## 8. 完整调用链总结

### 8.1 发送数据调用链
```
用户程序: send(sockfd, data, len, flags)
    ↓
系统调用: sys_sendto()
    ↓
Socket层: sock_sendmsg()
    ↓
协议族层: sock->ops->sendmsg (inet_sendmsg)
    ↓
传输层: sk->sk_prot->sendmsg (tcp_sendmsg)
    ↓
数据处理: skb_add_data_nocache() - 数据拷贝
    ↓
发送触发: tcp_push() -> __tcp_push_pending_frames()
    ↓
传输控制: tcp_write_xmit()
    ↓
网络层: ip_queue_xmit()
    ↓
数据链路层: dev_queue_xmit()
    ↓
物理传输: 网卡驱动发送
```

### 8.2 接收数据调用链
```
物理接收: 网卡接收数据包
    ↓
中断处理: network_interrupt_handler()
    ↓
软中断: net_rx_action()
    ↓
协议栈: ip_rcv() -> tcp_v4_rcv()
    ↓
Socket队列: tcp_data_queue() -> sk_receive_queue
    ↓
用户调用: recv(sockfd, buffer, len, flags)
    ↓
系统调用: sys_recvfrom()
    ↓
Socket层: sock_recvmsg()
    ↓
传输层: tcp_recvmsg()
    ↓
数据拷贝: skb_copy_datagram_msg()
    ↓
返回用户: 数据拷贝到用户缓冲区
```

## 9. 关键理解要点

1. **多层函数指针机制**：实现协议族的多态性
2. **用户态-内核态数据拷贝**：安全性和性能的平衡
3. **异步处理机制**：中断和软中断的配合
4. **缓冲区管理**：发送和接收队列的复杂管理
5. **错误处理**：各层的错误传播机制

这个底层机制展现了Linux网络栈的精妙设计，通过分层和抽象实现了高效的网络通信。