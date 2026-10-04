# LeetCode-236 二叉树的最近公共祖先

- 难度：中等
- 链接：https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/

## 问题描述
给定二叉树的根节点 `root` 和两个节点 `p`、`q`，返回它们的最近公共祖先（LCA）。

## 题解一：官方经典（递归返回命中）
- 思路：递归在左右子树中查找，如果左右都返回非空，即当前为 LCA；如果只有一侧非空，返回该侧；空则返回空。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode L = lowestCommonAncestor(root.left, p, q);
        TreeNode R = lowestCommonAncestor(root.right, p, q);
        if (L != null && R != null) return root;
        return L != null ? L : R;
    }
}
```

## 题解二：通用解法（父指针 + 集合）
- 标签：二叉树、递归、LCA、集合
- 思路：用哈希记录所有 `p` 的祖先，再向上遍历 `q` 的祖先，遇到第一个在集合中的即为 LCA。

```java
import java.util.*;
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        Deque<TreeNode> st = new ArrayDeque<>(); st.push(root);
        parent.put(root, null);
        while (!parent.containsKey(p) || !parent.containsKey(q)) {
            TreeNode node = st.pop();
            if (node.left != null) { parent.put(node.left, node); st.push(node.left); }
            if (node.right != null) { parent.put(node.right, node); st.push(node.right); }
        }
        Set<TreeNode> anc = new HashSet<>();
        for (TreeNode x = p; x != null; x = parent.get(x)) anc.add(x);
        for (TreeNode y = q; y != null; y = parent.get(y)) if (anc.contains(y)) return y;
        return null;
    }
}
```

## 题解三：最好理解（命中返回聚合）
- 直觉：左右递归各自返回命中结果，若两侧都有，说明当前节点就是“最近共同祖先”。

## 总结思路
- 递归法是面试常用模板；父指针法便于可视化理解。

## 相关标签
- 二叉树、递归、LCA、集合