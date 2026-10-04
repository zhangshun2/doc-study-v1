# LeetCode-739 每日温度

- 难度：中等
- 链接：https://leetcode.cn/problems/daily-temperatures/

## 问题描述
给定每日温度数组 `T`，返回数组 `ans`：`ans[i]` 为第 `i` 天之后更高温度出现的等待天数；若不存在则为 0。

## 题解一：官方经典（单调栈：存下标）
- 思路：维护递减栈（按温度），遇到更高温度就弹出并计算距离；把当前下标压栈。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[] dailyTemperatures(int[] T) {
        int n = T.length; int[] ans = new int[n];
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && T[i] > T[st.peek()]) {
                int j = st.pop(); ans[j] = i - j;
            }
            st.push(i);
        }
        return ans;
    }
}
```

## 题解二：通用解法（倒序跳跃）
- 标签：单调栈、倒序、next 跳跃
- 思路：从后往前，如果后一天温度不高就跳到它的答案指向的更远位置，像“next 数组”加速。

```java
class Solution {
    public int[] dailyTemperatures(int[] T) {
        int n = T.length; int[] ans = new int[n];
        for (int i = n - 2; i >= 0; i--) {
            int j = i + 1;
            while (j < n && T[j] <= T[i]) {
                if (ans[j] == 0) { j = n; break; }
                j = j + ans[j];
            }
            ans[i] = j < n ? j - i : 0;
        }
        return ans;
    }
}
```

## 题解三：最好理解（更高温度“下一次”）
- 直觉：对每一天，找下一个更高温度的下标；栈法是线性求“下一个更大元素”。

## 总结思路
- 单调栈是模板；倒序跳跃能减少比较次数但实现要注意越界。

## 相关标签
- 单调栈、数组、Next Greater Element