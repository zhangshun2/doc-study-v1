---
schemaVersion: 3
type: "core-model"
leetcodeId: 53
slug: "maximum-subarray"
titleCn: "最大子数组和"
titleEn: "Maximum Subarray"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/maximum-subarray/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "a50e13b9fc2f7998def4e76c16e28793a1251c6a3425ab49b51340ae767649a6"
primaryPattern: "动态规划"
topics: ["动态规划", "数组", "分治"]
priority: "P0"
problemPath: "题目/动态规划/53-Maximum-Subarray.md"
deepDivePath: "建模专题/T0/53-Maximum-Subarray-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 53. 最大子数组和：核心模型

> **双轨阅读：** [[题目/动态规划/53-Maximum-Subarray.md|标准题解]] · [[建模专题/T0/53-Maximum-Subarray-直观建模.md|完整建模]]

## 一句话本质

定义 dp[i] 为必须以 nums[i] 结尾的非空连续子数组的最大和。一个以 i 结尾的连续子数组，要么只有 nums[i]，要么把 nums[i] 接到某个以 i - 1 结尾的子数组后面： dp[i] = max(nums[i], dp[i - 1] + nums[i])

## 直观画面与扩题

像填写一张递推账本，当前格子的答案只由少量已经算好的前序格子决定。

在本题中，对象是 **可复用的子问题状态**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：定义 dp[i] 为必须以 nums[i] 结尾的非空连续子数组的最大和。一个以 i 结尾的连续子数组，要么只有 nums[i]，要么把 nums[i] 接到某个以 i - 1 结尾的子数组后面： dp[i] = max(nums[i], dp[i - 1] + nums[i])

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 可复用的子问题状态 | 把题目翻译成一条可执行关系：定义 dp[i] 为必须以 nums[i] 结尾的非空连续子数组的最大和。 | 令 current 表示上一轮的 dp[i - 1]。处理当前值 num 时执行： current = max(num, current + num) | 处理当前值 num 时执行： 令 current 表示上一轮的 dp[i - 1]。处理当前值 num 时执行： current = max(num, current + num) | 遍历到下标 i 后保持两个不变量： current 等于所有以 i 结尾的非空连续子数组中的最大和。 | 第一个不变量成立，因为任何以 i 结尾的连续子数组只能“从 i 开始”或“由以 i-1 结尾的子数组扩展”。 |

## 最小演算

官方首例输入：`nums = [-2,1,-3,4,-1,2,1,-5,4]`，输出：`6`。

1. **初始状态：** 令 current 表示上一轮的 dp[i - 1]。
2. **触发事件：** 处理当前值 num 时执行： 令 current 表示上一轮的 dp[i - 1]。
3. **结束条件：** 第一个不变量成立，因为任何以 i 结尾的连续子数组只能“从 i 开始”或“由以 i-1 结尾的子数组扩展”。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

遍历到下标 i 后保持两个不变量： current 等于所有以 i 结尾的非空连续子数组中的最大和。

## 代码映射

```text
1. 令 current 表示上一轮的 dp[i - 1]。
2. 处理当前值 num 时执行：
3. 处理当前值 num 时执行： 令 current 表示上一轮的 dp[i - 1]。处理当前值 num 时执行： current = max(num, current + num)
```

## 复杂度

- 时间复杂度：O(n)，每个元素只处理一次。
- 空间复杂度：O(1)，只使用两个状态变量。

## 30 秒识别信号

- 主题型：`动态规划`
- 切入点：先不要问“最大子数组从哪里开始”，先问“以位置 i 结尾的最大子数组和是多少”。

## 最小反例与易错点

- 全为负数时答案是最大的那个负数，不能把 best 初始化为 0。
- current 表示必须以当前位置结尾，best 才是全局答案，两者不能混用。

## 分层入口

- [[题目/动态规划/53-Maximum-Subarray.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/53-Maximum-Subarray-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
