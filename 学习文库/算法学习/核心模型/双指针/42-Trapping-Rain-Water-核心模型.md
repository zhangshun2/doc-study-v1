---
schemaVersion: 3
type: "core-model"
leetcodeId: 42
slug: "trapping-rain-water"
titleCn: "接雨水"
titleEn: "Trapping Rain Water"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/trapping-rain-water/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "f80b40d341f0c9f5042ef29773ff6d8420701db424a38e83bf30d55430c32866"
primaryPattern: "双指针"
topics: ["双指针", "栈", "数组", "动态规划", "单调栈"]
priority: "P0"
problemPath: "题目/双指针/42-Trapping-Rain-Water.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 42. 接雨水：核心模型

> **双轨阅读：** [[题目/双指针/42-Trapping-Rain-Water.md|标准题解]]

## 一句话本质

单个位置能接水必须同时有左墙和右墙，水位取两边最高墙的较小值。双指针不显式保存每个位置的左右最大值，而是维护当前区间外已经看到的 leftMax 与 rightMax。 当 leftMax <= rightMax 时，左指针位置右侧至少存在一面高为 rightMax 的墙，因此短板确定为 leftMax，该位置可立即结算 leftMax-height[left]。另一侧完全对称。

## 直观画面与扩题

像两个人从两端向中间收网，每走一步都能排除一批不可能答案。

在本题中，对象是 **有序区间两端的候选位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：单个位置能接水必须同时有左墙和右墙，水位取两边最高墙的较小值。双指针不显式保存每个位置的左右最大值，而是维护当前区间外已经看到的 leftMax 与 rightMax。 当 leftMax <= rightMax 时，左指针位置右侧至少存在一面高为 rightMax 的墙，因此短板确定为 leftMax，该位置可立即结算 leftMax-height[left]。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 有序区间两端的候选位置 | 把题目翻译成一条可执行关系：单个位置能接水必须同时有左墙和右墙，水位取两边最高墙的较小值。 | 令 left=0、right=n-1，并维护两侧扫描历史最高值。每轮更新两个最高值： leftMax <= rightMax：结算 left，然后 left++。 | 令 left=0、right=n-1，并维护两侧扫描历史最高值。 | 循环开始时，区间外位置均已正确结算；leftMax 与 rightMax 分别是从数组两端到当前指针的最大高度。 | 循环开始时，区间外位置均已正确结算；leftMax 与 rightMax 分别是从数组两端到当前指针的最大高度。 |

## 最小演算

官方首例输入：`height = [0,1,0,2,1,0,1,3,2,1,2,1]`，输出：`6`。

1. **初始状态：** 令 left=0、right=n-1，并维护两侧扫描历史最高值。
2. **触发事件：** 令 left=0、right=n-1，并维护两侧扫描历史最高值。
3. **结束条件：** 循环开始时，区间外位置均已正确结算；leftMax 与 rightMax 分别是从数组两端到当前指针的最大高度。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

循环开始时，区间外位置均已正确结算；leftMax 与 rightMax 分别是从数组两端到当前指针的最大高度。若 leftMax <= rightMax，当前左位置的左侧上界为 leftMax，右侧又已确认存在高度至少为 rightMax 的柱子，所以最终水位恰为 leftMax，可安全结算。右侧情况对称。每轮永久解决一个位置，直至所有位置处理完毕，因此总和正确。

## 代码映射

```text
1. 令 left=0、right=n-1，并维护两侧扫描历史最高值。
2. 每轮更新两个最高值：
3. 令 left=0、right=n-1，并维护两侧扫描历史最高值。每轮更新两个最高值： leftMax <= rightMax：结算 left，然后 left++。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`双指针`
- 切入点：位置 i 的水量为 min(leftMax[i], rightMax[i]) - height[i]，结果不会为负。

## 最小反例与易错点

- 本题是逐列累加水量，不是选择两根柱子求矩形面积；不要与第 11 题混淆。
- 必须使用两侧“历史最高值”，不能只比较 height[left] 和 height[right] 后随意套公式。

## 分层入口

- [[题目/双指针/42-Trapping-Rain-Water.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
