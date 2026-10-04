---
schemaVersion: 3
type: "core-model"
leetcodeId: 226
slug: "invert-binary-tree"
titleCn: "翻转二叉树"
titleEn: "Invert Binary Tree"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/invert-binary-tree/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "2edcd345fa15cf33650c40afed066b6e441dfd3720035e042799d8ef43c3fbcc"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "深度优先搜索", "广度优先搜索"]
priority: "P2"
problemPath: "题目/二叉树/226-Invert-Binary-Tree.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 226. 翻转二叉树：核心模型

> **双轨阅读：** [[题目/二叉树/226-Invert-Binary-Tree.md|标准题解]]

## 一句话本质

二叉树具有递归结构。若左右子树已经分别完成镜像，再交换它们的位置，整棵树就是镜像；也可以先交换根的两个孩子，再对交换后的子树执行同样操作。

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：二叉树具有递归结构。若左右子树已经分别完成镜像，再交换它们的位置，整棵树就是镜像；也可以先交换根的两个孩子，再对交换后的子树执行同样操作。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：二叉树具有递归结构。若左右子树已经分别完成镜像，再交换它们的位置，整棵树就是镜像； | 定义 invertTree(root)： 若 root == null，返回 null。递归翻转原左子树和原右子树。 | 若 root == null，返回 null。 | 对树高做归纳。空树显然已经翻转。假设高度小于 h 的树都能被正确翻转。对于高度为 h 的根，递归调用根据归纳假设得到原左右子树的正确镜像，再交换二者位置，恰好满足整棵树中所有左右方向反转。 | 若 root == null，返回 null。递归翻转原左子树和原右子树。把翻转后的右子树赋给 root.left，翻转后的左子树赋给 root.right。 |

## 最小演算

官方首例输入：`root = [4,2,7,1,3,6,9]`，输出：`[4,7,2,9,6,3,1]`。

1. **初始状态：** 定义 invertTree(root)： 若 root == null，返回 null。
2. **触发事件：** 若 root == null，返回 null。
3. **结束条件：** 若 root == null，返回 null。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

对树高做归纳。空树显然已经翻转。假设高度小于 h 的树都能被正确翻转。对于高度为 h 的根，递归调用根据归纳假设得到原左右子树的正确镜像，再交换二者位置，恰好满足整棵树中所有左右方向反转。因此算法对任意高度的二叉树正确。

## 代码映射

```text
1. 若 root == null，返回 null。
2. 递归翻转原左子树和原右子树。
3. 把翻转后的右子树赋给 root.left，翻转后的左子树赋给 root.right。
4. 返回 root。
```

## 复杂度

- 时间复杂度：O(n)，访问每个节点一次。
- 空间复杂度：O(h) 递归栈，h 为树高；平衡树为 O(log n)，链状树最坏 O(n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：整棵树翻转等价于：根节点左右孩子互换，并递归翻转两棵子树。

## 最小反例与易错点

- 空树必须直接返回 null。
- 算法原地修改原树；若要保留原树，应创建新节点构造镜像副本。

## 分层入口

- [[题目/二叉树/226-Invert-Binary-Tree.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
