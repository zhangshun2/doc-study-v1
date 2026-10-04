---
schemaVersion: 3
type: "core-model"
leetcodeId: 94
slug: "binary-tree-inorder-traversal"
titleCn: "二叉树的中序遍历"
titleEn: "Binary Tree Inorder Traversal"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/binary-tree-inorder-traversal/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "41a18eedbae0891524b44702a8d101a30a0bcd0f53cc484289edffcd3871d05d"
primaryPattern: "二叉树"
topics: ["二叉树", "栈", "树", "深度优先搜索"]
priority: "P0"
problemPath: "题目/二叉树/94-Binary-Tree-Inorder-Traversal.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 94. 二叉树的中序遍历：核心模型

> **双轨阅读：** [[题目/二叉树/94-Binary-Tree-Inorder-Traversal.md|标准题解]]

## 一句话本质

递归调用栈实际上保存了“左子树处理完后还要回来访问”的祖先节点。显式栈只是把这件事写出来： 一路向左：保存尚未访问的根 弹出栈顶：左子树已经完成，现在访问根 转向右子树：重复相同过程

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：递归调用栈实际上保存了“左子树处理完后还要回来访问”的祖先节点。显式栈只是把这件事写出来： 一路向左：保存尚未访问的根 弹出栈顶：左子树已经完成，现在访问根 转向右子树：重复相同过程

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：递归调用栈实际上保存了“左子树处理完后还要回来访问”的祖先节点。 | current 非空时不断压栈并向左。到达空指针后弹出栈顶，把值加入答案。将 current 指向被访问节点的右孩子。 | 到达空指针后弹出栈顶，把值加入答案。 | 栈中的每个节点都已经开始处理，但其自身和右子树尚未访问；current 指向下一棵需要展开的子树。 | 栈中的每个节点都已经开始处理，但其自身和右子树尚未访问；current 指向下一棵需要展开的子树。 |

## 最小演算

官方首例输入：`root = [1,null,2,3]`，输出：`[1,3,2]`。

1. **初始状态：** current 非空时不断压栈并向左。
2. **触发事件：** 到达空指针后弹出栈顶，把值加入答案。
3. **结束条件：** 栈中的每个节点都已经开始处理，但其自身和右子树尚未访问；current 指向下一棵需要展开的子树。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

栈中的每个节点都已经开始处理，但其自身和右子树尚未访问；current 指向下一棵需要展开的子树。持续向左保证弹出的节点已无未处理左子树，因此可按中序访问它；转向其右孩子后又建立相同状态。每个节点入栈、弹栈各一次，最终顺序恰为左、根、右。

## 代码映射

```text
1. current 非空时不断压栈并向左。
2. 到达空指针后弹出栈顶，把值加入答案。
3. 将 current 指向被访问节点的右孩子。
4. 当前为空且栈也为空时结束。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(h)，最坏退化树为 O(n)，平衡树为 O(log n)；不计输出列表。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：中序的“根”要等左子树处理完才访问，所以需要保存沿途节点。

## 最小反例与易错点

- ArrayDeque 不允许压入 null，只在节点非空时 push。
- 外层不能只写 current != null，否则走到最左空位置时会提前结束。

## 分层入口

- [[题目/二叉树/94-Binary-Tree-Inorder-Traversal.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
