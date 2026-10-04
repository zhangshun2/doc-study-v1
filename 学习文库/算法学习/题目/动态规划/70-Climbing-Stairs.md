---
schemaVersion: 3
type: "problem"
leetcodeId: 70
slug: "climbing-stairs"
titleCn: "爬楼梯"
titleEn: "Climbing Stairs"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/climbing-stairs/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "7cf0dbf0d6aafda3fb8f6d321076005ab2d5ac74d890553a1fc9508704c8261a"
sourceFactsSha256: "23fe127b18e7e7ebbd254ed9056a000962c3db6e595737b8afbce9cce4f642a7"
sourceSectionHashes:
  description: "824fa062b934b0c201b25de8cbc3f3e93853905e360d04d9ce9010d16ecb1b17"
  examples: "ddaed3b01e159ad2f30d9c50735092f4248cb557c831406ad873a5555213ccde"
  constraints: "af64926997b6422b3712635bfcef196a0c275276e09354fc031af0fd30e7e1ec"
  hints: "d65ff077a78e8c8b13e9381b7856bf2ffccc8724780bdf6fe5c0573eba58e86f"
  tags: "8dc4a86324ac61fe3f6f939d7b430f6110fa7c37a128f98966537274fe6b8073"
  signature: "a45089634013363b8b9c40cb406b0ad48135580169bcdbfda104f503b641fb6b"
  javaTemplate: "109314900fff0e790d84a16b55b8c8804dda586d771c5061e7a37ed36a302604"
primaryPattern: "动态规划"
topics: ["动态规划","记忆化","数学"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Dynamic Programming 动态规划","Memoization 记忆化"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 70. 爬楼梯 / Climbing Stairs

> **双轨入口：** [[核心模型/动态规划/70-Climbing-Stairs-核心模型.md|核心模型]] · [[建模专题/T0/70-Climbing-Stairs-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`动态规划`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Dynamic Programming 动态规划`、`Memoization 记忆化`
- LeetCode 当前标签：记忆化 (Memoization)、数学 (Math)、动态规划 (Dynamic Programming)
- 官方来源：<https://leetcode.cn/problems/climbing-stairs/>
- 直观建模专题：[从枚举完整走法到结算最后一步](../../建模专题/T0/70-Climbing-Stairs-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`7cf0dbf0d6aafda3fb8f6d321076005ab2d5ac74d890553a1fc9508704c8261a`
- 主模型：一维动态规划 / 斐波那契型递推

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

假设你正在爬楼梯。需要 `n` 阶你才能到达楼顶。

每次你可以爬 `1` 或 `2` 个台阶。你有多少种不同的方法可以爬到楼顶呢？

## 官方示例


**示例 1：**

```text
输入：n = 2
输出：2
解释：有两种方法可以爬到楼顶。
1. 1 阶 + 1 阶
2. 2 阶
```

**示例 2：**

```text
输入：n = 3
输出：3
解释：有三种方法可以爬到楼顶。
1. 1 阶 + 1 阶 + 1 阶
2. 1 阶 + 2 阶
3. 2 阶 + 1 阶
```

## 官方约束


- `1 <= n <= 45`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. To reach nth step, what could have been your previous steps? (Think about the step sizes)

## 学习提示（非官方）

1. 到达第 `i` 阶的最后一步，只可能从第 `i-1` 阶走 1 步，或从第 `i-2` 阶走 2 步。
2. 这两类路径的最后一步不同，因此互不重复。
3. 计算第 `i` 项时只需要前两项，可以压缩空间。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：n = 5
输出：8
解释：到达第 5 阶一共有 8 种不同的步长序列。
```

## 核心观察

设 `dp[i]` 为恰好到达第 `i` 阶的方法数。按最后一步分类：

```text
dp[i] = dp[i - 1] + dp[i - 2]
```

基础状态为 `dp[1] = 1`、`dp[2] = 2`。这个数列与斐波那契数列只相差一个下标偏移。

## 朴素方案：直接递归

递归定义 `climb(i) = climb(i-1) + climb(i-2)`，会重复计算大量相同状态。例如计算 `climb(5)` 的左右分支都会计算 `climb(3)`。

- 时间复杂度：`O(2^n)` 的指数级上界。
- 空间复杂度：`O(n)` 递归栈。
- 改进：用数组缓存已经算过的 `climb(i)`，得到记忆化搜索，时间降为 `O(n)`。

## 最优方案推导

自底向上按 `3` 到 `n` 的顺序计算。由于当前答案只依赖前两项，用 `prev2` 表示 `dp[i-2]`，`prev1` 表示 `dp[i-1]`：

```text
current = prev1 + prev2
prev2 = prev1
prev1 = current
```

更新顺序不能颠倒，否则会覆盖尚未使用的旧值。

## 正确性与不变量

循环处理 `step` 之前，`prev2` 等于到达 `step-2` 阶的方法数，`prev1` 等于到达 `step-1` 阶的方法数。所有到达 `step` 的方案按最后一步唯一分为来自这两阶的方案，因此两者相加得到完整且无重复的 `current`。变量右移后，不变量对下一阶继续成立。循环结束时 `prev1 = dp[n]`。

## 复杂度

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }

        int prev2 = 1;
        int prev1 = 2;
        for (int step = 3; step <= n; step++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) {
            return n;
        }

        int prev2 = 1;
        int prev1 = 2;
        for (int step = 3; step <= n; step++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}

public class Main {
    public static void main(String[] args) {
        int n = 2;
        int answer = new Solution().climbStairs(n);
        System.out.println("stairs = " + n);
        System.out.println("ways = " + answer);
    }
}
```

## 边界与易错点

- 题目从 `n = 1` 开始；若扩展到 `n = 0`，组合语义通常定义为一种空方案。
- 基础值是 `1,2`，不是直接返回标准斐波那契的 `F(n)`。
- 循环上界应包含 `n`。
- 若 `n` 更大，结果很快超过 `int`，需要 `long`、`BigInteger` 或对模数取余。

## 可扩展变式

- 每次可走 `1` 到 `k` 阶：`dp[i]` 等于前 `k` 项之和，可用滑动窗口优化。
- 每阶有代价（746）：状态改为到达某阶的最小花费。
- 某些台阶不可落脚：不可用状态置零。
- `n` 极大：用矩阵快速幂把时间降到 `O(log n)`。
