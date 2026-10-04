# LeetCode-96 不同的二叉搜索树

- 难度：中等
- 链接：https://leetcode.cn/problems/unique-binary-search-trees/

## 问题描述
给定整数 `n`，返回有 `n` 个节点（值 1..n）能组成的不同二叉搜索树数量。

## 题解一：官方经典（动态规划/卡特兰数）
- 思路：`G[n] = sum_{i=1..n} G[i-1] * G[n-i]`，左子树 `i-1` 个节点，右子树 `n-i` 个节点。
- 复杂度：时间 O(n^2)，空间 O(n)。

```java
class Solution {
    public int numTrees(int n) {
        int[] dp = new int[n + 1];
        dp[0] = dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            for (int root = 1; root <= i; root++) {
                dp[i] += dp[root - 1] * dp[i - root];
            }
        }
        return dp[n];
    }
}
```

## 题解二：通用解法（递归记忆化）
- 标签：动态规划、二叉搜索树、卡特兰数
- 思路：记忆化递归计算 `f(n)`，用数组缓存防止重复计算。

```java
class Solution {
    public int numTrees(int n) {
        int[] memo = new int[n + 1];
        memo[0] = memo[1] = 1;
        return f(n, memo);
    }
    private int f(int n, int[] memo) {
        if (memo[n] != 0) return memo[n];
        int ans = 0;
        for (int root = 1; root <= n; root++) {
            ans += f(root - 1, memo) * f(n - root, memo);
        }
        return memo[n] = ans;
    }
}
```

## 题解三：最好理解（从组合到递推）
- 直觉：以某个节点为根，左侧选 `i-1` 个、右侧选 `n-i` 个；所有根的组合数相加就是答案。

## 总结思路
- DP 与记忆化本质一致；若追求公式可用卡特兰数闭式，但实现上 DP 更直接。

## 相关标签
- 动态规划、二叉搜索树、卡特兰数