---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/双指针/三数之和/微模板与易错点卡片.md)
  - [模板索引：排序加双指针](../学习方法/模板索引.md#排序加双指针模板)
---
# LeetCode-15 三数之和

- 难度：中等
- 链接：https://leetcode.cn/problems/3sum/

## 问题描述
给定整数数组 `nums`，找出所有和为 0 且不重复的三元组。

## 题解一：官方经典（排序 + 双指针）
- 思路：排序后固定一个数 `i`，在其右侧用左右指针 `l,r` 找两数之和为 `-nums[i]`；过程中跳过重复元素确保结果不重复。
- 复杂度：时间 O(n^2)，空间 O(1)（不计输出）。

```java
import java.util.*;
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> ans = new ArrayList<>();
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            if (nums[i] > 0) break;
            int l = i + 1, r = n - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    ans.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (sum < 0) l++; else r--;
            }
        }
        return ans;
    }
}
```

## 题解二：通用解法（哈希辅助去重思路）
- 标签：数组、双指针、排序、哈希
- 思路：也可用 `Set` 辅助记录已选二元组以去重，但排序 + 双指针更简洁可靠；此处不赘述哈希版本代码。

## 题解三：最好理解（“定一个，找另外两个”）
- 直觉：确定一个数后问题化为两数之和；由于要去重，排序后跳过重复值是关键。

## 总结思路
- 排序 + 双指针是标准写法；边界与去重处理是实现重点。

## 相关标签
- 数组、双指针、排序、哈希