# LeetCode-39 组合总和

- 难度：中等
- 链接：https://leetcode.cn/problems/combination-sum/

## 问题描述
给定候选数字数组 `candidates`（不含负数）和目标数 `target`，找出所有和为 `target` 的组合。数字可以重复选取，组合中数字有顺序要求（通常按非降序输出）。

## 题解一：官方经典（回溯 + 剪枝）
- 思路：
  - 先排序，便于剪枝（当前和超出目标或剩余最小值也超出时终止）。
  - 回溯时传递当前起始索引 `start`，允许重复使用同一数字（递归时仍传 `start`）。
  - 到达 `sum == target` 加入答案；`sum > target` 回退。
- 复杂度：与解空间相关，最坏指数级；排序 O(n log n)。

```java
import java.util.*;
class Solution {
    List<List<Integer>> ans = new ArrayList<>();
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        backtrack(candidates, target, 0, 0, new ArrayList<>());
        return ans;
    }
    private void backtrack(int[] a, int target, int start, int sum, List<Integer> path) {
        if (sum == target) { ans.add(new ArrayList<>(path)); return; }
        for (int i = start; i < a.length; i++) {
            int v = a[i];
            if (sum + v > target) break; // 剪枝
            path.add(v);
            backtrack(a, target, i, sum + v, path);
            path.remove(path.size() - 1);
        }
    }
}
```

## 题解二：最好理解（“先选当前，再看剩余”）
- 标签：回溯、剪枝、排序
- 直觉：针对每个候选数，选择它并继续向下；未达到则继续选当前或换下一个；超出则回退。

## 总结思路
- 排序 + 起始索引能简化重复选择与剪枝；与“组合总和 II”不同的是这里允许重复选取同一元素。

## 相关标签
- 回溯、剪枝、组合构造