# LeetCode-85 最大矩形

- 难度：困难
- 链接：https://leetcode.cn/problems/maximal-rectangle/

## 问题描述
给定二进制矩阵，返回只包含 1 的最大矩形面积。

## 题解一：官方经典（逐行当柱状图 + 84题）
- 思路：逐行维护高度数组 `heights[j]`，每行调用“柱状图最大矩形”算法求最大面积。
- 复杂度：时间 O(m*n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0) return 0;
        int m = matrix.length, n = matrix[0].length, ans = 0;
        int[] h = new int[n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) h[j] = matrix[i][j] == '1' ? h[j] + 1 : 0;
            ans = Math.max(ans, largest(h));
        }
        return ans;
    }
    private int largest(int[] heights) {
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

## 题解二：通用解法（DP 左右边界）
- 标签：单调栈、DP、矩阵
- 思路：记录连续高度 `H`、左边界 `L` 和右边界 `R`，每行更新 `面积 = H[j] * (R[j] - L[j])`。

```java
class Solution {
    public int maximalRectangle(char[][] a) {
        if (a.length == 0) return 0;
        int m = a.length, n = a[0].length, ans = 0;
        int[] H = new int[n], L = new int[n], R = new int[n];
        Arrays.fill(R, n);
        for (int i = 0; i < m; i++) {
            int curL = 0, curR = n;
            for (int j = 0; j < n; j++) {
                if (a[i][j] == '1') { H[j]++; L[j] = Math.max(L[j], curL); }
                else { H[j] = 0; L[j] = 0; curL = j + 1; }
            }
            for (int j = n - 1; j >= 0; j--) {
                if (a[i][j] == '1') { R[j] = Math.min(R[j], curR); }
                else { R[j] = n; curR = j; }
            }
            for (int j = 0; j < n; j++) ans = Math.max(ans, H[j] * (R[j] - L[j]));
        }
        return ans;
    }
}
```

## 题解三：最好理解（行转柱状图）
- 直觉：每一行都把上面的连续 1 累积成高度，再用 84 题的解决方案求该行的最大面积，取最大即可。

## 总结思路
- 84 的复用是常见套路；DP 左右边界在一些场景更快。

## 相关标签
- 单调栈、DP、矩阵