# LeetCode-399 除法求值

- 难度：中等
- 链接：https://leetcode.cn/problems/evaluate-division/

## 问题描述
给定若干等式 `a/b = k`，以及若干查询 `x/y`，若能推导出结果则返回比值，否则返回 -1。

## 题解一：官方经典（图建模 + DFS/BFS）
- 思路：将变量作为图节点，`a->b` 边权为 `k`，同时建 `b->a` 边权为 `1/k`。对每次查询用 BFS/DFS 寻找路径并累计边权。
- 复杂度：单次查询 O(V+E) 最坏；总体取决于输入规模。

```java
import java.util.*;
class Solution {
    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        Map<String, Map<String, Double>> g = new HashMap<>();
        for (int i = 0; i < equations.size(); i++) {
            String a = equations.get(i).get(0), b = equations.get(i).get(1);
            double k = values[i];
            g.computeIfAbsent(a, x -> new HashMap<>()).put(b, k);
            g.computeIfAbsent(b, x -> new HashMap<>()).put(a, 1.0 / k);
        }
        double[] ans = new double[queries.size()];
        for (int qi = 0; qi < queries.size(); qi++) {
            String s = queries.get(qi).get(0), t = queries.get(qi).get(1);
            ans[qi] = bfs(s, t, g);
        }
        return ans;
    }
    private double bfs(String s, String t, Map<String, Map<String, Double>> g) {
        if (!g.containsKey(s) || !g.containsKey(t)) return -1.0;
        if (s.equals(t)) return 1.0;
        Deque<String> dq = new ArrayDeque<>(); dq.offer(s);
        Map<String, Double> dist = new HashMap<>(); dist.put(s, 1.0);
        while (!dq.isEmpty()) {
            String u = dq.poll();
            double cur = dist.get(u);
            for (Map.Entry<String, Double> e : g.get(u).entrySet()) {
                String v = e.getKey(); double w = e.getValue();
                if (!dist.containsKey(v)) {
                    dist.put(v, cur * w); dq.offer(v);
                    if (v.equals(t)) return dist.get(v);
                }
            }
        }
        return -1.0;
    }
}
```

## 题解二：并查集带权（可选）
- 标签：图论、可达性、并查集
- 思路：用带权并查集维护变量间比值，查询时同集合则返回两者相对权值，否则 -1。

## 总结思路
- 图搜索足以解决；带权并查集在大量查询时具有优势。

## 相关标签
- 图论、DFS、BFS