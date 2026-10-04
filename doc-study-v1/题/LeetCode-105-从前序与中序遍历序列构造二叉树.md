# LeetCode-105 从前序与中序遍历序列构造二叉树

- 难度：中等
- 链接：https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

## 问题描述
给定前序遍历和中序遍历的数组，构造并返回该二叉树。

## 题解一：官方经典（递归 + 哈希定位）
- 思路：前序的首元素是根；在中序中找到根的位置，左侧是左子树，右侧是右子树；用索引区间递归构造。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    private Map<Integer, Integer> pos;
    private int[] pre, in;
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        this.pre = preorder; this.in = inorder;
        pos = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) pos.put(inorder[i], i);
        return build(0, preorder.length - 1, 0, inorder.length - 1);
    }
    private TreeNode build(int pl, int pr, int il, int ir) {
        if (pl > pr) return null;
        int rootVal = pre[pl];
        int k = pos.get(rootVal);
        int leftSize = k - il;
        TreeNode root = new TreeNode(rootVal);
        root.left = build(pl + 1, pl + leftSize, il, k - 1);
        root.right = build(pl + leftSize + 1, pr, k + 1, ir);
        return root;
    }
}
```

## 题解二：通用解法（迭代栈模拟）
- 标签：二叉树、递归、栈、遍历
- 思路：用前序确定根，用栈记录路径，按中序弹栈确定左/右连接。

```java
import java.util.*;
class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder.length == 0) return null;
        Deque<TreeNode> st = new ArrayDeque<>();
        int i = 0, j = 0;
        TreeNode root = new TreeNode(preorder[i++]); st.push(root);
        while (i < preorder.length) {
            TreeNode node = st.peek();
            if (node.val != inorder[j]) {
                node.left = new TreeNode(preorder[i]);
                st.push(node.left); i++;
            } else {
                while (!st.isEmpty() && st.peek().val == inorder[j]) {
                    node = st.pop(); j++;
                }
                node.right = new TreeNode(preorder[i]);
                st.push(node.right); i++;
            }
        }
        return root;
    }
}
```

## 题解三：最好理解（区间递归）
- 直觉：在中序里切分左右区间，前序里对应切分左右数量，递归构造即可。

## 总结思路
- 哈希定位中序索引是关键；迭代更贴近遍历过程但实现更复杂。

## 相关标签
- 二叉树、递归、栈、遍历