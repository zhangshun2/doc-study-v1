# LeetCode-226 翻转二叉树

- 难度：简单
- 链接：https://leetcode.cn/problems/invert-binary-tree/

## 问题描述
翻转一棵二叉树，使每个节点的左右子树交换。

## 题解一：官方经典（递归交换）
- 思路：递归地交换 `left` 和 `right`，自顶向下或自底向上都可。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        TreeNode t = root.left; root.left = root.right; root.right = t;
        invertTree(root.left); invertTree(root.right);
        return root;
    }
}
```

## 题解二：通用解法（BFS 队列）
- 标签：二叉树、递归、BFS
- 思路：层序遍历，每访问一个节点就交换其左右。

```java
import java.util.*;
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) return null;
        Queue<TreeNode> q = new LinkedList<>(); q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            TreeNode t = node.left; node.left = node.right; node.right = t;
            if (node.left != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
        return root;
    }
}
```

## 题解三：最好理解（就地交换）
- 直觉：遍历到每个节点时把左右孩子对调即可。

## 总结思路
- 简单题，递归和迭代都行，注意空节点。

## 相关标签
- 二叉树、递归、BFS