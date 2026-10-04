---
schemaVersion: 3
type: "core-model"
leetcodeId: 155
slug: "min-stack"
titleCn: "最小栈"
titleEn: "Min Stack"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/min-stack/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "77ddb740d257d6d8ced461d34848f581945a2d805ea84e15f78f58f6fa1a9c68"
primaryPattern: "栈"
topics: ["栈", "设计"]
priority: "P0"
problemPath: "题目/栈/155-Min-Stack.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 155. 最小栈：核心模型

> **双轨阅读：** [[题目/栈/155-Min-Stack.md|标准题解]]

## 一句话本质

普通栈只能访问栈顶，扫描求最小值为 O(n)。关键是把每个历史时刻的最小值随栈状态一同保存。数据栈第 i 层存实际值，最小栈第 i 层存前 i 层的最小值，两个栈严格同步。

## 直观画面与扩题

像叠盘子和拆礼物盒，最后放入或最后打开的一层最先负责结算。

在本题中，对象是 **尚未结算的左侧符号或外层现场**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：普通栈只能访问栈顶，扫描求最小值为 O(n)。关键是把每个历史时刻的最小值随栈状态一同保存。数据栈第 i 层存实际值，最小栈第 i 层存前 i 层的最小值，两个栈严格同步。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 尚未结算的左侧符号或外层现场 | 把题目翻译成一条可执行关系：普通栈只能访问栈顶，扫描求最小值为 O(n)。关键是把每个历史时刻的最小值随栈状态一同保存。 | 压入 val 时，同时向最小栈压入： min(val, 之前的最小值) 弹出时两个栈一起弹。 | 压入 val 时，同时向最小栈压入： min(val, 之前的最小值) | 不变量：两个栈大小相等，且 minimums[i] 是 values[0..i] 的最小值。 | 初始时两个栈为空。不变量对压栈成立，因为新最小值正是 min(旧最小值, val)；同步弹栈后，新的栈顶恢复上一层保存的最小值。 |

## 最小演算

官方首例输入：`["MinStack","push","push","push","getMin","pop","top","getMin"] [[],[-2],[0],[-3],[],[],[],[]]`，输出：`[null,null,null,null,-3,null,0,-2]`。

1. **初始状态：** 压入 val 时，同时向最小栈压入： min(val, 之前的最小值) 弹出时两个栈一起弹。
2. **触发事件：** 压入 val 时，同时向最小栈压入： min(val, 之前的最小值)
3. **结束条件：** 初始时两个栈为空。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

不变量：两个栈大小相等，且 minimums[i] 是 values[0..i] 的最小值。 初始时两个栈为空。不变量对压栈成立，因为新最小值正是 min(旧最小值, val)；同步弹栈后，新的栈顶恢复上一层保存的最小值。因此任意时刻 getMin() 返回值都正确。

## 代码映射

```text
1. 压入 val 时，同时向最小栈压入：
2. 压入 val 时，同时向最小栈压入： min(val, 之前的最小值)
3. 压入 val 时，同时向最小栈压入： min(val, 之前的最小值) 弹出时两个栈一起弹。于是最小栈栈顶永远对应当前数据栈的最小值。也可只在 val <= currentMin 时记录最小值，但同步栈写法更不易出错。
```

## 复杂度

- 时间复杂度：构造、push、pop、top、getMin 均为 O(1)。
- 空间复杂度：用一个栈保存 val - min 的差值，但必须用 long 防止整数溢出。

## 30 秒识别信号

- 主题型：`栈`
- 切入点：当前最小值被弹出后，需要立刻知道“此前的最小值”。

## 最小反例与易错点

- 重复最小值必须正确处理；同步保存每层最小值天然解决此问题。
- ArrayDeque 不允许 null，本题只存整数，不受影响。

## 分层入口

- [[题目/栈/155-Min-Stack.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
