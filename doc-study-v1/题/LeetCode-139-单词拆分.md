# LeetCode-139 单词拆分

- 难度：中等
- 链接：https://leetcode.cn/problems/word-break/

## 问题描述
给定字符串 `s` 和字符串字典 `wordDict`，判断 `s` 是否能被空格拆分成由字典中单词组成的字符串。

## 题解一：官方经典（一维DP + 最大词长剪枝）
- 思路：`dp[i]` 表示 `s[0..i)` 是否可拆分。若存在 `j<i` 且 `dp[j]` 为真且 `s[j..i)` 在字典中，则 `dp[i]=true`。
- 优化：预计算字典最大词长，只枚举 `l<=maxLen` 的长度。
- 复杂度：时间 O(n·maxLen)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> dict = new HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        int maxLen = 0; for (String w : dict) maxLen = Math.max(maxLen, w.length());
        for (int i = 1; i <= n; i++) {
            for (int l = 1; l <= maxLen && l <= i; l++) {
                if (!dp[i - l]) continue;
                if (dict.contains(s.substring(i - l, i))) { dp[i] = true; break; }
            }
        }
        return dp[n];
    }
}
```

## 题解二：通用解法（BFS 或字典树剪枝）
- 标签：动态规划、字典树、BFS
- 思路：从起点做 BFS，能访问到末尾即成功；配合字典树可在长串场景下提升匹配效率。

## 总结思路
- 一维 DP 是主流解；根据数据规模可考虑 BFS/Trie 做性能优化。

## 相关标签
- 动态规划、哈希、字典树