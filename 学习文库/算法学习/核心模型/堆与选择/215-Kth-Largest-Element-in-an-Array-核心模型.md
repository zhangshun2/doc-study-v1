---
schemaVersion: 3
type: "core-model"
leetcodeId: 215
slug: "kth-largest-element-in-an-array"
titleCn: "数组中的第K个最大元素"
titleEn: "Kth Largest Element in an Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/kth-largest-element-in-an-array/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "967606a922921e6660ca6897c5f71857d79cadb7ee47c1ece70efdee55eea582"
primaryPattern: "堆与选择"
topics: ["堆与选择", "数组", "分治", "快速选择", "排序", "堆（优先队列）"]
priority: "P0"
problemPath: "题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md"
deepDivePath: "建模专题/T0/215-Kth-Largest-Element-in-an-Array-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 215. 数组中的第K个最大元素：核心模型

> **双轨阅读：** [[题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md|标准题解]] · [[建模专题/T0/215-Kth-Largest-Element-in-an-Array-直观建模.md|完整建模]]

## 一句话本质

第 K 大在升序数组中的位置是 n-K；分区后枢轴已经到达最终位置，只保留包含目标位置的一侧即可。

## 直观画面与扩题

像整理书架时只关心第 K 个位置：每次分好一本书的最终位置，确定目标在左边还是右边，另一半不必再排序。

在本题中，对象是 **候选区间、分区枢轴、目标升序下标**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

答案下标 target=n-K；partition 返回 pivotIndex，并保证左侧不大于枢轴、右侧不小于枢轴。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 候选区间、分区枢轴、目标升序下标 | 答案下标 target=n-K；partition 返回 pivotIndex，并保证左侧不大于枢轴、右侧不小于枢轴。 | 当前候选区间 [left,right] 和本轮枢轴的最终下标 pivotIndex。 | 对 [left,right] 做一次分区；将 pivotIndex 与 target 比较，舍弃不含 target 的一半。 | 每轮之前的候选区间始终包含答案下标 target，且区间外的元素已经不可能替代答案。 | pivotIndex==target 时，枢轴值就是第 K 大；区间不断缩小，最终必然命中。 |

## 最小演算

官方首例输入：`[3,2,1,5,6,4], k = 2`，输出：`5`。

1. **初始状态：** 当前候选区间 [left,right] 和本轮枢轴的最终下标 pivotIndex。
2. **触发事件：** 对 [left,right] 做一次分区；将 pivotIndex 与 target 比较，舍弃不含 target 的一半。
3. **结束条件：** pivotIndex==target 时，枢轴值就是第 K 大；区间不断缩小，最终必然命中。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

枢轴左侧都 <= 枢轴、右侧都 >= 枢轴，所以枢轴位置就是其升序最终位置；目标在哪一侧也可以据此唯一判断。

## 代码映射

```text
1. 令 target=n-K，left=0，right=n-1。
2. 在 [left,right] 中随机选枢轴并分区。
3. 得到枢轴最终位置 pivotIndex。
4. 若 pivotIndex==target，返回 nums[pivotIndex]。
5. 若 target 在左侧，缩小 right；否则增大 left。
```

## 复杂度

- 时间复杂度：随机化后期望 O(n)；极端连续选到最差枢轴时最坏 O(n^2)。
- 空间复杂度：O(1)，原地迭代分区。

## 30 秒识别信号

- 主题型：`堆与选择`
- 切入点：只关心顺序统计量，不要求整体有序，并且能从一次分区中安全排除一半候选。

## 最小反例与易错点

- 第 K 大的升序下标是 n-K，不是 K-1。
- 重复元素参与排名，不能先去重。

## 分层入口

- [[题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/215-Kth-Largest-Element-in-an-Array-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/选择结构/PriorityQueue-Comparator.md|PriorityQueue / Comparator]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
