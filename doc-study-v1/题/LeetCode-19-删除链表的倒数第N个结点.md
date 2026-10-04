# LeetCode-19 删除链表的倒数第 N 个结点

- 难度：中等
- 链接：https://leetcode.cn/problems/remove-nth-node-from-end-of-list/

## 问题描述
给定一个链表，删除链表的倒数第 `n` 个结点，并返回链表的头节点。要求一次遍历或两次遍历均可。

示例：`head = [1,2,3,4,5], n = 2` → 输出 `[1,2,3,5]`。

## 题解一：官方经典（一趟遍历快慢指针 + 哑节点）
- 思路：使用哑节点指向头；让 `fast` 先走 `n` 步，然后 `slow` 与 `fast` 同步走到末尾；此时 `slow.next` 即待删除节点。
- 关键点：考虑删除头结点；哑节点统一处理。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode fast = dummy, slow = dummy;
        for (int i = 0; i < n; i++) fast = fast.next; // 先走n步
        while (fast.next != null) { // 同步走到末尾
            fast = fast.next;
            slow = slow.next;
        }
        slow.next = slow.next.next; // 删除
        return dummy.next;
    }
}
```

## 题解二：通用解法（两趟遍历 + 计数）
- 标签：链表、双指针、哑节点
- 思路：第一次遍历统计长度 `len`，第二次从头走到 `len - n` 的前一个位置进行删除。

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        int len = 0;
        for (ListNode p = head; p != null; p = p.next) len++;
        int k = len - n;
        ListNode cur = dummy;
        for (int i = 0; i < k; i++) cur = cur.next;
        cur.next = cur.next.next;
        return dummy.next;
    }
}
```

## 题解三：最好理解（快慢指针直观版）
- 直觉：让前指针领先 `n`，再同步前进直到前指针到末尾，后指针恰在要删节点前。
- 写法同题解一，只是更强调“领先 n 步 + 同步”的心法。

```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0); dummy.next = head;
        ListNode fast = dummy, slow = dummy;
        while (n-- > 0) fast = fast.next;
        while (fast.next != null) { fast = fast.next; slow = slow.next; }
        slow.next = slow.next.next;
        return dummy.next;
    }
}
```

## 总结思路
- 哑节点统一删除逻辑；两种策略：一趟快慢指针或两趟计数。

## 相关标签
- 链表、双指针、哑节点