# LeetCode-461 汉明距离

- 难度：简单
- 链接：https://leetcode.cn/problems/hamming-distance/

## 问题描述
两个整数之间的汉明距离是对应二进制位不同的位数。求给定 `x` 和 `y` 的汉明距离。

## 题解一：官方经典（按位异或 + 计数）
- 思路：`z = x ^ y`，统计 `z` 中 1 的个数。
- 复杂度：时间 O(32) 常数，空间 O(1)。

```java
class Solution {
    public int hammingDistance(int x, int y) {
        int z = x ^ y, cnt = 0;
        while (z != 0) { cnt += (z & 1); z >>>= 1; }
        return cnt;
    }
}
```

## 题解二：库函数或低位消除
- 标签：位运算
- 思路：`Integer.bitCount(x ^ y)` 或用 `z &= (z - 1)` 每次消去最低位 1 来计数。

## 总结思路
- 本题属于位运算基础，异或后计数即可。

## 相关标签
- 位运算