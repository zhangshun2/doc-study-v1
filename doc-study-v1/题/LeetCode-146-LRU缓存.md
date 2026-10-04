# LeetCode-146 LRU 缓存

- 难度：中等
- 链接：https://leetcode.cn/problems/lru-cache/

## 问题描述
设计并实现一个 LRU (最近最少使用) 缓存，支持 `get(key)` 与 `put(key, value)`，要求在 O(1) 时间内完成。

## 题解一：官方经典（哈希表 + 双向链表）
- 思路：用 `HashMap` 存 `key -> Node`，用双向链表维护使用顺序，头部为最新，尾部为最旧；`get`/`put` 时移动节点到头部，容量超出时删除尾节点。
- 复杂度：`get`/`put` O(1)。

```java
class LRUCache {
    static class Node {
        int k, v; Node prev, next;
        Node(int k, int v){this.k=k;this.v=v;}
    }
    private final int cap;
    private Map<Integer, Node> map = new HashMap<>();
    private Node head = new Node(-1, -1), tail = new Node(-1, -1);
    public LRUCache(int capacity) {
        this.cap = capacity; head.next = tail; tail.prev = head;
    }
    public int get(int key) {
        Node n = map.get(key); if (n == null) return -1;
        moveToHead(n); return n.v;
    }
    public void put(int key, int value) {
        Node n = map.get(key);
        if (n != null) { n.v = value; moveToHead(n); }
        else {
            n = new Node(key, value); map.put(key, n); addToHead(n);
            if (map.size() > cap) { Node rm = removeTail(); map.remove(rm.k); }
        }
    }
    private void addToHead(Node n){ n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }
    private void removeNode(Node n){ n.prev.next = n.next; n.next.prev = n.prev; }
    private void moveToHead(Node n){ removeNode(n); addToHead(n); }
    private Node removeTail(){ Node rm = tail.prev; removeNode(rm); return rm; }
}
```

## 题解二：通用解法（LinkedHashMap）
- 标签：设计、哈希、双向链表、LinkedHashMap
- 思路：使用 `LinkedHashMap` 的访问顺序特性，重写 `removeEldestEntry` 自动驱逐最旧元素。

```java
import java.util.*;
class LRUCache extends LinkedHashMap<Integer, Integer> {
    private final int cap;
    public LRUCache(int capacity) {
        super(16, 0.75f, true); // access-order
        this.cap = capacity;
    }
    public int get(int key) { return super.getOrDefault(key, -1); }
    public void put(int key, int value) { super.put(key, value); }
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer,Integer> eldest) {
        return size() > cap;
    }
}
```

## 题解三：最好理解（手写双链表的直觉）
- 直觉：每次访问就把元素提到队头，满了就把队尾淘汰。
- 更容易理解内部逻辑，但要注意链表指针操作的正确性。

## 总结思路
- 工程常用两法：自定义双链表更灵活；`LinkedHashMap`更省代码但可定制性有限。

## 相关标签
- 设计题、哈希表、双向链表、LinkedHashMap