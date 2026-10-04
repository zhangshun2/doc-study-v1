---
schemaVersion: 3
type: "problem"
leetcodeId: 55
slug: "jump-game"
titleCn: "跳跃游戏"
titleEn: "Jump Game"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/jump-game/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "b3c6b2adabfe4dd6b96e15a4f210f33c533503534a5d385f21508eb7c8e2f4c4"
sourceFactsSha256: "10ace42f7ee6e16091dfa4c99eb9097fe14fe80cc9969af3713bc77fbd265e3f"
sourceSectionHashes:
  description: "0d4f66e13caaced3e0f09991f5c1b71380adf94e4f8608037e97bd1e84039320"
  examples: "906a774ee25ad60de7543afc8152893c817f6e8ccfb7cae498e84e66188d0a42"
  constraints: "a7cd1e522015fcd1b161fa77143aed36a7486434fd9ee1f86b7ebece0998631a"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "50138f4725e2b1ef5a622c840c91295240fe97e4f26b5e926075b4b0abbb6902"
  signature: "f70a6df4c2a36b5c82f3322fae8653c39b3ba4e5b898accdf4340f1bbc40d7d2"
  javaTemplate: "8c813375d7382dfd6da3ebf3a3fe9b1b6ace8756414031f83591ec93dd4c2c36"
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
# 55. 跳跃游戏 / Jump Game

> **双轨入口：** [[核心模型/贪心/55-Jump-Game-核心模型.md|核心模型]] · [[建模专题/T0/55-Jump-Game-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`贪心`
- 清单优先级：`P0`
- 清单代表标签：`Greedy 贪心`
- LeetCode 当前标签：贪心 (Greedy)、数组 (Array)、动态规划 (Dynamic Programming)
- 官方来源：<https://leetcode.cn/problems/jump-game/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`b3c6b2adabfe4dd6b96e15a4f210f33c533503534a5d385f21508eb7c8e2f4c4`
- 主模型：维护最远可达位置
- 直观建模专题：[从分支搜索到最远可达前缀](../../建模专题/T0/55-Jump-Game-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个非负整数数组 `nums` ，你最初位于数组的 **第一个下标** 。数组中的每个元素代表你在该位置可以跳跃的最大长度。

判断你是否能够到达最后一个下标，如果可以，返回 `true` ；否则，返回 `false` 。

## 官方示例


**示例 1：**

```text
输入：nums = [2,3,1,1,4]
输出：true
解释：可以先跳 1 步，从下标 0 到达下标 1, 然后再从下标 1 跳 3 步到达最后一个下标。
```

**示例 2：**

```text
输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。
```

## 官方约束


- `1 <= nums.length <= 10^4`

- `0 <= nums[i] <= 10^5`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 不需要枚举每个位置究竟跳几步，只需关心目前能覆盖到的最右位置。
2. 当下标 `i` 大于最远可达位置时，`i` 无法作为新的起跳点。
3. 只要某个可达位置能将覆盖范围延伸到末尾，就可立即返回 `true`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 只需判断可达性，不要求最少跳数或具体路径。
- 期望使用 `O(n)` 时间和 `O(1)` 额外空间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [0]
输出：true
解释：起点本身就是最后一个位置。
```

## 核心观察

如果当前可以到达区间 `[0,farthest]` 中的每个位置，那么遍历其中下标 `i` 时，可以用下面的式子扩大覆盖范围：

```text
farthest = max(farthest, i + nums[i])
```

关键不是“这一跳落在哪里”，而是“所有已知选择共同能覆盖到哪里”。只要 `i <= farthest`，位置 `i` 就可达；若 `i > farthest`，后面的任何位置也无法由当前覆盖触达。

## 朴素方案：回溯所有跳法

从下标 `i` 尝试 `1` 到 `nums[i]` 的每种步长，递归判断能否抵达末尾。大量路径会反复访问同一下标，最坏呈指数增长。加入记忆化后可降到 `O(n^2)`，但仍枚举了不必要的跳跃长度。

- 纯回溯时间复杂度：最坏指数级。
- 记忆化时间复杂度：最坏 `O(n^2)`。
- 递归空间复杂度：`O(n)`。

## 最优方案推导

对于可达性，较远覆盖永远不比更近覆盖差，因此只保留最强状态 `farthest`：

1. 若 `i > farthest`，当前点不可达，返回 `false`。
2. 否则用 `i + nums[i]` 更新 `farthest`。
3. 若 `farthest >= n - 1`，末尾已经可达，返回 `true`。

这是贪心选择：持续保留所有可达选择的最远覆盖，不保存具体跳法。

## 正确性与不变量

处理下标 `i` 之前，`farthest` 是利用已处理且可达的位置能够抵达的最远下标。如果 `i <= farthest`，则 `i` 可达，从它可扩展到 `i + nums[i]`，取最大值后仍是全部已处理位置的最远覆盖。如果 `i > farthest`，没有已处理位置能到达 `i`，而跳跃只能向右，所以无法跨越这一断点。

## 复杂度

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public boolean canJump(int[] nums) {
        int farthest = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > farthest) {
                return false;
            }
            farthest = Math.max(farthest, i + nums[i]);
            if (farthest >= nums.length - 1) {
                return true;
            }
        }
        return true;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public boolean canJump(int[] nums) {
        int farthest = 0;
        for (int i = 0; i < nums.length; i++) {
            if (i > farthest) {
                return false;
            }
            farthest = Math.max(farthest, i + nums[i]);
            if (farthest >= nums.length - 1) {
                return true;
            }
        }
        return true;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {2, 3, 1, 1, 4};
        boolean answer = new Solution().canJump(nums);
        System.out.println("nums = " + Arrays.toString(nums));
        System.out.println("can reach last index = " + answer);
    }
}
```

## 边界与易错点

- 长度为 `1` 时无需跳跃，应返回 `true`。
- 数组中出现 `0` 不一定失败，之前的覆盖范围可能直接跨过它。
- 必须先验证 `i <= farthest`，再把 `i` 当作起跳点更新范围。
- 本题不求最少跳数；最少跳数是 45. 跳跃游戏 II，需要维护当前层边界。

## 可扩展变式

- 45. 跳跃游戏 II：在可达前提下求最少跳跃次数。
- 返回一条可行路径：扩展覆盖范围时记录前驱位置。
- 允许向左跳：单向覆盖不再成立，通常转化为图搜索。
- 跳跃游戏 III、IV：加入目标值或相同值传送，需要 BFS 和访问标记。
