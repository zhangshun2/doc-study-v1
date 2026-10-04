# LeetCode-437 路径总和 III

- 难度：中等
- 链接：https://leetcode.cn/problems/path-sum-iii/

## 问题描述
给定一个二叉树和整数 `targetSum`，返回路径和等于 `targetSum` 的路径数量。路径方向必须向下（父到子），但可以从任意节点开始。

## 题解一：官方经典（前缀和 + 哈希）
- 思路：在 DFS 中维护当前路径前缀和 `sum`，统计 `sum - target` 在哈希表中的出现次数。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    private Map<Long, Integer> cnt = new HashMap<>();
    private int ans = 0; private int target;
    public int pathSum(TreeNode root, int targetSum) {
        target = targetSum; cnt.put(0L, 1);
        dfs(root, 0L); return ans;
    }
    private void dfs(TreeNode node, long sum) {
        if (node == null) return;
        sum += node.val;
        ans += cnt.getOrDefault(sum - target, 0);
        cnt.put(sum, cnt.getOrDefault(sum, 0) + 1);
        dfs(node.left, sum); dfs(node.right, sum);
        cnt.put(sum, cnt.get(sum) - 1);
    }
}
```

## 题解二：通用解法（枚举起点 + DFS）
- 标签：二叉树、DFS、前缀和、哈希
- 思路：对每个节点作为起点，搜索向下的路径和为 `target` 的数量。

```java
class Solution {
    public int pathSum(TreeNode root, int targetSum) {
        if (root == null) return 0;
        return from(root, targetSum) + pathSum(root.left, targetSum) + pathSum(root.right, targetSum);
    }
    private int from(TreeNode node, int target) {
        if (node == null) return 0;
        int cnt = (node.val == target) ? 1 : 0;
        cnt += from(node.left, target - node.val);
        cnt += from(node.right, target - node.val);
        return cnt;
    }
}
```

## 题解三：最好理解（前缀思想）
- 直觉：想象从根到当前的路径和是 `sum`，如果之前某个位置的和是 `sum - target`，那么中间这一段就是目标路径。

## 总结思路
- 前缀哈希模板非常常用；枚举起点更直观但复杂度更高。

## 相关标签
- 二叉树、DFS、前缀和、哈希