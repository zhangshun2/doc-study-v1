# LeetCode-78 子集

- 难度：中等
- 链接：https://leetcode.cn/problems/subsets/

## 问题描述
给定不含重复元素的整数数组 `nums`，返回该数组所有可能的子集（幂集）。

## 题解一：官方经典（回溯枚举）
- 思路：按照索引递进，每一位可以“选”或“不选”；当到达末尾，将当前路径加入答案。
- 复杂度：时间 O(n·2^n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    List<List<Integer>> ans = new ArrayList<>();
    public List<List<Integer>> subsets(int[] nums) {
        backtrack(nums, 0, new ArrayList<>());
        return ans;
    }
    private void backtrack(int[] a, int idx, List<Integer> path) {
        if (idx == a.length) { ans.add(new ArrayList<>(path)); return; }
        // 不选当前
        backtrack(a, idx + 1, path);
        // 选当前
        path.add(a[idx]);
        backtrack(a, idx + 1, path);
        path.remove(path.size() - 1);
    }
}
```

## 题解二：通用解法（迭代层扩展）
- 标签：回溯、枚举、迭代
- 思路：从空集开始，针对每个元素，把它加到所有已有子集上形成新子集并合并；更直观但同复杂度。

```java
import java.util.*;
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        ans.add(new ArrayList<>());
        for (int v : nums) {
            int size = ans.size();
            for (int i = 0; i < size; i++) {
                List<Integer> t = new ArrayList<>(ans.get(i));
                t.add(v);
                ans.add(t);
            }
        }
        return ans;
    }
}
```

## 总结思路
- 回溯与迭代层扩展都属于幂集常见模板；根据个人偏好任选其一。

## 相关标签
- 回溯、枚举、幂集