# LeetCode-84 柱状图中最大的矩形

- 难度：困难
- 链接：https://leetcode.cn/problems/largest-rectangle-in-histogram/

## 问题描述
给定柱状图数组 `heights`，返回能形成的最大矩形面积。

## 题解一：官方经典（单调栈 + 哨兵）
- 思路：维护递增高度的栈，遇到更小高度时弹出，计算以弹出高度为最矮的最大宽度；在数组首尾加哨兵简化边界。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length; int[] h = new int[n + 2];
        System.arraycopy(heights, 0, h, 1, n);
        Deque<Integer> st = new ArrayDeque<>(); st.push(0);
        int ans = 0;
        for (int i = 1; i < h.length; i++) {
            while (h[i] < h[st.peek()]) {
                int mid = st.pop();
                int w = i - st.peek() - 1;
                ans = Math.max(ans, h[mid] * w);
            }
            st.push(i);
        }
        return ans;
    }
}
```

## 题解二：通用解法（前后更小元素）
- 标签：单调栈、数组
- 思路：预处理每个位置左侧第一个更小和右侧第一个更小的下标，面积为 `heights[i] * (right[i] - left[i] - 1)`。

```java
import java.util.*;
class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length; int[] L = new int[n], R = new int[n];
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && heights[st.peek()] >= heights[i]) st.pop();
            L[i] = st.isEmpty() ? -1 : st.peek();
            st.push(i);
        }
        st.clear();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && heights[st.peek()] >= heights[i]) st.pop();
            R[i] = st.isEmpty() ? n : st.peek();
            st.push(i);
        }
        int ans = 0;
        for (int i = 0; i < n; i++) ans = Math.max(ans, heights[i] * (R[i] - L[i] - 1));
        return ans;
    }
}
```

## 题解三：最好理解（“以我为最矮”）
- 直觉：对每个`i`，向左右扩展直到遇到更矮柱子，这段宽度乘以高度就是以 `i` 为最矮的最大矩形。

## 总结思路
- 栈解更高效也更通用；前后更小的预处理便于理解边界。

## 相关标签
- 单调栈、数组、哨兵