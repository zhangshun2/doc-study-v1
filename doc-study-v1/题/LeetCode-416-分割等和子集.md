# LeetCode-416 分割等和子集

- 难度：中等
- 链接：https://leetcode.cn/problems/partition-equal-subset-sum/

## 问题描述
给定一个只包含正整数的数组，判断是否可以将数组分割成两个子集，使两个子集的元素和相等。

## 题解一：官方经典（0/1 背包可达性）
- 思路：若总和为奇数直接返回 `false`。目标为 `sum/2`，使用一维布尔 DP：`dp[j] = dp[j] || dp[j - v]`。
- 复杂度：时间 O(n·sum)，空间 O(sum)。

```java
class Solution {
    public boolean canPartition(int[] nums) {
        int sum = 0; for (int v : nums) sum += v;
        if ((sum & 1) == 1) return false;
        int target = sum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;
        for (int v : nums) {
            for (int j = target; j >= v; j--) {
                dp[j] = dp[j] || dp[j - v];
            }
        }
        return dp[target];
    }
}
```

## 题解二：通用解法（记忆化搜索）
- 标签：动态规划、背包、子集和
- 思路：回溯选择/不选择，记忆 `(i, remain)` 状态；与 DP 等价但实现风格不同。

## 总结思路
- 典型子集和判定；注意倒序遍历避免重复使用同一元素。

## 相关标签
- 动态规划、背包