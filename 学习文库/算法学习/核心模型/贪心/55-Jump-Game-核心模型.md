---
schemaVersion: 3
type: "core-model"
leetcodeId: 55
slug: "jump-game"
titleCn: "跳跃游戏"
titleEn: "Jump Game"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/jump-game/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "10ace42f7ee6e16091dfa4c99eb9097fe14fe80cc9969af3713bc77fbd265e3f"
primaryPattern: "贪心"
topics: ["贪心", "数组", "动态规划"]
priority: "P0"
problemPath: "题目/贪心/55-Jump-Game.md"
deepDivePath: "建模专题/T0/55-Jump-Game-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 55. 跳跃游戏：核心模型

> **双轨阅读：** [[题目/贪心/55-Jump-Game.md|标准题解]] · [[建模专题/T0/55-Jump-Game-直观建模.md|完整建模]]

## 一句话本质

如果当前可以到达区间 [0,farthest] 中的每个位置，那么遍历其中下标 i 时，可以用下面的式子扩大覆盖范围： farthest = max(farthest, i + nums[i])

## 直观画面与扩题

像边走边扩展安全可达范围，只保留当下能够证明不会伤害未来的信息。

在本题中，对象是 **当前可达范围、边界和已证明安全的局部选择**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：如果当前可以到达区间 [0,farthest] 中的每个位置，那么遍历其中下标 i 时，可以用下面的式子扩大覆盖范围： farthest = max(farthest, i + nums[i])

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 当前可达范围、边界和已证明安全的局部选择 | 把题目翻译成一条可执行关系：如果当前可以到达区间 [0,farthest] 中的每个位置，那么遍历其中下标 i 时，可以用下面的式子扩大覆盖范围： farthest = max(farthest, i + nums[i]) | 对于可达性，较远覆盖永远不比更近覆盖差，因此只保留最强状态 farthest： 若 i > farthest，当前点不可达，返回 false。 | 若 i > farthest，当前点不可达，返回 false。 | 处理下标 i 之前，farthest 是利用已处理且可达的位置能够抵达的最远下标。如果 i <= farthest，则 i 可达，从它可扩展到 i + nums[i]，取最大值后仍是全部已处理位置的最远覆盖。 | 若 i > farthest，当前点不可达，返回 false。否则用 i + nums[i] 更新 farthest。 |

## 最小演算

官方首例输入：`nums = [2,3,1,1,4]`，输出：`true`。

1. **初始状态：** 对于可达性，较远覆盖永远不比更近覆盖差，因此只保留最强状态 farthest： 若 i > farthest，当前点不可达，返回 false。
2. **触发事件：** 若 i > farthest，当前点不可达，返回 false。
3. **结束条件：** 若 i > farthest，当前点不可达，返回 false。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

处理下标 i 之前，farthest 是利用已处理且可达的位置能够抵达的最远下标。如果 i <= farthest，则 i 可达，从它可扩展到 i + nums[i]，取最大值后仍是全部已处理位置的最远覆盖。如果 i > farthest，没有已处理位置能到达 i，而跳跃只能向右，所以无法跨越这一断点。

## 代码映射

```text
1. 若 i > farthest，当前点不可达，返回 false。
2. 否则用 i + nums[i] 更新 farthest。
3. 若 farthest >= n - 1，末尾已经可达，返回 true。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`贪心`
- 切入点：不需要枚举每个位置究竟跳几步，只需关心目前能覆盖到的最右位置。

## 最小反例与易错点

- 长度为 1 时无需跳跃，应返回 true。
- 数组中出现 0 不一定失败，之前的覆盖范围可能直接跨过它。

## 分层入口

- [[题目/贪心/55-Jump-Game.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/55-Jump-Game-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
