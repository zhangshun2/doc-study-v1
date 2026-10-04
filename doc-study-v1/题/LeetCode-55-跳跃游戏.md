# LeetCode-55 跳跃游戏

- 难度：中等
- 链接：https://leetcode.cn/problems/jump-game/

## 问题描述
给定非负整数数组 `nums`，其中每个元素代表你在该位置可以跳跃的最大长度。判断是否能到达最后一个下标。

## 题解一：官方经典（贪心维护最远可达）
- 思路：遍历数组，维护当前最远可达位置 `far`；若遍历到位置 `i` 时 `i > far` 则不可达；每一步更新 `far = max(far, i + nums[i])`。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public boolean canJump(int[] nums) {
        int far = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > far) return false;
            far = Math.max(far, i + nums[i]);
        }
        return true;
    }
}
```

## 题解二：通用解法（动态规划可达性）
- 标签：数组、贪心、动态规划
- 思路：`dp[i]` 表示位置 `i` 是否可达；若存在 `j` 可达且 `j + nums[j] >= i` 则 `dp[i]=true`；最坏 O(n^2) 不优但直观。

```java
class Solution {
    public boolean canJump(int[] nums) {
        int n = nums.length; boolean[] dp = new boolean[n]; dp[0] = true;
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && j + nums[j] >= i) { dp[i] = true; break; }
            }
        }
        return dp[n - 1];
    }
}
```

## 题解三：最好理解（“电量最远能到哪”）
- 直觉：每个位置提供一段“电量”扩展最远可达，如果当前下标已经超出最远可达，就断电无法到达终点。

## 总结思路
- 贪心一遍最优且简单；DP用于理解但不推荐在面试实现。

## 相关标签
- 数组、贪心、动态规划