# LeetCode-240 搜索二维矩阵 II

- 难度：中等
- 链接：https://leetcode.cn/problems/search-a-2d-matrix-ii/

## 问题描述
给定一个 `m x n` 矩阵，其中每行每列均升序，判断目标值是否存在于矩阵中。

## 题解一：官方经典（从右上角出发的单调搜索）
- 思路：从右上角开始，若当前值大于目标则左移，若小于目标则下移；利用行列的单调性。
- 复杂度：时间 O(m+n)，空间 O(1)。

```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int i = 0, j = n - 1;
        while (i < m && j >= 0) {
            int v = matrix[i][j];
            if (v == target) return true;
            if (v > target) j--; else i++;
        }
        return false;
    }
}
```

## 题解二：通用解法（分治 / 二分）
- 标签：矩阵搜索、双指针、二分
- 思路：可对每行或每列做二分查找，或使用分治缩小区域（复杂度略高）。

## 总结思路
- 右上角搜索最优；行/列二分作为替代。

## 相关标签
- 数组、矩阵、搜索