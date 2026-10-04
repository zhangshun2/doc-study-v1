---
schemaVersion: 3
type: "core-model"
leetcodeId: 300
slug: "longest-increasing-subsequence"
titleCn: "最长递增子序列"
titleEn: "Longest Increasing Subsequence"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-increasing-subsequence/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "ff921defc4f92f3d8b9ff5649695ed01a2ee2d85957d59e3be6f267495a26012"
primaryPattern: "动态规划"
topics: ["动态规划", "数组", "二分查找", "最长上升子序列"]
priority: "P0"
problemPath: "题目/动态规划/300-Longest-Increasing-Subsequence.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 300. 最长递增子序列：核心模型

> **双轨阅读：** [[题目/动态规划/300-Longest-Increasing-Subsequence.md|标准题解]]

## 一句话本质

若已经存在两个长度同为 L 的递增子序列，结尾分别为 6 和 10，那么结尾为 6 的序列不会比结尾为 10 的更差。只保留最小结尾即可为未来留出最大空间。 令 tails[i] 表示长度为 i+1 的递增子序列能够取得的最小结尾值。tails 严格递增。

## 直观画面与扩题

像填写一张递推账本，当前格子的答案只由少量已经算好的前序格子决定。

在本题中，对象是 **可复用的子问题状态**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：若已经存在两个长度同为 L 的递增子序列，结尾分别为 6 和 10，那么结尾为 6 的序列不会比结尾为 10 的更差。只保留最小结尾即可为未来留出最大空间。 令 tails[i] 表示长度为 i+1 的递增子序列能够取得的最小结尾值。tails 严格递增。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 可复用的子问题状态 | 把题目翻译成一条可执行关系：若已经存在两个长度同为 L 的递增子序列，结尾分别为 6 和 10，那么结尾为 6 的序列不会比结尾为 10 的更差。 | 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）： 找到则用 num 替换 tails[left]，让该长度的结尾尽可能小。 | 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）： 找到则用 num 替换 tails[left]，让该长度的结尾尽可能小。 | 处理完任意前缀后，tails[i] 是该前缀内所有长度为 i+1 的严格递增子序列中的最小结尾。 | 处理完任意前缀后，tails[i] 是该前缀内所有长度为 i+1 的严格递增子序列中的最小结尾。 |

## 最小演算

官方首例输入：`nums = [10,9,2,5,3,7,101,18]`，输出：`4`。

1. **初始状态：** 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）： 找到则用 num 替换 tails[left]，让该长度的结尾尽可能小。
2. **触发事件：** 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）： 找到则用 num 替换 tails[left]，让该长度的结尾尽可能小。
3. **结束条件：** 处理完任意前缀后，tails[i] 是该前缀内所有长度为 i+1 的严格递增子序列中的最小结尾。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

处理完任意前缀后，tails[i] 是该前缀内所有长度为 i+1 的严格递增子序列中的最小结尾。 对新值 num，第一个 >= num 的位置之前所有结尾都小于 num，故可以从长度 left 的序列扩展出长度 left+1；用 num 更新该长度不会丢失更优选择。

## 代码映射

```text
1. 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）：
2. 逐个处理 num，在 tails[0..size) 中查找第一个 >= num 的位置 left（lower bound）： 找到则用 num 替换 tails[left]，让该长度的结尾尽可能小。
3. 处理完任意前缀后，tails[i] 是该前缀内所有长度为 i+1 的严格递增子序列中的最小结尾。
```

## 复杂度

- 时间复杂度：O(n log n)，每个元素做一次二分。
- 空间复杂度：O(n)，保存 tails。

## 30 秒识别信号

- 主题型：`动态规划`
- 切入点：基础 DP：dp[i] 表示以 nums[i] 结尾的 LIS 长度。

## 最小反例与易错点

- 严格递增需要找第一个 >= num 的位置；若找第一个 > num，会把相等值错误地延长。
- tails 通常不是某一条真实 LIS，不能直接当作答案序列输出。

## 分层入口

- [[题目/动态规划/300-Longest-Increasing-Subsequence.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
