# TCP协议层数据传输实现详解

## 1. TCP数据传输核心机制

### 1.1 skb_add_data_nocache深度解析

#### 1.1.1 函数调用链
```c
// tcp_sendmsg中的关键调用
err = skb_add_data_nocache(sk, skb, &msg->msg_iter, copy);
    ↓
skb_do_copy_data_nocache(sk, skb, from, skb_put(skb, copy), copy, offset)
    ↓
csum_and_copy_from_iter() 或 copy_from_iter()
```

#### 1.1.2 skb_add_data_nocache完整实现
```c
static inline int skb_add_data_nocache(struct sock *sk, struct sk_buff *skb,
                                      struct iov_iter *from, int copy) {
    int err, offset = skb->len;
    
    // 1. 扩展skb数据区域
    // skb_put会移动tail指针，为新数据分配空间
    err = skb_do_copy_data_nocache(sk, skb, from, 
                                  skb_put(skb, copy), copy, offset);
    if (err)
        __skb_trim(skb, offset);  // 失败时回滚tail指针
    
    return err;
}

// skb_put的实现 - 扩展数据区域
static inline unsigned char *skb_put(struct sk_buff *skb, unsigned int len) {
    unsigned char *tmp = skb_tail_pointer(skb);
    
    SKB_LINEAR_ASSERT(skb);  // 确保是线性缓冲区
    skb->tail += len;        // 移动tail指针
    skb->len += len;         // 增加数据长度
    
    // 检查是否超出缓冲区边界
    if (unlikely(skb->tail > skb->end))
        skb_over_panic(skb, len, __builtin_return_address(0));
    
    return tmp;  // 返回原tail位置，即新数据的起始位置
}
```

#### 1.1.3 数据拷贝和校验和计算
```c
static int skb_do_copy_data_nocache(struct sock *sk, struct sk_buff *skb,
                                   struct iov_iter *from, char *to,
                                   int copy, int offset) {
    // 检查校验和计算方式
    if (skb->ip_summed == CHECKSUM_NONE) {
        // 软件校验和：边拷贝边计算
        __wsum csum = 0;
        if (csum_and_copy_from_iter(to, copy, &csum, from) != copy)
            return -EFAULT;
        
        // 累加到现有校验和
        skb->csum = csum_block_add(skb->csum, csum, offset);
    } else {
        // 硬件校验和卸载：直接拷贝
        if (copy_from_iter(to, copy, from) != copy)
            return -EFAULT;
    }
    return 0;
}

// 带校验和的数据拷贝
size_t csum_and_copy_from_iter(void *addr, size_t bytes, __wsum *csum,
                              struct iov_iter *i) {
    char *to = addr;
    __wsum sum, next;
    size_t off = 0;
    
    sum = *csum;
    
    // 遍历iovec数组
    iterate_and_advance(i, bytes, v,
        // 从用户空间拷贝数据并计算校验和
        next = csum_and_copy_from_user(v.iov_base, 
                                      (to += v.iov_len) - v.iov_len,
                                      v.iov_len, 0, &err);
        if (!err)
            sum = csum_block_add(sum, next, off);
        off += v.iov_len;
    )
    
    *csum = sum;
    return bytes;
}
```

### 1.2 数据流转换过程

#### 1.2.1 用户数据到sk_buff的转换
```
用户数据 (char *data, size_t len)
    ↓ copy_from_iter()
内核缓冲区 (sk_buff->data)
    ↓ TCP头部添加
TCP段 (TCP Header + Data)
    ↓ IP头部添加  
IP数据包 (IP Header + TCP Segment)
    ↓ 以太网头部添加
以太网帧 (Ethernet Header + IP Packet)
    ↓ 网卡发送
物理网络传输
```

#### 1.2.2 sk_buff结构变化
```c
// 初始状态
struct sk_buff *skb = alloc_skb(size, GFP_KERNEL);
// head    data    tail    end
//  |       |       |       |
//  +-------+-------+-------+
//          |<-len->|

// 添加用户数据后
skb_add_data_nocache(sk, skb, &msg->msg_iter, copy);
// head    data         tail    end
//  |       |            |       |
//  +-------+------------+-------+
//          |<---len---->|

// 添加TCP头部
tcp_transmit_skb(sk, skb, 1, gfp);
// head data              tail    end
//  |    |                 |       |
//  +----+-----------------+-------+
//       |<----len-------->|
//       TCP头|用户数据
```

