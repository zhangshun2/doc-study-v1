# LeetCode-287 寻找重复数

- 难度：中等
- 链接：https://leetcode.cn/problems/find-the-duplicate-number/

## 问题描述
给定包含 `n+1` 个整数的数组 `nums`，每个整数在 `1..n` 范围内，数组中只有一个重复的数字，求该重复数字。要求不修改数组，使用 O(1) 额外空间。

## 题解一：官方经典（Floyd 环检测）
- 思路：将数组视为链表，索引为节点，值为下一节点指针；由于存在重复，必有环。先相遇再找环入口即为重复数。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0], fast = nums[0];
        do { slow = nums[slow]; fast = nums[nums[fast]]; } while (slow != fast);
        int finder = nums[0];
        while (finder != slow) { finder = nums[finder]; slow = nums[slow]; }
        return finder;
    }
}
```

## 题解二：通用解法（二分计数）
- 标签：二分、快慢指针
- 思路：对值域 `[1..n]` 二分，统计小于等于中点的元素个数，依据抽屉原理判断重复在左/右。

## 总结思路
- Floyd 满足题目“只读 + 常数空间”约束；二分计数作为替代方案。

## 相关标签
- 二分、快慢指针