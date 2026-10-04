# LeetCode-200 岛屿数量

- 难度：中等
- 链接：https://leetcode.cn/problems/number-of-islands/

## 问题描述
给定 `m x n` 的二维网格 `grid`，其中 `'1'` 表示陆地，`'0'` 表示水域，统计岛屿数量。岛屿由水平或垂直方向相邻的陆地相连构成。

## 题解一：官方经典（DFS 淹没法）
- 思路：遍历网格，遇到 `'1'` 计数加一，并用 DFS 将其四邻接陆地全部淹没为 `'0'`，避免重复计数。
- 复杂度：时间 O(m·n)，空间 O(m·n) 最坏递归栈。

```java
class Solution {
    public int numIslands(char[][] grid) {
        int m = grid.length, n = grid[0].length, cnt = 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') { cnt++; dfs(grid, i, j); }
            }
        }
        return cnt;
    }
    private void dfs(char[][] g, int i, int j) {
        if (i < 0 || i >= g.length || j < 0 || j >= g[0].length) return;
        if (g[i][j] != '1') return;
        g[i][j] = '0';
        dfs(g, i + 1, j); dfs(g, i - 1, j); dfs(g, i, j + 1); dfs(g, i, j - 1);
    }
}
```

## 题解二：通用解法（BFS 队列）
- 标签：DFS、BFS、连通分量、涂色
- 思路：遇到 `'1'` 时，入队并进行层序扩展，将联通的 `'1'` 置为 `'0'`。适合迭代不使用递归栈。

```java
import java.util.*;
class Solution {
    public int numIslands(char[][] grid) {
        int m = grid.length, n = grid[0].length, cnt = 0;
        int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (grid[i][j] == '1') {
                    cnt++;
                    Deque<int[]> dq = new ArrayDeque<>(); dq.offer(new int[]{i,j}); grid[i][j]='0';
                    while(!dq.isEmpty()){
                        int[] p=dq.poll();
                        for(int[] d:dirs){
                            int x=p[0]+d[0], y=p[1]+d[1];
                            if(x>=0&&x<m&&y>=0&&y<n&&grid[x][y]=='1'){
                                grid[x][y]='0'; dq.offer(new int[]{x,y});
                            }
                        }
                    }
                }
            }
        }
        return cnt;
    }
}
```

## 总结思路
- “发现一个岛屿 + 淹没整个连通块”是标准模板；DFS 与 BFS 等价。

## 相关标签
- DFS、BFS、连通分量、涂色