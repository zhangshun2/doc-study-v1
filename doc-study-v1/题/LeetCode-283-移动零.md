---
相关文档导航:
  - [数组专题导航](../数组专题/导航.md)
  - [学习顺序-数组专题12题](../数组专题/学习顺序-数组专题12题.md)
  - [微模板与易错点卡片](../数组专题/双指针/移动零/微模板与易错点卡片.md)
  - [模板索引：快慢指针](../学习方法/模板索引.md#快慢指针模板)
---
# LeetCode-283 移动零

- 难度：简单
- 链接：https://leetcode.cn/problems/move-zeroes/

## 问题描述
将数组中的所有 0 移动到数组末尾，同时保持非零元素的相对顺序。原地操作。

## 题解一：官方经典（快慢指针写回非零）
- 思路：慢指针 `slow` 指向下一个应写入非零的位置，快指针 `i` 遍历数组发现非零就写到 `slow` 并递增；最后将剩余位置填 0。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) nums[slow++] = nums[i];
        }
        while (slow < nums.length) nums[slow++] = 0;
    }
}
```

## 题解二：通用解法（交换非零到前面）
- 标签：数组、双指针
- 思路：遇到非零与 `slow` 位置交换，把非零聚集到前面，同时保持相对顺序（因为每个元素第一次到位）。

```java
class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) {
                int t = nums[slow]; nums[slow] = nums[i]; nums[i] = t;
                slow++;
            }
        }
    }
}
```

## 题解三：最好理解（“把非零往前挪，最后补零”）
- 直觉：先稳定地把所有非零按原顺序挪到前面，后面自然空出的位置统一补 0。

## 总结思路
- 写回法更直观稳定；交换法代码略短但会产生多余交换。

## 相关标签
- 数组、双指针