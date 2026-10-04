---
schemaVersion: 3
type: "core-model"
leetcodeId: 33
slug: "search-in-rotated-sorted-array"
titleCn: "搜索旋转排序数组"
titleEn: "Search in Rotated Sorted Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/search-in-rotated-sorted-array/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "4ca0d92f6ff1a8f1224dd4b852b24a4b88fd7396ca40c7d40f58d2c424c4638e"
primaryPattern: "二分查找"
topics: ["二分查找", "数组"]
priority: "P0"
problemPath: "题目/二分查找/33-Search-in-Rotated-Sorted-Array.md"
deepDivePath: "建模专题/T0/33-Search-in-Rotated-Sorted-Array-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 33. 搜索旋转排序数组：核心模型

> **双轨阅读：** [[题目/二分查找/33-Search-in-Rotated-Sorted-Array.md|标准题解]] · [[建模专题/T0/33-Search-in-Rotated-Sorted-Array-直观建模.md|完整建模]]

## 一句话本质

旋转只制造了一个“下降断点”。一个区间被中点切开时，断点最多落在其中一半，所以另一半必然保持有序。只要找出有序的一半，就能判断目标是否在这个值域中，从而恢复二分的排除能力。

## 直观画面与扩题

像查字典时每翻一次就丢掉确定不可能的一半，关键是保留包含答案的边界。

在本题中，对象是 **搜索区间、边界和中间分割位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：旋转只制造了一个“下降断点”。一个区间被中点切开时，断点最多落在其中一半，所以另一半必然保持有序。只要找出有序的一半，就能判断目标是否在这个值域中，从而恢复二分的排除能力。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 搜索区间、边界和中间分割位置 | 把题目翻译成一条可执行关系：旋转只制造了一个“下降断点”。一个区间被中点切开时，断点最多落在其中一半，所以另一半必然保持有序。 | 每轮先检查 nums[mid]。若左半有序，判断 target 是否满足 nums[left] <= target < nums[mid]； | 每轮先检查 nums[mid]。 | 循环开始时，如果目标存在，它一定在闭区间 [left,right]。因为元素互异，左右至少一半可明确为有序。 | 循环开始时，如果目标存在，它一定在闭区间 [left,right]。因为元素互异，左右至少一半可明确为有序。 |

## 最小演算

官方首例输入：`nums = [4,5,6,7,0,1,2], target = 0`，输出：`4`。

1. **初始状态：** 每轮先检查 nums[mid]。
2. **触发事件：** 每轮先检查 nums[mid]。
3. **结束条件：** 循环开始时，如果目标存在，它一定在闭区间 [left,right]。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

循环开始时，如果目标存在，它一定在闭区间 [left,right]。因为元素互异，左右至少一半可明确为有序。若目标值落在有序半段的闭开值域内，则它只能位于该半段；否则它不可能位于该半段，可以安全排除。每轮保留的区间仍满足不变量且长度至少减半。命中时返回正确下标，区间为空则证明目标不存在。

## 代码映射

```text
1. 每轮先检查 nums[mid]。
2. 若左半有序，判断 target 是否满足 nums[left] <= target < nums[mid]；
3. 满足就收缩到左半，否则去右半。
4. 若右半有序，则使用 nums[mid] < target <= nums[right] 对称判断。
```

## 复杂度

- 时间复杂度：O(log n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`二分查找`
- 切入点：任意二分区间中，以 mid 分割后至少有一半仍然有序。

## 最小反例与易错点

- 区间是闭区间，因此循环条件为 left <= right。
- 判断左半有序要用 <=，确保单元素区间被正确归类。

## 分层入口

- [[题目/二分查找/33-Search-in-Rotated-Sorted-Array.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/33-Search-in-Rotated-Sorted-Array-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
