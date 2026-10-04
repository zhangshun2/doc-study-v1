# LeetCode-76 最小覆盖子串

- 难度：困难
- 链接：https://leetcode.cn/problems/minimum-window-substring/

## 问题描述
给定字符串 `s` 和 `t`，返回 `s` 中包含 `t` 所有字符的最小子串；若不存在返回空串。

## 题解一：官方经典（滑动窗口 + 计数）
- 思路：窗口右扩满足需求后左缩到刚好不满足为止，过程中记录最短区间；用数组或哈希表维护需求与窗口内计数。
- 复杂度：时间 O(n)，空间 O(Σ字符种类)。

```java
class Solution {
    public String minWindow(String s, String t) {
        if (t.length() == 0 || s.length() < t.length()) return "";
        int[] need = new int[128];
        for (char c : t.toCharArray()) need[c]++;
        int required = 0; for (int i = 0; i < 128; i++) if (need[i] > 0) required++;
        int[] have = new int[128];
        int formed = 0, l = 0, r = 0, bestL = 0, bestLen = Integer.MAX_VALUE;
        while (r < s.length()) {
            char c = s.charAt(r++);
            have[c]++; if (need[c] > 0 && have[c] == need[c]) formed++;
            while (formed == required) {
                if (r - l < bestLen) { bestLen = r - l; bestL = l; }
                char d = s.charAt(l++);
                if (need[d] > 0 && have[d] == need[d]) formed--; have[d]--;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
    }
}
```

## 题解二：通用解法（哈希表 + 统计已满足字符种类）
- 标签：字符串、滑动窗口、哈希
- 思路：用 `Map<Character,Integer>` 维护需求与窗口计数，实时统计已满足的字符种类数来判断是否可收缩。

```java
import java.util.*;
class Solution {
    public String minWindow(String s, String t) {
        Map<Character, Integer> need = new HashMap<>();
        for (char c : t.toCharArray()) need.put(c, need.getOrDefault(c, 0) + 1);
        Map<Character, Integer> have = new HashMap<>();
        int formed = 0, required = need.size();
        int l = 0, r = 0, bestL = 0, bestLen = Integer.MAX_VALUE;
        while (r < s.length()) {
            char c = s.charAt(r++);
            have.put(c, have.getOrDefault(c, 0) + 1);
            if (need.containsKey(c) && have.get(c).intValue() == need.get(c).intValue()) formed++;
            while (formed == required) {
                if (r - l < bestLen) { bestLen = r - l; bestL = l; }
                char d = s.charAt(l++);
                have.put(d, have.get(d) - 1);
                if (need.containsKey(d) && have.get(d) < need.get(d)) formed--;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
    }
}
```

## 题解三：最好理解（“先满足，再尽量缩短”）
- 直觉：右指针不断加入字符直到涵盖 `t` 所有需求，然后移动左指针剔除多余字符保持刚好满足，这段就是候选最短串。

## 总结思路
- 数组更快；哈希更通用（支持多字符集）。关键在于“满足-收缩”的节奏控制。

## 相关标签
- 字符串、滑动窗口、哈希