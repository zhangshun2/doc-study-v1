# LeetCode-141 环形链表

- 难度：简单
- 链接：https://leetcode.cn/problems/linked-list-cycle/

## 问题描述
给定一个链表，判断链表中是否有环。环的定义是某个节点的 `next` 指针指向了此前出现的节点。

## 题解一：官方经典（快慢指针/Floyd 判环）
- 思路：用 `slow` 每次走一步，`fast` 每次走两步；若存在环，二者必相遇。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public boolean hasCycle(ListNode head) {
        if (head == null || head.next == null) return false;
        ListNode slow = head, fast = head.next;
        while (fast != null && fast.next != null) {
            if (slow == fast) return true;
            slow = slow.next;
            fast = fast.next.next;
        }
        return false;
    }
}
```

## 题解二：通用解法（哈希集合）
- 标签：链表、快慢指针、哈希
- 思路：遍历链表，将节点引用存入 `Set`，若出现重复即有环。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public boolean hasCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) return true;
            head = head.next;
        }
        return false;
    }
}
```

## 题解三：最好理解（快慢指针直觉）
- 直觉：一个跑得快、一个跑得慢，如果是在环里跑，快的总能追上慢的。
- 写法同题解一，重点记“退出条件”和“相遇即判环”。

## 总结思路
- 首选 O(1) 空间的快慢指针；哈希表更直观但占用空间。

## 相关标签
- 链表、快慢指针、哈希