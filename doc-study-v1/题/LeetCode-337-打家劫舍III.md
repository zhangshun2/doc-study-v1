# LeetCode-337 打家劫舍 III

- 难度：中等
- 链接：https://leetcode.cn/problems/house-robber-iii/

## 问题描述
在二叉树上打家劫舍，不能同时选择父子节点，求最大收益。

## 题解一：官方经典（树形 DP 返回二元组）
- 思路：对每个节点返回 `{不偷该节点的最大收益, 偷该节点的最大收益}`，合并左右子树结果即可。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public int rob(TreeNode root) {
        int[] r = dfs(root); return Math.max(r[0], r[1]);
    }
    private int[] dfs(TreeNode node) {
        if (node == null) return new int[]{0, 0};
        int[] L = dfs(node.left), R = dfs(node.right);
        int steal = node.val + L[0] + R[0];
        int skip = Math.max(L[0], L[1]) + Math.max(R[0], R[1]);
        return new int[]{skip, steal};
    }
}
```

## 题解二：通用解法（记忆化递归）
- 标签：二叉树、动态规划、递归、记忆化
- 思路：用哈希表记忆以某节点为根的最大收益，避免重复计算。

```java
import java.util.*;
class Solution {
    private Map<TreeNode, Integer> memo = new HashMap<>();
    public int rob(TreeNode root) {
        if (root == null) return 0;
        if (memo.containsKey(root)) return memo.get(root);
        int val1 = root.val;
        if (root.left != null) val1 += rob(root.left.left) + rob(root.left.right);
        if (root.right != null) val1 += rob(root.right.left) + rob(root.right.right);
        int val2 = rob(root.left) + rob(root.right);
        int ans = Math.max(val1, val2);
        memo.put(root, ans); return ans;
    }
}
```

## 题解三：最好理解（偷与不偷）
- 直觉：每个节点只有两种状态：偷它或不偷它；不偷可以选择孩子的最优，偷则只能选孙子。

## 总结思路
- 树形 DP 模板题；返回二元组的写法更清晰易用。

## 相关标签
- 二叉树、动态规划、递归、记忆化