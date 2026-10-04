# LeetCode-124 二叉树中的最大路径和

- 难度：困难
- 链接：https://leetcode.cn/problems/binary-tree-maximum-path-sum/

## 问题描述
返回二叉树中“路径和”的最大值。路径可以从任意节点到任意节点，但必须沿父子关系连通。

## 题解一：官方经典（DFS 返回最大贡献）
- 思路：对每个节点，计算其左/右子树向上的最大贡献 `max(0, gain)`；更新全局最大为 `leftGain + rightGain + node.val`。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    private int ans = Integer.MIN_VALUE;
    public int maxPathSum(TreeNode root) {
        dfs(root); return ans;
    }
    private int dfs(TreeNode node) {
        if (node == null) return 0;
        int L = Math.max(0, dfs(node.left));
        int R = Math.max(0, dfs(node.right));
        ans = Math.max(ans, L + R + node.val);
        return Math.max(L, R) + node.val;
    }
}
```

## 题解二：通用解法（分治/返回两值）
- 标签：二叉树、DFS、分治、动态规划
- 思路：返回二元组 `{向上最大、子树内最大}`，父节点综合左右返回值得到本节点答案。

```java
class Solution {
    public int maxPathSum(TreeNode root) {
        return helper(root)[1];
    }
    private int[] helper(TreeNode node) {
        if (node == null) return new int[]{0, Integer.MIN_VALUE};
        int[] L = helper(node.left), R = helper(node.right);
        int up = Math.max(Math.max(L[0], R[0]) + node.val, node.val);
        int cross = Math.max(0, L[0]) + Math.max(0, R[0]) + node.val;
        int best = Math.max(Math.max(L[1], R[1]), cross);
        return new int[]{Math.max(0, up), best};
    }
}
```

## 题解三：最好理解（“贡献值”直觉）
- 直觉：向父亲贡献只能选左右中较大的路径且不能为负；但在当前节点处可同时使用左右两侧形成一条“经过当前”的最佳路径。

## 总结思路
- 关键在于“向上贡献”和“经过当前”的区分；模板常用。

## 相关标签
- 二叉树、DFS、分治、动态规划