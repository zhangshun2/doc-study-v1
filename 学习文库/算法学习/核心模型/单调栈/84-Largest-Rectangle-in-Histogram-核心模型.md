---
schemaVersion: 3
type: "core-model"
leetcodeId: 84
slug: "largest-rectangle-in-histogram"
titleCn: "柱状图中最大的矩形"
titleEn: "Largest Rectangle in Histogram"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/largest-rectangle-in-histogram/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "753498798efd0ec98ef4d7e7574de7d027d2ed446ceed78f0d3b76503072c4b4"
primaryPattern: "单调栈"
topics: ["单调栈", "栈", "数组", "区间最值查询"]
priority: "P0"
problemPath: "题目/单调栈/84-Largest-Rectangle-in-Histogram.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 84. 柱状图中最大的矩形：核心模型

> **双轨阅读：** [[题目/单调栈/84-Largest-Rectangle-in-Histogram.md|标准题解]]

## 一句话本质

对于被弹出的下标 middle： 当前下标 i 是它右侧第一个更矮柱子的位置。 弹出后新的栈顶 leftLess 是它左侧第一个更矮柱子的位置。 因而高度 heights[middle] 能延伸的宽度为 i - leftLess - 1。

## 直观画面与扩题

像站在队列里等更高的邻居，只有第一次更高事件到来时才结算当前等待者。

在本题中，对象是 **等待未来更大或更小事件结算的候选**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：对于被弹出的下标 middle： 当前下标 i 是它右侧第一个更矮柱子的位置。 弹出后新的栈顶 leftLess 是它左侧第一个更矮柱子的位置。 因而高度 heights[middle] 能延伸的宽度为 i - leftLess - 1。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 等待未来更大或更小事件结算的候选 | 把题目翻译成一条可执行关系：对于被弹出的下标 middle： 当前下标 i 是它右侧第一个更矮柱子的位置。 | 栈中保存尚未找到右侧更矮柱子的下标，柱高保持单调不降。当当前高度小于栈顶高度时： 弹出栈顶 middle，当前下标就是其右边界。 | 弹出栈顶 middle，当前下标就是其右边界。 | 栈内下标递增、对应高度单调不降，且其中每根柱子尚未遇到右侧第一个更矮值。遇到更矮的当前柱时，所有高于它的栈顶都首次获得右边界； | 栈内下标递增、对应高度单调不降，且其中每根柱子尚未遇到右侧第一个更矮值。遇到更矮的当前柱时，所有高于它的栈顶都首次获得右边界； |

## 最小演算

官方首例输入：`heights = [2,1,5,6,2,3]`，输出：`10`。

1. **初始状态：** 栈中保存尚未找到右侧更矮柱子的下标，柱高保持单调不降。
2. **触发事件：** 弹出栈顶 middle，当前下标就是其右边界。
3. **结束条件：** 栈内下标递增、对应高度单调不降，且其中每根柱子尚未遇到右侧第一个更矮值。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

栈内下标递增、对应高度单调不降，且其中每根柱子尚未遇到右侧第一个更矮值。遇到更矮的当前柱时，所有高于它的栈顶都首次获得右边界；弹出后栈顶由于单调性是左侧最近的严格更矮位置。因此计算的是以该柱高度能达到的最大矩形，不可能通过继续向两边扩展获得更大宽度。每根柱子最终都被结算一次，取最大即全局答案。

## 代码映射

```text
1. 弹出栈顶 middle，当前下标就是其右边界。
2. 新栈顶就是其左边界。
3. 计算 heights[middle] * (i - stack.peek() - 1)。
4. 持续弹出，直到单调性恢复，再压入当前下标。
```

## 复杂度

- 时间复杂度：O(n)，每个下标至多入栈一次、出栈一次。
- 空间复杂度：O(n)，最坏递增数组全部入栈。

## 30 秒识别信号

- 主题型：`单调栈`
- 切入点：以某根柱子高度为矩形高度时，只需找到左右两侧第一个严格更矮的柱子。

## 最小反例与易错点

- 宽度公式是 i - stack.peek() - 1，其中栈顶是在弹出后读取。
- 末尾需要哨兵高度 0，否则递增数组中的柱子不会被结算。

## 分层入口

- [[题目/单调栈/84-Largest-Rectangle-in-Histogram.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
