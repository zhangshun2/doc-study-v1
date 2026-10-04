# LeetCode-621 任务调度器

- 难度：中等
- 链接：https://leetcode.cn/problems/task-scheduler/

## 问题描述
给定任务列表，每个任务用字母表示；相同任务之间需要至少 `n` 的冷却时间。求完成所有任务的最短时间单位数。

## 题解一：官方经典（贪心公式）
- 思路：设最高频次为 `maxF`，最高频任务数为 `cntMax`。最短时间为 `max(tasks.length, (maxF - 1) * (n + 1) + cntMax)`。
- 复杂度：时间 O(Σ字母)，空间 O(Σ字母)。

```java
class Solution {
    public int leastInterval(char[] tasks, int n) {
        int[] cnt = new int[26];
        for (char c : tasks) cnt[c - 'A']++;
        int maxF = 0; for (int x : cnt) maxF = Math.max(maxF, x);
        int cntMax = 0; for (int x : cnt) if (x == maxF) cntMax++;
        return Math.max(tasks.length, (maxF - 1) * (n + 1) + cntMax);
    }
}
```

## 题解二：通用解法（优先队列模拟）
- 标签：数组、贪心、队列、优先队列
- 思路：用大顶堆按剩余频次取任务，每轮取最多 `n+1` 个不同任务执行一次，频次减 1 后未清零的重新入堆；堆空则结束。

```java
import java.util.*;
class Solution {
    public int leastInterval(char[] tasks, int n) {
        int[] cnt = new int[26];
        for (char c : tasks) cnt[c - 'A']++;
        PriorityQueue<Integer> pq = new PriorityQueue<>((a,b) -> b - a);
        for (int x : cnt) if (x > 0) pq.offer(x);
        int time = 0;
        while (!pq.isEmpty()) {
            int k = n + 1;
            List<Integer> tmp = new ArrayList<>();
            while (k-- > 0 && !pq.isEmpty()) {
                int x = pq.poll();
                if (x - 1 > 0) tmp.add(x - 1);
                time++;
            }
            for (int x : tmp) pq.offer(x);
            if (!pq.isEmpty()) time += k + 1; // 补上本轮未满的空闲位
        }
        return time;
    }
}
```

## 题解三：最好理解（“把最高频任务当骨架填空”）
- 直觉：最高频任务之间必须插入 `n` 个空位，先搭好这些“骨架”，再放入其他任务填空；如果任务很多，空位不够则直接串行执行。

## 总结思路
- 公式法高效简洁；堆模拟有助于理解冷却过程。

## 相关标签
- 数组、贪心、队列、优先队列