---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/二分查找/寻找两个正序数组的中位数/微模板与易错点卡片.md)
  - [模板索引：划分二分](../学习方法/模板索引.md#划分二分模板)
---
# LeetCode-4 寻找两个正序数组的中位数

- 难度：困难
- 链接：https://leetcode.cn/problems/median-of-two-sorted-arrays/

## 问题描述
给定两个大小分别为 `m` 和 `n` 的正序（升序）数组 `nums1` 和 `nums2`，请你找出并返回这两个正序数组的中位数，要求时间复杂度为 O(log(m+n))。

## 题解一：官方经典（二分查找分割线）
- 思路：在较短数组上二分，选择一个分割点 `i`，另一个数组对应分割点 `j` 使左右两侧元素数量平衡；确保左侧最大值不大于右侧最小值，计算中位数。
- 复杂度：时间 O(log min(m,n))，空间 O(1)。

```java
class Solution {
    public double findMedianSortedArrays(int[] A, int[] B) {
        if (A.length > B.length) return findMedianSortedArrays(B, A);
        int m = A.length, n = B.length;
        int totalLeft = (m + n + 1) / 2;
        int l = 0, r = m;
        while (l <= r) {
            int i = (l + r) / 2; // A 切分
            int j = totalLeft - i; // B 切分
            int Aleft = (i == 0) ? Integer.MIN_VALUE : A[i - 1];
            int Aright = (i == m) ? Integer.MAX_VALUE : A[i];
            int Bleft = (j == 0) ? Integer.MIN_VALUE : B[j - 1];
            int Bright = (j == n) ? Integer.MAX_VALUE : B[j];
            if (Aleft <= Bright && Bleft <= Aright) {
                if (((m + n) % 2) == 1) return Math.max(Aleft, Bleft);
                return (Math.max(Aleft, Bleft) + Math.min(Aright, Bright)) / 2.0;
            } else if (Aleft > Bright) {
                r = i - 1;
            } else {
                l = i + 1;
            }
        }
        return 0.0; // 不会到达
    }
}
```

## 题解二：通用解法（找第 k 小的递归/迭代）
- 标签：数组、二分查找
- 思路：中位数是第 `(m+n+1)/2` 和 `(m+n+2)/2` 小的数的平均值；用“每次丢弃 k/2 个较小元素”的方法在两个有序数组上找第 k 小。

```java
class Solution {
    public double findMedianSortedArrays(int[] A, int[] B) {
        int m = A.length, n = B.length;
        int left = kth(A, B, (m + n + 1) / 2);
        int right = kth(A, B, (m + n + 2) / 2);
        return (left + right) / 2.0;
    }
    private int kth(int[] A, int[] B, int k) {
        int i = 0, j = 0;
        while (true) {
            if (i == A.length) return B[j + k - 1];
            if (j == B.length) return A[i + k - 1];
            if (k == 1) return Math.min(A[i], B[j]);
            int half = k / 2;
            int ni = Math.min(i + half, A.length) - 1;
            int nj = Math.min(j + half, B.length) - 1;
            if (A[ni] <= B[nj]) { k -= (ni - i + 1); i = ni + 1; }
            else { k -= (nj - j + 1); j = nj + 1; }
        }
    }
}
```

## 题解三：最好理解（“左右平衡的切分”）
- 直觉：把两个数组“拼接”的中位数等价于找到一个切分，让左边的元素数量和右边平衡，且左最大不大于右最小。

## 总结思路
- 二分切分在较短数组上进行，保证对数复杂度；找第 k 小是另一种更通用的写法。

## 相关标签
- 数组、二分查找