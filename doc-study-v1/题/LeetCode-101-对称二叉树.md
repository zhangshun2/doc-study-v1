# LeetCode-101 对称二叉树

- 难度：简单
- 链接：https://leetcode.cn/problems/symmetric-tree/

## 问题描述
判断一个二叉树是否镜像对称。

## 题解一：官方经典（递归镜像）
- 思路：递归判断 `left.left` 对 `right.right`，`left.right` 对 `right.left`；值需相等。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        return mirror(root.left, root.right);
    }
    private boolean mirror(TreeNode a, TreeNode b) {
        if (a == null || b == null) return a == b;
        if (a.val != b.val) return false;
        return mirror(a.left, b.right) && mirror(a.right, b.left);
    }
}
```

## 题解二：通用解法（队列成对比较）
- 标签：二叉树、递归、队列、BFS
- 思路：用队列保存成对节点，逐对比较值与结构，按镜像关系入队。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public boolean isSymmetric(TreeNode root) {
        if (root == null) return true;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root.left); q.offer(root.right);
        while (!q.isEmpty()) {
            TreeNode a = q.poll(), b = q.poll();
            if (a == null && b == null) continue;
            if (a == null || b == null || a.val != b.val) return false;
            q.offer(a.left); q.offer(b.right);
            q.offer(a.right); q.offer(b.left);
        }
        return true;
    }
}
```

## 题解三：最好理解（镜像直觉）
- 直觉：左右两边像照镜子；一侧的左孩子对应另一侧的右孩子。

## 总结思路
- 递归更简洁；迭代更利于理解队列顺序与边界情况处理。

## 相关标签
- 二叉树、递归、队列、BFS