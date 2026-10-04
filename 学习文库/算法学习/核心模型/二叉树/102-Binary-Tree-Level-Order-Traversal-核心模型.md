---
schemaVersion: 3
type: "core-model"
leetcodeId: 102
slug: "binary-tree-level-order-traversal"
titleCn: "二叉树的层序遍历"
titleEn: "Binary Tree Level Order Traversal"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/binary-tree-level-order-traversal/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "7140380f10d13897dd22f942555d8dbf40c62c69b889dc26960571656433e154"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "广度优先搜索"]
priority: "P0"
problemPath: "题目/二叉树/102-Binary-Tree-Level-Order-Traversal.md"
deepDivePath: "建模专题/T0/102-Binary-Tree-Level-Order-Traversal-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 102. 二叉树的层序遍历：核心模型

> **双轨阅读：** [[题目/二叉树/102-Binary-Tree-Level-Order-Traversal.md|标准题解]] · [[建模专题/T0/102-Binary-Tree-Level-Order-Traversal-直观建模.md|完整建模]]

## 一句话本质

若当前队列按从左到右顺序只包含某一层节点，那么依次弹出这些节点，并按左孩子、右孩子的顺序入队，队列随后就会按从左到右顺序只包含下一层节点。queue.size() 的快照因此能准确切分层次。

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：若当前队列按从左到右顺序只包含某一层节点，那么依次弹出这些节点，并按左孩子、右孩子的顺序入队，队列随后就会按从左到右顺序只包含下一层节点。queue.size() 的快照因此能准确切分层次。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：若当前队列按从左到右顺序只包含某一层节点，那么依次弹出这些节点，并按左孩子、右孩子的顺序入队，队列随后就会按从左到右顺序只包含下一层节点。 | 外层循环每次处理一层，先保存本层大小。内层恰好弹出本层节点，将值加入 level，并把非空孩子入队。 | 外层循环每次处理一层，先保存本层大小。 | 每轮外层循环开始时，队列恰好按从左到右顺序保存当前层的所有节点。固定的 levelSize 保证本轮只弹出这些节点； | 根为空时直接返回空结果。根节点入队。外层循环每次处理一层，先保存本层大小。内层恰好弹出本层节点，将值加入 level，并把非空孩子入队。 |

## 最小演算

官方首例输入：`root = [3,9,20,null,null,15,7]`，输出：`[[3],[9,20],[15,7]]`。

1. **初始状态：** 外层循环每次处理一层，先保存本层大小。
2. **触发事件：** 外层循环每次处理一层，先保存本层大小。
3. **结束条件：** 根为空时直接返回空结果。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮外层循环开始时，队列恰好按从左到右顺序保存当前层的所有节点。固定的 levelSize 保证本轮只弹出这些节点；每个父节点按左后右加入孩子，而父节点本身也从左到右处理，所以新入队节点正好构成下一层的正确顺序。由层数归纳，所有层均被完整、按序输出。

## 代码映射

```text
1. 根为空时直接返回空结果。
2. 根节点入队。
3. 外层循环每次处理一层，先保存本层大小。
4. 内层恰好弹出本层节点，将值加入 level，并把非空孩子入队。
5. 内层结束后把 level 加入结果。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(w)，w 为树的最大宽度，最坏 O(n)；返回结果另占 O(n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：队列天然按“先发现、先处理”的顺序访问同一层节点。

## 最小反例与易错点

- levelSize 必须在内层循环前保存，不能让循环条件动态读取不断增长的 queue.size()。
- 空孩子不应入 ArrayDeque，因为它不允许 null。

## 分层入口

- [[题目/二叉树/102-Binary-Tree-Level-Order-Traversal.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/102-Binary-Tree-Level-Order-Traversal-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
