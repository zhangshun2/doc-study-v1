---
schemaVersion: 3
type: "core-model"
leetcodeId: 238
slug: "product-of-array-except-self"
titleCn: "除了自身以外数组的乘积"
titleEn: "Product of Array Except Self"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/product-of-array-except-self/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "fa3260ef4dccb3742fa42c3f1ee4864fbc229159dcb345dc8152931450f00fa2"
primaryPattern: "数组与哈希"
topics: ["数组与哈希", "数组", "前缀和"]
priority: "P1"
problemPath: "题目/数组与哈希/238-Product-of-Array-Except-Self.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 238. 除了自身以外数组的乘积：核心模型

> **双轨阅读：** [[题目/数组与哈希/238-Product-of-Array-Except-Self.md|标准题解]]

## 一句话本质

对位置 i： answer[i] = 左侧元素 nums[0..i-1] 的乘积 右侧元素 nums[i+1..n-1] 的乘积 = prefixBefore(i) * suffixAfter(i)

## 直观画面与扩题

像边收卡片边登记索引：每来一张，就先查旧记录里有没有能配对的卡片。

在本题中，对象是 **数组元素与下标、已经扫描过的历史信息**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：对位置 i： answer[i] = 左侧元素 nums[0..i-1] 的乘积 右侧元素 nums[i+1..n-1] 的乘积 = prefixBefore(i) * suffixAfter(i)

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 数组元素与下标、已经扫描过的历史信息 | 把题目翻译成一条可执行关系：对位置 i： answer[i] = 左侧元素 nums[0..i-1] 的乘积 右侧元素 nums[i+1..n-1] 的乘积 = prefixBefore(i) * suffixAfter(i) | 第二遍从右到左，维护 suffix 为 i 右侧全部元素乘积：先执行 answer[i] *= suffix，再执行 suffix *= nums[i]。 | 第一遍从左到右，令 answer[i] 等于 i 左侧全部元素乘积。 | 第一遍处理位置 i 前，累计变量是 nums[0..i) 的乘积，所以写入的正是左侧积。第二遍处理位置 i 前，suffix 是 nums(i..n) 即 nums[i+1..n-1] 的乘积。 | 第二遍处理位置 i 前，suffix 是 nums(i..n) 即 nums[i+1..n-1] 的乘积。 |

## 最小演算

官方首例输入：`nums = [1,2,3,4]`，输出：`[24,12,8,6]`。

1. **初始状态：** 第二遍从右到左，维护 suffix 为 i 右侧全部元素乘积：先执行 answer[i] *= suffix，再执行 suffix *= nums[i]。
2. **触发事件：** 第一遍从左到右，令 answer[i] 等于 i 左侧全部元素乘积。
3. **结束条件：** 第二遍处理位置 i 前，suffix 是 nums(i..n) 即 nums[i+1..n-1] 的乘积。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

第一遍处理位置 i 前，累计变量是 nums[0..i) 的乘积，所以写入的正是左侧积。 第二遍处理位置 i 前，suffix 是 nums(i..n) 即 nums[i+1..n-1] 的乘积。输出中原有左侧积，乘上 suffix 后恰为除自身外所有元素的乘积。更新后不变量对下一个位置成立。

## 代码映射

```text
1. 第一遍从左到右，令 answer[i] 等于 i 左侧全部元素乘积。
2. 初始化左侧空积为 1。
3. 第二遍从右到左，维护 suffix 为 i 右侧全部元素乘积：先执行 answer[i] *= suffix，再执行 suffix *= nums[i]。顺序不能颠倒，否则会错误地把自身乘入。
```

## 复杂度

- 时间复杂度：O(n)，两次线性扫描。
- 空间复杂度：O(1) 额外空间，不计必须返回的 answer 数组。

## 30 秒识别信号

- 主题型：`数组与哈希`
- 切入点：answer[i] 可以拆成左边所有元素乘积乘以右边所有元素乘积。

## 最小反例与易错点

- 空集合的乘积定义为 1，因此 prefix、suffix 初值都必须是 1。
- 第二遍必须先乘 suffix，再把当前 nums[i] 纳入后缀积。

## 分层入口

- [[题目/数组与哈希/238-Product-of-Array-Except-Self.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
