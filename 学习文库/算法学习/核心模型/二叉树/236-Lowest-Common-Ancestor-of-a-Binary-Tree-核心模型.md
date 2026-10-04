---
schemaVersion: 3
type: "core-model"
leetcodeId: 236
slug: "lowest-common-ancestor-of-a-binary-tree"
titleCn: "二叉树的最近公共祖先"
titleEn: "Lowest Common Ancestor of a Binary Tree"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "bee8794928fac787cbb359b2271ef64f2fae52970fa6d9dcfa1f6470bfc2ada8"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "深度优先搜索", "最近公共祖先", "Binary Lifting"]
priority: "P0"
problemPath: "题目/二叉树/236-Lowest-Common-Ancestor-of-a-Binary-Tree.md"
deepDivePath: "建模专题/T0/236-Lowest-Common-Ancestor-of-a-Binary-Tree-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 236. 二叉树的最近公共祖先：核心模型

> **双轨阅读：** [[题目/二叉树/236-Lowest-Common-Ancestor-of-a-Binary-Tree.md|标准题解]] · [[建模专题/T0/236-Lowest-Common-Ancestor-of-a-Binary-Tree-直观建模.md|完整建模]]

## 一句话本质

递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。在题目保证两节点存在的前提下，可以让函数返回：当前子树中若含目标或其最近公共祖先，则返回该关键节点；否则返回 null。

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。在题目保证两节点存在的前提下，可以让函数返回：当前子树中若含目标或其最近公共祖先，则返回该关键节点；否则返回 null。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。 | 递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。在题目保证两节点存在的前提下，可以让函数返回：当前子树中若含目标或其最近公共祖先，则返回该关键节点； | 分别递归左右子树，得到 left、right。 | 对任意子树，递归返回值满足： 不含 p、q 时返回 null。只含其中一个时返回该目标节点。 | 对任意子树，递归返回值满足： 不含 p、q 时返回 null。只含其中一个时返回该目标节点。 |

## 最小演算

官方首例输入：`root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1`，输出：`3`。

1. **初始状态：** 递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。
2. **触发事件：** 分别递归左右子树，得到 left、right。
3. **结束条件：** 对任意子树，递归返回值满足： 不含 p、q 时返回 null。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

对任意子树，递归返回值满足： 不含 p、q 时返回 null。

## 代码映射

```text
1. root == null 返回 null。
2. root == p || root == q，返回 root。
3. 分别递归左右子树，得到 left、right。
4. 两者都非空，说明 p、q 分处两边，当前节点是 LCA。
5. 否则返回唯一非空结果；都为空则返回 null。
```

## 复杂度

- 时间复杂度：O(n)，最坏访问每个节点一次。
- 空间复杂度：O(h) 递归栈；平衡树为 O(log n)，链状树最坏 O(n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：若当前节点就是 p 或 q，它应向上报告“找到了目标”。

## 最小反例与易错点

- 必须接受“一个目标是另一个目标祖先”的情况，命中目标时直接返回。
- 比较 root == p 使用节点引用，避免节点值不唯一的变式中出错。

## 分层入口

- [[题目/二叉树/236-Lowest-Common-Ancestor-of-a-Binary-Tree.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/236-Lowest-Common-Ancestor-of-a-Binary-Tree-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
