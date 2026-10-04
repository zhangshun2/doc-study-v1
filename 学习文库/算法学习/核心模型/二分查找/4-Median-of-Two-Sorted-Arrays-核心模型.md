---
schemaVersion: 3
type: "core-model"
leetcodeId: 4
slug: "median-of-two-sorted-arrays"
titleCn: "寻找两个正序数组的中位数"
titleEn: "Median of Two Sorted Arrays"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/median-of-two-sorted-arrays/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "5c409108fd36de4c1b9288f353aecfa88209022dc5225b90cec7270145e575eb"
primaryPattern: "二分查找"
topics: ["二分查找", "数组", "分治"]
priority: "P0"
problemPath: "题目/二分查找/4-Median-of-Two-Sorted-Arrays.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 4. 寻找两个正序数组的中位数：核心模型

> **双轨阅读：** [[题目/二分查找/4-Median-of-Two-Sorted-Arrays.md|标准题解]]

## 一句话本质

不需要真的合并数组，只需要找到中位数两侧的边界。设分割后左右部分分别为： A: [0 ... i-1] | [i ... m-1] B: [0 ... j-1] | [j ... n-1]

## 直观画面与扩题

像查字典时每翻一次就丢掉确定不可能的一半，关键是保留包含答案的边界。

在本题中，对象是 **搜索区间、边界和中间分割位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：不需要真的合并数组，只需要找到中位数两侧的边界。设分割后左右部分分别为： A: [0 ... i-1] | [i ... m-1] B: [0 ... j-1] | [j ... n-1]

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 搜索区间、边界和中间分割位置 | 把题目翻译成一条可执行关系：不需要真的合并数组，只需要找到中位数两侧的边界。设分割后左右部分分别为： A: [0 ... i-1] \| [i ... m-1] B: [0 ... j-1] \| [j ... n-1] | 在短数组 A 中二分 i，由左侧元素总数确定 j。使用 Integer.MIN_VALUE 和 Integer.MAX_VALUE 表示分割位于数组边缘时不存在的边界。 | 若 aLeft > bRight，A 左侧拿多了，high = i - 1。 | 二分始终搜索所有可能的 A 左侧长度。aLeft > bRight 时，任何更大的 i 只会让 aLeft 不减、bRight 不增，均不可能合法，因此可以排除右半区； | 二分始终搜索所有可能的 A 左侧长度。aLeft > bRight 时，任何更大的 i 只会让 aLeft 不减、bRight 不增，均不可能合法，因此可以排除右半区； |

## 最小演算

官方首例输入：`nums1 = [1,3], nums2 = [2]`，输出：`2.00000`。

1. **初始状态：** 在短数组 A 中二分 i，由左侧元素总数确定 j。
2. **触发事件：** 若 aLeft > bRight，A 左侧拿多了，high = i - 1。
3. **结束条件：** 二分始终搜索所有可能的 A 左侧长度。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

二分始终搜索所有可能的 A 左侧长度。aLeft > bRight 时，任何更大的 i 只会让 aLeft 不减、bRight 不增，均不可能合法，因此可以排除右半区；另一种不等式同理可排除左半区。找到合法分割时，左侧数量正确且所有左侧值不大于所有右侧值，中位数公式因此成立。

## 代码映射

```text
1. 在短数组 A 中二分 i，由左侧元素总数确定 j。
2. 使用 Integer.MIN_VALUE 和 Integer.MAX_VALUE 表示分割位于数组边缘时不存在的边界。
3. 若 aLeft > bRight，A 左侧拿多了，high = i - 1。
```

## 复杂度

- 时间复杂度：O(log(min(m,n)))。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`二分查找`
- 切入点：将合并序列切成左右两部分，使左半部分元素个数为 (m+n+1)/2。

## 最小反例与易错点

- 必须确保 A 是短数组，否则 j 可能越界。
- 左侧元素个数用 (total+1)/2，这样奇数长度时多出的一个归左侧，中位数就是 leftMax。

## 分层入口

- [[题目/二分查找/4-Median-of-Two-Sorted-Arrays.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
