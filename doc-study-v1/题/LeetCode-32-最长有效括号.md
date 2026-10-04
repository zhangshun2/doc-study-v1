# LeetCode-32 最长有效括号

- 难度：困难
- 链接：https://leetcode.cn/problems/longest-valid-parentheses/

## 问题描述
给定只包含 `(` 和 `)` 的字符串，返回最长有效括号子串的长度。

## 题解一：官方经典（栈下标 + 基准 -1）
- 思路：栈保存“可能成为合法起点的下标”，遇到 `)` 弹栈；若栈空则把当前下标作为新基准，否则用 `i - 栈顶` 更新最大长度。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int longestValidParentheses(String s) {
        Deque<Integer> st = new ArrayDeque<>();
        st.push(-1);
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') st.push(i);
            else {
                st.pop();
                if (st.isEmpty()) st.push(i);
                else ans = Math.max(ans, i - st.peek());
            }
        }
        return ans;
    }
}
```

## 题解二：通用解法（动态规划）
- 标签：栈、DP、双指针
- 思路：`dp[i]` 表示以 `i` 结尾的最长合法长度；若 `s[i] == ')'`，分两种情况：`...()` 或 `...))`。

```java
class Solution {
    public int longestValidParentheses(String s) {
        int n = s.length(), ans = 0; int[] dp = new int[n];
        for (int i = 1; i < n; i++) {
            if (s.charAt(i) == ')') {
                if (s.charAt(i - 1) == '(') {
                    dp[i] = (i >= 2 ? dp[i - 2] : 0) + 2;
                } else {
                    int j = i - 1 - dp[i - 1];
                    if (j >= 0 && s.charAt(j) == '(') {
                        dp[i] = dp[i - 1] + 2 + (j >= 1 ? dp[j - 1] : 0);
                    }
                }
                ans = Math.max(ans, dp[i]);
            }
        }
        return ans;
    }
}
```

## 题解三：最好理解（左右扫描计数）
- 直觉：从左到右统计 `cntL` 与 `cntR`，相等时更新答案；`cntR > cntL` 重置；为覆盖 `((()))` 等情况，再从右到左扫描。

```java
class Solution {
    public int longestValidParentheses(String s) {
        int ans = 0, cntL = 0, cntR = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') cntL++; else cntR++;
            if (cntL == cntR) ans = Math.max(ans, 2 * cntR);
            else if (cntR > cntL) { cntL = 0; cntR = 0; }
        }
        cntL = 0; cntR = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            if (s.charAt(i) == ')') cntR++; else cntL++;
            if (cntL == cntR) ans = Math.max(ans, 2 * cntL);
            else if (cntL > cntR) { cntL = 0; cntR = 0; }
        }
        return ans;
    }
}
```

## 总结思路
- 栈与 DP 都是经典模板；双向扫描是易理解的线性方法。

## 相关标签
- 栈、动态规划、双指针