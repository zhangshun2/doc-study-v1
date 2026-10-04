# LeetCode-48 旋转图像

- 难度：中等
- 链接：https://leetcode.cn/problems/rotate-image/

## 问题描述
给定一个 `n x n` 的二维矩阵 `matrix` 表示图像，请将图像顺时针旋转 90°。要求原地旋转（空间 O(1)）。

## 题解一：官方经典（转置 + 每行反转）
- 思路：
  - 先对矩阵进行主对角线转置（`matrix[i][j]` 与 `matrix[j][i]` 交换）。
  - 再对每一行进行反转，即可得到顺时针 90° 的结果。
- 复杂度：时间 O(n^2)，空间 O(1)。

```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int t = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = t;
            }
        }
        for (int i = 0; i < n; i++) {
            for (int l = 0, r = n - 1; l < r; l++, r--) {
                int t = matrix[i][l];
                matrix[i][l] = matrix[i][r];
                matrix[i][r] = t;
            }
        }
    }
}
```

## 题解二：通用解法（四点交换 / 分层旋转）
- 标签：矩阵、模拟、原地交换
- 思路：按层（外圈到内圈）旋转，每次将四个对应位置元素做循环交换；不依赖转置。

## 总结思路
- 转置 + 反转实现最简洁；分层四点交换直观但实现细节较多。

## 相关标签
- 数组、矩阵、模拟