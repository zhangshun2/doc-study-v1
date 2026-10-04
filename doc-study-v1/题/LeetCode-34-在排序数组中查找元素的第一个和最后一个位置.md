---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/二分查找/在排序数组中查找元素的第一个和最后一个位置/微模板与易错点卡片.md)
  - [模板索引：上下界二分](../学习方法/模板索引.md#上下界二分模板)
---
# LeetCode-34 在排序数组中查找元素的第一个和最后一个位置

- 难度：中等
- 链接：https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/

## 问题描述
在排序数组中查找给定值 `target` 的起始和结束位置；若不存在则返回 `[-1, -1]`。要求时间 O(log n)。

## 题解一：官方经典（两次二分找左右边界）
- 思路：一次二分找左边界（第一个 >= target 的位置），一次二分找右边界（最后一个 <= target 的位置）；结合校验是否命中。
- 复杂度：时间 O(log n)，空间 O(1)。

```java
class Solution {
    public int[] searchRange(int[] nums, int target) {
        int left = lowerBound(nums, target);
        if (left == nums.length || nums[left] != target) return new int[]{-1, -1};
        int right = upperBound(nums, target) - 1;
        return new int[]{left, right};
    }
    private int lowerBound(int[] a, int x) {
        int l = 0, r = a.length; // [l, r)
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (a[mid] >= x) r = mid; else l = mid + 1;
        }
        return l;
    }
    private int upperBound(int[] a, int x) {
        int l = 0, r = a.length; // [l, r)
        while (l < r) {
            int mid = (l + r) >>> 1;
            if (a[mid] > x) r = mid; else l = mid + 1;
        }
        return l;
    }
}
```

## 题解二：通用解法（一次二分后线性扩展，不推荐）
- 标签：数组、二分查找
- 思路：先普通二分找到任意一个命中位置，再向两边线性扩展找到边界；最坏 O(n) 不满足要求，仅作理解参考。

## 题解三：最好理解（“左右边界即lower/upper bound”）
- 直觉：排序数组里，左边界是第一个不小于目标的位置，右边界是第一个大于目标的位置减一，直接用两次二分即可。

## 总结思路
- `lower_bound` 与 `upper_bound` 模板要熟练掌握；边界等式与不等式条件要小心。

## 相关标签
- 数组、二分查找