## 2. tcp_push机制详解

### 2.1 tcp_push触发条件
```c
// tcp_sendmsg中的调用
if (copied && !(flags & MSG_SENDPAGE_NOTLAST))
    tcp_push(sk, flags, mss_now, tp->nonagle, size_goal);

// tcp_push的实现
static inline void tcp_push(struct sock *sk, int flags, int mss_now,
                           int nonagle, int size_goal) {
    if (tcp_send_head(sk)) {  // 检查是否有待发送数据
        struct tcp_sock *tp = tcp_sk(sk);
        
        // 1. 设置PSH标志
        if (!(flags & MSG_MORE) || forced_push(tp))
            tcp_mark_push(tp, tcp_write_queue_tail(sk));
        
        // 2. 设置紧急指针
        tcp_mark_urg(tp, flags);
        
        // 3. 触发实际发送
        __tcp_push_pending_frames(sk, mss_now, nonagle);
    }
}
```

### 2.2 强制推送判断
```c
static inline bool forced_push(const struct tcp_sock *tp) {
    return after(tp->write_seq, tp->pushed_seq + (tp->max_window >> 1));
}

// 设置PSH标志
static inline void tcp_mark_push(struct tcp_sock *tp, struct sk_buff *skb) {
    TCP_SKB_CB(skb)->tcp_flags |= TCPHDR_PSH;
    tp->pushed_seq = tp->write_seq;
}

// 设置紧急指针
static inline void tcp_mark_urg(struct tcp_sock *tp, int flags) {
    if (flags & MSG_OOB)
        tp->snd_up = tp->write_seq;
}
```

### 2.3 实际发送处理
```c
void __tcp_push_pending_frames(struct sock *sk, unsigned int cur_mss,
                              int nonagle) {
    // 检查连接状态
    if (unlikely(sk->sk_state == TCP_CLOSE))
        return;
    
    // 调用发送函数
    if (tcp_write_xmit(sk, cur_mss, nonagle, 0,
                      sk_gfp_atomic(sk, GFP_ATOMIC)))
        tcp_check_probe_timer(sk);  // 检查探测定时器
}
```

## 3. TCP发送队列管理

### 3.1 发送队列结构
```c
struct tcp_sock {
    struct sock sk;
    
    // 发送相关
    u32 write_seq;          // 下一个要写入的序列号
    u32 pushed_seq;         // 最后推送的序列号
    u32 snd_nxt;           // 下一个要发送的序列号
    u32 snd_una;           // 最老的未确认序列号
    
    // 发送窗口
    u32 snd_wnd;           // 发送窗口大小
    u32 max_window;        // 最大窗口大小
    u32 mss_cache;         // 缓存的MSS值
    
    // 拥塞控制
    u32 snd_cwnd;          // 拥塞窗口
    u32 snd_ssthresh;      // 慢启动阈值
    
    // 重传相关
    struct sk_buff_head out_of_order_queue;  // 乱序队列
    struct tcp_sack_block duplicate_sack[1]; // SACK块
};

// Socket发送队列
struct sock {
    struct sk_buff_head sk_write_queue;  // 发送队列
    atomic_t sk_wmem_alloc;              // 已分配的写内存
    int sk_sndbuf;                       // 发送缓冲区大小
};
```

### 3.2 队列操作函数
```c
// 将skb加入发送队列尾部
static inline void tcp_add_write_queue_tail(struct sock *sk, struct sk_buff *skb) {
    __skb_queue_tail(&sk->sk_write_queue, skb);
    
    // 如果是第一个包，设置为发送头
    if (sk->sk_send_head == NULL) {
        sk->sk_send_head = skb;
        
        if (tcp_sk(sk)->highest_sack == NULL)
            tcp_sk(sk)->highest_sack = skb;
    }
}

// 从发送队列移除skb
static inline void tcp_unlink_write_queue(struct sk_buff *skb, struct sock *sk) {
    __skb_unlink(skb, &sk->sk_write_queue);
    
    if (sk->sk_send_head == skb)
        sk->sk_send_head = NULL;
}

// 获取发送队列头部
static inline struct sk_buff *tcp_send_head(const struct sock *sk) {
    return sk->sk_send_head;
}
```

