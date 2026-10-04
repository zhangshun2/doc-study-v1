---
schemaVersion: 3
type: "core-model"
leetcodeId: 322
slug: "coin-change"
titleCn: "零钱兑换"
titleEn: "Coin Change"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/coin-change/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "7800922739ae43b447b6e10ed2dd3a2c15f9a2b99943bd74986383254de6ff67"
primaryPattern: "动态规划"
topics: ["动态规划", "广度优先搜索", "数组", "背包问题", "完全背包"]
priority: "P0"
problemPath: "题目/动态规划/322-Coin-Change.md"
deepDivePath: "建模专题/T0/322-Coin-Change-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 322. 零钱兑换：核心模型

> **双轨阅读：** [[题目/动态规划/322-Coin-Change.md|标准题解]] · [[建模专题/T0/322-Coin-Change-直观建模.md|完整建模]]

## 一句话本质

一个最优方案拿走最后一枚硬币后，剩余金额也必须是最优的；因此枚举“最后一枚”即可得到 dp[x] 的所有来源。

## 直观画面与扩题

像填写按金额递增的账本：要算凑出 11 元的最少硬币，只看拿走最后一枚后留下的 10、9 或 6 元账目。

在本题中，对象是 **金额、硬币面额、已经算好的子金额答案**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

dp[x] = min(dp[x-coin]+1)，其中 coin <= x；同一个 coin 可以重复选择。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 金额、硬币面额、已经算好的子金额答案 | dp[x] = min(dp[x-coin]+1)，其中 coin <= x；同一个 coin 可以重复选择。 | dp[x] 表示恰好凑出金额 x 的最少硬币数；dp[0]=0，其余先记为不可达。 | 从金额 current=1 递增到 amount，枚举每个 coin <= current，并用 dp[current-coin]+1 更新 dp[current]。 | 处理 current 前，所有小于 current 的金额都已经是各自的最优答案。 | dp[amount] 仍为哨兵时返回 -1，否则返回它的最少硬币数。 |

## 最小演算

官方首例输入：`coins = [1, 2, 5], amount = 11`，输出：`3`。

1. **初始状态：** dp[x] 表示恰好凑出金额 x 的最少硬币数；dp[0]=0，其余先记为不可达。
2. **触发事件：** 从金额 current=1 递增到 amount，枚举每个 coin <= current，并用 dp[current-coin]+1 更新 dp[current]。
3. **结束条件：** dp[amount] 仍为哨兵时返回 -1，否则返回它的最少硬币数。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

任意可行方案都能按最后一枚硬币拆分；算法枚举了所有可能的最后一枚，并复用已经最优的子金额，所以既不会漏解，也不会得到更大答案。

## 代码映射

```text
1. 令 unreachable=amount+1。
2. dp[0]=0，其余位置填 unreachable。
3. 令 current 从 1 增加到 amount。
4. 枚举不超过 current 的 coin。
5. 用 dp[current-coin]+1 更新 dp[current]。
6. 返回 dp[amount]；仍不可达则为 -1。
```

## 复杂度

- 时间复杂度：O(amount * coins.length)。
- 空间复杂度：O(amount)。

## 30 秒识别信号

- 主题型：`动态规划`
- 切入点：问题可拆成“最后选择一次”，选择后剩余部分与原问题同型，并且子问题按一个维度递增计算。

## 最小反例与易错点

- amount=0 的答案是 0，不需要硬币。
- 哨兵不要用 Integer.MAX_VALUE 后直接加一；amount+1 不会溢出且大于任何可行枚数。

## 分层入口

- [[题目/动态规划/322-Coin-Change.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/322-Coin-Change-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
