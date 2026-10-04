# LeetCode-94 二叉树的中序遍历

- 难度：简单
- 链接：https://leetcode.cn/problems/binary-tree-inorder-traversal/

## 问题描述
给定二叉树根节点 `root`，返回其中序遍历（左-中-右）。

## 题解一：官方经典（递归）
- 思路：递归访问左子树、记录当前节点、递归访问右子树。
- 复杂度：时间 O(n)，空间 O(n)（递归栈）。

```java
import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, res); return res;
    }
    private void dfs(TreeNode node, List<Integer> res) {
        if (node == null) return;
        dfs(node.left, res);
        res.add(node.val);
        dfs(node.right, res);
    }
}
```

## 题解二：通用解法（迭代栈）
- 标签：二叉树、递归、栈、遍历
- 思路：用栈模拟递归过程，指针一路压左子树，弹出时记录节点，再转向右子树。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) { stack.push(cur); cur = cur.left; }
            TreeNode node = stack.pop(); res.add(node.val);
            cur = node.right;
        }
        return res;
    }
}
```

## 题解三：最好理解（迭代直觉）
- 直觉：一路向左把节点压栈，遇到空就回退一个记录值，再转向其右子树继续。

## 总结思路
- 遍历三件套：递归最简洁；迭代更通用；Morris 可降空间但实现稍复杂（此处不展开）。

## 相关标签
- 二叉树、递归、栈、遍历