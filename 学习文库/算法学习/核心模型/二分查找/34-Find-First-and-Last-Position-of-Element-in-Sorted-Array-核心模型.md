---
schemaVersion: 3
type: "core-model"
leetcodeId: 34
slug: "find-first-and-last-position-of-element-in-sorted-array"
titleCn: "在排序数组中查找元素的第一个和最后一个位置"
titleEn: "Find First and Last Position of Element in Sorted Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "4fae36e4ca276a41b42c38895c4c0d38872ddc4b78563dffc610a85203707502"
primaryPattern: "二分查找"
topics: ["二分查找", "数组"]
priority: "P0"
problemPath: "题目/二分查找/34-Find-First-and-Last-Position-of-Element-in-Sorted-Array.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 34. 在排序数组中查找元素的第一个和最后一个位置：核心模型

> **双轨阅读：** [[题目/二分查找/34-Find-First-and-Last-Position-of-Element-in-Sorted-Array.md|标准题解]]

## 一句话本质

有序数组中的同值元素形成连续区间。问题可拆成两个单调边界： first = lowerBound(target) // 第一个 >= target afterLast = upperBound(target) // 第一个 > target

## 直观画面与扩题

像查字典时每翻一次就丢掉确定不可能的一半，关键是保留包含答案的边界。

在本题中，对象是 **搜索区间、边界和中间分割位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：有序数组中的同值元素形成连续区间。问题可拆成两个单调边界： first = lowerBound(target) // 第一个 >= target afterLast = upperBound(target) // 第一个 > target

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 搜索区间、边界和中间分割位置 | 把题目翻译成一条可执行关系：有序数组中的同值元素形成连续区间。问题可拆成两个单调边界： first = lowerBound(target) // 第一个 >= target afterLast = upperBound(target) // 第一个 > target | 有序数组中的同值元素形成连续区间。问题可拆成两个单调边界： first = lowerBound(target) // 第一个 >= target | lowerBound 遇到 nums[mid] >= target 时保留 mid 并向左找，否则向右； | lowerBound 始终保持 [0,left) 中元素小于目标，而 [right,n) 中元素大于等于目标； | lowerBound 始终保持 [0,left) 中元素小于目标，而 [right,n) 中元素大于等于目标； |

## 最小演算

官方首例输入：`nums = [5,7,7,8,8,10], target = 8`，输出：`[3,4]`。

1. **初始状态：** 有序数组中的同值元素形成连续区间。
2. **触发事件：** lowerBound 遇到 nums[mid] >= target 时保留 mid 并向左找，否则向右； lowerBound 遇到 nums[mid] >= target 时保留 mid 并向左找，否则向右；upperBound 遇到 nums[mid] <= target 时向右，否则保留 mid 并向左。
3. **结束条件：** lowerBound 始终保持 [0,left) 中元素小于目标，而 [right,n) 中元素大于等于目标；区间收缩到空时 left==right，正是第一个大于等于目标的位置。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

lowerBound 始终保持 [0,left) 中元素小于目标，而 [right,n) 中元素大于等于目标；区间收缩到空时 left==right，正是第一个大于等于目标的位置。upperBound 对称地保持左侧元素小于等于目标、右侧元素大于目标。因此当目标存在时，两边界围出的闭区间恰好包含全部目标值；不存在时的显式校验会返回 [-1,-1]。

## 代码映射

```text
1. lowerBound 遇到 nums[mid] >= target 时保留 mid 并向左找，否则向右；
2. upperBound 遇到 nums[mid] <= target 时向右，否则保留 mid 并向左。
3. 两者最终都在 [0,n] 返回一个插入位置。
```

## 复杂度

- 时间复杂度：两次二分均为 O(log n)，总体 O(log n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`二分查找`
- 切入点：普通二分命中任意一个目标位置后不要停止，要继续向边界搜索。

## 最小反例与易错点

- lowerBound 可能返回 nums.length，访问数组前必须检查。
- 不要用 lowerBound(target+1)-1 的写法处理任意 int 目标，target+1 可能溢出；单独实现 upperBound 更稳健。

## 分层入口

- [[题目/二分查找/34-Find-First-and-Last-Position-of-Element-in-Sorted-Array.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
