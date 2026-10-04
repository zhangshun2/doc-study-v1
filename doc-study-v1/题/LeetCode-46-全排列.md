# LeetCode-46 全排列

- 难度：中等
- 链接：https://leetcode.cn/problems/permutations/

## 问题描述
给定不含重复数字的数组 `nums`，返回其所有可能的排列。

## 题解一：官方经典（回溯 + 访问标记）
- 思路：维护路径与已使用标记数组 `used`；在未使用的元素中逐一选择加入路径，递归到长度等于 `n` 时加入答案。
- 复杂度：时间 O(n·n!)，空间 O(n) 路径与标记开销。

```java
import java.util.*;
class Solution {
    List<List<Integer>> ans = new ArrayList<>();
    public List<List<Integer>> permute(int[] nums) {
        boolean[] used = new boolean[nums.length];
        backtrack(nums, used, new ArrayList<>());
        return ans;
    }
    private void backtrack(int[] nums, boolean[] used, List<Integer> path) {
        if (path.size() == nums.length) { ans.add(new ArrayList<>(path)); return; }
        for (int i = 0; i < nums.length; i++) {
            if (used[i]) continue;
            used[i] = true; path.add(nums[i]);
            backtrack(nums, used, path);
            path.remove(path.size() - 1); used[i] = false;
        }
    }
}
```

## 题解二：通用解法（原地交换）
- 标签：回溯、排列、原地交换
- 思路：通过固定位置 `pos`，在 `pos..n-1` 中交换一个元素到 `pos`，递归处理后再交换回去；省略了 `used` 数组。

```java
import java.util.*;
class Solution {
    List<List<Integer>> ans = new ArrayList<>();
    public List<List<Integer>> permute(int[] nums) {
        dfs(nums, 0);
        return ans;
    }
    private void dfs(int[] a, int pos) {
        if (pos == a.length) { 
            List<Integer> t = new ArrayList<>();
            for (int v : a) t.add(v);
            ans.add(t); return; 
        }
        for (int i = pos; i < a.length; i++) {
            swap(a, pos, i);
            dfs(a, pos + 1);
            swap(a, pos, i);
        }
    }
    private void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}
```

## 总结思路
- 两种写法等价；原地交换更节省空间，`used` 写法更易读。

## 相关标签
- 回溯、排列、原地交换