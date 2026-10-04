# LeetCode-2 两数相加

- 难度：中等
- 链接：https://leetcode.cn/problems/add-two-numbers/

## 问题描述
给定两个非空链表，表示两个非负整数。它们每位数字按逆序存储，每个节点只存储单个数字。将两数相加并以相同形式返回一个链表。可以假设除了数字 0 本身，两个数都不会以 0 开头。

输入：`l1 = [2,4,3]`, `l2 = [5,6,4]`
输出：`[7,0,8]`（因为 342 + 465 = 807）

## 题解一：官方经典（迭代 + 进位模拟）
- 思路：同时遍历 `l1`、`l2`，逐位相加并维护 `carry`。新建结果链表尾插节点。
- 关键点：空指针保护，最后可能有进位需要额外节点。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), cur = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int x = (l1 != null) ? l1.val : 0;
            int y = (l2 != null) ? l2.val : 0;
            int sum = x + y + carry;
            carry = sum / 10;
            cur.next = new ListNode(sum % 10);
            cur = cur.next;
            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        return dummy.next;
    }
}
```

## 题解二：通用解法（递归）
- 标签：链表、模拟、递归、进位
- 思路：递归处理当前位并传递进位；将空链表视为 0。
- 适用场景：与迭代同等，但递归风格更贴近“按位处理”。

```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        return add(l1, l2, 0);
    }
    private ListNode add(ListNode a, ListNode b, int carry) {
        if (a == null && b == null && carry == 0) return null;
        int x = (a != null) ? a.val : 0;
        int y = (b != null) ? b.val : 0;
        int sum = x + y + carry;
        ListNode node = new ListNode(sum % 10);
        node.next = add(a == null ? null : a.next, b == null ? null : b.next, sum / 10);
        return node;
    }
}
```

## 题解三：最好理解（双指针 + 哑节点）
- 直觉：像手算加法，逐位相加，超过10进位；用哑节点简化尾插逻辑。
- 代码与题解一几乎一致，这里强调“哑节点 + 逐位相加”的写法。

```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0), tail = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int sum = (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0) + carry;
            carry = sum / 10;
            tail.next = new ListNode(sum % 10);
            tail = tail.next;
            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        return dummy.next;
    }
}
```

## 总结思路
- 逐位相加 + 进位；用哑节点简化链表构造；递归与迭代任选其一。

## 相关标签
- 链表、模拟、递归、双指针、数学