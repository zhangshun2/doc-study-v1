# LeetCode-617 合并二叉树

- 难度：简单
- 链接：https://leetcode.cn/problems/merge-two-binary-trees/

## 问题描述
将两棵二叉树合并为一棵新树。如果两个节点重叠，则将值相加；否则直接使用非空节点。

## 题解一：官方经典（递归合并）
- 思路：同时递归两棵树，构建新节点为两者值之和，左右孩子同样递归合并。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public TreeNode mergeTrees(TreeNode t1, TreeNode t2) {
        if (t1 == null) return t2;
        if (t2 == null) return t1;
        TreeNode node = new TreeNode(t1.val + t2.val);
        node.left = mergeTrees(t1.left, t2.left);
        node.right = mergeTrees(t1.right, t2.right);
        return node;
    }
}
```

## 题解二：通用解法（BFS 队列原地）
- 标签：二叉树、递归、BFS
- 思路：用队列同时遍历两棵树，原地将 `t1` 修改为合并后的树。

```java
import java.util.*;
class Solution {
    public TreeNode mergeTrees(TreeNode t1, TreeNode t2) {
        if (t1 == null) return t2; if (t2 == null) return t1;
        Queue<TreeNode[]> q = new LinkedList<>(); q.offer(new TreeNode[]{t1, t2});
        while (!q.isEmpty()) {
            TreeNode[] pair = q.poll(); TreeNode a = pair[0], b = pair[1];
            a.val += b.val;
            if (a.left != null && b.left != null) q.offer(new TreeNode[]{a.left, b.left});
            else if (a.left == null) a.left = b.left;
            if (a.right != null && b.right != null) q.offer(new TreeNode[]{a.right, b.right});
            else if (a.right == null) a.right = b.right;
        }
        return t1;
    }
}
```

## 题解三：最好理解（同步遍历）
- 直觉：两个树同步走，重叠就相加；缺失用另一棵的节点补上。

## 总结思路
- 原地或新建都可；原地更省空间。

## 相关标签
- 二叉树、递归、BFS