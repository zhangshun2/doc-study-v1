---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/排序/数组中的第K个最大元素/微模板与易错点卡片.md)
  - [模板索引：快速选择/堆](../学习方法/模板索引.md#快速选择或堆模板)
---
# LeetCode-215 数组中的第K个最大元素

- 难度：中等
- 链接：https://leetcode.cn/problems/kth-largest-element-in-an-array/

## 问题描述
给定未排序的数组 `nums`，返回其中第 `k` 个最大的元素。注意：不是第 `k` 个不同元素。

## 题解一：官方经典（快速选择 Quickselect）
- 思路：将问题转化为找第 `n-k` 个最小元素。使用分区（类似快速排序）每次将元素按枢轴分成左右两部分，迭代定位目标索引。
- 复杂度：均摊时间 O(n)，最坏 O(n^2)，空间 O(1)。

```java
import java.util.*;
class Solution {
    public int findKthLargest(int[] nums, int k) {
        int n = nums.length, target = n - k;
        int l = 0, r = n - 1;
        while (l <= r) {
            int p = partition(nums, l, r);
            if (p == target) return nums[p];
            if (p < target) l = p + 1; else r = p - 1;
        }
        return -1;
    }
    private int partition(int[] a, int l, int r) {
        int pivot = a[r], i = l;
        for (int j = l; j < r; j++) {
            if (a[j] <= pivot) { swap(a, i, j); i++; }
        }
        swap(a, i, r);
        return i;
    }
    private void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}
```

## 题解二：通用解法（小顶堆维护前 K 大）
- 标签：数组、排序、堆、分治
- 思路：用大小为 `k` 的小顶堆维护当前最大的 `k` 个数；遍历时把新数入堆，若堆超过 `k` 则弹出堆顶（最小）。最终堆顶即答案。
- 复杂度：时间 O(n log k)，空间 O(k)。

```java
import java.util.*;
class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for (int x : nums) { pq.offer(x); if (pq.size() > k) pq.poll(); }
        return pq.peek();
    }
}
```

## 题解三：最好理解（排序取第 K 个）
- 直觉：直接排序降序后取第 `k` 个元素；实现最简单，但时间 O(n log n)。

```java
import java.util.*;
class Solution {
    public int findKthLargest(int[] nums, int k) {
        Arrays.sort(nums);
        return nums[nums.length - k];
    }
}
```

## 总结思路
- 快速选择均摊最优；小顶堆适合数据流或 `k` 远小于 `n`；排序最简单但非最优。

## 相关标签
- 数组、排序、堆、分治