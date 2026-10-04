# LeetCode-234 回文链表

- 难度：简单
- 链接：https://leetcode.cn/problems/palindrome-linked-list/

## 问题描述
给定一个链表的头节点，判断该链表是否为回文链表。

## 题解一：官方经典（快慢指针 + 反转后半段）
- 思路：快慢指针找中点，反转后半段，与前半段逐一比较。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) return true;
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode second = reverse(slow);
        ListNode p1 = head, p2 = second;
        boolean ok = true;
        while (p2 != null) {
            if (p1.val != p2.val) { ok = false; break; }
            p1 = p1.next; p2 = p2.next;
        }
        // 可选：恢复链表
        // reverse(second);
        return ok;
    }
    private ListNode reverse(ListNode head) {
        ListNode prev = null, cur = head;
        while (cur != null) {
            ListNode nxt = cur.next; cur.next = prev; prev = cur; cur = nxt;
        }
        return prev;
    }
}
```

## 题解二：通用解法（数组/栈）
- 标签：链表、快慢指针、反转、栈
- 思路：把节点值复制到数组或栈，做双指针或比较栈顶。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> arr = new ArrayList<>();
        for (ListNode p = head; p != null; p = p.next) arr.add(p.val);
        int i = 0, j = arr.size() - 1;
        while (i < j) { if (!arr.get(i).equals(arr.get(j))) return false; i++; j--; }
        return true;
    }
}
```

## 题解三：最好理解（反转后半段的直觉）
- 直觉：把后半段“翻过来”，两端一起比；奇偶长度用快慢指针自然处理。

## 总结思路
- O(1) 空间更优；如需保留结构可在比较后再反转恢复。

## 相关标签
- 链表、快慢指针、反转、栈