## 4. TCP段构造过程

### 4.1 tcp_transmit_skb实现
```c
static int tcp_transmit_skb(struct sock *sk, struct sk_buff *skb, int clone_it,
                           gfp_t gfp_mask) {
    const struct inet_connection_sock *icsk = inet_csk(sk);
    struct inet_sock *inet;
    struct tcp_sock *tp;
    struct tcp_skb_cb *tcb;
    struct tcphdr *th;
    int err;
    
    BUG_ON(!skb || !tcp_skb_pcount(skb));
    
    if (clone_it) {
        skb_mstamp_get(&skb->skb_mstamp);
        
        if (unlikely(skb_cloned(skb)))
            skb = pskb_copy(skb, gfp_mask);
        else
            skb = skb_clone(skb, gfp_mask);
        if (unlikely(!skb))
            return -ENOBUFS;
    }
    
    inet = inet_sk(sk);
    tp = tcp_sk(sk);
    tcb = TCP_SKB_CB(skb);
    
    // 1. 添加TCP头部空间
    skb_push(skb, tcp_header_size);
    skb_reset_transport_header(skb);
    
    // 2. 构造TCP头部
    th = tcp_hdr(skb);
    th->source = inet->inet_sport;      // 源端口
    th->dest = inet->inet_dport;        // 目标端口
    th->seq = htonl(tcb->seq);          // 序列号
    th->ack_seq = htonl(tp->rcv_nxt);   // 确认号
    
    // 3. 设置TCP标志
    *(((__be16 *)th) + 6) = htons(((tcp_header_size >> 2) << 12) |
                                  tcb->tcp_flags);
    
    // 4. 设置窗口大小
    th->window = htons(tcp_select_window(sk));
    th->check = 0;
    th->urg_ptr = 0;
    
    // 5. 处理紧急指针
    if (unlikely(tcb->tcp_flags & TCPHDR_URG)) {
        if (after(tcb->end_seq, tp->snd_up)) {
            th->urg_ptr = htons(tp->snd_up - tcb->seq);
            th->urg = 1;
        }
    }
    
    // 6. 添加TCP选项
    tcp_options_write((__be32 *)(th + 1), tp, &opts);
    
    // 7. 计算校验和
    if (likely(!(tcb->tcp_flags & TCPHDR_SYN)))
        th->check = tcp_v4_check(skb->len, inet->inet_saddr,
                                inet->inet_daddr, csum_partial(th, th->doff << 2,
                                skb->csum));
    
    // 8. 传递给IP层
    err = icsk->icsk_af_ops->queue_xmit(sk, skb, &inet->cork.fl);
    
    if (likely(err <= 0))
        return err;
    
    tcp_enter_cwr(sk);
    
    return net_xmit_eval(err);
}
```

### 4.2 TCP选项处理
```c
static void tcp_options_write(__be32 *ptr, struct tcp_sock *tp,
                             struct tcp_out_options *opts) {
    u16 options = opts->options;    // TCP选项标志
    
    // 1. MSS选项
    if (unlikely(OPTION_MSS & options)) {
        *ptr++ = htonl((TCPOPT_MSS << 24) |
                      (TCPOLEN_MSS << 16) |
                      opts->mss);
    }
    
    // 2. 时间戳选项
    if (likely(OPTION_TS & options)) {
        if (unlikely(OPTION_SACK_ADVERTISE & options)) {
            *ptr++ = htonl((TCPOPT_SACK_PERM << 24) |
                          (TCPOLEN_SACK_PERM << 16) |
                          (TCPOPT_TIMESTAMP << 8) |
                          TCPOLEN_TIMESTAMP);
            *ptr++ = htonl(opts->tsval);
            *ptr++ = htonl(opts->tsecr);
        } else {
            *ptr++ = htonl((TCPOPT_NOP << 24) |
                          (TCPOPT_NOP << 16) |
                          (TCPOPT_TIMESTAMP << 8) |
                          TCPOLEN_TIMESTAMP);
            *ptr++ = htonl(opts->tsval);
            *ptr++ = htonl(opts->tsecr);
        }
    }
    
    // 3. SACK选项
    if (unlikely(OPTION_SACK_ADVERTISE & options)) {
        *ptr++ = htonl((TCPOPT_NOP << 24) |
                      (TCPOPT_NOP << 16) |
                      (TCPOPT_SACK_PERM << 8) |
                      TCPOLEN_SACK_PERM);
    }
    
    // 4. 窗口缩放选项
    if (unlikely(OPTION_WSCALE & options)) {
        *ptr++ = htonl((TCPOPT_NOP << 24) |
                      (TCPOPT_WINDOW << 16) |
                      (TCPOLEN_WINDOW << 8) |
                      opts->ws);
    }
}
```

