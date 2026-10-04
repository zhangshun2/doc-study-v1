# LeetCode-21 合并两个有序链表

- 难度：简单
- 链接：https://leetcode.cn/problems/merge-two-sorted-lists/

## 问题描述
将两个升序链表合并为一个升序链表并返回。可就地合并或新建链表。

示例：`l1 = [1,2,4], l2 = [1,3,4]` → 输出 `[1,1,2,3,4,4]`。

## 题解一：官方经典（递归合并）
- 思路：比较两个头节点，较小者作为结果头，并递归合并其后续。
- 复杂度：时间 O(m+n)，空间 O(m+n)（递归栈）。

```java
class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        if (l1 == null) return l2;
        if (l2 == null) return l1;
        if (l1.val < l2.val) {
            l1.next = mergeTwoLists(l1.next, l2);
            return l1;
        } else {
            l2.next = mergeTwoLists(l1, l2.next);
            return l2;
        }
    }
}
```

## 题解二：通用解法（迭代 + 哑节点）
- 标签：链表、双指针、迭代、哑节点
- 思路：用 `dummy` 和 `tail` 指针，逐个选择较小值链接，最后把剩余部分接上。
- 复杂度：时间 O(m+n)，空间 O(1)。

```java
class Solution {
    public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) { tail.next = l1; l1 = l1.next; }
            else { tail.next = l2; l2 = l2.next; }
            tail = tail.next;
        }
        tail.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }
}
```

## 题解三：最好理解（就地合并的直觉写法）
- 直觉：始终把更小的节点接到结果尾部；当一条链用完，直接接另一条链。
- 与题解二一致，强调“哑节点 + 尾指针”的套路。

## 总结思路
- 两种常用写法：递归更简洁、迭代更省空间；哑节点模板通用。

## 相关标签
- 链表、双指针、迭代、递归、哑节点