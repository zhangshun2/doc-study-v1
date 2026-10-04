# LeetCode-406 根据身高重建队列

- 难度：中等
- 链接：https://leetcode.cn/problems/queue-reconstruction-by-height/

## 问题描述
给出若干人的身高 `h` 和在队列中前面有 `k` 个身高不低于 `h` 的人，将队列还原。

## 题解一：官方经典（排序 + 按 k 插入）
- 思路：按身高从高到低、`k` 从小到大排序；高的先放，按 `k` 位置插入到结果列表，对更矮的人不影响其前方的“更高者数量”。
- 复杂度：时间 O(n^2)（链表插入均摊），空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[][] reconstructQueue(int[][] people) {
        Arrays.sort(people, (a,b) -> a[0]==b[0] ? a[1]-b[1] : b[0]-a[0]);
        List<int[]> res = new ArrayList<>();
        for (int[] p : people) res.add(p[1], p);
        return res.toArray(new int[res.size()][]);
    }
}
```

## 题解二：通用解法（树状结构/线段树定位）
- 标签：数组、排序、贪心、数据结构
- 思路：在空位数组上用线段树/树状数组查找第 `k` 个空位进行放置，整体 O(n log n)，实现复杂但更稳定。

## 题解三：最好理解（“高的先安排，按位置插入”）
- 直觉：高个子插入后不会被矮个子影响其前面更高者计数，因此先安排高的，再按 `k` 位置插入即可。

## 总结思路
- 排序+插入是常规解；如需更优复杂度可用线段树定位空位。

## 相关标签
- 数组、排序、贪心、数据结构