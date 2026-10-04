---
schemaVersion: 3
type: "problem"
leetcodeId: 236
slug: "lowest-common-ancestor-of-a-binary-tree"
titleCn: "二叉树的最近公共祖先"
titleEn: "Lowest Common Ancestor of a Binary Tree"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "615128c16c8427123c2cfb47a3bd740f869565778988597bcafb7f480317a2fc"
sourceFactsSha256: "bee8794928fac787cbb359b2271ef64f2fae52970fa6d9dcfa1f6470bfc2ada8"
sourceSectionHashes:
  description: "e0255e1ebecb1bd22e90d4fafe2960e6d149230015df2b5064fc5872f3039262"
  examples: "92e04bdf0aa830a19325f1654247621284f9539ec51377ee729bd15555b11ce4"
  constraints: "0a10c013d483a1621952d51dc2048269a8b392055583d421b1a6a3139ba74baa"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "867c1be509b399052c3ef56eb4a25d5e4991e5e9a9b53ec673f779b2cd8fecad"
  signature: "8da2136885a080bacdb9c2a52c25b1d219b0e88749ee6c0db27ae0ea9bbbc1e1"
  javaTemplate: "ff659a013c2de165bd73d63013fa23426311940fde2e106e62019247b36d692c"
primaryPattern: "二叉树"
topics: ["二叉树","树","深度优先搜索","最近公共祖先","Binary Lifting"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Tree 树","Depth-First Search 深度优先"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 236. 二叉树的最近公共祖先 / Lowest Common Ancestor of a Binary Tree

> **双轨入口：** [[核心模型/二叉树/236-Lowest-Common-Ancestor-of-a-Binary-Tree-核心模型.md|核心模型]] · [[建模专题/T0/236-Lowest-Common-Ancestor-of-a-Binary-Tree-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`二叉树`
- 清单优先级：`P0`
- 清单代表标签：`Tree 树`、`Depth-First Search 深度优先`
- LeetCode 当前标签：树 (Tree)、深度优先搜索 (Depth-First Search)、二叉树 (Binary Tree)、最近公共祖先、Binary Lifting
- 官方来源：<https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`615128c16c8427123c2cfb47a3bd740f869565778988597bcafb7f480317a2fc`
- **主解法**：后序递归 DFS
- **直观建模专题**：[让子树向父节点汇报最小充分信息](../../建模专题/T0/236-Lowest-Common-Ancestor-of-a-Binary-Tree-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。

[百度百科](https://baike.baidu.com/item/%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88/8918834?fr=aladdin)中最近公共祖先的定义为：“对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（**一个节点也可以是它自己的祖先**）。”

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2018/12/14/binarytree.png)

```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
输出：3
解释：节点 5 和节点 1 的最近公共祖先是节点 3 。
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2018/12/14/binarytree.png)

```text
输入：root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
输出：5
解释：节点 5 和节点 4 的最近公共祖先是节点 5 。因为根据定义最近公共祖先节点可以为节点本身。
```

**示例 3：**

```text
输入：root = [1,2], p = 1, q = 2
输出：1
```

## 官方约束


- 树中节点数目在范围 `[2, 10^5]` 内。

- `-10^9 <= Node.val <= 10^9`

- 所有 `Node.val` `互不相同` 。

- `p != q`

- `p` 和 `q` 均存在于给定的二叉树中。

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 若当前节点就是 `p` 或 `q`，它应向上报告“找到了目标”。
2. 左右子树各报告一个非空结果时，当前节点就是首次汇合处。
3. 只有一侧非空时，把该侧结果原样向上传递。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- LeetCode 传入的是节点引用，不应仅按值构造或比较替代节点身份。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

递归函数不必同时返回“是否找到 p”“是否找到 q”等复杂状态。在题目保证两节点存在的前提下，可以让函数返回：当前子树中若含目标或其最近公共祖先，则返回该关键节点；否则返回 `null`。

## 朴素方案

分别从根到 `p`、`q` 做 DFS 并记录两条路径，再从头找最后一个相同节点。时间 `O(n)`、额外空间 `O(n)`，正确但需要存路径。还可为每个节点建立父指针，再沿祖先集合求交，同样需要 `O(n)` 哈希空间。

## 最优方案推导

后序处理当前节点：

1. `root == null` 返回 `null`。
2. `root == p || root == q`，返回 `root`。
3. 分别递归左右子树，得到 `left`、`right`。
4. 两者都非空，说明 `p`、`q` 分处两边，当前节点是 LCA。
5. 否则返回唯一非空结果；都为空则返回 `null`。

## 正确性与不变量

对任意子树，递归返回值满足：

- 不含 `p`、`q` 时返回 `null`。
- 只含其中一个时返回该目标节点。
- 同时含二者时返回它们在该子树中的最近公共祖先。

叶子及空树显然成立。对内部节点，若目标分居左右，当前根是二者路径首次交汇点；若集中在一边，最近公共祖先也在那一边；若根本身是目标，根据“节点是自身祖先”的定义应直接返回根。归纳可知根调用返回正确答案。

## 复杂度

- **时间复杂度**：`O(n)`，最坏访问每个节点一次。
- **空间复杂度**：`O(h)` 递归栈；平衡树为 `O(log n)`，链状树最坏 `O(n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) {
            return root;
        }
        return left != null ? left : right;
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

    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) {
            return root;
        }

        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) {
            return root;
        }
        return left != null ? left : right;
    }
}

public class Main {
    public static void main(String[] args) {
        TreeNode node5 = new TreeNode(5);
        TreeNode node1 = new TreeNode(1);
        TreeNode node4 = new TreeNode(4);
        TreeNode root = new TreeNode(3, node5, node1);
        node5.left = new TreeNode(6);
        node5.right = new TreeNode(2, new TreeNode(7), node4);
        node1.left = new TreeNode(0);
        node1.right = new TreeNode(8);

        Solution solution = new Solution();
        System.out.println(solution.lowestCommonAncestor(root, node5, node1).val); // 3
        System.out.println(solution.lowestCommonAncestor(root, node5, node4).val); // 5
    }
}
```

## 边界与易错点

- 必须接受“一个目标是另一个目标祖先”的情况，命中目标时直接返回。
- 比较 `root == p` 使用节点引用，避免节点值不唯一的变式中出错。
- 若题目不保证 `p`、`q` 都存在，此简洁返回语义不足以验证两者，应额外统计命中数。
- `10^5` 深度的极端链状树可能导致 Java 递归栈溢出，可改为迭代建立父指针。

## 可扩展变式

- 二叉搜索树 LCA：利用键值大小同时向左或向右，无需遍历整树。
- 多个节点的 LCA：将“命中 p/q”扩展为目标节点集合。
- 大量在线 LCA 查询：可用倍增、Euler Tour + RMQ 等预处理。
- 节点可能不存在：递归结果同时携带找到目标的数量，只有计数为 2 才返回答案。
