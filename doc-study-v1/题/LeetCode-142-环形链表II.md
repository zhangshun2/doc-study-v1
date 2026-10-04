# LeetCode-142 环形链表 II

- 难度：中等
- 链接：https://leetcode.cn/problems/linked-list-cycle-ii/

## 问题描述
给定一个链表，返回链表开始入环的第一个节点。如果链表无环，则返回 `null`。

## 题解一：官方经典（Floyd 判环 + 入环节点推导）
- 思路：先用快慢指针判环并找到相遇点。然后将其中一个指针移到头节点，两指针每次走一步，再次相遇点即为入环节点。
- 证明要点：设入环前长度 `a`，环长度 `b`，相遇时走过距离满足关系，重新出发一步步会在入环处相遇。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public ListNode detectCycle(ListNode head) {
        if (head == null || head.next == null) return null;
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next; fast = fast.next.next;
            if (slow == fast) {
                ListNode p = head;
                while (p != slow) { p = p.next; slow = slow.next; }
                return p;
            }
        }
        return null;
    }
}
```

## 题解二：通用解法（哈希集合定位入环）
- 标签：链表、快慢指针、哈希
- 思路：遍历节点，将首次出现的节点放入 `Set`，若遇到已存在的节点即为入环点。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public ListNode detectCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        while (head != null) {
            if (!seen.add(head)) return head;
            head = head.next;
        }
        return null;
    }
}
```

## 题解三：最好理解（两次相遇的直觉）
- 直觉：第一次相遇在环内，第二次从头与相遇点同步走，因步数关系会在入环点再次相遇。
- 新手重点理解“相遇后重置一个指针到头”的原因。

## 总结思路
- 首选 O(1) 空间 Floyd 模板；哈希更直观但占空间。

## 相关标签
- 链表、快慢指针、哈希