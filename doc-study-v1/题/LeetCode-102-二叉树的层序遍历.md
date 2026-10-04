# LeetCode-102 二叉树的层序遍历

- 难度：中等
- 链接：https://leetcode.cn/problems/binary-tree-level-order-traversal/

## 问题描述
返回二叉树的层序遍历结果（逐层从左到右）。

## 题解一：官方经典（BFS 队列）
- 思路：用队列按层处理，每层循环按当前队列大小取出节点，记录值并将子节点入队。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        if (root == null) return res;
        Queue<TreeNode> q = new LinkedList<>(); q.offer(root);
        while (!q.isEmpty()) {
            int sz = q.size(); List<Integer> level = new ArrayList<>();
            for (int i = 0; i < sz; i++) {
                TreeNode node = q.poll(); level.add(node.val);
                if (node.left != null) q.offer(node.left);
                if (node.right != null) q.offer(node.right);
            }
            res.add(level);
        }
        return res;
    }
}
```

## 题解二：通用解法（DFS 带层号）
- 标签：二叉树、BFS、队列、DFS
- 思路：递归时携带深度 `d`，确保 `res` 有第 `d` 层的列表，然后将值加入对应层。

```java
import java.util.*;
class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(root, 0, res); return res;
    }
    private void dfs(TreeNode node, int d, List<List<Integer>> res) {
        if (node == null) return;
        if (res.size() == d) res.add(new ArrayList<>());
        res.get(d).add(node.val);
        dfs(node.left, d + 1, res);
        dfs(node.right, d + 1, res);
    }
}
```

## 题解三：最好理解（逐层采样）
- 直觉：像按楼层采样，每次把当前楼层的所有房间访问完，再去下一层。

## 总结思路
- BFS 是层序的首选；DFS 也可，但更适合需要记录层号或做变体的场景。

## 相关标签
- 二叉树、BFS、队列、DFS