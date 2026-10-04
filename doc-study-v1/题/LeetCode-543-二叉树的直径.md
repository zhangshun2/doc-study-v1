# LeetCode-543 二叉树的直径

- 难度：简单
- 链接：https://leetcode.cn/problems/diameter-of-binary-tree/

## 问题描述
返回二叉树的直径长度，即任意两个节点路径的最大边数（节点数-1）。

## 题解一：官方经典（DFS 返回深度 + 更新直径）
- 思路：每个节点的“经过节点的直径”是 `左深度 + 右深度`；递归返回当前节点的深度 `1 + max(左,右)`。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    private int ans = 0;
    public int diameterOfBinaryTree(TreeNode root) {
        depth(root); return ans;
    }
    private int depth(TreeNode node) {
        if (node == null) return 0;
        int L = depth(node.left), R = depth(node.right);
        ans = Math.max(ans, L + R);
        return 1 + Math.max(L, R);
    }
}
```

## 题解二：通用解法（分治）
- 标签：二叉树、DFS、分治
- 思路：返回二元组 `{深度, 子树直径}`，父节点综合得到新直径。

```java
class Solution {
    public int diameterOfBinaryTree(TreeNode root) {
        return solve(root)[1];
    }
    private int[] solve(TreeNode node) {
        if (node == null) return new int[]{0, 0};
        int[] L = solve(node.left), R = solve(node.right);
        int depth = 1 + Math.max(L[0], R[0]);
        int dia = Math.max(Math.max(L[1], R[1]), L[0] + R[0]);
        return new int[]{depth, dia};
    }
}
```

## 题解三：最好理解（“深度叠加”）
- 直觉：直径就是左右深度之和；深度返回给父节点以继续计算。

## 总结思路
- 模板题，关键是区分“返回深度”和“更新直径”。

## 相关标签
- 二叉树、DFS、分治