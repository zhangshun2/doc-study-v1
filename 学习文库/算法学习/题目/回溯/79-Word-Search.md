---
schemaVersion: 3
type: "problem"
leetcodeId: 79
slug: "word-search"
titleCn: "单词搜索"
titleEn: "Word Search"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/word-search/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "7c250d8c690824a65f06f731436a8595f21192f125f21140f0bbad6988044023"
sourceFactsSha256: "cf2c7e400728cce91f9090535b127bcd04d8824d746d91ccda17956c26a63ed9"
sourceSectionHashes:
  description: "a236d740eb864dffc3d7692be6edf58dba91db5a14a87b4ba1644a3c1674ba1a"
  examples: "203f6c62eee330700fc3a2d7d2f1f70f3c567dc418c834432d8f39798092e62c"
  constraints: "6c2fb436f34895d4fe746067711b86b0622f709497858e1be08efdcf5454e56d"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "72c06f8a4c3b18c24d7bdf87648b596f35b2f2d2b4304c71a01b88766622ccfb"
  signature: "869ea6420bb3c6eeb72c5bf30b8ecce02ef663634d58768752841f40bf9ac4fc"
  javaTemplate: "4c7ac717ac349dfe521df619d8032ed3c53cbce5043ccad7c21f71994766f6a2"
