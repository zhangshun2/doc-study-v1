# LeetCode-3 无重复字符的最长子串

- 难度：中等
- 链接：https://leetcode.cn/problems/longest-substring-without-repeating-characters/

## 问题描述
给定字符串 `s`，找出不包含重复字符的最长子串的长度。

## 题解一：官方经典（滑动窗口 + 哈希索引）
- 思路：维护左边界 `left`，用哈希记录字符最近出现位置，当发现重复时将 `left` 跳到该字符上次位置的下一位；每次更新最大长度。
- 复杂度：时间 O(n)，空间 O(Σ字符种类)。

```java
import java.util.*;
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> last = new HashMap<>();
        int ans = 0, left = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (last.containsKey(c)) left = Math.max(left, last.get(c) + 1);
            last.put(c, i);
            ans = Math.max(ans, i - left + 1);
        }
        return ans;
    }
}
```

## 题解二：通用解法（滑动窗口 + Set 去重）
- 标签：字符串、滑动窗口、哈希、双指针
- 思路：右指针尝试加入字符，若重复则左指针不断移出直到不重复；期间维护窗口长度。

```java
import java.util.*;
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> set = new HashSet<>();
        int ans = 0, l = 0;
        for (int r = 0; r < s.length(); r++) {
            char c = s.charAt(r);
            while (set.contains(c)) {
                set.remove(s.charAt(l++));
            }
            set.add(c);
            ans = Math.max(ans, r - l + 1);
        }
        return ans;
    }
}
```

## 题解三：最好理解（记录上次位置，窗口左边界只增不减）
- 直觉：每次遇到重复字符，将左边界跳到“那个字符上次出现位置 + 1”，窗口不会后退，只会前进。

## 总结思路
- 两种滑动窗口写法本质一致；哈希索引写法更简洁，避免多次左移。

## 相关标签
- 字符串、滑动窗口、哈希、双指针