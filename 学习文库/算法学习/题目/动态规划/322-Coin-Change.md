---
schemaVersion: 3
type: "problem"
leetcodeId: 322
slug: "coin-change"
titleCn: "零钱兑换"
titleEn: "Coin Change"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/coin-change/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "39384d1bcea0942daa5e9f5d30d293f319c19e884c1ff192fbdef6006f63f2a2"
sourceFactsSha256: "7800922739ae43b447b6e10ed2dd3a2c15f9a2b99943bd74986383254de6ff67"
sourceSectionHashes:
  description: "295692226466f129fff0f5de8cdcc26e3f66ec67f4b68599e700e71bcbc75d9a"
  examples: "983ec9c4e25364026fae63dd54232da173b3f2ec9f2ce4ac3109a9d0b5e7d1c1"
  constraints: "d82c5cef1087e727ddfdd70e9ca6cfe08830822b5ffeafcf49f9ac6c5f0855db"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "27c9abf76cc50632417c831e678b0b928f55a3e1a813cae762daa7a53b2fb13a"
  signature: "c7320ce2efe21654260c3335f9426a2c2a38bbc20c07e29341bcad9560d68131"
  javaTemplate: "9b6c64ce9d37b336ab91710da35923253ab613c32f1473436b5a3a46b562b0b3"
primaryPattern: "动态规划"
topics: ["动态规划","广度优先搜索","数组","背包问题","完全背包"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Dynamic Programming 动态规划"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 322. 零钱兑换 / Coin Change

> **双轨入口：** [[核心模型/动态规划/322-Coin-Change-核心模型.md|核心模型]] · [[建模专题/T0/322-Coin-Change-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P0`
- 清单代表标签：`Dynamic Programming 动态规划`
- LeetCode 当前标签：广度优先搜索 (Breadth-First Search)、数组 (Array)、动态规划 (Dynamic Programming)、背包问题、完全背包
- 官方来源：<https://leetcode.cn/problems/coin-change/>
- 直观建模专题：[从枚举硬币序列到结算最后一枚硬币](../../建模专题/T0/322-Coin-Change-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`39384d1bcea0942daa5e9f5d30d293f319c19e884c1ff192fbdef6006f63f2a2`
- **主解法**：完全背包一维动态规划

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `coins` ，表示不同面额的硬币；以及一个整数 `amount` ，表示总金额。

计算并返回可以凑成总金额所需的 **最少的硬币个数** 。如果没有任何一种硬币组合能组成总金额，返回 `-1` 。

你可以认为每种硬币的数量是无限的。

## 官方示例


**示例 1：**

```text
输入：coins = [1, 2, 5], amount = 11
输出：3
解释：11 = 5 + 5 + 1
```

**示例 2：**

```text
输入：coins = [2], amount = 3
输出：-1
```

**示例 3：**

```text
输入：coins = [1], amount = 0
输出：0
```

## 官方约束


- `1 <= coins.length <= 12`

- `1 <= coins[i] <= 2^31 - 1`

- `0 <= amount <= 10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. `dp[x]` 可定义为凑出金额 `x` 的最少硬币数。
2. 若最后使用面额 `coin`，此前需要最优地凑出 `x - coin`。
3. 不可达状态设为 `amount + 1`，比任何可能答案都大且加一不会溢出。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

一个最优方案拿掉最后一枚硬币后，剩余部分也必须是对应金额的最优方案，否则替换成更优剩余方案就能减少硬币总数。由此得到：

```text
dp[x] = min(dp[x - coin] + 1)，其中 coin <= x
```

基础状态 `dp[0] = 0`。

## 朴素方案

递归枚举每一步选哪枚硬币，会产生大量重复金额状态，分支数约为硬币种数，最坏呈指数增长。贪心每次选最大硬币也不可靠，例如面额 `[1,3,4]`、金额 6：贪心得到 `4+1+1` 三枚，最优为 `3+3` 两枚。

加入记忆化后，每个剩余金额只计算一次，复杂度与自底向上 DP 相同。

## 最优方案推导

初始化 `dp[0]=0`，其余填入不可达哨兵 `amount+1`。从金额 1 到 `amount` 递增枚举，对每种不超过当前金额的硬币尝试转移。金额递增保证 `dp[current-coin]` 已经计算完成；同一硬币可以重复使用，符合完全背包。

最后若 `dp[amount] > amount`，说明不可达，返回 `-1`。

## 正确性与不变量

按金额做归纳。`dp[0]=0` 显然最优。假设小于 `x` 的状态均正确。任意凑出 `x` 的方案都有一枚最后硬币 `coin`，去掉后凑出 `x-coin`，根据归纳假设至少需要 `dp[x-coin]` 枚，所以方案至少为转移值之一。算法又枚举所有可选最后硬币，并能把对应最优子方案加一构造成方案，因此取得的最小值恰为最优答案。

## 复杂度

- **时间复杂度**：`O(amount * coins.length)`。
- **空间复杂度**：`O(amount)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int coinChange(int[] coins, int amount) {
        int unreachable = amount + 1;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, unreachable);
        dp[0] = 0;

        for (int current = 1; current <= amount; current++) {
            for (int coin : coins) {
                if (coin <= current) {
                    dp[current] = Math.min(
                            dp[current], dp[current - coin] + 1);
                }
            }
        }
        return dp[amount] == unreachable ? -1 : dp[amount];
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public int coinChange(int[] coins, int amount) {
        int unreachable = amount + 1;
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, unreachable);
        dp[0] = 0;

        for (int current = 1; current <= amount; current++) {
            for (int coin : coins) {
                if (coin <= current) {
                    dp[current] = Math.min(
                            dp[current], dp[current - coin] + 1);
                }
            }
        }
        return dp[amount] == unreachable ? -1 : dp[amount];
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.coinChange(
                new int[]{1, 2, 5}, 11)); // 3
        System.out.println(solution.coinChange(
                new int[]{2}, 3)); // -1
        System.out.println(solution.coinChange(
                new int[]{1}, 0)); // 0
    }
}
```

## 边界与易错点

- `amount == 0` 时答案是 0，不需要硬币。
- 哨兵不要用 `Integer.MAX_VALUE` 后直接加一，否则会溢出。
- `amount + 1` 是安全哨兵：面额至少为 1，任何可行方案最多使用 `amount` 枚。
- 本题硬币无限；若每枚只能用一次，循环方向和状态转移语义会变化。
- 判断不可达可写 `dp[amount] == unreachable`，前提是所有更新都只会取更小值。

## 可扩展变式

- 输出具体硬币组合：记录 `chosen[x]`，从 `amount` 反向减去所选硬币。
- 统计组合数：转为计数 DP，硬币在外层可避免不同顺序重复计数。
- 统计排列数：金额在外层，顺序不同视为不同方案。
- 每种硬币数量有限：二进制拆分为 0/1 背包，或使用单调队列优化多重背包。
