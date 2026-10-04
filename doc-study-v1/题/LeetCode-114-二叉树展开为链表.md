# LeetCode-114 二叉树展开为链表

- 难度：中等
- 链接：https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/

## 问题描述
将二叉树原地展开为“右指针链表”，顺序为先序遍历。

## 题解一：官方经典（递归先序 + 原地重连）
- 思路：递归展开左右子树，将左子树接到右侧，并把原右子树接到左子树末端。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public void flatten(TreeNode root) {
        if (root == null) return;
        flatten(root.left); flatten(root.right);
        if (root.left != null) {
            TreeNode p = root.left;
            while (p.right != null) p = p.right;
            p.right = root.right;
            root.right = root.left;
            root.left = null;
        }
    }
}
```

## 题解二：通用解法（迭代栈/前序）
- 标签：二叉树、先序遍历、栈、原地修改
- 思路：用栈模拟先序遍历，每弹出一个节点，把它的右指针指向下一个访问的节点。

```java
import java.util.*;
class Solution {
    public void flatten(TreeNode root) {
        if (root == null) return;
        Deque<TreeNode> st = new ArrayDeque<>(); st.push(root);
        TreeNode prev = null;
        while (!st.isEmpty()) {
            TreeNode cur = st.pop();
            if (prev != null) { prev.right = cur; prev.left = null; }
            if (cur.right != null) st.push(cur.right);
            if (cur.left != null) st.push(cur.left);
            prev = cur;
        }
    }
}
```

## 题解三：最好理解（先序串联）
- 直觉：按照先序访问的顺序把所有节点用 `right` 接成一条链，同时把 `left` 置空。

## 总结思路
- 递归与迭代都可；迭代更直观、便于控制遍历顺序。

## 相关标签
- 二叉树、先序遍历、栈、原地修改