---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/二分查找/搜索旋转排序数组/微模板与易错点卡片.md)
  - [模板索引：旋转数组二分](../学习方法/模板索引.md#旋转数组二分模板)
---
# LeetCode-33 搜索旋转排序数组

- 难度：中等
- 链接：https://leetcode.cn/problems/search-in-rotated-sorted-array/

## 问题描述
给定在某未知点旋转过的升序数组（不含重复），并给定目标值 `target`，返回其索引；若不存在返回 -1。要求时间 O(log n)。

## 题解一：官方经典（二分查找定位有序半边）
- 思路：标准二分，每次判断 `nums[l..mid]` 是否有序；若有序再判断 `target` 是否落入该半边范围，否则去另一半；反之亦然。
- 复杂度：时间 O(log n)，空间 O(1)。

```java
class Solution {
    public int search(int[] nums, int target) {
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = (l + r) >>> 1;
            if (nums[mid] == target) return mid;
            if (nums[l] <= nums[mid]) { // 左边有序
                if (nums[l] <= target && target < nums[mid]) r = mid - 1; else l = mid + 1;
            } else { // 右边有序
                if (nums[mid] < target && target <= nums[r]) l = mid + 1; else r = mid - 1;
            }
        }
        return -1;
    }
}
```

## 题解二：通用解法（找到最小值再普通二分）
- 标签：数组、二分查找
- 思路：先二分找到旋转点（最小值索引），然后在两段各自做一次普通二分；实现相对直观但通常比一遍法略慢。

```java
class Solution {
    public int search(int[] nums, int target) {
        int pivot = findMinIndex(nums);
        int res = binSearch(nums, 0, pivot - 1, target);
        return res != -1 ? res : binSearch(nums, pivot, nums.length - 1, target);
    }
    private int findMinIndex(int[] a) {
        int l = 0, r = a.length - 1;
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (a[mid] > a[r]) l = mid + 1; else r = mid;
        }
        return l;
    }
    private int binSearch(int[] a, int l, int r, int x) {
        while (l <= r) {
            int mid = (l + r) >>> 1;
            if (a[mid] == x) return mid;
            if (a[mid] < x) l = mid + 1; else r = mid - 1;
        }
        return -1;
    }
}
```

## 题解三：最好理解（“每次选有序的那半边”）
- 直觉：旋转后数组仍由两段有序片段组成；二分时优先处理有序片段，并且判断目标是否在该片段内。

## 总结思路
- 一遍法更高效也更常用；分段法更直观，适合理解问题结构。

## 相关标签
- 数组、二分查找