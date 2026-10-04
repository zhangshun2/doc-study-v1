---
schemaVersion: 3
type: "problem"
leetcodeId: 94
slug: "binary-tree-inorder-traversal"
titleCn: "二叉树的中序遍历"
titleEn: "Binary Tree Inorder Traversal"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/binary-tree-inorder-traversal/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "b00930afa0a92f0c5b617da175a8d2b1a051dc27726204e13ea910f0b9e6ef5f"
sourceFactsSha256: "41a18eedbae0891524b44702a8d101a30a0bcd0f53cc484289edffcd3871d05d"
sourceSectionHashes:
  description: "c73496126f52c61e6b9300cbf867ec0a1a50ed6b0a7dde0563cac85b73bd475b"
  examples: "f8fccd90f2f8449075870e714be962a897e8183dec8ddfe128ca7ec08aa38eed"
  constraints: "25d53eec791e367a54e50ee98f3965c61a43e8d498a9109946cccff3559f6bed"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "1fa95e635390a878766b484df90f910e5de54ee4c4080973b854ddf804cba8c1"
  signature: "efcc505b794944f52118de788d7bd48bb9db10e8e836f4c8ce85efbf69d208bd"
  javaTemplate: "0896bcbe2d6a4ae530ea81113298ff5ea74ec1200baef8574bbcb28316944a05"
primaryPattern: "二叉树"
topics: ["二叉树","栈","树","深度优先搜索"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Tree 树"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 94. 二叉树的中序遍历 / Binary Tree Inorder Traversal

> **双轨入口：** [[核心模型/二叉树/94-Binary-Tree-Inorder-Traversal-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`二叉树`
- 清单优先级：`P0`
- 清单代表标签：`Tree 树`
- LeetCode 当前标签：栈 (Stack)、树 (Tree)、深度优先搜索 (Depth-First Search)、二叉树 (Binary Tree)
- 官方来源：<https://leetcode.cn/problems/binary-tree-inorder-traversal/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`b00930afa0a92f0c5b617da175a8d2b1a051dc27726204e13ea910f0b9e6ef5f`
- 主模型：显式栈模拟“左、根、右”递归

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个二叉树的根节点 `root` ，返回 *它的 **中序** 遍历* 。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/09/15/inorder_1.jpg)

```text
输入：root = [1,null,2,3]
输出：[1,3,2]
```

**示例 2：**

```text
输入：root = []
输出：[]
```

**示例 3：**

```text
输入：root = [1]
输出：[1]
```

## 官方约束


- 树中节点数目在范围 `[0, 100]` 内

- `-100 <= Node.val <= 100`

**进阶:** 递归算法很简单，你可以通过迭代算法完成吗？

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 中序的“根”要等左子树处理完才访问，所以需要保存沿途节点。
2. 迭代时先持续向左压栈；无左路可走时弹栈访问，再转向右孩子。
3. 外层循环条件要同时考虑 `current != null` 和栈非空。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 递归和迭代都应为 `O(n)` 时间。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

递归调用栈实际上保存了“左子树处理完后还要回来访问”的祖先节点。显式栈只是把这件事写出来：

```text
一路向左：保存尚未访问的根
弹出栈顶：左子树已经完成，现在访问根
转向右子树：重复相同过程
```

## 朴素方案：递归

递归严格按照左、根、右书写，最直观：

```java
private void inorder(TreeNode node, List<Integer> result) {
    if (node == null) {
        return;
    }
    inorder(node.left, result);
    result.add(node.val);
    inorder(node.right, result);
}
```

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(h)` 递归栈，`h` 为树高，最坏 `O(n)`。
- 局限：树极深时可能导致调用栈溢出；迭代版更显式可控。

## 最优方案推导

使用 `current` 表示当前准备展开的子树：

1. `current` 非空时不断压栈并向左。
2. 到达空指针后弹出栈顶，把值加入答案。
3. 将 `current` 指向被访问节点的右孩子。
4. 当前为空且栈也为空时结束。

该方案与递归有相同渐进复杂度，但不使用语言调用栈。

## 正确性与不变量

栈中的每个节点都已经开始处理，但其自身和右子树尚未访问；`current` 指向下一棵需要展开的子树。持续向左保证弹出的节点已无未处理左子树，因此可按中序访问它；转向其右孩子后又建立相同状态。每个节点入栈、弹栈各一次，最终顺序恰为左、根、右。

## 复杂度

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(h)`，最坏退化树为 `O(n)`，平衡树为 `O(log n)`；不计输出列表。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;

        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            result.add(current.val);
            current = current.right;
        }
        return result;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;

        while (current != null || !stack.isEmpty()) {
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            current = stack.pop();
            result.add(current.val);
            current = current.right;
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(1);
        root.right = new TreeNode(2);
        root.right.left = new TreeNode(3);
        System.out.println(new Solution().inorderTraversal(root));
    }
}
```

## 边界与易错点

- `ArrayDeque` 不允许压入 `null`，只在节点非空时 `push`。
- 外层不能只写 `current != null`，否则走到最左空位置时会提前结束。
- 访问节点发生在弹栈后，而不是压栈时。
- 中序是“左、根、右”；前序与后序的访问时机不同。

## 可扩展变式

- BST 中序遍历得到严格递增序列，可用于验证搜索树或找第 `k` 小元素。
- Morris 中序遍历：利用临时线索实现 `O(1)` 额外空间，但会临时修改树指针。
- 统一迭代模板：给节点增加“展开/访问”标记，可统一前中后序。
- 中序遍历迭代器（173）：延迟展开左链，让每次 `next()` 均摊 `O(1)`。