## 5. 拥塞控制和流量控制

### 5.1 发送窗口计算
```c
static u16 tcp_select_window(struct sock *sk) {
    struct tcp_sock *tp = tcp_sk(sk);
    u32 old_win = tp->rcv_wnd;
    u32 cur_win = tcp_receive_window(tp);
    u32 new_win = __tcp_select_window(sk);
    
    // 窗口收缩检查
    if (new_win < cur_win) {
        if (new_win == 0)
            NET_INC_STATS_BH(sock_net(sk), LINUX_MIB_TCPWANTZEROWINDOWADV);
        return new_win;
    }
    
    // 避免窗口收缩
    if (new_win < old_win) {
        new_win = ALIGN(old_win, 1 << tp->rx_opt.rcv_wscale);
        if (new_win == 0)
            new_win = ALIGN(old_win, 1);
    }
    
    tp->rcv_wnd = new_win;
    tp->rcv_wup = tp->rcv_nxt;
    
    // 确保窗口大小不超过65535
    new_win = min(new_win, 65535U);
    return new_win >> tp->rx_opt.rcv_wscale;
}
```

### 5.2 拥塞窗口管理
```c
// 慢启动
static void tcp_slow_start(struct tcp_sock *tp, u32 acked) {
    u32 cwnd = tp->snd_cwnd + acked;
    
    if (cwnd > tp->snd_ssthresh)
        cwnd = tp->snd_ssthresh + 1;
    
    tp->snd_cwnd = min(cwnd, tp->snd_cwnd_clamp);
}

// 拥塞避免
static void tcp_cong_avoid_ai(struct tcp_sock *tp, u32 w) {
    if (tp->snd_cwnd_cnt >= w) {
        if (tp->snd_cwnd < tp->snd_cwnd_clamp)
            tp->snd_cwnd++;
        tp->snd_cwnd_cnt = 0;
    } else {
        tp->snd_cwnd_cnt++;
    }
}

// 快速重传
static void tcp_enter_frto(struct sock *sk) {
    const struct inet_connection_sock *icsk = inet_csk(sk);
    struct tcp_sock *tp = tcp_sk(sk);
    
    tp->frto_counter = 1;
    tp->snd_cwnd = tcp_packets_in_flight(tp) + 1;
    tp->frto_highmark = tp->snd_nxt;
    
    tcp_set_ca_state(sk, TCP_CA_Disorder);
    tp->high_seq = tp->snd_nxt;
    
    icsk->icsk_retransmits = 0;
}
```

## 6. 重传机制

### 6.1 RTO计算
```c
static void tcp_set_rto(struct sock *sk) {
    const struct tcp_sock *tp = tcp_sk(sk);
    
    // 根据RTT计算RTO
    inet_csk(sk)->icsk_rto = __tcp_set_rto(tp);
    
    // 限制RTO范围
    inet_csk(sk)->icsk_rto = tcp_bound_rto(inet_csk(sk)->icsk_rto);
}

static inline u32 __tcp_set_rto(const struct tcp_sock *tp) {
    return usecs_to_jiffies((tp->srtt_us >> 3) + tp->rttvar_us);
}

static inline u32 tcp_bound_rto(u32 rto) {
    return min(rto, TCP_RTO_MAX);
}
```

