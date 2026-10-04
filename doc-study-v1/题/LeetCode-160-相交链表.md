# LeetCode-160 相交链表

- 难度：简单
- 链接：https://leetcode.cn/problems/intersection-of-two-linked-lists/

## 问题描述
给定两个单链表的头节点 `headA` 和 `headB`，如果两个链表相交，返回相交的起始节点；如果不相交，返回 `null`。

## 题解一：官方经典（双指针切换头）
- 思路：用两个指针 `a` 和 `b` 分别从两链表出发，每当走到尾部就切换到另一条链表的头。两个指针总会在相交点或同时到达 `null`。
- 复杂度：时间 O(n+m)，空间 O(1)。

```java
class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        if (headA == null || headB == null) return null;
        ListNode a = headA, b = headB;
        while (a != b) {
            a = (a == null) ? headB : a.next;
            b = (b == null) ? headA : b.next;
        }
        return a;
    }
}
```

## 题解二：通用解法（哈希集合 / 长度对齐）
- 标签：链表、双指针、哈希
- 哈希集合思路：遍历 A 链表将节点放入 `Set`，遍历 B 链表遇到已存在节点即相交点。
- 长度对齐思路：先统计两链表长度，让长链表先走差值步，再同步前进直到相遇。

```java
import java.util.*;
class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        Set<ListNode> seen = new HashSet<>();
        for (ListNode p = headA; p != null; p = p.next) seen.add(p);
        for (ListNode q = headB; q != null; q = q.next) {
            if (seen.contains(q)) return q;
        }
        return null;
    }
}
```

## 题解三：最好理解（走两遍等长的直觉）
- 直觉：两指针分别把“另一条链表”补上，路径长度一样了，自然会在交点相遇；若不相交，则同时到达 `null`。

## 总结思路
- 首选双指针切换头，代码短、空间 O(1)；哈希更直观但需 O(n) 空间；长度对齐适合思维清晰的场景。

## 相关标签
- 链表、双指针、哈希