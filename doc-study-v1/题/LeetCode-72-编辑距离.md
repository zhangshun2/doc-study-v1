# LeetCode-72 编辑距离

- 难度：困难
- 链接：https://leetcode.cn/problems/edit-distance/

## 问题描述
给定两个字符串 `word1` 与 `word2`，计算将 `word1` 转换为 `word2` 所需的最少操作数（插入、删除、替换）。

## 题解一：官方经典（二维DP）
- 思路：`dp[i][j]` 为 `word1[0..i)` 到 `word2[0..j)` 的最少操作数；若末字符相同沿用对角，否则在插删换三者中取最小 +1。
- 复杂度：时间 O(mn)，空间 O(mn)。

```java
class Solution {
    public int minDistance(String a, String b) {
        int m = a.length(), n = b.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 0; i <= m; i++) dp[i][0] = i;
        for (int j = 0; j <= n; j++) dp[0][j] = j;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (a.charAt(i - 1) == b.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];
                else dp[i][j] = 1 + Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]);
            }
        }
        return dp[m][n];
    }
}
```

## 题解二：通用解法（递归 + 记忆化）
- 标签：字符串、动态规划、递归
- 思路：自顶向下递归，分末字符是否相等；用二维数组记忆避免重复计算。

```java
import java.util.*;
class Solution {
    private int[][] memo;
    public int minDistance(String a, String b) {
        memo = new int[a.length() + 1][b.length() + 1];
        for (int[] row : memo) Arrays.fill(row, -1);
        return dfs(a, b, a.length(), b.length());
    }
    private int dfs(String a, String b, int i, int j) {
        if (i == 0) return j;
        if (j == 0) return i;
        if (memo[i][j] != -1) return memo[i][j];
        if (a.charAt(i - 1) == b.charAt(j - 1)) return memo[i][j] = dfs(a, b, i - 1, j - 1);
        int ins = dfs(a, b, i, j - 1);
        int del = dfs(a, b, i - 1, j);
        int rep = dfs(a, b, i - 1, j - 1);
        return memo[i][j] = 1 + Math.min(Math.min(ins, del), rep);
    }
}
```

## 题解三：最好理解（插删换的最小代价）
- 直觉：把两个串尾部字符比对，若相同就同时去掉；若不同就选择插入、删除或替换代价最小的一步继续。

## 总结思路
- DP是标准写法；递归更易理解但需要记忆化加速。

## 相关标签
- 字符串、动态规划、递归