---
schemaVersion: 3
type: "core-model"
leetcodeId: 62
slug: "unique-paths"
titleCn: "不同路径"
titleEn: "Unique Paths"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/unique-paths/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "764f942398811ddc525530f391db2620b3c3c3a475974ff6a389a3e332079f79"
primaryPattern: "动态规划"
topics: ["动态规划", "数学", "组合数学"]
priority: "P1"
problemPath: "题目/动态规划/62-Unique-Paths.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 62. 不同路径：核心模型

> **双轨阅读：** [[题目/动态规划/62-Unique-Paths.md|标准题解]]

## 一句话本质

定义 ways[row][col] 为到达格子 (row,col) 的路径数。最后一步来源分成互斥的两类： ways[row][col] = ways[row - 1][col] + ways[row][col - 1]

## 直观画面与扩题

像填写一张递推账本，当前格子的答案只由少量已经算好的前序格子决定。

在本题中，对象是 **可复用的子问题状态**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：定义 ways[row][col] 为到达格子 (row,col) 的路径数。最后一步来源分成互斥的两类： ways[row][col] = ways[row - 1][col] + ways[row][col - 1]

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 可复用的子问题状态 | 把题目翻译成一条可执行关系：定义 ways[row][col] 为到达格子 (row,col) 的路径数。 | 二维表每一行只依赖上一行和本行左侧，因此使用长度为 n 的数组： 初始全部填 1，代表第一行每格只有一种走法。 | 从第二行开始，按列从左到右更新 dp[col] += dp[col - 1]。 | 处理第 row 行第 col 列后，dp[col] 等于到达当前格子的路径数，而右侧尚未更新的元素仍保存上一行路径数。 | 处理第 row 行第 col 列后，dp[col] 等于到达当前格子的路径数，而右侧尚未更新的元素仍保存上一行路径数。 |

## 最小演算

官方首例输入：`m = 3, n = 7`，输出：`28`。

1. **初始状态：** 二维表每一行只依赖上一行和本行左侧，因此使用长度为 n 的数组： 初始全部填 1，代表第一行每格只有一种走法。
2. **触发事件：** 从第二行开始，按列从左到右更新 dp[col] += dp[col - 1]。
3. **结束条件：** 处理第 row 行第 col 列后，dp[col] 等于到达当前格子的路径数，而右侧尚未更新的元素仍保存上一行路径数。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

处理第 row 行第 col 列后，dp[col] 等于到达当前格子的路径数，而右侧尚未更新的元素仍保存上一行路径数。转移 dp[col] = dp[col] + dp[col-1] 正好相加上方与左方的全部路径。逐行完成后，dp[n-1] 即右下角路径数。

## 代码映射

```text
1. 初始全部填 1，代表第一行每格只有一种走法。
2. 从第二行开始，按列从左到右更新 dp[col] += dp[col - 1]。
3. 更新前 dp[col] 是上方值，更新后的 dp[col - 1] 是左方值。
```

## 复杂度

- 时间复杂度：O(mn)。
- 空间复杂度：O(n)；调整行列后可写成 O(min(m,n))。

## 30 秒识别信号

- 主题型：`动态规划`
- 切入点：到达一个非边界格子的最后一步只可能来自上方或左方。

## 最小反例与易错点

- m = 1 或 n = 1 时只有一条路径。
- 一维 DP 必须从左向右更新；反向会使用上一行的左方值，破坏转移。

## 分层入口

- [[题目/动态规划/62-Unique-Paths.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
