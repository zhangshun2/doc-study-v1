# LeetCode-148 排序链表

- 难度：中等
- 链接：https://leetcode.cn/problems/sort-list/

## 问题描述
给你链表的头节点 `head`，请将其升序排序并返回排序后的链表。要求时间复杂度 O(n log n) 且空间复杂度 O(1)（不计递归栈）。

## 题解一：官方经典（归并排序：自顶向下）
- 思路：快慢指针找中点切分，递归排序左右，再归并两个有序链表。
- 复杂度：时间 O(n log n)，空间 O(log n)（递归栈）。

```java
class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode slow = head, fast = head.next;
        while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode mid = slow.next; slow.next = null;
        ListNode left = sortList(head);
        ListNode right = sortList(mid);
        return merge(left, right);
    }
    private ListNode merge(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0), t = dummy;
        while (a != null && b != null) {
            if (a.val < b.val) { t.next = a; a = a.next; }
            else { t.next = b; b = b.next; }
            t = t.next;
        }
        t.next = (a != null) ? a : b;
        return dummy.next;
    }
}
```

## 题解二：通用解法（归并排序：自底向上迭代）
- 标签：链表、归并排序、分治
- 思路：先统计长度，每次按 `size=1,2,4,...` 规模两两归并，迭代完成排序。
- 复杂度：时间 O(n log n)，空间 O(1)。

```java
class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) return head;
        int n = 0; for (ListNode p = head; p != null; p = p.next) n++;
        ListNode dummy = new ListNode(0); dummy.next = head;
        for (int size = 1; size < n; size <<= 1) {
            ListNode cur = dummy.next, tail = dummy;
            while (cur != null) {
                ListNode left = cur;
                ListNode right = split(left, size);
                cur = split(right, size);
                tail.next = merge(left, right);
                while (tail.next != null) tail = tail.next;
            }
        }
        return dummy.next;
    }
    private ListNode split(ListNode head, int n) {
        while (n > 1 && head != null) { head = head.next; n--; }
        if (head == null) return null;
        ListNode second = head.next; head.next = null; return second;
    }
    private ListNode merge(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0), t = dummy;
        while (a != null && b != null) {
            if (a.val < b.val) { t.next = a; a = a.next; }
            else { t.next = b; b = b.next; }
            t = t.next;
        }
        t.next = (a != null) ? a : b;
        return dummy.next;
    }
}
```

## 题解三：最好理解（递归归并直觉版）
- 直觉：不断对半拆，分别排好，再像合并两个有序链表一样接回去。
- 对新手友好：代码结构清晰，易于验证。

## 总结思路
- 链表排序最常用归并两法：递归更直观，迭代更符合 O(1) 空间要求。

## 相关标签
- 链表、归并排序、分治