### 6.2 重传定时器
```c
void tcp_reset_xmit_timer(struct sock *sk, const int what,
                         unsigned long when, const unsigned long max_when) {
    struct inet_connection_sock *icsk = inet_csk(sk);
    
    if (when > max_when) {
        pr_debug("reset_xmit_timer: sk=%p %d when=0x%lx, caller=%p\n",
                sk, what, when, __builtin_return_address(0));
        when = max_when;
    }
    
    if (what == ICSK_TIME_RETRANS || what == ICSK_TIME_PROBE0) {
        icsk->icsk_pending = what;
        icsk->icsk_timeout = jiffies + when;
        sk_reset_timer(sk, &icsk->icsk_retransmit_timer, icsk->icsk_timeout);
    } else if (what == ICSK_TIME_DACK) {
        icsk->icsk_ack.pending |= ICSK_ACK_TIMER;
        icsk->icsk_ack.timeout = jiffies + when;
        sk_reset_timer(sk, &icsk->icsk_delack_timer, icsk->icsk_ack.timeout);
    }
}
```

## 7. 数据流图示

### 7.1 发送数据流
```
用户数据
    ↓ skb_add_data_nocache()
sk_buff (用户数据)
    ↓ tcp_push()
发送队列 (sk_write_queue)
    ↓ tcp_write_xmit()
TCP段构造
    ↓ tcp_transmit_skb()
添加TCP头部
    ↓ ip_queue_xmit()
添加IP头部
    ↓ dev_queue_xmit()
添加以太网头部
    ↓ 网卡驱动
物理传输
```

### 7.2 内存布局变化
```
初始sk_buff:
[head][data=tail][unused][end]

添加用户数据后:
[head][data][user_data][tail][unused][end]

添加TCP头部后:
[head][tcp_hdr][data][user_data][tail][unused][end]

添加IP头部后:
[head][ip_hdr][tcp_hdr][data][user_data][tail][unused][end]
```

## 8. 性能优化要点

### 8.1 Nagle算法
```c
static inline bool tcp_nagle_check(const struct tcp_sock *tp,
                                  const struct sk_buff *skb,
                                  unsigned int mss_now, int nonagle) {
    return skb->len < mss_now &&
           ((nonagle & TCP_NAGLE_CORK) ||
            (!nonagle && tp->packets_out && tcp_minshall_check(tp)));
}
```

### 8.2 TSO (TCP Segmentation Offload)
```c
static bool tcp_tso_should_defer(struct sock *sk, struct sk_buff *skb,
                                bool *is_cwnd_limited, u32 max_segs) {
    const struct inet_connection_sock *icsk = inet_csk(sk);
    const struct tcp_sock *tp = tcp_sk(sk);
    u32 age, send_win, cong_win, limit, in_flight;
    
    // 检查是否应该延迟发送以便TSO
    if (TCP_SKB_CB(skb)->tcp_flags & TCPHDR_FIN)
        return false;
    
    if (icsk->icsk_ca_state >= TCP_CA_Recovery)
        return false;
    
    // 计算各种限制
    in_flight = tcp_packets_in_flight(tp);
    cong_win = tp->snd_cwnd;
    send_win = tcp_wnd_end(tp) - TCP_SKB_CB(skb)->seq;
    
    limit = min(send_win, cong_win * tp->mss_cache);
    
    if (limit >= max_segs * tp->mss_cache)
        return false;
    
    return true;
}
```

## 9. 总结

TCP协议层数据传输的核心实现包括：

1. **数据拷贝机制**：`skb_add_data_nocache`实现用户数据到内核缓冲区的高效拷贝
2. **发送触发机制**：`tcp_push`根据多种条件决定何时发送数据
3. **队列管理**：复杂的发送队列和重传队列管理
4. **协议封装**：TCP头部构造和选项处理
5. **流量控制**：发送窗口和拥塞窗口的动态调整
6. **可靠性保证**：重传机制和定时器管理

这些机制共同保证了TCP协议的可靠性、有序性和流量控制特性。