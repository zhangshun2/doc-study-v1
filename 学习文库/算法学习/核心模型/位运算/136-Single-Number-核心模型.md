---
schemaVersion: 3
type: "core-model"
leetcodeId: 136
slug: "single-number"
titleCn: "只出现一次的数字"
titleEn: "Single Number"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/single-number/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "7c0ce70d1411921347d6a44307a2bc172fbd08c84858b0780bf7b2ab3f640b41"
primaryPattern: "位运算"
topics: ["位运算", "数组"]
priority: "P1"
problemPath: "题目/位运算/136-Single-Number.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 136. 只出现一次的数字：核心模型

> **双轨阅读：** [[题目/位运算/136-Single-Number.md|标准题解]]

## 一句话本质

设唯一元素为 u，其他元素为成对的 a,a,b,b。由于异或可任意重排和分组： a ^ a ^ b ^ b ^ u = (a ^ a) ^ (b ^ b) ^ u = 0 ^ 0 ^ u

## 直观画面与扩题

像把每个二进制位当成独立开关，相同信息出现两次时可以通过异或相互抵消。

在本题中，对象是 **整数的二进制位**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：设唯一元素为 u，其他元素为成对的 a,a,b,b。由于异或可任意重排和分组： a ^ a ^ b ^ b ^ u = (a ^ a) ^ (b ^ b) ^ u = 0 ^ 0 ^ u

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 整数的二进制位 | 把题目翻译成一条可执行关系：设唯一元素为 u，其他元素为成对的 a,a,b,b。由于异或可任意重排和分组： a ^ a ^ b ^ b ^ u = (a ^ a) ^ (b ^ b) ^ u = 0 ^ 0 ^ u | 初始化 answer = 0，顺序遍历数组并执行 answer ^= num。任何成对值无论相隔多远，最终都会因交换律和结合律消为零； | 任何成对值无论相隔多远，最终都会因交换律和结合律消为零；初始化 answer = 0，顺序遍历数组并执行 answer ^= num。 | 处理完数组前 i 个元素后，answer 等于这 i 个元素的异或结果。循环更新显然保持该不变量。 | 处理完数组前 i 个元素后，answer 等于这 i 个元素的异或结果。循环更新显然保持该不变量。 |

## 最小演算

官方首例输入：`nums = [2,2,1]`，输出：`1`。

1. **初始状态：** 初始化 answer = 0，顺序遍历数组并执行 answer ^= num。
2. **触发事件：** 任何成对值无论相隔多远，最终都会因交换律和结合律消为零； 初始化 answer = 0，顺序遍历数组并执行 answer ^= num。
3. **结束条件：** 处理完数组前 i 个元素后，answer 等于这 i 个元素的异或结果。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

处理完数组前 i 个元素后，answer 等于这 i 个元素的异或结果。循环更新显然保持该不变量。全部处理后，利用交换律和结合律可把所有相同的两个元素配对，每对异或为零；零不会改变剩余值，所以最终 answer 恰好等于只出现一次的元素。

## 代码映射

```text
1. 初始化 answer = 0，顺序遍历数组并执行 answer ^= num。
2. 任何成对值无论相隔多远，最终都会因交换律和结合律消为零；
3. 循环结束只留下唯一值。
```

## 复杂度

- 时间复杂度：O(n)，每个元素异或一次。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`位运算`
- 切入点：异或运算满足 x ^ x = 0 和 x ^ 0 = x。

## 最小反例与易错点

- 异或技巧依赖“其他元素恰好出现两次”；出现三次时不能直接套用。
- 不要把异或 ^ 与逻辑或、乘方混淆；Java 中 ^ 是按位异或。

## 分层入口

- [[题目/位运算/136-Single-Number.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
