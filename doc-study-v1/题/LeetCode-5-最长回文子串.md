# LeetCode-5 最长回文子串

- 难度：中等
- 链接：https://leetcode.cn/problems/longest-palindromic-substring/

## 问题描述
给定字符串 `s`，返回其最长回文子串。

## 题解一：官方经典（中心扩展）
- 思路：枚举每个中心（单字符中心与双字符中心），向两侧扩展，更新最长长度与起点。
- 复杂度：时间 O(n^2)，空间 O(1)。

```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length(); if (n < 2) return s;
        int start = 0, maxLen = 1;
        for (int i = 0; i < n; i++) {
            int len1 = expand(s, i, i);
            int len2 = expand(s, i, i + 1);
            int len = Math.max(len1, len2);
            if (len > maxLen) {
                maxLen = len;
                start = i - (len - 1) / 2;
            }
        }
        return s.substring(start, start + maxLen);
    }
    private int expand(String s, int l, int r) {
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
        return r - l - 1;
    }
}
```

## 题解二：通用解法（动态规划）
- 标签：字符串、中心扩展、动态规划
- 思路：`dp[i][j]` 表示 `s[i..j]` 是否为回文；转移：两端字符相等且内部为回文。

```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length(); if (n < 2) return s;
        boolean[][] dp = new boolean[n][n];
        int start = 0, maxLen = 1;
        for (int i = 0; i < n; i++) dp[i][i] = true;
        for (int len = 2; len <= n; len++) {
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                if (s.charAt(i) == s.charAt(j)) {
                    dp[i][j] = (len == 2) || dp[i + 1][j - 1];
                    if (dp[i][j] && len > maxLen) { maxLen = len; start = i; }
                }
            }
        }
        return s.substring(start, start + maxLen);
    }
}
```

## 题解三：最好理解（“定中心，往两边扩”）
- 直觉：回文以中心对称，定中心后向两边比对相等就扩大边界，直到不相等为止。

## 总结思路
- 中心扩展更实用；DP有助于理解结构，但空间较大。

## 相关标签
- 字符串、中心扩展、动态规划