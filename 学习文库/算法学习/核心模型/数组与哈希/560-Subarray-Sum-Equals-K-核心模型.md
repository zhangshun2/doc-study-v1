---
schemaVersion: 3
type: "core-model"
leetcodeId: 560
slug: "subarray-sum-equals-k"
titleCn: "和为 K 的子数组"
titleEn: "Subarray Sum Equals K"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/subarray-sum-equals-k/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "1708db4719789bf75357d28017d9f5af765db4b18b5597235445665ccb921ae8"
primaryPattern: "数组与哈希"
topics: ["数组与哈希", "数组", "哈希表", "前缀和"]
priority: "P0"
problemPath: "题目/数组与哈希/560-Subarray-Sum-Equals-K.md"
deepDivePath: "建模专题/T0/560-Subarray-Sum-Equals-K-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 560. 和为 K 的子数组：核心模型

> **双轨阅读：** [[题目/数组与哈希/560-Subarray-Sum-Equals-K.md|标准题解]] · [[建模专题/T0/560-Subarray-Sum-Equals-K-直观建模.md|完整建模]]

## 一句话本质

若扫描到下标 right 时前缀和为 sum，某个更早前缀和为 previous，则其后连续区间和为： sum - previous = k <=> previous = sum - k

## 直观画面与扩题

像边收卡片边登记索引：每来一张，就先查旧记录里有没有能配对的卡片。

在本题中，对象是 **数组元素与下标、已经扫描过的历史信息**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：若扫描到下标 right 时前缀和为 sum，某个更早前缀和为 previous，则其后连续区间和为： sum - previous = k <=> previous = sum - k

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 数组元素与下标、已经扫描过的历史信息 | 把题目翻译成一条可执行关系：若扫描到下标 right 时前缀和为 sum，某个更早前缀和为 previous，则其后连续区间和为： sum - previous = k <=> previous = sum - k | 必须先查询再记录当前前缀，否则在 k=0 时会把空子数组错误计入。若扫描到下标 right 时前缀和为 sum，某个更早前缀和为 previous，则其后连续区间和为： sum - previous = k <=> previous = sum - k | 更新 prefix += num。 | 处理当前元素前，哈希表准确记录从空前缀到上一个位置为止的所有前缀和频次。当前以该位置为右端点、和为 k 的子数组，与此前值为 prefix-k 的前缀一一对应，所以增加该频次既不漏也不重。 | 处理当前元素前，哈希表准确记录从空前缀到上一个位置为止的所有前缀和频次。当前以该位置为右端点、和为 k 的子数组，与此前值为 prefix-k 的前缀一一对应，所以增加该频次既不漏也不重。 |

## 最小演算

官方首例输入：`nums = [1,1,1], k = 2`，输出：`2`。

1. **初始状态：** 必须先查询再记录当前前缀，否则在 k=0 时会把空子数组错误计入。
2. **触发事件：** 更新 prefix += num。
3. **结束条件：** 处理当前元素前，哈希表准确记录从空前缀到上一个位置为止的所有前缀和频次。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

处理当前元素前，哈希表准确记录从空前缀到上一个位置为止的所有前缀和频次。当前以该位置为右端点、和为 k 的子数组，与此前值为 prefix-k 的前缀一一对应，所以增加该频次既不漏也不重。随后记录当前前缀，为后续右端点服务。不变量归纳保持，最终答案是全部合法子数组数。

## 代码映射

```text
1. 更新 prefix += num。
2. 把 frequency[prefix-k] 加到答案。
3. 再将当前 prefix 的频次加一。
```

## 复杂度

- 时间复杂度：期望 O(n)，每个元素进行常数次哈希操作。
- 空间复杂度：O(n)，最坏每个前缀和都不同。

## 30 秒识别信号

- 主题型：`数组与哈希`
- 切入点：令 prefix[i] 表示前 i 个元素之和，区间 [left,right] 的和是两个前缀和之差。

## 最小反例与易错点

- 初始化 0 -> 1 不可缺少，否则漏掉从数组起点开始的区间。
- 存频次而不是布尔值；同一前缀和可能多次出现，每次都对应不同起点。

## 分层入口

- [[题目/数组与哈希/560-Subarray-Sum-Equals-K.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/560-Subarray-Sum-Equals-K-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
