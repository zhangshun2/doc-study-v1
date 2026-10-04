# LeetCode-208 实现 Trie (前缀树)

- 难度：中等
- 链接：https://leetcode.cn/problems/implement-trie-prefix-tree/

## 问题描述
实现一个前缀树，支持插入单词、搜索单词和前缀匹配。

## 题解一：官方经典（数组指针版）
- 思路：每个节点维护 26 个子指针与是否为单词结尾标记；插入/搜索/前缀判断按字符路径遍历。
- 复杂度：每次操作 O(L)，L 为单词长度。

```java
class Trie {
    static class Node {
        Node[] next = new Node[26];
        boolean end;
    }
    private final Node root = new Node();

    public void insert(String word) {
        Node p = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (p.next[i] == null) p.next[i] = new Node();
            p = p.next[i];
        }
        p.end = true;
    }
    public boolean search(String word) {
        Node p = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (p.next[i] == null) return false;
            p = p.next[i];
        }
        return p.end;
    }
    public boolean startsWith(String prefix) {
        Node p = root;
        for (char c : prefix.toCharArray()) {
            int i = c - 'a';
            if (p.next[i] == null) return false;
            p = p.next[i];
        }
        return true;
    }
}
```

## 题解二：通用解法（哈希子节点）
- 标签：数据结构、字典树
- 思路：将子节点结构改为 `Map<Character,Node>` 支持一般字符集；接口不变。

## 总结思路
- Trie 的接口与复杂度稳定；根据字符集选择数组或哈希实现。

## 相关标签
- 数据结构、字典树