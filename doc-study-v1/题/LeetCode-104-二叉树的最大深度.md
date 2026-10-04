# LeetCode-104 二叉树的最大深度

- 难度：简单
- 链接：https://leetcode.cn/problems/maximum-depth-of-binary-tree/

## 问题描述
给定二叉树根节点 `root`，返回其最大深度（从根到最远叶子的最长路径上的节点数量）。

## 题解一：官方经典（递归 DFS）
- 思路：深度 = `1 + max(左深度, 右深度)`；遇到空节点返回 0。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
    }
}
```

## 题解二：通用解法（BFS 层序）
- 标签：二叉树、DFS、BFS、层序
- 思路：按层遍历，层数即最大深度。

```java
import java.util.*;
class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        Queue<TreeNode> q = new LinkedList<>(); q.offer(root);
        int depth = 0;
        while (!q.isEmpty()) {
            int sz = q.size(); depth++;
            for (int i = 0; i < sz; i++) {
                TreeNode node = q.poll();
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
        }
        return depth;
    }
}
```

## 题解三：最好理解（递归直觉）
- 直觉：从下往上返回每棵子树的高度，父节点取更大的那一个再加 1。

## 总结思路
- 递归最简洁；需要逐层统计时用 BFS 更直观。

## 相关标签
- 二叉树、DFS、BFS、层序