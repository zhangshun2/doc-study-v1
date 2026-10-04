---
schemaVersion: 3
type: "core-model"
leetcodeId: 169
slug: "majority-element"
titleCn: "多数元素"
titleEn: "Majority Element"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/majority-element/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "f4b192d33ee938da62f1e7a17cac42d054eac57ad4860753bf24378c42384cce"
primaryPattern: "数组与哈希"
topics: ["数组与哈希", "数组", "哈希表", "分治", "计数", "排序", "摩尔投票算法"]
priority: "P2"
problemPath: "题目/数组与哈希/169-Majority-Element.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 169. 多数元素：核心模型

> **双轨阅读：** [[题目/数组与哈希/169-Majority-Element.md|标准题解]]

## 一句话本质

多数元素的数量超过其他所有元素数量之和。任意删除两个不同的元素，不会改变剩余数组中的多数元素身份。Boyer-Moore 算法在线完成这种“异类配对抵消”。

## 直观画面与扩题

像边收卡片边登记索引：每来一张，就先查旧记录里有没有能配对的卡片。

在本题中，对象是 **数组元素与下标、已经扫描过的历史信息**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：多数元素的数量超过其他所有元素数量之和。任意删除两个不同的元素，不会改变剩余数组中的多数元素身份。Boyer-Moore 算法在线完成这种“异类配对抵消”。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 数组元素与下标、已经扫描过的历史信息 | 把题目翻译成一条可执行关系：多数元素的数量超过其他所有元素数量之和。任意删除两个不同的元素，不会改变剩余数组中的多数元素身份。 | 维护 candidate 和 votes： votes == 0 时，把当前元素设为新候选人。 | votes == 0 时，把当前元素设为新候选人。 | 扫描过程中，可以把已处理前缀划分为若干对“值不同的已抵消元素”和 votes 个值为 candidate 的未抵消元素。 | 对完整数组删除任意数量的异值对后，原多数元素仍至少剩一个。最终未抵消元素全等于 candidate，因此候选人就是题目保证存在的多数元素。 |

## 最小演算

官方首例输入：`nums = [3,2,3]`，输出：`3`。

1. **初始状态：** 维护 candidate 和 votes： votes == 0 时，把当前元素设为新候选人。
2. **触发事件：** votes == 0 时，把当前元素设为新候选人。
3. **结束条件：** 对完整数组删除任意数量的异值对后，原多数元素仍至少剩一个。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

扫描过程中，可以把已处理前缀划分为若干对“值不同的已抵消元素”和 votes 个值为 candidate 的未抵消元素。当票数归零时，该前缀全部配对抵消，对后续多数判断没有影响。 对完整数组删除任意数量的异值对后，原多数元素仍至少剩一个。

## 代码映射

```text
1. 维护 candidate 和 votes：
2. votes == 0 时，把当前元素设为新候选人。
3. 维护 candidate 和 votes： votes == 0 时，把当前元素设为新候选人。
```

## 复杂度

- 时间复杂度：O(n)，仅扫描一次。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`数组与哈希`
- 切入点：哈希计数很直接，但需要额外空间。

## 最小反例与易错点

- votes == 0 时要先更新候选人，再根据当前元素加票。
- 算法第一轮只能产生“候选人”。本题因保证多数元素存在，可以直接返回。

## 分层入口

- [[题目/数组与哈希/169-Majority-Element.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
