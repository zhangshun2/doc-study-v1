---
schemaVersion: 3
type: "problem"
leetcodeId: 101
slug: "symmetric-tree"
titleCn: "对称二叉树"
titleEn: "Symmetric Tree"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/symmetric-tree/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "a9c3ba8a4aa8ab816c59a9d14760294c21fceba4d09efce43fe088a72e0780b6"
sourceFactsSha256: "6df8091f2cca178a8377d3007f3c0f014d9020ed94b3d730894e70feec44e5fa"
sourceSectionHashes:
  description: "30c36d5e1bb8109c3748f51db6c08ad1baf9e828c51a7defab5f361d8bbec6a0"
  examples: "b7f0bf414bd4a0f194ae47d735680e8e65b36ff6bc9e23f040003b416ffc4b5c"
  constraints: "f5574292d683aabec5ed5dfb196c2c5a8484895ea2e63edbe85ee029c5485921"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "e32e72f81f8e5091ad0d0f02edb155a7a1704c2e9d85d0326ce177f50341d0ad"
  signature: "d58c4e649a6897deb5a2beb898d4c440829e9bafb3504d201be53fd4717ede5c"
  javaTemplate: "80c5739526f45009debee9d5123ef99d1a3769b9229647b406b54fd0bf3ff018"
primaryPattern: "二叉树"
topics: ["二叉树","树","深度优先搜索","广度优先搜索"]
priority: "P2"
checklistPriorities: ["P2"]
checklistTags: ["Binary Tree 二叉树"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 101. 对称二叉树 / Symmetric Tree

> **双轨入口：** [[核心模型/二叉树/101-Symmetric-Tree-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`二叉树`
- 清单优先级：`P2`
- 清单代表标签：`Binary Tree 二叉树`
- LeetCode 当前标签：树 (Tree)、深度优先搜索 (Depth-First Search)、广度优先搜索 (Breadth-First Search)、二叉树 (Binary Tree)
- 官方来源：<https://leetcode.cn/problems/symmetric-tree/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`a9c3ba8a4aa8ab816c59a9d14760294c21fceba4d09efce43fe088a72e0780b6`
- 主模型：成对镜像递归

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

## 官方示例


**示例 1：**

![Official problem illustration](https://pic.leetcode.cn/1698026966-JDYPDU-image.png)

```text
输入：root = [1,2,2,3,4,4,3]
输出：true
```

**示例 2：**

![Official problem illustration](https://pic.leetcode.cn/1698027008-nPFLbM-image.png)

```text
输入：root = [1,2,2,null,3,null,3]
输出：false
```

## 官方约束


- 树中节点数目在范围 `[1, 1000]` 内

- `-100 <= Node.val <= 100`

**进阶：**你可以运用递归和迭代两种方法解决这个问题吗？

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 不要写一个只接收单节点的普通遍历函数；镜像判断天然需要同时接收两个节点。
2. 两个节点都为空时对称，只有一个为空时不对称。
3. 值相等后应比较 `left.left` 与 `right.right`，以及 `left.right` 与 `right.left`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

定义 `isMirror(a,b)` 判断两棵树是否互为镜像。镜像的递归定义为：

```text
a 和 b 都为空；或者
a.val == b.val
且 a.left 与 b.right 镜像
且 a.right 与 b.left 镜像
```

这比先分别遍历左右子树再比较序列更直接，因为单独的遍历序列若不记录空节点，可能丢失结构信息。

## 朴素方案：序列化后比较

分别以“根、左、右”和“根、右、左”的次序序列化左右子树，并保留所有空指针标记，再比较两个序列。可正确完成，但需要 `O(n)` 的序列存储，步骤也更多。如果漏掉空标记，会把结构不同但值序列相同的树误判为对称。

## 最优方案推导

从 `root.left` 与 `root.right` 开始成对比较：

1. 两者均为空，当前这一对对称。
2. 恰有一个为空，结构不对称。
3. 值不同，不对称。
4. 递归比较外侧一对和内侧一对，两者都通过才对称。

每个节点只参与一次配对比较。

## 正确性与不变量

每次调用 `isMirror(left,right)` 都判断关于整棵树中轴处于对应位置的两个子树。空状态和节点值检查保证当前根结构和值相同；交叉递归恰好检查镜像定义要求的两对子树。通过结构归纳，叶节点对满足条件，若两对子树均镜像则当前两树镜像；任何结构或值差异都会在对应层被检测。

## 复杂度

- 时间复杂度：`O(n)`，每个节点最多访问一次。
- 空间复杂度：`O(h)` 递归栈，最坏 `O(n)`，平衡树为 `O(log n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public boolean isSymmetric(TreeNode root) {
        return isMirror(root.left, root.right);
    }

    private boolean isMirror(TreeNode left, TreeNode right) {
        if (left == null && right == null) {
            return true;
        }
        if (left == null || right == null) {
            return false;
        }
        if (left.val != right.val) {
            return false;
        }
        return isMirror(left.left, right.right)
                && isMirror(left.right, right.left);
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
    public boolean isSymmetric(TreeNode root) {
        return isMirror(root.left, root.right);
    }

    private boolean isMirror(TreeNode left, TreeNode right) {
        if (left == null && right == null) {
            return true;
        }
        if (left == null || right == null) {
            return false;
        }
        if (left.val != right.val) {
            return false;
        }
        return isMirror(left.left, right.right)
                && isMirror(left.right, right.left);
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.left = new TreeNode(2);
        root.right = new TreeNode(2);
        root.left.left = new TreeNode(3);
        root.left.right = new TreeNode(4);
        root.right.left = new TreeNode(4);
        root.right.right = new TreeNode(3);
        System.out.println(new Solution().isSymmetric(root));
    }
}
```

## 边界与易错点

- `root` 按题目约束非空；若用于通用代码，可先处理 `root == null` 为 `true`。
- 不能比较 `left.left` 与 `right.left`，镜像需要交叉比较。
- 只比较节点值会漏掉结构差异。
- BFS 实现时队列需要保留空位置；`ArrayDeque` 不接受 `null`，可改存节点对对象。

## 可扩展变式

- 判断两棵树相同（100）：对应比较左对左、右对右，不做交叉。
- 翻转二叉树（226）：交换每个节点左右子树后可与原树比较。
- 迭代镜像判断：队列每次加入一对待比较节点。
- 判断某棵子树是否为另一棵的镜像：直接复用 `isMirror` 定义。
