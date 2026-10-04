# LeetCode-238 除自身以外数组的乘积

- 难度：中等
- 链接：https://leetcode.cn/problems/product-of-array-except-self/

## 问题描述
给你一个整数数组 `nums`，返回数组 `answer`，其中 `answer[i]` 等于 `nums` 中除 `nums[i]` 之外其余各元素的乘积。要求时间 O(n)，不使用除法，并在 O(1) 额外空间（不计输出数组）。

## 题解一：官方经典（前缀积 + 后缀积）
- 思路：先计算每个位置的左侧乘积（前缀），再从右往左用一个变量维护右侧乘积（后缀）乘到结果上。
- 复杂度：时间 O(n)，空间 O(1)（输出数组不计）。

```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length; int[] ans = new int[n];
        ans[0] = 1;
        for (int i = 1; i < n; i++) ans[i] = ans[i - 1] * nums[i - 1];
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) { ans[i] *= suffix; suffix *= nums[i]; }
        return ans;
    }
}
```

## 题解二：通用解法（显式前后缀数组）
- 标签：数组、前缀与后缀、乘积
- 思路：分别构造前缀积数组 `L` 与后缀积数组 `R`，`ans[i] = L[i-1] * R[i+1]`；空间 O(n)。

```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length; int[] L = new int[n], R = new int[n], ans = new int[n];
        L[0] = 1; for (int i = 1; i < n; i++) L[i] = L[i - 1] * nums[i - 1];
        R[n - 1] = 1; for (int i = n - 2; i >= 0; i--) R[i] = R[i + 1] * nums[i + 1];
        for (int i = 0; i < n; i++) ans[i] = L[i] * R[i];
        return ans;
    }
}
```

## 题解三：最好理解（“左乘右乘”）
- 直觉：每个位置的结果就是左边所有数的乘积乘以右边所有数的乘积。

## 总结思路
- 原地前后缀是最优实现；显式数组更易理解但占空间。

## 相关标签
- 数组、前缀后缀、乘积