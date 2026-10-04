# LeetCode-300 最长递增子序列

- 难度：中等
- 链接：https://leetcode.cn/problems/longest-increasing-subsequence/

## 问题描述
给定整数数组 `nums`，找到其中最长严格递增子序列的长度。

## 题解一：官方经典（贪心 + 二分 / patience sorting）
- 思路：维护 `tails` 数组，`tails[k]` 为长度为 `k+1` 的递增子序列的最小尾值；对每个数在 `tails` 中二分查找替换位置，最终 `tails` 的长度即为答案。
- 复杂度：时间 O(n log n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int v : nums) {
            int i = Arrays.binarySearch(tails, 0, size, v);
            if (i < 0) i = -i - 1;
            tails[i] = v;
            if (i == size) size++;
        }
        return size;
    }
}
```

## 题解二：基础DP O(n^2)
- 标签：动态规划、二分、贪心
- 思路：`dp[i]` 为以 `i` 结尾的 LIS 长度，枚举 `j<i` 更新；易理解但较慢。

## 总结思路
- 首选贪心+二分；DP便于入门与对比验证。

## 相关标签
- 动态规划、二分、贪心