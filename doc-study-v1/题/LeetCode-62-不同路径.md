# LeetCode-62 不同路径

- 难度：中等
- 链接：https://leetcode.cn/problems/unique-paths/

## 问题描述
在 `m x n` 的网格中从左上角走到右下角，每一步只能向右或向下，问有多少不同路径。

## 题解一：官方经典（二维DP）
- 思路：`dp[i][j] = dp[i-1][j] + dp[i][j-1]`，第一行与第一列初始化为 1（只有直走一种方式）。可压缩到一维 `dp[j]`。
- 复杂度：时间 O(m·n)，空间 O(n)。

```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        for (int j = 0; j < n; j++) dp[j] = 1;
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[j] += dp[j - 1];
            }
        }
        return dp[n - 1];
    }
}
```

## 题解二：最好理解（组合数学）
- 标签：动态规划、组合计数、数学
- 思路：总共走 `(m-1) + (n-1)` 步，从中选择 `(m-1)` 次下或 `(n-1)` 次右，答案为组合数 `C(m+n-2, m-1)`。用长整型累乘/除避免溢出。

```java
class Solution2 {
    public int uniquePaths(int m, int n) {
        int a = m - 1, b = n - 1; // choose a from a+b
        long ans = 1;
        for (int i = 1; i <= a; i++) {
            ans = ans * (a + b - a + i) / i; // (b+i)/i
        }
        return (int) ans;
    }
}
```

## 总结思路
- DP与组合数学都可；DP适合通用扩展（障碍物等变体），组合法在无障碍时更简洁高效。

## 相关标签
- 动态规划、组合计数、数学