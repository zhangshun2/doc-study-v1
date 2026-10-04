# LeetCode-169 多数元素

- 难度：简单
- 链接：https://leetcode.cn/problems/majority-element/

## 问题描述
给定大小为 `n` 的数组，返回其中的多数元素（出现次数大于 `n/2` 的元素）。保证多数元素一定存在。

## 题解一：官方经典（Boyer-Moore 投票算法）
- 思路：维护候选人 `cand` 和计数 `cnt`；遍历时相同元素计数+1，不同计数-1，当计数为 0 更换候选人。最终 `cand` 即多数元素。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int majorityElement(int[] nums) {
        int cand = 0, cnt = 0;
        for (int x : nums) {
            if (cnt == 0) { cand = x; cnt = 1; }
            else if (x == cand) cnt++;
            else cnt--;
        }
        return cand;
    }
}
```

## 题解二：通用解法（哈希计数）
- 标签：数组、哈希、贪心
- 思路：用哈希表统计频次，返回最大频次的元素；实现简单但空间 O(n)。

```java
import java.util.*;
class Solution {
    public int majorityElement(int[] nums) {
        Map<Integer, Integer> cnt = new HashMap<>();
        int cand = 0, best = 0;
        for (int x : nums) {
            int c = cnt.getOrDefault(x, 0) + 1;
            cnt.put(x, c);
            if (c > best) { best = c; cand = x; }
        }
        return cand;
    }
}
```

## 题解三：最好理解（“多的盖过少的”）
- 直觉：用投票思想让多数元素抵消掉其他元素，剩下的一定是多数元素。

## 总结思路
- 投票算法是本题模板；哈希更直观但占空间。

## 相关标签
- 数组、哈希、贪心