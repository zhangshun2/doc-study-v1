---
schemaVersion: 3
type: "problem"
leetcodeId: 200
slug: "number-of-islands"
titleCn: "岛屿数量"
titleEn: "Number of Islands"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/number-of-islands/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "10a22fad93fdb92f5db5b577ba9b5645dac433300433a8c4101b1bffffe8473d"
sourceFactsSha256: "af07384bea2d5b2c5954ff83f3711b414411491319573bca9397db97fb7bb95f"
sourceSectionHashes:
  description: "5b598fddb7242029208ba8d84d6279f4dd31398a07bdf0631f55f3381c6952c5"
  examples: "e9bf3adffe1f317732ca9de037c55bc8c81fc1c14d4778e18e09bde731dbc315"
  constraints: "49fdb00debdbb8f2ad28ed2c1df8fed53b8a252e40cefd617224fa4090dbec17"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "d255f3ca08b65278e6383f36fda53f06debd3e64847878ee09a0c749f6111909"
  signature: "693369d26dbb91c3a51ea5c4f042de4cd3a0b2820c19784b9c9ca3f8dcd2c2ba"
  javaTemplate: "44f908077b79aa31d967271378fd35883e65958f11de678dc6191bff91b57c9e"
primaryPattern: "图与搜索"
topics: ["图与搜索","深度优先搜索","广度优先搜索","并查集","数组","矩阵"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Depth-First Search 深度优先","Breadth-First Search 广度优先","Matrix 矩阵","Union Find 并查集"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 200. 岛屿数量 / Number of Islands

> **双轨入口：** [[核心模型/图与搜索/200-Number-of-Islands-核心模型.md|核心模型]] · [[建模专题/T0/200-Number-of-Islands-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`图与搜索`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Depth-First Search 深度优先`、`Breadth-First Search 广度优先`、`Matrix 矩阵`、`Union Find 并查集`
- LeetCode 当前标签：深度优先搜索 (Depth-First Search)、广度优先搜索 (Breadth-First Search)、并查集 (Union Find)、数组 (Array)、矩阵 (Matrix)
- 官方来源：<https://leetcode.cn/problems/number-of-islands/>
- 直观建模专题：[从数格子到数连通块](../../建模专题/T0/200-Number-of-Islands-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`10a22fad93fdb92f5db5b577ba9b5645dac433300433a8c4101b1bffffe8473d`
- **主解法**：网格 DFS（显式栈）

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

## 官方示例


**示例 1：**

```text
输入：grid = [
  ['1','1','1','1','0'],
  ['1','1','0','1','0'],
  ['1','1','0','0','0'],
  ['0','0','0','0','0']
]
输出：1
```

**示例 2：**

```text
输入：grid = [
  ['1','1','0','0','0'],
  ['1','1','0','0','0'],
  ['0','0','1','0','0'],
  ['0','0','0','1','1']
]
输出：3
```

## 官方约束


- `m == grid.length`

- `n == grid[i].length`

- `1 <= m, n <= 300`

- `grid[i][j]` 的值为 `'0'` 或 `'1'`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 每发现一块尚未访问的陆地，就发现了一个新连通分量。
2. 从该格出发，把同一岛屿的所有陆地一次性标记，避免重复计数。
3. 递归 DFS 在全是陆地的大网格上可能导致 Java 栈溢出，可以使用显式栈或 BFS。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

将每个陆地格看作图的节点，四方向相邻陆地间有边。问题就是统计无向图的连通分量数。外层遍历负责找到每个分量的第一个节点，内层 DFS/BFS 负责消费完整分量。

## 朴素方案

对每个陆地格都单独搜索它能到达的所有陆地，却不记录访问状态，会反复遍历同一个岛，最坏可达 `O((mn)^2)`。即使记录访问，如果每次搜索都重新创建整张访问矩阵也有额外开销。

## 最优方案推导

从左到右、从上到下扫描：

1. 遇到 `'0'` 跳过。
2. 遇到 `'1'`，岛屿计数加一，并从该点进行 DFS。
3. 每当陆地入栈时立即改为 `'0'`，表示已经发现，防止同一节点被多个邻居重复入栈。

每个格子最多入栈一次。若不能修改输入，可使用 `boolean[][] visited`。

## 正确性与不变量

外层扫描到某个仍为 `'1'` 的格子时，它不可能属于此前计数过的岛屿，否则此前的完整搜索已经将其标记。因此它必属于一个新岛屿，计数加一正确。

DFS 沿所有四方向陆地边扩展，既不会越过水域进入其他岛，也不会漏掉当前连通分量中的陆地。搜索结束后整个岛均已标记。故每个岛恰好计数一次。

## 复杂度

- **时间复杂度**：`O(mn)`，每个格最多被检查常数次。
- **空间复杂度**：`O(mn)` 最坏情况，显式栈可能包含大量陆地；修改原网格省去访问矩阵。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    private static final int[][] DIRECTIONS = {
            {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    public int numIslands(char[][] grid) {
        int rows = grid.length;
        int cols = grid[0].length;
        int islands = 0;

        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (grid[row][col] != '1') {
                    continue;
                }
                islands++;
                floodFill(grid, row, col);
            }
        }
        return islands;
    }

    private void floodFill(char[][] grid, int startRow, int startCol) {
        int rows = grid.length;
        int cols = grid[0].length;
        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{startRow, startCol});
        grid[startRow][startCol] = '0';

        while (!stack.isEmpty()) {
            int[] cell = stack.pop();
            for (int[] direction : DIRECTIONS) {
                int nextRow = cell[0] + direction[0];
                int nextCol = cell[1] + direction[1];
                if (nextRow >= 0 && nextRow < rows
                        && nextCol >= 0 && nextCol < cols
                        && grid[nextRow][nextCol] == '1') {
                    grid[nextRow][nextCol] = '0';
                    stack.push(new int[]{nextRow, nextCol});
                }
            }
        }
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    private static final int[][] DIRECTIONS = {
            {1, 0}, {-1, 0}, {0, 1}, {0, -1}
    };

    public int numIslands(char[][] grid) {
        int rows = grid.length;
        int cols = grid[0].length;
        int islands = 0;

        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if (grid[row][col] != '1') {
                    continue;
                }
                islands++;
                floodFill(grid, row, col);
            }
        }
        return islands;
    }

    private void floodFill(char[][] grid, int startRow, int startCol) {
        int rows = grid.length;
        int cols = grid[0].length;
        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{startRow, startCol});
        grid[startRow][startCol] = '0';

        while (!stack.isEmpty()) {
            int[] cell = stack.pop();
            for (int[] direction : DIRECTIONS) {
                int nextRow = cell[0] + direction[0];
                int nextCol = cell[1] + direction[1];
                if (nextRow >= 0 && nextRow < rows
                        && nextCol >= 0 && nextCol < cols
                        && grid[nextRow][nextCol] == '1') {
                    grid[nextRow][nextCol] = '0';
                    stack.push(new int[]{nextRow, nextCol});
                }
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        char[][] grid1 = {
                {'1', '1', '1', '1', '0'},
                {'1', '1', '0', '1', '0'},
                {'1', '1', '0', '0', '0'},
                {'0', '0', '0', '0', '0'}
        };
        char[][] grid2 = {
                {'1', '1', '0', '0', '0'},
                {'1', '1', '0', '0', '0'},
                {'0', '0', '1', '0', '0'},
                {'0', '0', '0', '1', '1'}
        };
        Solution solution = new Solution();
        System.out.println(solution.numIslands(grid1)); // 1
        System.out.println(solution.numIslands(grid2)); // 3
    }
}
```

## 边界与易错点

- 输入元素是字符 `'1'`/`'0'`，不是整数 `1`/`0`。
- 对角相邻不连通。
- 此解法会修改输入；若调用方仍需原矩阵，使用 `visited` 或先复制。
- 标记时机应是“入栈时”而非“出栈时”，否则同一格可能重复入栈。
- Java 递归深度有限，`300 * 300` 的蛇形岛屿可能让递归 DFS 栈溢出。

## 可扩展变式

- 八方向岛屿：增加四个对角方向。
- 最大岛屿面积：DFS 返回或累计当前连通分量大小。
- 动态增加陆地：使用并查集维护连通分量数量。
- 不规则边界上的封闭岛屿：先从边缘消除与外界连通的陆地。
