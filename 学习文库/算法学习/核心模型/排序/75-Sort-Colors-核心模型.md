---
schemaVersion: 3
type: "core-model"
leetcodeId: 75
slug: "sort-colors"
titleCn: "颜色分类"
titleEn: "Sort Colors"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/sort-colors/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "c134a307de94954e82675289d0d8453fc4145e65af8e2badff730bfab89bc81c"
primaryPattern: "排序"
topics: ["排序", "数组", "双指针", "冒泡排序", "快速排序"]
priority: "P0"
problemPath: "题目/排序/75-Sort-Colors.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 75. 颜色分类：核心模型

> **双轨阅读：** [[题目/排序/75-Sort-Colors.md|标准题解]]

## 一句话本质

维护三个指针： low：下一个 0 应放的位置。 current：当前待分类元素。 high：下一个 2 应放的位置。 循环中保持四段结构： [0, low) 全是 0 [low, current) 全是 1

## 直观画面与扩题

像先按统一顺序排队，原本杂乱的局部关系就会变成一次线性扫描。

在本题中，对象是 **已经按关键字段获得全局顺序的元素**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：维护三个指针： low：下一个 0 应放的位置。 current：当前待分类元素。 high：下一个 2 应放的位置。 循环中保持四段结构： [0, low) 全是 0 [low, current) 全是 1

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 已经按关键字段获得全局顺序的元素 | 把题目翻译成一条可执行关系：维护三个指针： low：下一个 0 应放的位置。current：当前待分类元素。 | 维护三个指针： low：下一个 0 应放的位置。current：当前待分类元素。high：下一个 2 应放的位置。 | 检查 nums[current]： 为 0：与 nums[low] 交换，low++、current++。 | 初始时四个区间除未分类区外均为空，不变量成立。每次操作都把当前未分类元素移动到它所属的确定区域，并至少让未分类区缩小一格：处理 0 扩大左侧零区，处理 1 扩大中间一区，处理 2 扩大右侧二区。 | 初始时四个区间除未分类区外均为空，不变量成立。每次操作都把当前未分类元素移动到它所属的确定区域，并至少让未分类区缩小一格：处理 0 扩大左侧零区，处理 1 扩大中间一区，处理 2 扩大右侧二区。 |

## 最小演算

官方首例输入：`nums = [2,0,2,1,1,0]`，输出：`[0,0,1,1,2,2]`。

1. **初始状态：** 维护三个指针： low：下一个 0 应放的位置。
2. **触发事件：** 检查 nums[current]： 为 0：与 nums[low] 交换，low++、current++。
3. **结束条件：** 初始时四个区间除未分类区外均为空，不变量成立。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

初始时四个区间除未分类区外均为空，不变量成立。每次操作都把当前未分类元素移动到它所属的确定区域，并至少让未分类区缩小一格：处理 0 扩大左侧零区，处理 1 扩大中间一区，处理 2 扩大右侧二区。操作不会破坏其他确定区域。当 current > high 时未分类区为空，整个数组按 0、1、2 排列。

## 代码映射

```text
1. 检查 nums[current]：
2. 检查 nums[current]： 为 0：与 nums[low] 交换，low++、current++。
3. 维护三个指针： low：下一个 0 应放的位置。 current：当前待分类元素。 high：下一个 2 应放的位置。
```

## 复杂度

- 时间复杂度：O(n)，每轮都缩小未分类区，每个元素至多被常数次交换检查。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`排序`
- 切入点：把数组划分成“确定是 0、确定是 1、尚未处理、确定是 2”四段。

## 最小反例与易错点

- 循环条件必须是 current <= high，因为 current == high 时仍有一个元素未分类。
- 与 high 交换后不能 current++。

## 分层入口

- [[题目/排序/75-Sort-Colors.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
