---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/双指针/最短无序连续子数组/微模板与易错点卡片.md)
  - [模板索引：边界双指针](../学习方法/模板索引.md#排序或边界双指针)
---
# LeetCode-581 最短无序连续子数组

- 难度：中等
- 链接：https://leetcode.cn/problems/shortest-unsorted-continuous-subarray/

## 问题描述
给定一个整数数组，你需要找出一个连续子数组，使得只要对这个子数组进行升序排序，整个数组就变为升序。返回该子数组的最短长度。

## 题解一：官方经典（单调栈确定左右边界）
- 思路：从左到右用递增栈找第一个破坏递增的位置作为左边界，从右到左用递减栈找第一个破坏递减的位置作为右边界；综合得到区间。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int findUnsortedSubarray(int[] nums) {
        int n = nums.length;
        int left = n, right = -1;
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && nums[st.peek()] > nums[i]) { left = Math.min(left, st.pop()); }
            st.push(i);
        }
        st.clear();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && nums[st.peek()] < nums[i]) { right = Math.max(right, st.pop()); }
            st.push(i);
        }
        return right == -1 ? 0 : right - left + 1;
    }
}
```

## 题解二：通用解法（线性扫描跟踪最大最小）
- 标签：数组、栈、双指针
- 思路：正向扫描维护 `maxSeen`，凡是 `nums[i] < maxSeen` 就说明右边界应更新到 `i`；反向扫描维护 `minSeen`，凡是 `nums[i] > minSeen` 就说明左边界应更新到 `i`。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int findUnsortedSubarray(int[] nums) {
        int n = nums.length;
        int left = n, right = -1;
        int maxSeen = Integer.MIN_VALUE, minSeen = Integer.MAX_VALUE;
        for (int i = 0; i < n; i++) {
            if (nums[i] < maxSeen) right = i; else maxSeen = Math.max(maxSeen, nums[i]);
        }
        for (int i = n - 1; i >= 0; i--) {
            if (nums[i] > minSeen) left = i; else minSeen = Math.min(minSeen, nums[i]);
        }
        return right == -1 ? 0 : right - left + 1;
    }
}
```

## 题解三：最好理解（“找出被破坏的范围”）
- 直觉：从左看哪里开始“比前面更小”，从右看哪里开始“比后面更大”，这两处夹住的区间就是需要排序的范围。

## 总结思路
- 单调栈和线性扫描都能精准锁定边界；线性扫描更省空间。

## 相关标签
- 数组、栈、双指针