---
schemaVersion: 3
type: "core-model"
leetcodeId: 101
slug: "symmetric-tree"
titleCn: "对称二叉树"
titleEn: "Symmetric Tree"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/symmetric-tree/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "6df8091f2cca178a8377d3007f3c0f014d9020ed94b3d730894e70feec44e5fa"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "深度优先搜索", "广度优先搜索"]
priority: "P2"
problemPath: "题目/二叉树/101-Symmetric-Tree.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 101. 对称二叉树：核心模型

> **双轨阅读：** [[题目/二叉树/101-Symmetric-Tree.md|标准题解]]

## 一句话本质

定义 isMirror(a,b) 判断两棵树是否互为镜像。镜像的递归定义为： a 和 b 都为空；或者 a.val == b.val 且 a.left 与 b.right 镜像 且 a.right 与 b.left 镜像

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：定义 isMirror(a,b) 判断两棵树是否互为镜像。镜像的递归定义为： a 和 b 都为空；或者 a.val == b.val 且 a.left 与 b.right 镜像 且 a.right 与 b.left 镜像

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：定义 isMirror(a,b) 判断两棵树是否互为镜像。镜像的递归定义为： a 和 b 都为空； | 这比先分别遍历左右子树再比较序列更直接，因为单独的遍历序列若不记录空节点，可能丢失结构信息。 | 两者均为空，当前这一对对称。 | 每次调用 isMirror(left,right) 都判断关于整棵树中轴处于对应位置的两个子树。 | 每次调用 isMirror(left,right) 都判断关于整棵树中轴处于对应位置的两个子树。 |

## 最小演算

官方首例输入：`root = [1,2,2,3,4,4,3]`，输出：`true`。

1. **初始状态：** 这比先分别遍历左右子树再比较序列更直接，因为单独的遍历序列若不记录空节点，可能丢失结构信息。
2. **触发事件：** 两者均为空，当前这一对对称。
3. **结束条件：** 每次调用 isMirror(left,right) 都判断关于整棵树中轴处于对应位置的两个子树。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每次调用 isMirror(left,right) 都判断关于整棵树中轴处于对应位置的两个子树。空状态和节点值检查保证当前根结构和值相同；交叉递归恰好检查镜像定义要求的两对子树。通过结构归纳，叶节点对满足条件，若两对子树均镜像则当前两树镜像；任何结构或值差异都会在对应层被检测。

## 代码映射

```text
1. 两者均为空，当前这一对对称。
2. 恰有一个为空，结构不对称。
3. 值不同，不对称。
4. 递归比较外侧一对和内侧一对，两者都通过才对称。
```

## 复杂度

- 时间复杂度：O(n)，每个节点最多访问一次。
- 空间复杂度：O(h) 递归栈，最坏 O(n)，平衡树为 O(log n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：不要写一个只接收单节点的普通遍历函数；镜像判断天然需要同时接收两个节点。

## 最小反例与易错点

- root 按题目约束非空；若用于通用代码，可先处理 root == null 为 true。
- 不能比较 left.left 与 right.left，镜像需要交叉比较。

## 分层入口

- [[题目/二叉树/101-Symmetric-Tree.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
