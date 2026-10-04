# LeetCode-560 和为 K 的子数组

- 难度：中等
- 链接：https://leetcode.cn/problems/subarray-sum-equals-k/

## 问题描述
给定整数数组 `nums` 和整数 `k`，统计和为 `k` 的连续子数组个数。

## 题解一：官方经典（前缀和 + 哈希计数）
- 思路：`pre[i]` 为前缀和，若 `pre[j]-pre[i]=k` 则 `i..j-1` 和为 `k`。遍历时维护哈希表记录各前缀和出现次数；当前 `pre` 贡献 `count += mp.get(pre-k)`。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> mp = new HashMap<>();
        mp.put(0, 1);
        int pre = 0, ans = 0;
        for (int x : nums) {
            pre += x;
            ans += mp.getOrDefault(pre - k, 0);
            mp.put(pre, mp.getOrDefault(pre, 0) + 1);
        }
        return ans;
    }
}
```

## 题解二：通用解法（枚举右端点 + 二维前缀）
- 标签：数组、哈希、前缀和
- 思路：也可枚举右端点，使用前缀数组在 O(1) 时间查询左端点的前缀值；整体依然 O(n) 时间、O(n) 空间。

## 题解三：最好理解（“现在的前缀和减去以前的某个前缀等于 k”）
- 直觉：找多少个历史前缀和与当前前缀和相差 `k`，这些对应的区间就是答案。

## 总结思路
- 前缀和 + 哈希是模板，注意初始化 `mp.put(0,1)` 表示空前缀。

## 相关标签
- 数组、哈希、前缀和