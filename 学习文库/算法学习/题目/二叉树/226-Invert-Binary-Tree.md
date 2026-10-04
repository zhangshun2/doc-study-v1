---
schemaVersion: 3
type: "problem"
leetcodeId: 226
slug: "invert-binary-tree"
titleCn: "翻转二叉树"
titleEn: "Invert Binary Tree"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/invert-binary-tree/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "3a2c823984b415501aff1ac4f2257b2dfedeab4d8af89187b689844378e4f5fb"
sourceFactsSha256: "2edcd345fa15cf33650c40afed066b6e441dfd3720035e042799d8ef43c3fbcc"
sourceSectionHashes:
  description: "6eedd0f2a56f28a26d3e64447f0d1f1211722d3b95679f664e8cbdd94093cb81"
  examples: "76fa6008340be3c19f4fb501469eae377776148eff2689f1988c26d37d36c31d"
  constraints: "9e0a17d2b1cc64300af8cce9016263f1069d95a0b4647cc7e513ab9572ca9ea5"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "e32e72f81f8e5091ad0d0f02edb155a7a1704c2e9d85d0326ce177f50341d0ad"
  signature: "05e44277236dd78b27a1d5f4bc2f543f8027be2e27c8a77bbfba3b194ba84014"
  javaTemplate: "b3312a3a4e0af7ca19e9523697f20c7c7cbefa51c45a10a41e169bd0d736d3ad"
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
# 226. 翻转二叉树 / Invert Binary Tree

> **双轨入口：** [[核心模型/二叉树/226-Invert-Binary-Tree-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`二叉树`
- 清单优先级：`P2`
- 清单代表标签：`Binary Tree 二叉树`
- LeetCode 当前标签：树 (Tree)、深度优先搜索 (Depth-First Search)、广度优先搜索 (Breadth-First Search)、二叉树 (Binary Tree)
- 官方来源：<https://leetcode.cn/problems/invert-binary-tree/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`3a2c823984b415501aff1ac4f2257b2dfedeab4d8af89187b689844378e4f5fb`
- **主解法**：递归 DFS

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/03/14/invert1-tree.jpg)

```text
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/03/14/invert2-tree.jpg)

```text
输入：root = [2,1,3]
输出：[2,3,1]
```

**示例 3：**

```text
输入：root = []
输出：[]
```

## 官方约束


- 树中节点数目范围在 `[0, 100]` 内

- `-100 <= Node.val <= 100`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 整棵树翻转等价于：根节点左右孩子互换，并递归翻转两棵子树。
2. 空节点是递归终止条件。
3. 交换后递归新左右子树，或先递归原左右子树再交换，都可以，但不要丢失引用。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

二叉树具有递归结构。若左右子树已经分别完成镜像，再交换它们的位置，整棵树就是镜像；也可以先交换根的两个孩子，再对交换后的子树执行同样操作。

## 朴素方案

先层序遍历把整棵树序列化到数组，再根据索引关系重建镜像树。该方案需要额外 `O(n)` 存储，还要处理大量空位，完全没有利用现有节点连接。直接遍历每个节点并交换孩子更简单且最优。

## 最优方案推导

定义 `invertTree(root)`：

1. 若 `root == null`，返回 `null`。
2. 递归翻转原左子树和原右子树。
3. 把翻转后的右子树赋给 `root.left`，翻转后的左子树赋给 `root.right`。
4. 返回 `root`。

这是后序思路；每个节点只处理一次。

## 正确性与不变量

对树高做归纳。空树显然已经翻转。假设高度小于 `h` 的树都能被正确翻转。对于高度为 `h` 的根，递归调用根据归纳假设得到原左右子树的正确镜像，再交换二者位置，恰好满足整棵树中所有左右方向反转。因此算法对任意高度的二叉树正确。

## 复杂度

- **时间复杂度**：`O(n)`，访问每个节点一次。
- **空间复杂度**：`O(h)` 递归栈，`h` 为树高；平衡树为 `O(log n)`，链状树最坏 `O(n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode invertedLeft = invertTree(root.left);
        TreeNode invertedRight = invertTree(root.right);
        root.left = invertedRight;
        root.right = invertedLeft;
        return root;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode() {
    }

    TreeNode(int val) {
        this.val = val;
    }

    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode invertedLeft = invertTree(root.left);
        TreeNode invertedRight = invertTree(root.right);
        root.left = invertedRight;
        root.right = invertedLeft;
        return root;
    }
}

public class Main {
    private static List<Integer> levelOrder(TreeNode root) {
        List<Integer> values = new ArrayList<>();
        if (root == null) {
            return values;
        }
        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            values.add(node.val);
            if (node.left != null) {
                queue.offer(node.left);
            }
            if (node.right != null) {
                queue.offer(node.right);
            }
        }
        return values;
    }

    public static void main(String[] args) {
        TreeNode root = new TreeNode(4,
                new TreeNode(2, new TreeNode(1), new TreeNode(3)),
                new TreeNode(7, new TreeNode(6), new TreeNode(9)));
        TreeNode inverted = new Solution().invertTree(root);
        System.out.println(levelOrder(inverted)); // [4, 7, 2, 9, 6, 3, 1]
        System.out.println(levelOrder(new Solution().invertTree(null))); // []
    }
}
```

## 边界与易错点

- 空树必须直接返回 `null`。
- 算法原地修改原树；若要保留原树，应创建新节点构造镜像副本。
- 不要在没有临时引用的情况下连续赋值，否则原左/右子树可能丢失。
- 层序迭代也可实现：每出队一个节点就交换左右孩子，再把非空孩子入队。

## 可扩展变式

- 判断两棵树是否互为镜像：递归比较 `a.left` 与 `b.right`、`a.right` 与 `b.left`。
- 判断对称二叉树：比较根的左右子树是否镜像。
- 生成镜像副本：不修改输入，为每个原节点新建对应节点。
- N 叉树镜像：翻转每个节点的孩子列表，并递归处理各孩子。
