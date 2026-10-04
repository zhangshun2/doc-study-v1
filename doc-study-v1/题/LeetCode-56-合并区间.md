# LeetCode-56 合并区间

- 难度：中等
- 链接：https://leetcode.cn/problems/merge-intervals/

## 问题描述
给定由区间组成的数组，将所有重叠的区间合并，返回不重叠的区间集合。

## 题解一：官方经典（排序 + 线性合并）
- 思路：按区间起点升序排序；遍历时如果当前区间与答案最后一个区间重叠（`cur.start <= last.end`），则合并更新 `last.end = max(last.end, cur.end)`；否则直接加入答案。
- 复杂度：时间 O(n log n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a,b) -> a[0]==b[0]?a[1]-b[1]:a[0]-b[0]);
        List<int[]> res = new ArrayList<>();
        for (int[] it : intervals) {
            if (res.isEmpty() || res.get(res.size()-1)[1] < it[0]) res.add(new int[]{it[0], it[1]});
            else res.get(res.size()-1)[1] = Math.max(res.get(res.size()-1)[1], it[1]);
        }
        return res.toArray(new int[res.size()][]);
    }
}
```

## 题解二：通用解法（扫描线思想）
- 标签：数组、排序、贪心
- 思路：将每个区间拆成事件（进入+1，离开-1），按位置排序扫描计数，计数从 0→1 是新段起点，从 1→0 是段结束；适合统计覆盖次数，但合并实现略重。

## 题解三：最好理解（“把重叠的粘在一起”）
- 直觉：排序后，能接上的就把区间右端延长；不能接就开一个新区间。

## 总结思路
- 排序+合并是标准模板；扫描线用于更复杂的区间计数问题。

## 相关标签
- 数组、排序、贪心