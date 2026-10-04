# LeetCode-79 单词搜索

- 难度：中等
- 链接：https://leetcode.cn/problems/word-search/

## 问题描述
给定二维字符网格 `board` 和字符串 `word`，判断能否在网格中通过上下左右相邻的单元格组成该字符串，其中每个单元格只能使用一次。

## 题解一：官方经典（DFS 回溯）
- 思路：从每个起点出发，递归匹配当前位置字符并向四个方向扩展；使用访问标记避免重复使用同一单元；当索引到达 `word.length()` 说明匹配成功。
- 复杂度：时间最坏 O(m·n·4^L)，空间 O(L) 递归栈与访问标记（可原地临时修改）。

```java
class Solution {
    public boolean exist(char[][] board, String word) {
        int m = board.length, n = board[0].length;
        boolean[][] vis = new boolean[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (dfs(board, word, 0, i, j, vis)) return true;
            }
        }
        return false;
    }
    private boolean dfs(char[][] b, String w, int k, int i, int j, boolean[][] vis) {
        if (k == w.length()) return true;
        if (i < 0 || i >= b.length || j < 0 || j >= b[0].length) return false;
        if (vis[i][j] || b[i][j] != w.charAt(k)) return false;
        vis[i][j] = true;
        boolean ok = dfs(b, w, k + 1, i + 1, j, vis) || dfs(b, w, k + 1, i - 1, j, vis)
                   || dfs(b, w, k + 1, i, j + 1, vis) || dfs(b, w, k + 1, i, j - 1, vis);
        vis[i][j] = false;
        return ok;
    }
}
```

## 题解二：最好理解（原地标记）
- 标签：DFS、回溯、网格搜索
- 思路：用原地字符替换（如将当前格改成特殊值）做临时访问标记，递归返回后再复原；可省去额外 `vis` 数组。

## 总结思路
- 关键在“匹配 + 扩展 +回退”的结构与访问标记；原地法更省空间但需谨慎复原。

## 相关标签
- DFS、回溯、网格搜索