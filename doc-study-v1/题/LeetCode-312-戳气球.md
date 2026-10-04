# LeetCode-312 戳气球

- 难度：困难
- 链接：https://leetcode.cn/problems/burst-balloons/

## 问题描述
给定 `nums`，每次戳破一个气球获得 `left*val*right` 的金币，左右为未戳破相邻气球值。问最大金币数。

## 题解一：官方经典（区间DP：最后戳法）
- 思路：在两端各加 1 得到 `arr`，定义 `dp[l][r]` 为开区间 `(l,r)` 内最大收益，枚举最后戳的 `k`：
  - `dp[l][r] = max(dp[l][k] + dp[k][r] + arr[l]*arr[k]*arr[r])`，其中 `l+1 <= k <= r-1`。
- 复杂度：时间 O(n^3)，空间 O(n^2)。

```java
class Solution {
    public int maxCoins(int[] nums) {
        int n = nums.length;
        int[] a = new int[n + 2];
        a[0] = a[n + 1] = 1;
        for (int i = 0; i < n; i++) a[i + 1] = nums[i];
        int[][] dp = new int[n + 2][n + 2];
        for (int len = 2; len <= n + 1; len++) {
            for (int l = 0; l + len <= n + 1; l++) {
                int r = l + len;
                for (int k = l + 1; k < r; k++) {
                    dp[l][r] = Math.max(dp[l][r], dp[l][k] + dp[k][r] + a[l] * a[k] * a[r]);
                }
            }
        }
        return dp[0][n + 1];
    }
}
```

## 题解二：通用解法（记忆化搜索）
- 标签：动态规划、区间DP
- 思路：同转移，用递归 + 记忆化实现，代码更直观。

## 总结思路
- “最后戳”的区间 DP 定式是本题关键；加边界 1 简化相邻计算。

## 相关标签
- 动态规划、区间DP