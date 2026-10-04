# LeetCode-206 反转链表

- 难度：简单
- 链接：https://leetcode.cn/problems/reverse-linked-list/

## 问题描述
给你单链表的头节点 `head`，请将该链表反转，并返回反转后的链表。 

## 题解一：官方经典（迭代反转）
- 思路：用三个指针 `prev`、`cur`、`next`，逐步反转 `cur.next = prev`，最终返回 `prev`。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null, cur = head;
        while (cur != null) {
            ListNode nxt = cur.next;
            cur.next = prev; prev = cur; cur = nxt;
        }
        return prev;
    }
}
```

## 题解二：通用解法（递归反转）
- 标签：链表、迭代、递归
- 思路：递归到尾部，将子问题反转完成后，把当前节点接到尾部：`head.next.next = head; head.next = null`。
- 复杂度：时间 O(n)，空间 O(n)（递归栈）。

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode newHead = reverseList(head.next);
        head.next.next = head; head.next = null;
        return newHead;
    }
}
```

## 题解三：最好理解（迭代直觉）
- 直觉：像把一串箭头方向一次次调转过来；每次把当前节点的箭头改指向前一个节点。
- 写法同题解一，适合快速上手。

## 总结思路
- 面试常问两法：迭代 O(1) 空间更常用；递归更优雅但有栈开销。

## 相关标签
- 链表、双指针、递归