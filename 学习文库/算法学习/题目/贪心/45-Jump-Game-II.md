---
schemaVersion: 3
type: "problem"
leetcodeId: 45
slug: "jump-game-ii"
titleCn: "跳跃游戏 II"
titleEn: "Jump Game II"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/jump-game-ii/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "5d857b231862f115642b0a55475c3e8209342d5de4d0fee78e5ad7fce2122f2e"
sourceFactsSha256: "05ff6df1d34837bb162f4025b561e99e82bbe643bfb8e27f9179d5b18df19ab6"
sourceSectionHashes:
  description: "f8f7422a061d3f259cf240493f8b69065a242061cfef31ce623c297a0eeba6ea"
  examples: "78f3ca1536122e0d09d43c0f4b96345abc217d33c0724640cb8752d5cd4bc9cd"
  constraints: "8fe1da0656b484bbffb04a07df0dbce561c1ecc2d1700582a32d6b55ea6bd344"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "50138f4725e2b1ef5a622c840c91295240fe97e4f26b5e926075b4b0abbb6902"
  signature: "fd158ec90cb4daaace134a11f09708ee5715dc77782e82dedb0e75ff4022d9b8"
  javaTemplate: "82a39556a6c5cfc3221184ddc0dbc4da270daa64bf3b0e2afcf928187cfc744a"
primaryPattern: "贪心"
topics: ["贪心","数组","动态规划"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Greedy 贪心"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 45. 跳跃游戏 II / Jump Game II

> **双轨入口：** [[核心模型/贪心/45-Jump-Game-II-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`贪心`
- 清单优先级：`P0`
- 清单代表标签：`Greedy 贪心`
- LeetCode 当前标签：贪心 (Greedy)、数组 (Array)、动态规划 (Dynamic Programming)
- 官方来源：<https://leetcode.cn/problems/jump-game-ii/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`5d857b231862f115642b0a55475c3e8209342d5de4d0fee78e5ad7fce2122f2e`
- 主模型：按跳跃次数分层的贪心区间扩张

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个长度为 `n` 的 **0 索引**整数数组 `nums`。初始位置在下标 0。

每个元素 `nums[i]` 表示从索引 `i` 向后跳转的最大长度。换句话说，如果你在索引 `i` 处，你可以跳转到任意 `(i + j)` 处：

- `0 <= j <= nums[i]` 且

- `i + j < n`

返回到达 `n - 1` 的最小跳跃次数。测试用例保证可以到达 `n - 1`。

## 官方示例


**示例 1:**

```text
输入: nums = [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 2。
     从下标为 0 跳到下标为 1 的位置，跳 1 步，然后跳 3 步到达数组的最后一个位置。
```

**示例 2:**

```text
输入: nums = [2,3,0,1,4]
输出: 2
```

## 官方约束


- `1 <= nums.length <= 10^4`

- `0 <= nums[i] <= 1000`

- 题目保证可以到达 `n - 1`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 不要贪心地直接跳到当前可到达的最远下标；那个落点未必带来下一步最远覆盖。
2. 把一次跳跃能覆盖的下标看成 BFS 的一层。
3. 扫描当前层内所有位置，记录它们下一跳可覆盖的最远边界 `farthest`。
4. 扫描到当前层边界 `currentEnd` 时，才把跳跃次数加一并进入下一层。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 最优贪心为 `O(n)` 时间、`O(1)` 空间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [0]
输出：0
解释：起点已经是终点，不需要跳跃。
```

## 核心观察

从起点跳 1 次能到达一个连续区间；从该区间任意位置再跳一次，所有可达位置的并集仍是一个从左侧开始的连续区间。只关心每层最远边界，而不需要保存所有路径。

三个状态的含义：

```text
jumps       已经确定使用的跳跃次数
currentEnd  使用 jumps 次能够覆盖的最远位置
farthest    在扫描当前层时发现的下一层最远位置
```

## 朴素方案：动态规划或显式 BFS

动态规划令 `dp[i]` 表示到达 `i` 的最少步数，从每个位置更新其可达后继。最坏会枚举大量边。

- 时间复杂度：最坏 `O(n^2)`。
- 空间复杂度：`O(n)`。

显式 BFS 虽能得到最短跳数，但保存队列和访问状态是不必要的，因为可达集合具有连续区间结构。

## 最优方案：贪心分层扫描

只扫描到 `n-2`，因为一旦下一层覆盖末尾，不需要真的从末尾再跳。每个 `i` 都更新 `farthest=max(farthest,i+nums[i])`。当 `i==currentEnd` 时，当前层扫描完毕，必须使用一次跳跃，把边界更新为 `farthest`。

### 正确性与不变量

扫描当前层时，`farthest` 是从所有不超过当前跳数可达的位置再跳一步能到达的最远下标。到达 `currentEnd` 后，当前层所有候选已完整考察，任何使用 `jumps+1` 次的路径都不可能超过 `farthest`，而 `farthest` 又确实由某个可达位置产生，因此它恰是下一层边界。按层首次覆盖终点的跳数就是最短跳数，与无权图 BFS 的最短路性质一致。

- 时间复杂度：`O(n)`，每个下标最多扫描一次。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int jump(int[] nums) {
        int jumps = 0;
        int currentEnd = 0;
        int farthest = 0;

        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == currentEnd) {
                jumps++;
                currentEnd = farthest;
            }
        }
        return jumps;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public int jump(int[] nums) {
        int jumps = 0;
        int currentEnd = 0;
        int farthest = 0;

        for (int i = 0; i < nums.length - 1; i++) {
            farthest = Math.max(farthest, i + nums[i]);
            if (i == currentEnd) {
                jumps++;
                currentEnd = farthest;
            }
        }
        return jumps;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.jump(new int[]{2, 3, 1, 1, 4})); // 2
        System.out.println(solution.jump(new int[]{2, 3, 0, 1, 4})); // 2
        System.out.println(solution.jump(new int[]{0}));             // 0
        System.out.println(solution.jump(new int[]{1, 1, 1, 1}));    // 3
    }
}
```

## 边界与易错点

- 循环必须止于 `nums.length-2`；若处理最后下标，可能多统计一次跳跃。
- `jumps++` 的时机是扫描到当前层边界，不是每访问一个位置。
- “当前直接跳最远”不是正确证明；本解法是考察当前层所有落点后，让下一层覆盖最远。
- 单元素数组无需跳跃，循环不会执行，答案为 0。
- 若题目不保证可达，需要在层结束时检查 `farthest == currentEnd` 并报告失败。

## 可扩展变式

- 跳跃游戏 I 只问能否到达，维护单个最远可达位置即可。
- 若要输出一条最短路径，需要额外记录产生每层最远边界的落点或父节点。
- 跳跃带不同代价时不再是无权分层问题，可能需要 Dijkstra 或动态规划。
