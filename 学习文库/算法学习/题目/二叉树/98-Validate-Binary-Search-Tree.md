---
schemaVersion: 3
type: "problem"
leetcodeId: 98
slug: "validate-binary-search-tree"
titleCn: "验证二叉搜索树"
titleEn: "Validate Binary Search Tree"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/validate-binary-search-tree/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "6eb3cc799cf28249ccb3750b0712a2b0be7e6bbb17208d3e8dcad204cff01d33"
sourceFactsSha256: "d8e6532f1a37916ef3c9e048a1ca162a4a9c7905bfb5b379774a7baa592e5c78"
sourceSectionHashes:
  description: "7bb36698f02a718b073881d5d7f599a0aa35bb8083f3ee7dc8bfb031f6567055"
  examples: "d944a5350834de5404e79422b61f6c182171a1eb960b3e013c65775fbe75923b"
  constraints: "f7ed82c2df8cbd47b2764a4f15528bcdc536f08e29711b1d9d9c178f7dd11022"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "447c9e49655e500e25a79886de08bcc6d9f11bb2da27ccf466fc57a14f4c7e6f"
  signature: "71cbe5d83f2aa7ac2a44784b6e02a2016d296d8cea3006215feabbf25cdde4b5"
  javaTemplate: "58ba6d5360194bd25349c0336a85a5ad6c622d2e99c7a46cb798508813b6ca02"
primaryPattern: "二叉树"
topics: ["二叉树","树","深度优先搜索","二叉搜索树"]
priority: "P2"
checklistPriorities: ["P2"]
checklistTags: ["Binary Search Tree 二叉搜索树","Binary Tree 二叉树"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 98. 验证二叉搜索树 / Validate Binary Search Tree

> **双轨入口：** [[核心模型/二叉树/98-Validate-Binary-Search-Tree-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`二叉树`
- 清单优先级：`P2`
- 清单代表标签：`Binary Search Tree 二叉搜索树`、`Binary Tree 二叉树`
- LeetCode 当前标签：树 (Tree)、深度优先搜索 (Depth-First Search)、二叉搜索树 (Binary Search Tree)、二叉树 (Binary Tree)
- 官方来源：<https://leetcode.cn/problems/validate-binary-search-tree/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`6eb3cc799cf28249ccb3750b0712a2b0be7e6bbb17208d3e8dcad204cff01d33`
- 主模型：递归传递严格取值范围

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个二叉树的根节点 `root` ，判断其是否是一个有效的二叉搜索树。

**有效** 二叉搜索树定义如下：

- 节点的左子树只包含** 严格小于**当前节点的数。

- 节点的右子树只包含 **严格大于** 当前节点的数。

- 所有左子树和右子树自身必须也是二叉搜索树。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/12/01/tree1.jpg)

```text
输入：root = [2,1,3]
输出：true
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/12/01/tree2.jpg)

```text
输入：root = [5,1,4,null,null,3,6]
输出：false
解释：根节点的值是 5 ，但是右子节点的值是 4 。
```

## 官方约束


- 树中节点数目范围在`[1, 10^4]` 内

- `-2^31 <= Node.val <= 2^31 - 1`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 只比较节点与左右孩子是不够的，右子树深处仍必须大于根节点。
2. 递归进入左子树时收紧上界，进入右子树时收紧下界。
3. 边界必须是严格不等式，并使用 `long` 避开整数极值冲突。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：root = [2,2,2]
输出：false
解释：BST 要求严格小于和严格大于，重复值不合法。
```

## 核心观察

每个节点都有一个由祖先共同决定的合法开区间 `(lower,upper)`。根节点范围是负无穷到正无穷：

- 检查节点值满足 `lower < val < upper`。
- 左孩子继承下界，并把当前值作为新上界。
- 右孩子继承上界，并把当前值作为新下界。

## 朴素错误方案：只比较父子

检查 `node.left.val < node.val` 和 `node.right.val > node.val` 能发现局部错误，却无法发现跨层约束。示例 `[5,1,6,null,null,3,7]` 中，每对直接父子都看似正确，但值 `3` 位于根 `5` 的右子树，整棵树不是 BST。

另一方案是中序遍历后判断严格递增，时间同样为 `O(n)`，若保存完整序列需 `O(n)` 额外空间；边遍历边比较可降到 `O(h)`。

## 最优方案推导

把祖先约束作为递归参数传下去。使用 `long lower`、`long upper`，根节点初值为 `Long.MIN_VALUE` 和 `Long.MAX_VALUE`，从而允许节点本身取任意 `int` 值。

遇到空节点返回 `true`。当前值越界立即返回 `false`，否则递归验证左右子树，两个结果必须都为真。

## 正确性与不变量

调用 `validate(node,lower,upper)` 时，区间恰好表示该位置由全部祖先施加的值限制。当前节点满足区间后，左子树增加“严格小于当前值”的限制，右子树增加“严格大于当前值”的限制。若递归全部成功，则任意节点都满足所有祖先关系，符合 BST 定义；若存在违反定义的节点，它必会超出递归传递到该处的区间而被发现。

## 复杂度

- 时间复杂度：`O(n)`，每个节点访问一次。
- 空间复杂度：`O(h)` 递归栈，最坏 `O(n)`，平衡树为 `O(log n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private boolean validate(TreeNode node, long lower, long upper) {
        if (node == null) {
            return true;
        }
        if (node.val <= lower || node.val >= upper) {
            return false;
        }
        return validate(node.left, lower, node.val)
                && validate(node.right, node.val, upper);
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
    public boolean isValidBST(TreeNode root) {
        return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private boolean validate(TreeNode node, long lower, long upper) {
        if (node == null) {
            return true;
        }
        if (node.val <= lower || node.val >= upper) {
            return false;
        }
        return validate(node.left, lower, node.val)
                && validate(node.right, node.val, upper);
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(2);
        root.left = new TreeNode(1);
        root.right = new TreeNode(3);
        System.out.println(new Solution().isValidBST(root));
    }
}
```

## 边界与易错点

- 重复值不合法，比较必须使用 `<=` 和 `>=` 判错。
- 不要用 `Integer.MIN_VALUE` 作为开区间下界，否则值恰好为该极值的合法根会被误判。
- 每个递归分支只能收紧一侧边界，另一侧必须继承祖先限制。
- BST 定义约束整棵子树，不是仅约束直接孩子。

## 可扩展变式

- 用中序遍历验证：记录前一个访问值，要求当前值严格更大。
- 恢复被交换的 BST（99）：中序序列中查找逆序对。
- 第 `k` 小元素（230）：利用 BST 中序有序性质。
- 若业务定义允许重复值，需要明确重复值统一放左还是右，并调整一侧为闭区间。
