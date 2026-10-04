---
schemaVersion: 3
type: "problem"
leetcodeId: 102
slug: "binary-tree-level-order-traversal"
titleCn: "二叉树的层序遍历"
titleEn: "Binary Tree Level Order Traversal"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/binary-tree-level-order-traversal/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "226812e968f5f6a0013987b6780b53764f1376e754415ea46f662f038bab88e2"
sourceFactsSha256: "7140380f10d13897dd22f942555d8dbf40c62c69b889dc26960571656433e154"
sourceSectionHashes:
  description: "b3d83fff4c6d3de4278b547d7eab74735e61d679dee8636ac1bd4fbe643fd8f9"
  examples: "febe3bc749fc9a32a0e8fa1643ba8cf53d71b550500153a1952de8bf154b6c5d"
  constraints: "c4efbbe23019b50dfc8a11e232d27eca467f98c39d2cad66c1184db8ce659051"
  hints: "cca9a1df185b4397613803695b21b54004c5cfe4b5e1da91a7268ef27a396ede"
  tags: "2f1329bf9dfec1c64fd745101008b53e584a2d1b032199579f8d4a3ac73e907c"
  signature: "479b60a33d4c0bccdf6cd8cda51f23c580e25075dc871e722a9d36698315c5da"
  javaTemplate: "ce8670db9260c29f49ea87639545328684936433b7f9f7eefad504bacd189d9b"
primaryPattern: "二叉树"
topics: ["二叉树","树","广度优先搜索"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Tree 树","Breadth-First Search 广度优先"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 102. 二叉树的层序遍历 / Binary Tree Level Order Traversal

> **双轨入口：** [[核心模型/二叉树/102-Binary-Tree-Level-Order-Traversal-核心模型.md|核心模型]] · [[建模专题/T0/102-Binary-Tree-Level-Order-Traversal-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`二叉树`
- 清单优先级：`P0`
- 清单代表标签：`Tree 树`、`Breadth-First Search 广度优先`
- LeetCode 当前标签：树 (Tree)、广度优先搜索 (Breadth-First Search)、二叉树 (Binary Tree)
- 官方来源：<https://leetcode.cn/problems/binary-tree-level-order-traversal/>
- 直观建模专题：[把“这一层”冻结成一次前沿批次](../../建模专题/T0/102-Binary-Tree-Level-Order-Traversal-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`226812e968f5f6a0013987b6780b53764f1376e754415ea46f662f038bab88e2`
- 主模型：队列按层 BFS

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你二叉树的根节点 `root` ，返回其节点值的 **层序遍历** 。 （即逐层地，从左到右访问所有节点）。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```text
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

**示例 2：**

```text
输入：root = [1]
输出：[[1]]
```

**示例 3：**

```text
输入：root = []
输出：[]
```

## 官方约束


- 树中节点数目在范围 `[0, 2000]` 内

- `-1000 <= Node.val <= 1000`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Use a queue to perform BFS.

## 学习提示（非官方）

1. 队列天然按“先发现、先处理”的顺序访问同一层节点。
2. 每轮开始时记录 `levelSize = queue.size()`，它就是当前层的节点数。
3. 只循环处理这 `levelSize` 个节点；期间加入的孩子属于下一层，不能在本轮处理。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

若当前队列按从左到右顺序只包含某一层节点，那么依次弹出这些节点，并按左孩子、右孩子的顺序入队，队列随后就会按从左到右顺序只包含下一层节点。`queue.size()` 的快照因此能准确切分层次。

## 朴素方案：DFS 携带深度

递归访问节点时携带 `depth`，若结果列表还没有该层就创建，再把节点值放入 `result.get(depth)`。先递归左子树再递归右子树，可以保持每层从左到右。

- 时间复杂度：`O(n)`。
- 空间复杂度：递归栈 `O(h)`，加输出。
- 评价：也是最优解；BFS 对“按层”语义更直接，并便于扩展层平均值、最短深度等题。

## 最优方案推导

1. 根为空时直接返回空结果。
2. 根节点入队。
3. 外层循环每次处理一层，先保存本层大小。
4. 内层恰好弹出本层节点，将值加入 `level`，并把非空孩子入队。
5. 内层结束后把 `level` 加入结果。

## 正确性与不变量

每轮外层循环开始时，队列恰好按从左到右顺序保存当前层的所有节点。固定的 `levelSize` 保证本轮只弹出这些节点；每个父节点按左后右加入孩子，而父节点本身也从左到右处理，所以新入队节点正好构成下一层的正确顺序。由层数归纳，所有层均被完整、按序输出。

## 复杂度

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(w)`，`w` 为树的最大宽度，最坏 `O(n)`；返回结果另占 `O(n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) {
            return result;
        }

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> level = new ArrayList<>(levelSize);
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }
            result.add(level);
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
import java.util.List;
import java.util.Queue;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

class Solution {
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) {
            return result;
        }

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> level = new ArrayList<>(levelSize);
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }
            result.add(level);
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode root = new TreeNode(3);
        root.left = new TreeNode(9);
        root.right = new TreeNode(20);
        root.right.left = new TreeNode(15);
        root.right.right = new TreeNode(7);
        System.out.println(new Solution().levelOrder(root));
    }
}
```

## 边界与易错点

- `levelSize` 必须在内层循环前保存，不能让循环条件动态读取不断增长的 `queue.size()`。
- 空孩子不应入 `ArrayDeque`，因为它不允许 `null`。
- 入队次序为左后右，才能得到题目要求的层内顺序。
- 空树直接返回空列表，不进入队列。

## 可扩展变式

- 103. 锯齿形层序遍历：按层号决定追加方向，或用双端队列。
- 199. 二叉树右视图：记录每层最后一个节点。
- 637. 二叉树的层平均值：每层累加后除以 `levelSize`。
- 107. 自底向上的层序遍历：普通层序后反转结果或从头部插入。
