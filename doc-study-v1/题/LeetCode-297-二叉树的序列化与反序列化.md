# LeetCode-297 二叉树的序列化与反序列化

- 难度：困难
- 链接：https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/

## 问题描述
设计一个算法将二叉树转换成字符串（序列化）和将字符串还原为二叉树（反序列化）。

## 题解一：官方经典（BFS 层序 + 占位符）
- 思路：层序遍历输出值，用 `#` 表示空指针；反序列化时按顺序复原左右孩子。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
public class Codec {
    public String serialize(TreeNode root) {
        if (root == null) return "";
        StringBuilder sb = new StringBuilder();
        Queue<TreeNode> q = new LinkedList<>(); q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node == null) { sb.append("#,"); continue; }
            sb.append(node.val).append(',');
            q.offer(node.left); q.offer(node.right);
        }
        return sb.toString();
    }
    public TreeNode deserialize(String data) {
        if (data == null || data.isEmpty()) return null;
        String[] arr = data.split(",");
        int idx = 0; TreeNode root = parse(arr[idx++]);
        Queue<TreeNode> q = new LinkedList<>(); q.offer(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            TreeNode L = parse(arr[idx++]); TreeNode R = parse(arr[idx++]);
            node.left = L; node.right = R;
            if (L != null) q.offer(L);
            if (R != null) q.offer(R);
        }
        return root;
    }
    private TreeNode parse(String s){ return s.equals("#")?null:new TreeNode(Integer.parseInt(s)); }
}
```

## 题解二：通用解法（DFS 先序 + 空标记）
- 标签：二叉树、序列化、反序列化、BFS、DFS
- 思路：先序输出节点值与 `#` 空标记；反序列化用索引递归构造。

```java
import java.util.*;
public class Codec {
    private int idx;
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        pre(root, sb); return sb.toString();
    }
    private void pre(TreeNode node, StringBuilder sb) {
        if (node == null) { sb.append("#,"); return; }
        sb.append(node.val).append(',');
        pre(node.left, sb); pre(node.right, sb);
    }
    public TreeNode deserialize(String data) {
        String[] arr = data.split(","); idx = 0;
        return build(arr);
    }
    private TreeNode build(String[] arr) {
        if (idx >= arr.length || arr[idx].equals("#")) { idx++; return null; }
        TreeNode node = new TreeNode(Integer.parseInt(arr[idx++]));
        node.left = build(arr); node.right = build(arr);
        return node;
    }
}
```

## 题解三：最好理解（遍历视角）
- 直觉：把树“拍平”为序列；BFS像层层记录房间号，DFS像递归记录入栈/出栈。

## 总结思路
- 两法都常用：BFS便于可视化，DFS更紧凑；注意空节点占位与边界处理。

## 相关标签
- 二叉树、序列化、反序列化、BFS、DFS