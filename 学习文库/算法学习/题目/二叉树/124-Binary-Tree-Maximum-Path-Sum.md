---
schemaVersion: 3
type: "problem"
leetcodeId: 124
slug: "binary-tree-maximum-path-sum"
titleCn: "二叉树中的最大路径和"
titleEn: "Binary Tree Maximum Path Sum"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/binary-tree-maximum-path-sum/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "072a45a20f48b1817ce058360ba7385c27e2ac03a491fc76f3228270552bde60"
sourceFactsSha256: "6457b9cf60daf8909e113ca24b0e16a929eaf68fa833b70c68df2e1ab471a63a"
sourceSectionHashes:
  description: "54cae52e53db8ba1da0704f8e5a52ac194e757d347c4d0f9f53d6f6fbbcb5e6a"
  examples: "3fc24eb58a9f8076e30742f5b4a4cc047833ecc92dadb4988bf740f4d450a38d"
  constraints: "6a10a1a61e522319db65749b8aef8f44913ddeef1fc4bcfefee7f9881e059ac0"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "6b1f35ad7b37c501816f965c7a45c32224d21219698cce56549500fdca3fab6c"
  signature: "42732204e8c8aa00f8e9a2cc80aa4f213f2f12edb984af819a832feb59fdcc84"
  javaTemplate: "fad621e676b2aabf50db094afb7f965c71646823c4a1e0886e4cbae20037b6c9"
primaryPattern: "二叉树"
topics: ["二叉树","树","深度优先搜索","动态规划","树形 DP"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Depth-First Search 深度优先"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 124. 二叉树中的最大路径和 / Binary Tree Maximum Path Sum

> **双轨入口：** [[核心模型/二叉树/124-Binary-Tree-Maximum-Path-Sum-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`二叉树`
- 清单优先级：`P0`
- 清单代表标签：`Depth-First Search 深度优先`
- LeetCode 当前标签：树 (Tree)、深度优先搜索 (Depth-First Search)、动态规划 (Dynamic Programming)、二叉树 (Binary Tree)、树形 DP
- 官方来源：<https://leetcode.cn/problems/binary-tree-maximum-path-sum/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`072a45a20f48b1817ce058360ba7385c27e2ac03a491fc76f3228270552bde60`
- 主模型：树形 DP / 后序递归

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

二叉树中的**路径** 被定义为一条节点序列，序列中每对相邻节点之间都存在一条边。同一个节点在一条路径序列中 **至多出现一次** 。该路径**至少包含一个**节点，且不一定经过根节点。

**路径和** 是路径中各节点值的总和。

给你一个二叉树的根节点 `root` ，返回其 **最大路径和** 。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/10/13/exx1.jpg)

```text
输入：root = [1,2,3]
输出：6
解释：最优路径是 2 -> 1 -> 3 ，路径和为 2 + 1 + 3 = 6
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/10/13/exx2.jpg)

```text
输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径是 15 -> 20 -> 7 ，路径和为 15 + 20 + 7 = 42
```

## 官方约束


- 树中节点数目范围是 `[1, 3 * 10^4]`

- `-1000 <= Node.val <= 1000`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 区分“当前节点向父节点能贡献什么”和“以当前节点为最高点能形成什么完整路径”。
2. 返回给父节点的路径不能同时选择左右两支，否则到父节点后会产生分叉，不再是一条路径。
3. 负贡献应舍弃为 `0`，但全局答案不能初始化为 `0`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：root = [-3]
输出：-3
解释：路径不能为空，因此答案是唯一节点的值，而不是 0。
```

## 核心观察

后序处理节点 `node`，先得到左右孩子向上延伸的最大贡献 `leftGain`、`rightGain`。负贡献只会降低路径和，因此截断为零：

```text
leftGain = max(0, gain(node.left))
rightGain = max(0, gain(node.right))
```

以当前节点为最高点的完整路径可以同时连接左右：

```text
throughNode = node.val + leftGain + rightGain
```

但返回父节点时只能选一边：

```text
return node.val + max(leftGain, rightGain)
```

## 朴素方案：枚举路径端点

把树看作无向图，对每个节点作为起点执行 DFS，计算到所有其他节点的路径和并取最大。树有唯一简单路径，但为每个起点重复遍历整棵树。

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(n)` 用于递归和父节点访问控制。
- 局限：同一子树的向上贡献被反复计算。

## 最优方案推导

每条简单路径都有唯一的“最高节点”，也就是路径中最接近根的节点。在这个节点处，路径可以由左侧贡献、节点自身、右侧贡献组成。后序遍历计算每个节点向上的单支贡献，并在该节点处尝试把两支合并更新全局最大值。这样每一种可能的最高节点恰好被考虑一次。

## 正确性与不变量

`gain(node)` 返回从 `node` 出发向下、且不分叉的最大非空路径和，所以它可以合法连接到父节点。全局变量 `best` 在处理节点后，记录已处理子树中任意路径的最大和。任何路径都有唯一最高节点；当 DFS 处理该节点时，其左右部分分别不超过已算出的最大非负贡献，因此 `throughNode` 至少等于该路径和，并且本身也是合法路径。对所有节点取最大，结果恰为全局最优。

## 复杂度

- 时间复杂度：`O(n)`，每个节点处理一次。
- 空间复杂度：`O(h)` 递归栈，最坏链状树为 `O(n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    private int best;

    public int maxPathSum(TreeNode root) {
        best = Integer.MIN_VALUE;
        maxGain(root);
        return best;
    }

    private int maxGain(TreeNode node) {
        if (node == null) {
            return 0;
        }

        int leftGain = Math.max(0, maxGain(node.left));
        int rightGain = Math.max(0, maxGain(node.right));
        int throughNode = node.val + leftGain + rightGain;
        best = Math.max(best, throughNode);

        return node.val + Math.max(leftGain, rightGain);
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

class Solution {
    private int best;

    public int maxPathSum(TreeNode root) {
        best = Integer.MIN_VALUE;
        maxGain(root);
        return best;
    }

    private int maxGain(TreeNode node) {
        if (node == null) {
            return 0;
        }

        int leftGain = Math.max(0, maxGain(node.left));
        int rightGain = Math.max(0, maxGain(node.right));
        int throughNode = node.val + leftGain + rightGain;
        best = Math.max(best, throughNode);

        return node.val + Math.max(leftGain, rightGain);
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(3);
        System.out.println(new Solution().maxPathSum(root));
    }
}
```

## 边界与易错点

- `best` 必须初始化为 `Integer.MIN_VALUE`，否则全负树会错误返回 `0`。
- 更新全局答案时可以用左右两支，返回父节点时只能用一支。
- 路径不必经过根节点，不能只返回根的向上贡献。
- 若复用同一个 `Solution` 实例多次调用，必须在每次公开方法开始时重置 `best`。
- 节点数很大且树退化时，Java 递归可能栈溢出；工程环境可改为显式后序栈。

## 可扩展变式

- 543. 二叉树的直径：贡献改为边数，合并左右深度更新答案。
- 687. 最长同值路径：只有子节点值相同时才接收其贡献。
- 返回最大路径节点序列：更新全局答案时同时保存两侧路径或前驱。
- N 叉树最大路径和：选择所有子贡献中最大的两支合并。
