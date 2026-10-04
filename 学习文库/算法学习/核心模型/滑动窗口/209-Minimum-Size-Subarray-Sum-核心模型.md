---
schemaVersion: 3
type: "core-model"
leetcodeId: 209
slug: "minimum-size-subarray-sum"
titleCn: "长度最小的子数组"
titleEn: "Minimum Size Subarray Sum"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/minimum-size-subarray-sum/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "d00e4a27c91b276049bc1396e3a449196e674ff55434bbf1f69ea5891955884b"
primaryPattern: "滑动窗口"
topics: ["滑动窗口", "数组", "二分查找", "前缀和"]
priority: "P1"
problemPath: "题目/滑动窗口/209-Minimum-Size-Subarray-Sum.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 209. 长度最小的子数组：核心模型

> **双轨阅读：** [[题目/滑动窗口/209-Minimum-Size-Subarray-Sum.md|标准题解]]

## 一句话本质

元素全为正，窗口和对左右指针具有单调性。右指针扩张是为了首次达到目标；达到后，左指针不断收缩，找到以当前右端点结尾的最短合法窗口。两个指针都只向右走，无需回退。

## 直观画面与扩题

像手持一个可伸缩的取景框，右边纳入新画面，左边只在规则被破坏时收缩。

在本题中，对象是 **连续区间及其左右边界**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：元素全为正，窗口和对左右指针具有单调性。右指针扩张是为了首次达到目标；达到后，左指针不断收缩，找到以当前右端点结尾的最短合法窗口。两个指针都只向右走，无需回退。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 连续区间及其左右边界 | 把题目翻译成一条可执行关系：元素全为正，窗口和对左右指针具有单调性。右指针扩张是为了首次达到目标； | 维护窗口 [left, right] 和 windowSum： 右端加入 nums[right]。 | 右端加入 nums[right]。 | 每轮外层结束前，算法已检查所有右端点不超过 right 的潜在最优合法窗口。对固定 right，收缩循环依次检查所有仍合法的左端点，并在下一次收缩将使窗口不合法时停止； | 每轮外层结束前，算法已检查所有右端点不超过 right 的潜在最优合法窗口。对固定 right，收缩循环依次检查所有仍合法的左端点，并在下一次收缩将使窗口不合法时停止； |

## 最小演算

官方首例输入：`target = 7, nums = [2,3,1,2,4,3]`，输出：`2`。

1. **初始状态：** 维护窗口 [left, right] 和 windowSum： 右端加入 nums[right]。
2. **触发事件：** 右端加入 nums[right]。
3. **结束条件：** 每轮外层结束前，算法已检查所有右端点不超过 right 的潜在最优合法窗口。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

由于正数保证被移除的左端点不可能在未来某个更右端点下产生比当前保留左端点更短的窗口而需要回退，因此不漏解。

## 代码映射

```text
1. 右端加入 nums[right]。
2. 当 windowSum >= target 时，当前窗口合法，更新最短长度。
3. 移除 nums[left] 并令 left++，继续尝试更短窗口。
4. 和不足后，再扩张右端。
```

## 复杂度

- 时间复杂度：O(n)，每个元素最多被右指针加入一次、被左指针移除一次。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`滑动窗口`
- 切入点：固定右边界时，只要窗口和已经达标，就尽量移动左边界缩短窗口。

## 最小反例与易错点

- 无解时返回 0，不是 Integer.MAX_VALUE。
- 长度公式是 right - left + 1。

## 分层入口

- [[题目/滑动窗口/209-Minimum-Size-Subarray-Sum.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
