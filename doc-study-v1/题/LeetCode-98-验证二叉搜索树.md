# LeetCode-98 验证二叉搜索树

- 难度：中等
- 链接：https://leetcode.cn/problems/validate-binary-search-tree/

## 问题描述
判断给定二叉树是否为二叉搜索树（BST）。BST 的中序遍历为严格递增，或等价地每个节点值在合法区间内。

## 题解一：官方经典（上下界递归）
- 思路：为每个节点维护允许的最小/最大边界，递归检查 `min < node.val < max`，并向子树传递边界。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public boolean isValidBST(TreeNode root) {
        return valid(root, null, null);
    }
    private boolean valid(TreeNode node, Integer low, Integer high) {
        if (node == null) return true;
        if (low != null && node.val <= low) return false;
        if (high != null && node.val >= high) return false;
        return valid(node.left, low, node.val) && valid(node.right, node.val, high);
    }
}
```

## 题解二：通用解法（中序遍历单调递增）
- 标签：二叉树、BST、DFS、中序遍历
- 思路：中序遍历过程中，当前值必须严格大于上一个访问值。

```java
class Solution {
    private Long prev = Long.MIN_VALUE;
    public boolean isValidBST(TreeNode root) {
        return inorder(root);
    }
    private boolean inorder(TreeNode node) {
        if (node == null) return true;
        if (!inorder(node.left)) return false;
        if (node.val <= prev) return false;
        prev = (long) node.val;
        return inorder(node.right);
    }
}
```

## 题解三：最好理解（边界与顺序）
- 直觉：每个节点都“夹在”一个允许区间里；或把整棵树拍成中序序列，必须严格递增。

## 总结思路
- 两模板都常用：边界法更工程化、易扩展；中序法更直觉但需注意严格递增。

## 相关标签
- 二叉树、BST、DFS、中序遍历