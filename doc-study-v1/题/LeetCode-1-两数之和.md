---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/哈希表/两数之和/微模板与易错点卡片.md)
  - [模板索引：哈希映射](../学习方法/模板索引.md#数组哈希映射分组集合)
---
# LeetCode-1 两数之和

- 难度：简单
- 链接：https://leetcode.cn/problems/two-sum/

## 问题描述
给定整数数组 `nums` 和整数目标值 `target`，请你在该数组中找出和为 `target` 的两个整数，并返回它们的下标。假设每种输入只会对应一个答案，但数组中同一个元素不能使用两遍。

## 题解一：官方经典（哈希表一遍扫描）
- 思路：遍历数组，用哈希表记录已访问元素的值到下标映射；对当前值 `x` 查找 `target-x` 是否已出现，若出现则返回两者下标；否则记录当前值。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> idx = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (idx.containsKey(need)) return new int[]{idx.get(need), i};
            idx.put(nums[i], i);
        }
        return new int[0];
    }
}
```

## 题解二：通用解法（排序 + 双指针）
- 标签：数组、哈希、双指针
- 思路：将值与原下标打包排序，左右指针向中间靠拢找和为 `target` 的一对；注意最后要返回原下标。
- 复杂度：时间 O(n log n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[] twoSum(int[] nums, int target) {
        int n = nums.length;
        int[][] a = new int[n][2];
        for (int i = 0; i < n; i++) { a[i][0] = nums[i]; a[i][1] = i; }
        Arrays.sort(a, Comparator.comparingInt(x -> x[0]));
        int l = 0, r = n - 1;
        while (l < r) {
            int sum = a[l][0] + a[r][0];
            if (sum == target) return new int[]{a[l][1], a[r][1]};
            if (sum < target) l++; else r--;
        }
        return new int[0];
    }
}
```

## 题解三：最好理解（“找另一个数”）
- 直觉：遍历每个数 `x`，需要另一个数 `target-x`；用哈希表看它是否已经出现过，出现就配对成功。

## 总结思路
- 哈希一遍扫描最优；排序双指针适用于需要有序或需要输出数值对的变体。

## 相关标签
- 数组、哈希、双指针