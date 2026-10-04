# LeetCode-64 最小路径和

- 难度：中等
- 链接：https://leetcode.cn/problems/minimum-path-sum/

## 问题描述
给定 `m x n` 的网格 `grid`，每个单元格有一个非负整数，从左上角到右下角，只能向右或向下移动，求路径的最小和。

## 题解一：官方经典（二维/一维DP）
- 思路：`dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`；可用一维 `dp[j]` 原地更新（`dp[j] = grid[i][j] + min(dp[j], dp[j-1])`）。
- 复杂度：时间 O(m·n)，空间 O(n)。

```java
class Solution {
    public int minPathSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] dp = new int[n];
        dp[0] = grid[0][0];
        for (int j = 1; j < n; j++) dp[j] = dp[j - 1] + grid[0][j];
        for (int i = 1; i < m; i++) {
            dp[0] += grid[i][0];
            for (int j = 1; j < n; j++) {
                dp[j] = Math.min(dp[j], dp[j - 1]) + grid[i][j];
            }
        }
        return dp[n - 1];
    }
}
```

## 题解二：通用解法（原地复用网格）
- 标签：动态规划、网格DP、空间优化
- 思路：直接在 `grid` 上累加最小路径和，最后返回 `grid[m-1][n-1]`，减少额外空间。

```java
class Solution2 {
    public int minPathSum(int[][] g) {
        int m = g.length, n = g[0].length;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j == 0) continue;
                int up = i > 0 ? g[i - 1][j] : Integer.MAX_VALUE / 2;
                int left = j > 0 ? g[i][j - 1] : Integer.MAX_VALUE / 2;
                g[i][j] += Math.min(up, left);
            }
        }
        return g[m - 1][n - 1];
    }
}
```

## 总结思路
- 网格DP的经典模板；初始化首行首列后即可统一转移，空间优化到 O(n) 或原地累加。

## 相关标签
- 动态规划、网格DP、空间优化