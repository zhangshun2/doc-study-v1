---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/双指针/颜色分类/微模板与易错点卡片.md)
  - [模板索引：荷兰旗三指针](../学习方法/模板索引.md#荷兰旗三指针模板)
---
# LeetCode-75 颜色分类

- 难度：中等
- 链接：https://leetcode.cn/problems/sort-colors/

## 问题描述
数组只包含 0、1、2 三种颜色，请原地对它们排序，使得相同颜色相邻，顺序为 0、1、2。

## 题解一：官方经典（荷兰国旗三路划分）
- 思路：维护 `p0` 指向下一个 0 应放置位置，`p2` 指向下一个 2 应放置位置，遍历指针 `i` 根据值交换到对应区域。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public void sortColors(int[] nums) {
        int p0 = 0, i = 0, p2 = nums.length - 1;
        while (i <= p2) {
            if (nums[i] == 0) { swap(nums, i, p0); p0++; i++; }
            else if (nums[i] == 2) { swap(nums, i, p2); p2--; }
            else i++;
        }
    }
    private void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}
```

## 题解二：通用解法（计数排序，两遍）
- 标签：数组、双指针、排序
- 思路：先计数三种颜色数量，再按顺序写回数组；代码简单但两遍。

```java
class Solution {
    public void sortColors(int[] nums) {
        int[] cnt = new int[3];
        for (int x : nums) cnt[x]++;
        int idx = 0;
        for (int c = 0; c < 3; c++) {
            for (int k = 0; k < cnt[c]; k++) nums[idx++] = c;
        }
    }
}
```

## 题解三：最好理解（“0放左，2放右，1留中间”）
- 直觉：遍历过程中把 0 往左塞、2 往右塞，剩下的自然是 1 在中间。

## 总结思路
- 三路划分原地且一遍；计数排序更易写但需要两遍和额外空间。

## 相关标签
- 数组、双指针、排序