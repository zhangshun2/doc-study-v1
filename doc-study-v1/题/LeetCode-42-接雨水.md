# LeetCode-42 接雨水

- 难度：困难
- 链接：https://leetcode.cn/problems/trapping-rain-water/

## 问题描述
给定非负整数数组表示柱状图的高度，计算能接的雨水总量。

## 题解一：官方经典（单调栈）
- 思路：维护递减栈，遇到“右边界”时弹出中间低谷，根据左右边界高度计算当前可接水量。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int trap(int[] height) {
        int ans = 0; Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < height.length; i++) {
            while (!st.isEmpty() && height[i] > height[st.peek()]) {
                int mid = st.pop();
                if (st.isEmpty()) break;
                int left = st.peek();
                int h = Math.min(height[left], height[i]) - height[mid];
                int w = i - left - 1;
                ans += h * w;
            }
            st.push(i);
        }
        return ans;
    }
}
```

## 题解二：通用解法（双指针）
- 标签：单调栈、双指针、前缀后缀
- 思路：维护 `leftMax` 和 `rightMax`，谁小就决定该侧的水量并移动指针。

```java
class Solution {
    public int trap(int[] height) {
        int l = 0, r = height.length - 1, ans = 0;
        int leftMax = 0, rightMax = 0;
        while (l < r) {
            leftMax = Math.max(leftMax, height[l]);
            rightMax = Math.max(rightMax, height[r]);
            if (leftMax < rightMax) {
                ans += leftMax - height[l]; l++;
            } else {
                ans += rightMax - height[r]; r--;
            }
        }
        return ans;
    }
}
```

## 题解三：最好理解（前后最大）
- 直觉：每个位置的水量由其左侧最高和右侧最高决定，水高为两者最小值减当前位置高度。

```java
class Solution {
    public int trap(int[] height) {
        int n = height.length;
        int[] L = new int[n], R = new int[n];
        for (int i = 1; i < n; i++) L[i] = Math.max(L[i - 1], height[i - 1]);
        for (int i = n - 2; i >= 0; i--) R[i] = Math.max(R[i + 1], height[i + 1]);
        int ans = 0;
        for (int i = 0; i < n; i++) ans += Math.max(0, Math.min(L[i], R[i]) - height[i]);
        return ans;
    }
}
```

## 总结思路
- 栈与双指针均为高频模板；前后最大法适合入门理解。

## 相关标签
- 单调栈、双指针、前缀后缀