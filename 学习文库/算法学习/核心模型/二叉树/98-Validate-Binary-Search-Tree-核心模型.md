---
schemaVersion: 3
type: "core-model"
leetcodeId: 98
slug: "validate-binary-search-tree"
titleCn: "验证二叉搜索树"
titleEn: "Validate Binary Search Tree"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/validate-binary-search-tree/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "d8e6532f1a37916ef3c9e048a1ca162a4a9c7905bfb5b379774a7baa592e5c78"
primaryPattern: "二叉树"
topics: ["二叉树", "树", "深度优先搜索", "二叉搜索树"]
priority: "P2"
problemPath: "题目/二叉树/98-Validate-Binary-Search-Tree.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 98. 验证二叉搜索树：核心模型

> **双轨阅读：** [[题目/二叉树/98-Validate-Binary-Search-Tree.md|标准题解]]

## 一句话本质

每个节点都有一个由祖先共同决定的合法开区间 (lower,upper)。根节点范围是负无穷到正无穷： 检查节点值满足 lower < val < upper。 左孩子继承下界，并把当前值作为新上界。

## 直观画面与扩题

像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。

在本题中，对象是 **子树返回信息与当前节点**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：每个节点都有一个由祖先共同决定的合法开区间 (lower,upper)。根节点范围是负无穷到正无穷： 检查节点值满足 lower < val < upper。 左孩子继承下界，并把当前值作为新上界。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 子树返回信息与当前节点 | 把题目翻译成一条可执行关系：每个节点都有一个由祖先共同决定的合法开区间 (lower,upper)。 | 把祖先约束作为递归参数传下去。使用 long lower、long upper，根节点初值为 Long.MIN_VALUE 和 Long.MAX_VALUE，从而允许节点本身取任意 int 值。 | 把祖先约束作为递归参数传下去。 | 调用 validate(node,lower,upper) 时，区间恰好表示该位置由全部祖先施加的值限制。 | 遇到空节点返回 true。当前值越界立即返回 false，否则递归验证左右子树，两个结果必须都为真。 |

## 最小演算

官方首例输入：`root = [2,1,3]`，输出：`true`。

1. **初始状态：** 把祖先约束作为递归参数传下去。
2. **触发事件：** 把祖先约束作为递归参数传下去。
3. **结束条件：** 遇到空节点返回 true。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

调用 validate(node,lower,upper) 时，区间恰好表示该位置由全部祖先施加的值限制。当前节点满足区间后，左子树增加“严格小于当前值”的限制，右子树增加“严格大于当前值”的限制。若递归全部成功，则任意节点都满足所有祖先关系，符合 BST 定义；若存在违反定义的节点，它必会超出递归传递到该处的区间而被发现。

## 代码映射

```text
1. 把祖先约束作为递归参数传下去。
2. 使用 long lower、long upper，根节点初值为 Long.MIN_VALUE 和 Long.MAX_VALUE，从而允许节点本身取任意 int 值。
3. 把祖先约束作为递归参数传下去。使用 long lower、long upper，根节点初值为 Long.MIN_VALUE 和 Long.MAX_VALUE，从而允许节点本身取任意 int 值。
```

## 复杂度

- 时间复杂度：O(n)，每个节点访问一次。
- 空间复杂度：O(h) 递归栈，最坏 O(n)，平衡树为 O(log n)。

## 30 秒识别信号

- 主题型：`二叉树`
- 切入点：只比较节点与左右孩子是不够的，右子树深处仍必须大于根节点。

## 最小反例与易错点

- 重复值不合法，比较必须使用 <= 和 >= 判错。
- 不要用 Integer.MIN_VALUE 作为开区间下界，否则值恰好为该极值的合法根会被误判。

## 分层入口

- [[题目/二叉树/98-Validate-Binary-Search-Tree.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
