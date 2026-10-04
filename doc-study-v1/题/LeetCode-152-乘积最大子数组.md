# LeetCode-152 乘积最大子数组

- 难度：中等
- 链接：https://leetcode.cn/problems/maximum-product-subarray/

## 问题描述
给定一个整数数组 `nums`，找出乘积最大的连续子数组（至少包含一个数），返回该乘积。

## 题解一：官方经典（动态规划：维护最大/最小）
- 思路：当前最大乘积可能来自前一位置的最大或最小（因负数翻转）。维护 `maxHere` 与 `minHere`，遇到负数交换两者，再更新。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int maxProduct(int[] nums) {
        int maxHere = nums[0], minHere = nums[0], ans = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int v = nums[i];
            if (v < 0) { int t = maxHere; maxHere = minHere; minHere = t; }
            maxHere = Math.max(v, maxHere * v);
            minHere = Math.min(v, minHere * v);
            ans = Math.max(ans, maxHere);
        }
        return ans;
    }
}
```

## 题解二：通用解法（分段处理零）
- 标签：动态规划、贪心
- 思路：零会将乘积重置，可按零分段分别计算最大乘积；总体复杂度仍线性。

## 总结思路
- 关键在同时追踪最大与最小乘积，以应对负数翻转。

## 相关标签
- 动态规划、数组