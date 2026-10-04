# LeetCode-198 打家劫舍

- 难度：中等
- 链接：https://leetcode.cn/problems/house-robber/

## 问题描述
给定非负整数数组 `nums` 表示每个房屋的金额，不能偷相邻两间，求能偷取的最大金额。

## 题解一：官方经典（滚动DP）
- 思路：`dp[i]=max(dp[i-1], dp[i-2]+nums[i])`，用两个滚动变量表示不偷当前与偷当前的最优。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int rob(int[] nums) {
        int prev2 = 0, prev1 = 0; // dp[i-2], dp[i-1]
        for (int v : nums) {
            int cur = Math.max(prev1, prev2 + v);
            prev2 = prev1; prev1 = cur;
        }
        return prev1;
    }
}
```

## 题解二：通用解法（状态机描述）
- 标签：动态规划、状态转移
- 思路：定义 `take` 与 `skip` 两状态，迭代更新；与滚动 DP 等价但更直观于扩展到环形/二叉树版本。

## 总结思路
- 线性房屋场景下滚动 DP 最简；扩展题目（II/III）可在此基础上调整状态。

## 相关标签
- 动态规划、状态机