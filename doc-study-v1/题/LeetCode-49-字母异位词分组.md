# LeetCode-49 字母异位词分组

- 难度：中等
- 链接：https://leetcode.cn/problems/group-anagrams/

## 问题描述
给定字符串数组，将字母异位词分到同一组，返回所有分组。

## 题解一：官方经典（排序作为键）
- 思路：将每个字符串排序得到规范化形式作为键，哈希分组。
- 复杂度：时间 O(n k log k)，空间 O(nk)。

```java
import java.util.*;
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            char[] c = s.toCharArray();
            Arrays.sort(c);
            String key = new String(c);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}
```

## 题解二：通用解法（计数签名）
- 标签：字符串、哈希、排序
- 思路：26位字母计数作为签名，比排序更快；将计数序列序列化为键。

```java
import java.util.*;
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            int[] cnt = new int[26];
            for (int i = 0; i < s.length(); i++) cnt[s.charAt(i) - 'a']++;
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 26; i++) sb.append('#').append(cnt[i]);
            String key = sb.toString();
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(map.values());
    }
}
```

## 题解三：最好理解（“同字母同频”即同组）
- 直觉：异位词本质是字母频次相同；用排序或频次签名统一映射即可分组。

## 总结思路
- 排序键易写；计数键更高效。根据字符串长度选择方案。

## 相关标签
- 字符串、哈希、排序