primaryPattern: "回溯"
topics: ["回溯","深度优先搜索","数组","字符串","矩阵"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Backtracking 回溯"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 79. 单词搜索 / Word Search

> **双轨入口：** [[核心模型/回溯/79-Word-Search-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`回溯`
- 清单优先级：`P0`
- 清单代表标签：`Backtracking 回溯`
- LeetCode 当前标签：深度优先搜索 (Depth-First Search)、数组 (Array)、字符串 (String)、回溯 (Backtracking)、矩阵 (Matrix)
- 官方来源：<https://leetcode.cn/problems/word-search/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`7c250d8c690824a65f06f731436a8595f21192f125f21140f0bbad6988044023`
- 主模型：网格深度优先搜索与现场恢复

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个 `m x n` 二维字符网格 `board` 和一个字符串单词 `word` 。如果 `word` 存在于网格中，返回 `true` ；否则，返回 `false` 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/11/04/word2.jpg)

```text
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCCED"
输出：true
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/11/04/word-1.jpg)

```text
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "SEE"
输出：true
```

**示例 3：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/10/15/word3.jpg)

```text
输入：board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = "ABCB"
输出：false
```

## 官方约束


- `m == board.length`

- `n = board[i].length`

- `1 <= m, n <= 6`

- `1 <= word.length <= 15`

- `board` 和 `word` 仅由大小写英文字母组成

**进阶：**你可以使用搜索剪枝的技术来优化解决方案，使其在 `board` 更大的情况下可以更快解决问题？

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 枚举网格中每个格子作为单词起点。
2. 递归状态需要包含当前位置和正在匹配的 `word` 下标。
3. 为防止重复使用，进入格子后暂时标记；离开该递归分支时恢复原字符。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "ABCCED"
输出：true
解释：可以从左上角 A 开始，依次经过 B、C、C、E、D。
```

### 补充用例 2

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "SEE"
输出：true
```

### 补充用例 3

```text
输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
word = "ABCB"
输出：false
解释：最后一个 B 只能重复使用已经走过的单元格，不符合要求。
```

## 核心观察

函数 `dfs(row,col,index)` 表示：能否从 `(row,col)` 开始匹配 `word[index]` 及其后缀。一次递归只在当前格字符匹配时继续，然后从四个方向选择下一格。

不能使用全局永久 `visited`，因为“不可重复”只针对一条当前路径。一个格子在失败分支中使用后，其他起点或分支仍应允许使用它，这正是回溯恢复现场的原因。

## 朴素方案：枚举所有固定长度路径

从每个格子出发，不看字符是否匹配就枚举长度为 `word.length()` 的所有四向路径，最后拼接字符比较。粗略上界为 `O(mn * 4^L)`，并产生大量字符串和重复格检查。

改进点是在进入每层时立即比较当前字符；不匹配就终止，使实际搜索树显著缩小。走过第一步后也不能原路返回，因此更紧的常见上界是 `O(mn * 3^L)`，但最坏仍为指数级。

## 最优方案推导

1. 枚举每个格子，只有它等于 `word[0]` 时 DFS 才会继续。
2. DFS 首先检查越界、字符不等；失败立即返回。
3. 若当前已匹配最后一个字符，返回 `true`。
4. 暂时把当前格改成不可能出现在输入中的 `'#'`，递归四邻格。
5. 无论成功或失败，在返回前恢复原字符。

原地标记避免额外 `visited` 矩阵，但会暂时修改输入，恢复步骤不可省略。

## 正确性与不变量

进入有效 DFS 节点时，从起点到当前位置的路径与 `word[0..index]` 完全相同，且路径中的单元格互不重复。标记当前格后，四个递归分支恰好枚举所有允许的下一步；越界、不匹配和已标记格都会被排除。任意合法单词路径必从某个枚举起点开始，并在每一步属于四分支之一，所以不会遗漏。恢复字符保证不同分支之间状态独立。

## 复杂度

- 时间复杂度：最坏 `O(mn * 3^L)`，其中 `L = word.length()`；用较松上界可写为 `O(mn * 4^L)`。
- 空间复杂度：`O(L)` 递归栈；原地标记不使用额外访问矩阵。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public boolean exist(char[][] board, String word) {
        for (int row = 0; row < board.length; row++) {
            for (int col = 0; col < board[0].length; col++) {
                if (dfs(board, word, row, col, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(
            char[][] board,
            String word,
            int row,
            int col,
            int index) {
        if (row < 0 || row >= board.length
                || col < 0 || col >= board[0].length
                || board[row][col] != word.charAt(index)) {
            return false;
        }
        if (index == word.length() - 1) {
            return true;
        }

        char original = board[row][col];
        board[row][col] = '#';
        boolean found = dfs(board, word, row + 1, col, index + 1)
                || dfs(board, word, row - 1, col, index + 1)
                || dfs(board, word, row, col + 1, index + 1)
                || dfs(board, word, row, col - 1, index + 1);
        board[row][col] = original;
        return found;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public boolean exist(char[][] board, String word) {
        for (int row = 0; row < board.length; row++) {
            for (int col = 0; col < board[0].length; col++) {
                if (dfs(board, word, row, col, 0)) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean dfs(
            char[][] board,
            String word,
            int row,
            int col,
            int index) {
        if (row < 0 || row >= board.length
                || col < 0 || col >= board[0].length
                || board[row][col] != word.charAt(index)) {
            return false;
        }
        if (index == word.length() - 1) {
            return true;
        }

        char original = board[row][col];
        board[row][col] = '#';
        boolean found = dfs(board, word, row + 1, col, index + 1)
                || dfs(board, word, row - 1, col, index + 1)
                || dfs(board, word, row, col + 1, index + 1)
                || dfs(board, word, row, col - 1, index + 1);
        board[row][col] = original;
        return found;
    }
}

public class Main {
    public static void main(String[] args) {
        char[][] board = {
            {'A', 'B', 'C', 'E'},
            {'S', 'F', 'C', 'S'},
            {'A', 'D', 'E', 'E'}
        };
        String word = "ABCCED";
        System.out.println(new Solution().exist(board, word));
    }
}
```

## 边界与易错点

- 找到最后一个匹配字符后应直接成功，不再访问下一层 `word.charAt(index)`。
- 使用逻辑短路后仍要在方法返回前恢复当前格，不能在分支中提前返回而跳过恢复。
- `'#'` 可作标记，因为约束保证输入只有英文字母。
- 四方向不包含对角线。
- 若先做字符频次检查，发现网格某字符总数少于单词需求，可提前返回 `false`。

## 可扩展变式

- 212. 单词搜索 II：同时查找多个单词，使用 Trie 共享前缀搜索。
- 返回具体路径：在递归中维护坐标列表，成功时复制。
- 允许单元格重复使用：去掉访问标记，但需要限制路径长度。
- 八方向搜索：扩展方向数组，搜索分支因子随之增大。
