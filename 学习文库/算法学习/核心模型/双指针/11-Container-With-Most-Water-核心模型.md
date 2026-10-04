---
schemaVersion: 3
type: "core-model"
leetcodeId: 11
slug: "container-with-most-water"
titleCn: "盛最多水的容器"
titleEn: "Container With Most Water"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/container-with-most-water/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "829357544b8af653c7cb84a6b9c8fefc1b5d49f71fb9174d3e6f414574f39f62"
primaryPattern: "双指针"
topics: ["双指针", "贪心", "数组"]
priority: "P0"
problemPath: "题目/双指针/11-Container-With-Most-Water.md"
deepDivePath: "建模专题/T0/11-Container-With-Most-Water-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 11. 盛最多水的容器：核心模型

> **双轨阅读：** [[题目/双指针/11-Container-With-Most-Water.md|标准题解]] · [[建模专题/T0/11-Container-With-Most-Water-直观建模.md|完整建模]]

## 一句话本质

面积同时受宽度和短板控制。左右指针初始拥有最大宽度。假设 height[left] <= height[right]，保持 left 不动而把 right 左移：新宽度更小，新高度仍不超过 height[left]，所以面积一定不超过当前面积。于是所有以当前 left 为左边界、右端位于内部的方案都可一次排除，应移动 left。

## 直观画面与扩题

像两个人从两端向中间收网，每走一步都能排除一批不可能答案。

在本题中，对象是 **有序区间两端的候选位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：面积同时受宽度和短板控制。左右指针初始拥有最大宽度。假设 height[left] <= height[right]，保持 left 不动而把 right 左移：新宽度更小，新高度仍不超过 height[left]，所以面积一定不超过当前面积。于是所有以当前 left 为左边界、右端位于内部的方案都可一次排除，应移动 left。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 有序区间两端的候选位置 | 把题目翻译成一条可执行关系：面积同时受宽度和短板控制。左右指针初始拥有最大宽度。假设 height[left] <= height[right]，保持 left 不动而把 right 左移：新宽度更小，新高度仍不超过 height[left]，所以面积一定不超过当前面积。 | 指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。相等时移动任意一侧都不会漏掉更优解； | 指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。 | 当前区间外的边界组合均已被证明不可能优于已记录答案。每轮若左边较短，所有使用该左边界和更靠内右边界的容器，宽度更小且高度上限不变，因此都不可能超过当前容器，可以安全排除左边界。 | 当前区间外的边界组合均已被证明不可能优于已记录答案。每轮若左边较短，所有使用该左边界和更靠内右边界的容器，宽度更小且高度上限不变，因此都不可能超过当前容器，可以安全排除左边界。 |

## 最小演算

官方首例输入：`[1,8,6,2,5,4,8,3,7]`，输出：`49`。

1. **初始状态：** 指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。
2. **触发事件：** 指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。
3. **结束条件：** 当前区间外的边界组合均已被证明不可能优于已记录答案。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

当前区间外的边界组合均已被证明不可能优于已记录答案。每轮若左边较短，所有使用该左边界和更靠内右边界的容器，宽度更小且高度上限不变，因此都不可能超过当前容器，可以安全排除左边界。右边较短时对称成立。算法不断安全排除一个边界，直至所有候选均已计算或被支配，best 即全局最优值。

## 代码映射

```text
1. 指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。
2. 相等时移动任意一侧都不会漏掉更优解；
3. 代码选择移动右侧。
```

## 复杂度

- 时间复杂度：O(n)，每个指针最多移动 n-1 次。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`双指针`
- 切入点：一对边界的面积是 (right-left) * min(height[left],height[right])。

## 最小反例与易错点

- 高度用 min，不是 max；水会从较短边界溢出。
- 宽度是下标差 right-left，不是元素个数 right-left+1。

## 分层入口

- [[题目/双指针/11-Container-With-Most-Water.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/11-Container-With-Most-Water-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
