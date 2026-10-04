# LeetCode-221 最大正方形

- 难度：中等
- 链接：https://leetcode.cn/problems/maximal-square/

## 问题描述
在由 `'0'` 和 `'1'` 组成的二维矩阵中，找到只包含 `'1'` 的最大正方形，并返回其面积。

## 题解一：官方经典（二维DP）
- 思路：`dp[i][j]` 表示以 `(i,j)` 为右下角的最大正方形边长；若 `matrix[i][j]=='1'`，则 `dp[i][j]=min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])+1`。
- 复杂度：时间 O(m·n)，空间 O(m·n)（可压缩到 O(n)）。

```java
class Solution {
    public int maximalSquare(char[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        int[][] dp = new int[m + 1][n + 1];
        int max = 0;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (matrix[i - 1][j - 1] == '1') {
                    dp[i][j] = Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1])) + 1;
                    max = Math.max(max, dp[i][j]);
                }
            }
        }
        return max * max;
    }
}
```

## 题解二：通用解法（一维滚动）
- 标签：动态规划、矩阵DP、空间优化
- 思路：用一维数组与一个临时变量保存左上值实现空间压缩。

## 总结思路
- 邻三者取最小再加一是核心；注意索引与初始化边界。

## 相关标签
- 动态规划、矩阵DP