# LeetCode-322 零钱兑换

- 难度：中等
- 链接：https://leetcode.cn/problems/coin-change/

## 问题描述
给定不同面额的硬币 `coins` 和总金额 `amount`，每种硬币可以使用多次，求凑成总金额的最少硬币数；若无法凑出则返回 -1。

## 题解一：官方经典（完全背包最少张数）
- 思路：`dp[x]` 表示金额 `x` 的最少硬币数，初始化为大值；对每个硬币更新 `dp[x] = min(dp[x], dp[x-coin]+1)`。
- 复杂度：时间 O(n·amount)，空间 O(amount)。

```java
import java.util.*;
class Solution {
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int c : coins) {
            for (int x = c; x <= amount; x++) {
                dp[x] = Math.min(dp[x], dp[x - c] + 1);
            }
        }
        return dp[amount] > amount ? -1 : dp[amount];
    }
}
```

## 题解二：通用解法（BFS 金额层）
- 标签：动态规划、背包、BFS
- 思路：从 0 金额开始层次扩展到 `amount`，首次到达层数即为最少硬币数；适合大面额与少硬币种类时。

## 总结思路
- 完全背包 DP 是通解；BFS也可用于理解“最少步数”。

## 相关标签
- 动态规划、背包