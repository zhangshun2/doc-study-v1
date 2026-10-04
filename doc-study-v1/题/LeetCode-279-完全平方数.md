# LeetCode-279 完全平方数

- 难度：中等
- 链接：https://leetcode.cn/problems/perfect-squares/

## 问题描述
给定正整数 `n`，求最少的完全平方数使其和为 `n`。

## 题解一：官方经典（完全背包DP）
- 思路：`dp[i]` 表示和为 `i` 的最少平方数数量，转移 `dp[i] = min(dp[i], dp[i - s*s] + 1)`。
- 复杂度：时间 O(n√n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int numSquares(int n) {
        int[] dp = new int[n + 1];
        Arrays.fill(dp, Integer.MAX_VALUE / 2);
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            for (int s = 1; s * s <= i; s++) {
                dp[i] = Math.min(dp[i], dp[i - s * s] + 1);
            }
        }
        return dp[n];
    }
}
```

## 题解二：通用解法（BFS 层次）
- 标签：动态规划、BFS、数论
- 思路：将 `n` 作为起点，每层减去一个平方数，首次到达 0 的层数就是答案；亦可结合四平方定理优化判断。

## 总结思路
- DP直观稳妥，BFS适合理解“最少步数”的本质；根据 `n` 的上限选择实现。

## 相关标签
- 动态规划、背包、BFS