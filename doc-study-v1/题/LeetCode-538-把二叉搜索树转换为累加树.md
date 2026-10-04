# LeetCode-538 把二叉搜索树转换为累加树

- 难度：中等
- 链接：https://leetcode.cn/problems/convert-bst-to-greater-tree/

## 问题描述
将二叉搜索树每个节点的值替换为“原值 + 大于它的所有节点值之和”。

## 题解一：官方经典（反中序遍历累加）
- 思路：按右-中-左顺序遍历，维护累加和，将当前节点值更新为累加后的值。
- 复杂度：时间 O(n)，空间 O(h)。

```java
class Solution {
    private int sum = 0;
    public TreeNode convertBST(TreeNode root) {
        if (root == null) return null;
        convertBST(root.right);
        sum += root.val; root.val = sum;
        convertBST(root.left);
        return root;
    }
}
```

## 题解二：通用解法（迭代栈）
- 标签：二叉树、BST、中序、反中序
- 思路：用栈进行反中序遍历，过程同递归。

```java
import java.util.*;
class Solution {
    public TreeNode convertBST(TreeNode root) {
        int sum = 0; Deque<TreeNode> st = new ArrayDeque<>();
        TreeNode cur = root;
        while (cur != null || !st.isEmpty()) {
            while (cur != null) { st.push(cur); cur = cur.right; }
            TreeNode node = st.pop();
            sum += node.val; node.val = sum;
            cur = node.left;
        }
        return root;
    }
}
```

## 题解三：最好理解（右侧优先）
- 直觉：先访问大的（右侧），一路累加后再更新当前节点，再去左侧。

## 总结思路
- 反中序是 BST 累加的标准模板。

## 相关标签
- 二叉树、BST、中序、反中序