---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/排序/前K个高频元素/微模板与易错点卡片.md)
  - [模板索引：桶/堆/哈希](../学习方法/模板索引.md#桶堆哈希组合模板)
---
# LeetCode-347 前 K 个高频元素

- 难度：中等
- 链接：https://leetcode.cn/problems/top-k-frequent-elements/

## 问题描述
给定非空整数数组，返回出现频率最高的 `k` 个元素。要求时间尽可能优。

## 题解一：官方经典（桶排序按频次分组）
- 思路：先用哈希统计频次，再按频次构建大小为 `n+1` 的桶（每个桶存该频次的所有元素），从高频到低频收集前 `k` 个。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int x : nums) cnt.put(x, cnt.getOrDefault(x, 0) + 1);
        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i <= nums.length; i++) buckets.add(new ArrayList<>());
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            buckets.get(e.getValue()).add(e.getKey());
        }
        int[] ans = new int[k]; int idx = 0;
        for (int f = buckets.size() - 1; f >= 0 && idx < k; f--) {
            for (int x : buckets.get(f)) { ans[idx++] = x; if (idx == k) break; }
        }
        return ans;
    }
}
```

## 题解二：通用解法（小顶堆保留前 K）
- 标签：数组、哈希、堆、桶排序
- 思路：哈希统计后，用小顶堆存 `(元素,频次)`，当堆大小超过 `k` 时弹出最小频次；最后输出堆内元素。

```java
import java.util.*;
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int x : nums) cnt.put(x, cnt.getOrDefault(x, 0) + 1);
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            pq.offer(new int[]{e.getKey(), e.getValue()});
            if (pq.size() > k) pq.poll();
        }
        int[] ans = new int[k]; int i = 0;
        while (!pq.isEmpty()) ans[i++] = pq.poll()[0];
        return ans;
    }
}
```

## 题解三：最好理解（“按频次分桶或用堆”）
- 直觉：高频靠前，可用“频次桶”一次性分组；或用“小顶堆”动态维护前 `k` 个高频。

## 总结思路
- 桶排序适合离散频次且 `n` 不小；小顶堆适合在线或内存受限场景。

## 相关标签
- 数组、哈希、堆、桶排序