---
schemaVersion: 3
type: "core-model"
leetcodeId: 287
slug: "find-the-duplicate-number"
titleCn: "寻找重复数"
titleEn: "Find the Duplicate Number"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/find-the-duplicate-number/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "40d8542d22206458b7ab6ebb5c11c3e79f418ec8db3cf1a030a3219fa1cef516"
primaryPattern: "数组与哈希"
topics: ["数组与哈希", "位运算", "数组", "双指针", "二分查找", "Floyd 判圈算法", "抽屉原理"]
priority: "P1"
problemPath: "题目/数组与哈希/287-Find-the-Duplicate-Number.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 287. 寻找重复数：核心模型

> **双轨阅读：** [[题目/数组与哈希/287-Find-the-Duplicate-Number.md|标准题解]]

## 一句话本质

函数图中每个节点只有一个后继。数组有 n + 1 个位置但值只有 n 种，根据抽屉原理存在重复指向。从 0 沿 nums[index] 前进，会形成“链尾 + 环”。重复数就是环入口，可用 Floyd 算法在 O(1) 空间找到。

## 直观画面与扩题

像边收卡片边登记索引：每来一张，就先查旧记录里有没有能配对的卡片。

在本题中，对象是 **数组元素与下标、已经扫描过的历史信息**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：函数图中每个节点只有一个后继。数组有 n + 1 个位置但值只有 n 种，根据抽屉原理存在重复指向。从 0 沿 nums[index] 前进，会形成“链尾 + 环”。重复数就是环入口，可用 Floyd 算法在 O(1) 空间找到。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 数组元素与下标、已经扫描过的历史信息 | 把题目翻译成一条可执行关系：函数图中每个节点只有一个后继。数组有 n + 1 个位置但值只有 n 种，根据抽屉原理存在重复指向。 | 函数图中每个节点只有一个后继。数组有 n + 1 个位置但值只有 n 种，根据抽屉原理存在重复指向。 | 第一阶段找相遇点：慢指针每次走一步 slow = nums[slow]，快指针每次走两步 fast = nums[nums[fast]]。 | 设从起点到环入口距离为 a，入口到首次相遇点距离为 b，环长为 c。相遇时慢指针走了 a+b，快指针走了其两倍，二者路程差是若干整环： 2(a+b) - (a+b) = a+b = k*c | 设从起点到环入口距离为 a，入口到首次相遇点距离为 b，环长为 c。相遇时慢指针走了 a+b，快指针走了其两倍，二者路程差是若干整环： 2(a+b) - (a+b) = a+b = k*c |

## 最小演算

官方首例输入：`nums = [1,3,4,2,2]`，输出：`2`。

1. **初始状态：** 函数图中每个节点只有一个后继。
2. **触发事件：** 第一阶段找相遇点：慢指针每次走一步 slow = nums[slow]，快指针每次走两步 fast = nums[nums[fast]]。
3. **结束条件：** 设从起点到环入口距离为 a，入口到首次相遇点距离为 b，环长为 c。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

设从起点到环入口距离为 a，入口到首次相遇点距离为 b，环长为 c。相遇时慢指针走了 a+b，快指针走了其两倍，二者路程差是若干整环： 2(a+b) - (a+b) = a+b = k*c

## 代码映射

```text
1. 第一阶段找相遇点：慢指针每次走一步 slow = nums[slow]，快指针每次走两步 fast = nums[nums[fast]]。
2. 两者必在环内相遇。
3. 函数图中每个节点只有一个后继。数组有 n + 1 个位置但值只有 n 种，根据抽屉原理存在重复指向。从 0 沿 nums[index] 前进，会形成“链尾 + 环”。重复数就是环入口，可用 Floyd 算法在 O(1) 空间找到。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`数组与哈希`
- 切入点：将数组下标看作节点，将 i -> nums[i] 看作一条有向边。

## 最小反例与易错点

- 这里的“节点”是数组下标，下一节点是数组值，不是在普通链表上操作。
- 二阶段起点可一致使用 nums[0]；若采用另一套以 0 为起点的初始化，公式和代码要成套，避免混搭。

## 分层入口

- [[题目/数组与哈希/287-Find-the-Duplicate-Number.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
