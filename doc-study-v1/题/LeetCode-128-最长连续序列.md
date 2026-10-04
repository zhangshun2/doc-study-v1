---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/哈希表/最长连续序列/微模板与易错点卡片.md)
  - [模板索引：哈希集合](../学习方法/模板索引.md#数组哈希映射分组集合)
---
# LeetCode-128 最长连续序列

- 难度：中等
- 链接：https://leetcode.cn/problems/longest-consecutive-sequence/

## 问题描述
给定未排序的整数数组 `nums`，找出最长连续序列的长度。要求时间复杂度为 O(n)。

## 题解一：官方经典（哈希集合 + 只从序列起点扩展）
- 思路：用哈希集合存所有数；对每个数 `x`，仅当 `x-1` 不在集合中才作为序列起点，向右扩展计数，更新最长长度。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int ans = 0;
        for (int x : set) {
            if (!set.contains(x - 1)) {
                int y = x;
                while (set.contains(y)) y++;
                ans = Math.max(ans, y - x);
            }
        }
        return ans;
    }
}
```

## 题解二：通用解法（排序后线性扫描）
- 标签：数组、哈希、排序
- 思路：排序后跳过重复，线性扫描维护当前连续段长度与最大值。
- 复杂度：时间 O(n log n)，空间 O(1) 或 O(n)。

```java
import java.util.*;
class Solution {
    public int longestConsecutive(int[] nums) {
        if (nums.length == 0) return 0;
        Arrays.sort(nums);
        int ans = 1, cur = 1;
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) continue;
            if (nums[i] == nums[i - 1] + 1) cur++;
            else { ans = Math.max(ans, cur); cur = 1; }
        }
        return Math.max(ans, cur);
    }
}
```

## 题解三：最好理解（“只从起点往右数”）
- 直觉：为避免重复扩展，只在一个连续段的最左端起点处开始数，这样每个数只被数一次。

## 总结思路
- 哈希起点扩展最符合 O(n) 要求；排序适用于不强调时间极限或内存受限场景。

## 相关标签
- 数组、哈希、排序