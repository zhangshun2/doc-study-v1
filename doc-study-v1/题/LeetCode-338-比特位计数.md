# LeetCode-338 比特位计数

- 难度：简单
- 链接：https://leetcode.cn/problems/counting-bits/

## 问题描述
给定整数 `n`，返回 `0..n` 每个数的二进制中 1 的个数组成的数组。

## 题解一：官方经典（低位消除法 DP）
- 思路：`res[i] = res[i & (i - 1)] + 1`，`i & (i-1)` 会消去 `i` 的最低位 1。
- 复杂度：时间 O(n)，空间 O(n)。

```java
class Solution {
    public int[] countBits(int n) {
        int[] res = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            res[i] = res[i & (i - 1)] + 1;
        }
        return res;
    }
}
```

## 题解二：通用解法（移位法 DP）
- 标签：位运算、动态规划
- 思路：`res[i] = res[i >> 1] + (i & 1)`，同为 O(n) 的递推形式。

## 总结思路
- 两种递推都简洁高效；理解位运算性质是关键。

## 相关标签
- 位运算、动态规划