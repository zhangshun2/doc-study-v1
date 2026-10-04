# LeetCode-53 最大子数组和

- 难度：中等
- 链接：https://leetcode.cn/problems/maximum-subarray/

## 问题描述
给定整数数组 `nums`，找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

## 题解一：官方经典（Kadane / 一维DP）
- 思路：用 `dp[i]` 表示以 `i` 结尾的最大子数组和，则 `dp[i] = max(nums[i], dp[i-1] + nums[i])`。答案为所有 `dp[i]` 的最大值。
- 复杂度：时间 O(n)，空间 O(1)（滚动变量）。

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int cur = nums[0], ans = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            ans = Math.max(ans, cur);
        }
        return ans;
    }
}
```

## 题解二：通用解法（分治 / 线段树思想）
- 标签：动态规划、贪心、分治
- 思路：分治维护区间四个量：总和、最大前缀和、最大后缀和、最大子段和，合并左右区间得到答案；适合扩展与理解结构化信息。

```java
class Solution2 {
    static class Node { int sum, pre, suf, best; Node(int s,int p,int f,int b){sum=s;pre=p;suf=f;best=b;} }
    public int maxSubArray(int[] nums) { return build(nums, 0, nums.length - 1).best; }
    private Node build(int[] a, int l, int r) {
        if (l == r) { int v = a[l]; return new Node(v, v, v, v); }
        int m = (l + r) >>> 1;
        Node L = build(a, l, m), R = build(a, m + 1, r);
        int sum = L.sum + R.sum;
        int pre = Math.max(L.pre, L.sum + R.pre);
        int suf = Math.max(R.suf, R.sum + L.suf);
        int best = Math.max(Math.max(L.best, R.best), L.suf + R.pre);
        return new Node(sum, pre, suf, best);
    }
}
```

## 总结思路
- Kadane 是最简洁高效模板；分治更有助于理解区间信息的融合，常用于更复杂的区间问题。

## 相关标签
- 动态规划、贪心、分治