# LeetCode-438 找到字符串中所有字母异位词

- 难度：中等
- 链接：https://leetcode.cn/problems/find-all-anagrams-in-a-string/

## 问题描述
给定两个字符串 `s` 和 `p`，在 `s` 中找出所有 `p` 的字母异位词的起始索引。返回按升序排列的结果列表。

## 题解一：官方经典（滑动窗口 + 频次数组）
- 思路：维护长度为 `len(p)` 的窗口，使用两个长度为 26 的数组记录 `p` 的频次 `need` 与窗口内频次 `win`；每次移动窗口更新 `win`，当两者相等时记录左端点。
- 复杂度：时间 O(n + Σ)，空间 O(Σ)，其中 Σ 为字符集大小（26）。

```java
import java.util.*;
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        int n = s.length(), m = p.length();
        if (n < m) return res;
        int[] need = new int[26], win = new int[26];
        for (int i = 0; i < m; i++) need[p.charAt(i) - 'a']++;
        for (int i = 0; i < n; i++) {
            win[s.charAt(i) - 'a']++;
            if (i >= m) win[s.charAt(i - m) - 'a']--;
            if (i >= m - 1 && Arrays.equals(need, win)) res.add(i - m + 1);
        }
        return res;
    }
}
```

## 题解二：通用解法（滑动窗口 + 匹配计数）
- 标签：字符串、滑动窗口、哈希、计数
- 思路：用 `need[26]` 记录目标频次，同时维护“已匹配种类数” `formed`；窗口右移更新计数，若某字母计数恰好匹配则 `formed++`，左移时若失配则 `formed--`；当 `formed == required` 且窗口大小为 `m` 时记录左端点。

```java
import java.util.*;
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        int n = s.length(), m = p.length();
        if (n < m) return res;
        int[] need = new int[26], win = new int[26];
        int required = 0, formed = 0;
        for (char c : p.toCharArray()) {
            if (need[c - 'a'] == 0) required++;
            need[c - 'a']++;
        }
        int l = 0;
        for (int r = 0; r < n; r++) {
            int cr = s.charAt(r) - 'a';
            win[cr]++;
            if (need[cr] > 0 && win[cr] == need[cr]) formed++;
            while (r - l + 1 > m) {
                int cl = s.charAt(l++) - 'a';
                if (need[cl] > 0 && win[cl] == need[cl]) formed--;
                win[cl]--;
            }
            if (r - l + 1 == m && formed == required) res.add(l);
        }
        return res;
    }
}
```

## 题解三：最好理解（“固定长度的字母计数对比”）
- 直觉：异位词就是字母频次相同，用一个固定长度窗口逐步滑动，每次对比频次数组是否一致，相同则记录。

## 总结思路
- 频次数组比哈希更快；匹配计数写法避免整数组对比，适用于更大字符集。

## 相关标签
- 字符串、滑动窗口、哈希、计数