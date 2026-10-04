---
schemaVersion: 3
type: "problem"
leetcodeId: 127
slug: "word-ladder"
titleCn: "单词接龙"
titleEn: "Word Ladder"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/word-ladder/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "b0bd9007fa9be614eedd22009feb0cc182dacdecb532a0443849a786c171fe9b"
sourceFactsSha256: "45b4c269ca419a808671309c167964ce7cc60a8b3e23a4c8c41eebd851d174ac"
sourceSectionHashes:
  description: "c1e5ac879d8ab10d980a0e0447b8971c649ea7b32360f644382c242e6c83d085"
  examples: "ed34711c988d6a01c946a562b43aa644156b35b9760ba8883ca9540a8b1e6cb5"
  constraints: "28840da7aa23b185828a2f747202ddaf03a34a6299b4a739df037b2504233387"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "76d59682eb7a17f5a07d6ecee9da0ff88c0dacb16015caba6a838a4d09c46f35"
  signature: "307eb9fb7f150314ed4c7984057323561a8a7c1f41b133ebd5cf3fe0414e7fa3"
  javaTemplate: "19f301333542ea9fc8a446d2794d12dd95daaca3b185815ede0716ecbfda36fd"
primaryPattern: "图与广度优先"
topics: ["图与广度优先","广度优先搜索","哈希表","字符串","双向搜索"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Breadth-First Search 广度优先"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 127. 单词接龙 / Word Ladder

> **双轨入口：** [[核心模型/图与广度优先/127-Word-Ladder-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`图与广度优先`
- 清单优先级：`P0`
- 清单代表标签：`Breadth-First Search 广度优先`
- LeetCode 当前标签：广度优先搜索 (Breadth-First Search)、哈希表 (Hash Table)、字符串 (String)、双向搜索
- 官方来源：<https://leetcode.cn/problems/word-ladder/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`b0bd9007fa9be614eedd22009feb0cc182dacdecb532a0443849a786c171fe9b`
- 主模型：隐式无权图最短路 BFS

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

字典 `wordList` 中从单词 `beginWord`* *到 `endWord` 的 **转换序列**是一个按下述规格形成的序列 `beginWord -> s_1 -> s_2 -> ... -> s_k`：

- 每一对相邻的单词只差一个字母。

-  对于 `1 <= i <= k` 时，每个 `s_i` 都在 `wordList` 中。注意， `beginWord`* *不需要在 `wordList` 中。

- `s_k == endWord`

给你两个单词**`beginWord`* *和 `endWord` 和一个字典 `wordList` ，返回 *从 `beginWord` 到 `endWord` 的 **最短转换序列** 中的 **单词数目*** 。如果不存在这样的转换序列，返回 `0` 。

## 官方示例


**示例 1：**

```text
输入：beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
输出：5
解释：一个最短转换序列是 "hit" -> "hot" -> "dot" -> "dog" -> "cog", 返回它的长度 5。
```

**示例 2：**

```text
输入：beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
输出：0
解释：endWord "cog" 不在字典中，所以无法进行转换。
```

## 官方约束


- `1 <= beginWord.length <= 10`

- `endWord.length == beginWord.length`

- `1 <= wordList.length <= 5000`

- `wordList[i].length == beginWord.length`

- `beginWord`、`endWord` 和 `wordList[i]` 由小写英文字母组成

- `beginWord != endWord`

- `wordList` 中的所有字符串 **互不相同**

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 把每个单词看作图节点，若两个单词只差一个字符，就在它们之间连边。
2. 不必显式构造所有单词对的边；可逐位置尝试替换为 `a` 到 `z` 来生成邻居。
3. 单词第一次入队时就从未访问集合删除，防止同一层或后续层重复入队。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：beginWord = "hit", endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]
输出：5
解释：最短序列之一是 hit -> hot -> dot -> dog -> cog，共 5 个单词。
```

### 补充用例 2

```text
输入：beginWord = "hit", endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]
输出：0
解释：结束单词不在字典中，无法形成合法序列。
```

### 补充用例 3

```text
输入：beginWord = "a", endWord = "c"
wordList = ["a","b","c"]
输出：2
解释：a 可以直接把一个字母改成 c，序列为 a -> c。
```

## 核心观察

这是一个边权均为 `1` 的隐式图最短路问题。BFS 按转换次数从小到大扩张：队列的第 1 层是 `beginWord`，第 2 层是改变一次可达的单词。第一次取到 `endWord` 时，当前层数必然最小。

字典用 `HashSet` 保存，可在均摊 `O(1)` 时间检查生成的候选是否存在。将已发现单词立即删除，同时充当访问标记。

## 朴素方案：显式两两建图

对字典中任意两个单词比较所有字符，差一位就连边，再从起点 BFS。若字典规模为 `N`、单词长度为 `L`：

- 建图时间复杂度：`O(N^2 * L)`。
- 图空间复杂度：最坏 `O(N^2)`。
- BFS 时间复杂度：`O(N + E)`。

`N = 5000` 时两两比较代价较大。隐式生成邻居只探索实际到达的节点。

## 最优方案推导

1. 把 `wordList` 放入集合；若不含 `endWord`，立即返回 `0`。
2. `beginWord` 入队，初始序列长度为 `1`。
3. 每层固定处理当前队列大小的单词。
4. 对每个字符位置，依次替换为 26 个小写字母，生成候选。
5. 候选在未访问集合中时删除并入队；若等于终点，返回 `steps + 1`。
6. 本层结束后 `steps++`。

## 正确性与不变量

每轮开始时，队列恰好包含从 `beginWord` 经过 `steps-1` 次转换首次到达的所有单词。替换每个位置为所有字母会枚举该单词在字典中的全部合法邻居；未访问集合保证每个节点只在最短距离首次进入队列。BFS 按距离递增处理，因此第一次发现 `endWord` 的序列长度最短。队列耗尽仍未发现，说明起点所在连通分量中没有终点。

## 复杂度

- 时间复杂度：`O(N * L * 26)` 次候选生成，每次构造字符串需要 `O(L)` 时可写成 `O(N * 26 * L^2)`；约束中 `L <= 10`。
- 空间复杂度：`O(N * L)` 用于字典与队列。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

class Solution {
    public int ladderLength(
            String beginWord,
            String endWord,
            List<String> wordList) {
        Set<String> unvisited = new HashSet<>(wordList); // 尚未到达过的字典单词
        if (!unvisited.contains(endWord)) {
            return 0; // 终点不在字典中，无法形成合法路径
        }

        Queue<String> queue = new ArrayDeque<>(); // 当前已经到达的单词
        queue.offer(beginWord); // 起点属于第 1 层
        unvisited.remove(beginWord);
        int steps = 1; // 当前路径包含的单词数量

        while (!queue.isEmpty()) {
            int levelSize = queue.size(); // 先固定当前层，避免下一层混进来
            for (int count = 0; count < levelSize; count++) {
                String current = queue.poll();
                char[] chars = current.toCharArray();

                for (int i = 0; i < chars.length; i++) {
                    char original = chars[i];
                    for (char replacement = 'a'; replacement <= 'z'; replacement++) {
                        if (replacement == original) {
                            continue; // 改回原字母没有产生新单词
                        }
                        chars[i] = replacement;
                        String next = new String(chars);
                        if (next.equals(endWord) && unvisited.contains(next)) {
                            return steps + 1; // 第一次到达终点
                        }
                        if (unvisited.contains(next)) { // 还没有到达过
                            unvisited.remove(next); // 标记为已经到达
                            queue.offer(next); // 加入下一层等待处理
                        }
                    }
                    chars[i] = original; // 恢复这一位，继续生成其他位置的候选
                }
            }
            steps++; // 当前层处理完，下一层的路径多一个单词
        }
        return 0;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

class Solution {
    public int ladderLength(
            String beginWord,
            String endWord,
            List<String> wordList) {
        Set<String> unvisited = new HashSet<>(wordList); // 尚未到达过的字典单词
        if (!unvisited.contains(endWord)) {
            return 0; // 终点不在字典中，无法形成合法路径
        }

        Queue<String> queue = new ArrayDeque<>(); // 当前已经到达的单词
        queue.offer(beginWord); // 起点属于第 1 层
        unvisited.remove(beginWord);
        int steps = 1; // 当前路径包含的单词数量

        while (!queue.isEmpty()) {
            int levelSize = queue.size(); // 先固定当前层，避免下一层混进来
            for (int count = 0; count < levelSize; count++) {
                String current = queue.poll();
                char[] chars = current.toCharArray();

                for (int i = 0; i < chars.length; i++) {
                    char original = chars[i];
                    for (char replacement = 'a'; replacement <= 'z'; replacement++) {
                        if (replacement == original) {
                            continue; // 改回原字母没有产生新单词
                        }
                        chars[i] = replacement;
                        String next = new String(chars);
                        if (next.equals(endWord) && unvisited.contains(next)) {
                            return steps + 1; // 第一次到达终点
                        }
                        if (unvisited.contains(next)) { // 还没有到达过
                            unvisited.remove(next); // 标记为已经到达
                            queue.offer(next); // 加入下一层等待处理
                        }
                    }
                    chars[i] = original; // 恢复这一位，继续生成其他位置的候选
                }
            }
            steps++; // 当前层处理完，下一层的路径多一个单词
        }
        return 0;
    }
}

public class Main {
    public static void main(String[] args) {
        String beginWord = "hit";
        String endWord = "cog";
        List<String> wordList = Arrays.asList(
                "hot", "dot", "dog", "lot", "log", "cog");
        int answer = new Solution().ladderLength(beginWord, endWord, wordList);
        System.out.println("shortest sequence length = " + answer);
    }
}
```

## 边界与易错点

- 返回的是序列中的单词数量，不是边数；起点层数为 `1`。
- `endWord` 不在字典时必须返回 `0`。
- 生成完某位置候选后要恢复原字符，再处理下一位置。
- 访问标记应在入队时设置，而不是出队时，否则同一单词会重复入队。
- 大规模数据可使用双向 BFS，从起点和终点中较小的一侧扩张，显著减少搜索宽度。

## 可扩展变式

- 126. 单词接龙 II：返回所有最短序列，需要记录同层前驱关系后回溯。
- 双向 BFS：两端搜索相遇时得到最短长度。
- 通配模式建图：把 `hot` 映射到 `*ot`、`h*t`、`ho*`，共享桶中的词互为邻居。
- 替换操作带不同成本：边权不再相同，应使用 Dijkstra 算法。
