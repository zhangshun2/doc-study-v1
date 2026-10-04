# LeetCode-647 回文子串

- 难度：中等
- 链接：https://leetcode.cn/problems/palindromic-substrings/

## 问题描述
返回字符串中回文子串的个数。子串须连续，且不同位置算不同子串。

## 题解一：官方经典（中心扩展）
- 思路：对每个可能的中心（`n` 个单中心 + `n-1` 个双中心），向两侧扩展，每次扩展成功计数加一。
- 复杂度：时间 O(n^2)，空间 O(1)。

```java
class Solution {
    public int countSubstrings(String s) {
        int n = s.length(), ans = 0;
        for (int center = 0; center < 2 * n - 1; center++) {
            int l = center / 2;
            int r = l + center % 2;
            while (l >= 0 && r < n && s.charAt(l) == s.charAt(r)) { ans++; l--; r++; }
        }
        return ans;
    }
}
```

## 题解二：通用解法（动态规划）
- 标签：字符串、中心扩展、动态规划
- 思路：`dp[i][j]` 表示 `s[i..j]` 是否为回文；从短到长填表，统计为 `true` 的个数。

```java
class Solution {
    public int countSubstrings(String s) {
        int n = s.length(), ans = 0;
        boolean[][] dp = new boolean[n][n];
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s.charAt(i) == s.charAt(j) && (j - i < 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true; ans++;
                }
            }
        }
        return ans;
    }
}
```

## 题解三：最好理解（“从中心向外数”）
- 直觉：每次从某个中心左右扩一格，能扩就说明新增一个回文子串，直到扩不动为止。

## 总结思路
- 中心扩展写法更简洁；DP有助于理解子结构关系。

## 相关标签
- 字符串、中心扩展、动态规划