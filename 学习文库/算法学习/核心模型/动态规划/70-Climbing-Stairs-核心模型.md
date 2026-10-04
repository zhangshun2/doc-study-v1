---
schemaVersion: 3
type: "core-model"
leetcodeId: 70
slug: "climbing-stairs"
titleCn: "爬楼梯"
titleEn: "Climbing Stairs"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/climbing-stairs/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "23fe127b18e7e7ebbd254ed9056a000962c3db6e595737b8afbce9cce4f642a7"
primaryPattern: "动态规划"
topics: ["动态规划", "记忆化", "数学"]
priority: "P0"
problemPath: "题目/动态规划/70-Climbing-Stairs.md"
deepDivePath: "建模专题/T0/70-Climbing-Stairs-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 70. 爬楼梯：核心模型

> **双轨阅读：** [[题目/动态规划/70-Climbing-Stairs.md|标准题解]] · [[建模专题/T0/70-Climbing-Stairs-直观建模.md|完整建模]]

## 一句话本质

设 dp[i] 为恰好到达第 i 阶的方法数。按最后一步分类： dp[i] = dp[i - 1] + dp[i - 2] 基础状态为 dp[1] = 1、dp[2] = 2。这个数列与斐波那契数列只相差一个下标偏移。

## 直观画面与扩题

像填写一张递推账本，当前格子的答案只由少量已经算好的前序格子决定。

在本题中，对象是 **可复用的子问题状态**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：设 dp[i] 为恰好到达第 i 阶的方法数。按最后一步分类： dp[i] = dp[i - 1] + dp[i - 2] 基础状态为 dp[1] = 1、dp[2] = 2。这个数列与斐波那契数列只相差一个下标偏移。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 可复用的子问题状态 | 把题目翻译成一条可执行关系：设 dp[i] 为恰好到达第 i 阶的方法数。按最后一步分类： dp[i] = dp[i - 1] + dp[i - 2] 基础状态为 dp[1] = 1、dp[2] = 2。 | 自底向上按 3 到 n 的顺序计算。由于当前答案只依赖前两项，用 prev2 表示 dp[i-2]，prev1 表示 dp[i-1]： current = prev1 + prev2 | 自底向上按 3 到 n 的顺序计算。 | 循环处理 step 之前，prev2 等于到达 step-2 阶的方法数，prev1 等于到达 step-1 阶的方法数。 | 循环处理 step 之前，prev2 等于到达 step-2 阶的方法数，prev1 等于到达 step-1 阶的方法数。 |

## 最小演算

官方首例输入：`n = 2`，输出：`2`。

1. **初始状态：** 自底向上按 3 到 n 的顺序计算。
2. **触发事件：** 自底向上按 3 到 n 的顺序计算。
3. **结束条件：** 循环处理 step 之前，prev2 等于到达 step-2 阶的方法数，prev1 等于到达 step-1 阶的方法数。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

循环处理 step 之前，prev2 等于到达 step-2 阶的方法数，prev1 等于到达 step-1 阶的方法数。所有到达 step 的方案按最后一步唯一分为来自这两阶的方案，因此两者相加得到完整且无重复的 current。变量右移后，不变量对下一阶继续成立。循环结束时 prev1 = dp[n]。

## 代码映射

```text
1. 自底向上按 3 到 n 的顺序计算。
2. 由于当前答案只依赖前两项，用 prev2 表示 dp[i-2]，prev1 表示 dp[i-1]：
3. 自底向上按 3 到 n 的顺序计算。由于当前答案只依赖前两项，用 prev2 表示 dp[i-2]，prev1 表示 dp[i-1]： current = prev1 + prev2
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`动态规划`
- 切入点：到达第 i 阶的最后一步，只可能从第 i-1 阶走 1 步，或从第 i-2 阶走 2 步。

## 最小反例与易错点

- 题目从 n = 1 开始；若扩展到 n = 0，组合语义通常定义为一种空方案。
- 基础值是 1,2，不是直接返回标准斐波那契的 F(n)。

## 分层入口

- [[题目/动态规划/70-Climbing-Stairs.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/70-Climbing-Stairs-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
