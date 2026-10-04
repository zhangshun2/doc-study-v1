---
schemaVersion: 3
type: "problem"
leetcodeId: 146
slug: "lru-cache"
titleCn: "LRU 缓存"
titleEn: "LRU Cache"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/lru-cache/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "a6953304ea26bc9dcec368d555067bf9b941268769e921be99256f72194d4c4e"
sourceFactsSha256: "e78e58bf2a46439a84485b9769e2c8f7e38c65e3e558da60f4e23546acc53fdb"
sourceSectionHashes:
  description: "9eef333aa54915a629b0435b23e483eca61f9efff0a7ac946b5dc21d35e3bd7f"
  examples: "d9d4dc5bd4d5b342f67354923815a9ffbe2e7bc8824016232d36a1c0e4f1f0c7"
  constraints: "4b15ea45cdd230d49f45f7f10b8c0a1d94edc1eaed9f9787440196ec63ef01dc"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0d6527b1c98d2c70a0ef95e8768110951421f4648dcb04cf4064fc2689ec288f"
  signature: "d0df9c225029774ba399abe189a29b047e29ab726bf8069744497b1f8fa4b54d"
  javaTemplate: "b27addc4502d604aac78f518eb282f7f880ad50aa085cb14d3e0ee84f49b62f8"
primaryPattern: "设计"
topics: ["设计","哈希表","链表","双向链表"]
priority: "P1"
checklistPriorities: ["P1","P2"]
checklistTags: ["Design 设计题","Doubly-Linked List 双向链表"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 146. LRU 缓存 / LRU Cache

> **双轨入口：** [[核心模型/设计/146-LRU-Cache-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`设计`
- 清单优先级：`P1`、`P2`
- 清单代表标签：`Design 设计题`、`Doubly-Linked List 双向链表`
- LeetCode 当前标签：设计 (Design)、哈希表 (Hash Table)、链表 (Linked List)、双向链表 (Doubly-Linked List)
- 官方来源：<https://leetcode.cn/problems/lru-cache/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`a6953304ea26bc9dcec368d555067bf9b941268769e921be99256f72194d4c4e`
- **主解法**：哈希表 + 双向链表

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

请你设计并实现一个满足  [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

实现 `LRUCache` 类：

- `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存

- `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。

- `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字。

函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

## 官方示例


**示例：**

```text
输入
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出
[null, null, null, 1, null, -1, null, -1, 3, 4]

解释
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1);    // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2);    // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1);    // 返回 -1 (未找到)
lRUCache.get(3);    // 返回 3
lRUCache.get(4);    // 返回 4
```

## 官方约束


- `1 <= capacity <= 3000`

- `0 <= key <= 10000`

- `0 <= value <= 10^5`

- 最多调用 `2 * 10^5` 次 `get` 和 `put`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 哈希表能 `O(1)` 找节点，却不能 `O(1)` 找出最久未使用项。
2. 双向链表能 `O(1)` 删除已知节点并移动到首部。
3. 使用虚拟头尾节点，可以统一空表、单节点和普通节点的处理。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 必须达到平均 `O(1)` 时间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：["LRUCache", "put", "get", "put", "get", "get"]
参数：[[1], [2,1], [2], [3,2], [2], [3]]
输出：[null, null, 1, null, -1, 2]
```

## 核心观察

缓存同时需要两种能力：按键直接定位，以及维护随访问变化的时间顺序。单个容器无法同时优雅满足二者，因此组合：

- `HashMap<key, Node>` 负责定位节点。
- 双向链表按新旧排序：靠近头部的是最近使用，靠近尾部的是最久未使用。

## 朴素方案

使用数组或普通链表保存访问顺序。`get` 时必须线性寻找键，或者 `put` 淘汰前线性寻找最旧元素，至少一个操作为 `O(n)`，不符合题目要求。只用 `HashMap` 又丢失访问顺序。

## 最优方案推导

维护虚拟节点 `head` 和 `tail`：

```text
head <-> 最近使用节点 <-> 中间节点 <-> 最久未使用节点 <-> tail
```

- `get` 命中：从原位置摘下节点，再插到 `head` 后。
- `put` 更新：修改值并移到头部。
- `put` 新增：创建节点、加入 map、插到头部；若超容，从 `tail.prev` 删除并同步移出 map。

所有链表操作只改固定数量的指针。

## 正确性与不变量

每次公开操作结束后保持：

1. map 中的键与链表中的真实节点一一对应。
2. 链表从头到尾严格按照最近访问时间由新到旧排列。
3. 节点数不超过 `capacity`。

命中的 `get` 和成功的 `put` 都把对应节点放到头部，故顺序不变量成立。超容时 `tail.prev` 必是顺序中最旧的节点，删除它正是 LRU 策略。由此所有返回和淘汰行为正确。

## 复杂度

- **时间复杂度**：`get`、`put` 平均均为 `O(1)`。
- **空间复杂度**：`O(capacity)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.HashMap;
import java.util.Map;

class LRUCache {
    private static class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> cache = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = cache.get(key);
        if (node == null) {
            return -1;
        }
        moveToFront(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node existing = cache.get(key);
        if (existing != null) {
            existing.value = value;
            moveToFront(existing);
            return;
        }

        Node node = new Node(key, value);
        cache.put(key, node);
        addFirst(node);
        if (cache.size() > capacity) {
            Node removed = removeLast();
            cache.remove(removed.key);
        }
    }

    private void moveToFront(Node node) {
        remove(node);
        addFirst(node);
    }

    private void addFirst(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private Node removeLast() {
        Node node = tail.prev;
        remove(node);
        return node;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.HashMap;
import java.util.Map;

class LRUCache {
    private static class Node {
        int key;
        int value;
        Node prev;
        Node next;

        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    private final int capacity;
    private final Map<Integer, Node> cache = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = cache.get(key);
        if (node == null) {
            return -1;
        }
        moveToFront(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node existing = cache.get(key);
        if (existing != null) {
            existing.value = value;
            moveToFront(existing);
            return;
        }

        Node node = new Node(key, value);
        cache.put(key, node);
        addFirst(node);
        if (cache.size() > capacity) {
            Node removed = removeLast();
            cache.remove(removed.key);
        }
    }

    private void moveToFront(Node node) {
        remove(node);
        addFirst(node);
    }

    private void addFirst(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private Node removeLast() {
        Node node = tail.prev;
        remove(node);
        return node;
    }
}

public class Main {
    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1);
        cache.put(2, 2);
        System.out.println(cache.get(1)); // 1
        cache.put(3, 3);
        System.out.println(cache.get(2)); // -1
        cache.put(4, 4);
        System.out.println(cache.get(1)); // -1
        System.out.println(cache.get(3)); // 3
        System.out.println(cache.get(4)); // 4
    }
}
```

## 边界与易错点

- 更新已有键不能增加缓存大小。
- 淘汰链表节点时必须同步从 map 删除，反之亦然。
- `get` 也是一次“使用”，命中后必须调整顺序；未命中不改变顺序。
- 移动节点前要先摘下，避免同一节点重复出现在链表中。
- 多线程环境下此实现不是线程安全的，需要锁或使用专门的并发缓存。

## 可扩展变式

- LFU 缓存：还需按访问频率分桶，并在同频率内维护 LRU。
- 支持过期时间：增加时间戳/最小堆或时间轮，淘汰策略不再只有容量。
- Java 工程中可利用 `LinkedHashMap(accessOrder=true)`，但面试实现仍应掌握双向链表原理。
