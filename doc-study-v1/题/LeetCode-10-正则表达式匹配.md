# LeetCode-10 正则表达式匹配

- 难度：困难
- 链接：https://leetcode.cn/problems/regular-expression-matching/

## 问题描述
实现支持 `.` 和 `*` 的正则匹配：`.` 匹配任意单字符，`*` 匹配前一个元素的零次或多次。

## 题解一：官方经典（二维DP）
- 思路：`dp[i][j]` 表示 `s[0..i)` 与 `p[0..j)` 是否匹配；关键在于 `*` 的两种选择：匹配零次或多次。
- 复杂度：时间 O(mn)，空间 O(mn)。

```java
class Solution {
    public boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;
        for (int j = 2; j <= n; j++) {
            if (p.charAt(j - 1) == '*') dp[0][j] = dp[0][j - 2];
        }
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char pc = p.charAt(j - 1);
                if (pc == '*') {
                    dp[i][j] = dp[i][j - 2] || ((p.charAt(j - 2) == '.' || p.charAt(j - 2) == s.charAt(i - 1)) && dp[i - 1][j]);
                } else {
                    dp[i][j] = (pc == '.' || pc == s.charAt(i - 1)) && dp[i - 1][j - 1];
                }
            }
        }
        return dp[m][n];
    }
}
```

## 题解二：通用解法（递归 + 记忆化）
- 标签：字符串、动态规划、递归
- 思路：递归考虑当前字符是否匹配，遇到 `*` 分支为“跳过”或“继续匹配一个”；用哈希记忆避免重复计算。

```java
import java.util.*;
class Solution {
    private Map<String, Boolean> memo = new HashMap<>();
    public boolean isMatch(String s, String p) { return dfs(0, 0, s, p); }
    private boolean dfs(int i, int j, String s, String p) {
        String key = i + "," + j;
        if (memo.containsKey(key)) return memo.get(key);
        boolean res;
        if (j == p.length()) res = (i == s.length());
        else {
            boolean first = (i < s.length()) && (p.charAt(j) == s.charAt(i) || p.charAt(j) == '.');
            if (j + 1 < p.length() && p.charAt(j + 1) == '*') {
                res = dfs(i, j + 2, s, p) || (first && dfs(i + 1, j, s, p));
            } else {
                res = first && dfs(i + 1, j + 1, s, p);
            }
        }
        memo.put(key, res); return res;
    }
}
```

## 题解三：最好理解（`*` 的两面性）
- 直觉：`*` 要么当作重复零次（跳过两个字符），要么重复多次（当前匹配一个并继续停留在 `*` 的位置）。

## 总结思路
- 二维DP是面试模板；递归更贴近模式匹配的自然思维。

## 相关标签
- 字符串、动态规划、递归