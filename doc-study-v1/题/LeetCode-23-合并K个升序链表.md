# LeetCode-23 合并 K 个升序链表

- 难度：困难
- 链接：https://leetcode.cn/problems/merge-k-sorted-lists/

## 问题描述
给定 `k` 个升序链表，请将它们合并为一个升序链表并返回。

## 题解一：官方经典（最小堆/优先队列）
- 思路：把每个链表的头节点放入小根堆，每次弹出最小节点并将其后续节点入堆。
- 复杂度：时间 O(N log k)，空间 O(k)。

```java
import java.util.*;
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a.val));
        for (ListNode node : lists) if (node != null) pq.offer(node);
        ListNode dummy = new ListNode(0), tail = dummy;
        while (!pq.isEmpty()) {
            ListNode cur = pq.poll();
            tail.next = cur; tail = tail.next;
            if (cur.next != null) pq.offer(cur.next);
        }
        return dummy.next;
    }
}
```

## 题解二：通用解法（分治归并）
- 标签：分治、归并、优先队列、链表
- 思路：两两合并链表，像归并排序的分治；递归或迭代都可。
- 复杂度：时间 O(N log k)，空间 O(log k)（递归栈）。

```java
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) return null;
        return merge(lists, 0, lists.length - 1);
    }
    private ListNode merge(ListNode[] lists, int l, int r) {
        if (l == r) return lists[l];
        int mid = (l + r) >>> 1;
        ListNode a = merge(lists, l, mid);
        ListNode b = merge(lists, mid + 1, r);
        return mergeTwo(a, b);
    }
    private ListNode mergeTwo(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), t = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) { t.next = l1; l1 = l1.next; }
            else { t.next = l2; l2 = l2.next; }
            t = t.next;
        }
        t.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }
}
```

## 题解三：最好理解（优先队列直觉版）
- 直觉：每次从所有链表头里拿最小的接到结果后面，然后把该链表的下一个节点扔回候选池（堆）。
- 对新手很友好：写法清晰，容易调试。

## 总结思路
- 两大通用模板：小根堆与分治归并；根据熟悉度选择即可。

## 相关标签
- 链表、优先队列、分治、归并