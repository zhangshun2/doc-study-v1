---
schemaVersion: 3
type: "core-model"
leetcodeId: 124
slug: "binary-tree-maximum-path-sum"
titleCn: "二叉树中的最大路径和"
titleEn: "Binary Tree Maximum Path Sum"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/binary-tree-maximum-path-sum/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "6457b9cf60daf8909e113ca24b0e16a929eaf68fa833b70c68df2e1ab471a63a"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "深度优先搜索", "动态规划", "树形 DP"]
priority: "P0"
problemPath: "题目/二叉树/124-Binary-Tree-Maximum-Path-Sum.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 124. 二叉树中的最大路径和：核心模型

> **双轨阅读：** [[题目/二叉树/124-Binary-Tree-Maximum-Path-Sum.md|标准题解]]

## 一句话本质

递归让每个节点分别回答一个问题：“向上贡献多少？”和“以我为最高点，能形成多大的完整路径？”

## 直观画面与扩题

像每个路口向父路口只报告最强的一条单线路，同时在本地比较“左路 + 自己 + 右路”能否刷新全局最佳。

在本题中，对象是 **当前节点、左右子树向上贡献、当前节点为最高点的完整路径和**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

gain(node)=node.val+max(0,gain(left),gain(right))；完整路径和=node.val+max(0,gain(left))+max(0,gain(right))。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 当前节点、左右子树向上贡献、当前节点为最高点的完整路径和 | gain(node)=node.val+max(0,gain(left),gain(right))； | 递归返回值 gain(node) 与全局答案 best。gain 只允许选择一条向下分支，best 记录任一节点处计算出的完整路径最大值。 | 后序处理当前节点：先取得两个孩子的 gain，再把非负贡献相加更新 best。 | 每次 gain(node) 返回后，它都是 node 向下连接至多一条分支时的最大非空路径和。 | 遍历所有节点后，best 是所有完整路径和的最大值。 |

## 最小演算

官方首例输入：`root = [1,2,3]`，输出：`6`。

1. **初始状态：** 递归返回值 gain(node) 与全局答案 best。
2. **触发事件：** 后序处理当前节点：先取得两个孩子的 gain，再把非负贡献相加更新 best。
3. **结束条件：** 遍历所有节点后，best 是所有完整路径和的最大值。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每条简单路径都有唯一最高节点；该节点处恰好可以组合左右贡献，而向上返回时只能保留一支，因此分类完整且不会构造分叉路径。

## 代码映射

```text
1. 令 best=Integer.MIN_VALUE。
2. 后序遍历 node。
3. 取得左侧最大贡献 max(0,gain(left))。
4. 取得右侧最大贡献 max(0,gain(right))。
5. 用 node.val+left+right 更新 best。
6. 返回 node.val+max(left,right) 作为向上单支贡献。
```

## 复杂度

- 时间复杂度：O(n)，每个节点处理一次。
- 空间复杂度：O(h) 递归栈，最坏链状树为 O(n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：树路径允许在某个节点汇合但不能继续分叉，并且子树只需向父节点报告一个最优标量。

## 最小反例与易错点

- best 不能初始化为 0，否则全负树会错误返回 0。
- 更新 best 可以同时使用左右两支；返回父节点时只能选贡献更大的一支。

## 分层入口

- [[题目/二叉树/124-Binary-Tree-Maximum-Path-Sum.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
