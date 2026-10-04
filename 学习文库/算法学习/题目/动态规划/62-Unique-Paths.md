---
schemaVersion: 3
type: "problem"
leetcodeId: 62
slug: "unique-paths"
titleCn: "不同路径"
titleEn: "Unique Paths"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/unique-paths/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "5dff079f199b339f20a1b640283e31564a7acad237310cfaacfee293b4b2aa29"
sourceFactsSha256: "764f942398811ddc525530f391db2620b3c3c3a475974ff6a389a3e332079f79"
sourceSectionHashes:
  description: "c96677f7b287391f09e7e2a0789931106adda671ddb526fef00b4b0dd1a400bb"
  examples: "8589661e4ebbff97d43297e7606abfe436772755a0ca6ee3a244356ec103f61f"
  constraints: "e4c893ee18e9a77d2d3027906a0027b58c7638577bf998549deb8a8c5718daac"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "d83af970bc4f59b4191769566e83001ab129523eccc8eba0352f1e3080874f9d"
  signature: "3dbe5f6f11697531c3c3b3472cc96e2a349d077448709515398861ac4c659d0d"
  javaTemplate: "9974e78d2dfb5d3611c1bad17c82cbc79b70ecd32ed339ebc5781acf711cbb17"
primaryPattern: "动态规划"
topics: ["动态规划","数学","组合数学"]
priority: "P1"
checklistPriorities: ["P1","P2"]
checklistTags: ["Math 数学","Combinatorics 组合数学"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 62. 不同路径 / Unique Paths

> **双轨入口：** [[核心模型/动态规划/62-Unique-Paths-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P1`、`P2`
- 清单代表标签：`Math 数学`、`Combinatorics 组合数学`
- LeetCode 当前标签：数学 (Math)、动态规划 (Dynamic Programming)、组合数学 (Combinatorics)
- 官方来源：<https://leetcode.cn/problems/unique-paths/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`5dff079f199b339f20a1b640283e31564a7acad237310cfaacfee293b4b2aa29`
- 主模型：二维网格动态规划，压缩为一维

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

一个机器人位于一个 `m x n`* *网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？

## 官方示例


**示例 1：**

![Official problem illustration](https://pic.leetcode.cn/1697422740-adxmsI-image.png)

```text
输入：m = 3, n = 7
输出：28
```

**示例 2：**

```text
输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下
```

**示例 3：**

```text
输入：m = 7, n = 3
输出：28
```

**示例 4：**

```text
输入：m = 3, n = 3
输出：6
```

## 官方约束


- `1 <= m, n <= 100`

- 题目数据保证答案小于等于 `2 * 10^9`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 到达一个非边界格子的最后一步只可能来自上方或左方。
2. 第一行和第一列都只有一种到达方式。
3. 一维压缩时，`dp[col]` 更新前代表上方路径数，`dp[col - 1]` 代表左方路径数。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 动态规划目标为 `O(mn)` 时间，可把空间降到 `O(n)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：m = 1, n = 5
输出：1
解释：只有一直向右这一种路径。
```

## 核心观察

定义 `ways[row][col]` 为到达格子 `(row,col)` 的路径数。最后一步来源分成互斥的两类：

```text
ways[row][col] = ways[row - 1][col] + ways[row][col - 1]
```

两类路径的最后一步方向不同，互不重复；所有合法路径又必属于其中一类，所以相加完整。

## 朴素方案：递归搜索

从 `(0,0)` 出发，每一步递归尝试向右和向下，到终点时计数。相同坐标会由大量不同前缀反复进入，递归树规模近似指数级。加入记忆化可变成 `O(mn)`，本质上就是自顶向下动态规划。

- 无记忆化时间复杂度：指数级。
- 递归栈空间：`O(m+n)`。

## 最优方案推导

二维表每一行只依赖上一行和本行左侧，因此使用长度为 `n` 的数组：

1. 初始全部填 `1`，代表第一行每格只有一种走法。
2. 从第二行开始，按列从左到右更新 `dp[col] += dp[col - 1]`。
3. 更新前 `dp[col]` 是上方值，更新后的 `dp[col - 1]` 是左方值。

若追求最小空间，可让数组长度为 `min(m,n)`；示例代码为保持坐标直观使用 `n`。

## 正确性与不变量

处理第 `row` 行第 `col` 列后，`dp[col]` 等于到达当前格子的路径数，而右侧尚未更新的元素仍保存上一行路径数。转移 `dp[col] = dp[col] + dp[col-1]` 正好相加上方与左方的全部路径。逐行完成后，`dp[n-1]` 即右下角路径数。

## 复杂度

- 时间复杂度：`O(mn)`。
- 空间复杂度：`O(n)`；调整行列后可写成 `O(min(m,n))`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int row = 1; row < m; row++) {
            for (int col = 1; col < n; col++) {
                dp[col] = dp[col] + dp[col - 1];
            }
        }
        return dp[n - 1];
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public int uniquePaths(int m, int n) {
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        for (int row = 1; row < m; row++) {
            for (int col = 1; col < n; col++) {
                dp[col] = dp[col] + dp[col - 1];
            }
        }
        return dp[n - 1];
    }
}

public class Main {
    public static void main(String[] args) {
        int m = 3;
        int n = 7;
        int answer = new Solution().uniquePaths(m, n);
        System.out.println("grid = " + m + " x " + n);
        System.out.println("unique paths = " + answer);
    }
}
```

## 数学方案补充

任何路径固定包含 `m-1` 次向下和 `n-1` 次向右，共 `m+n-2` 步。因此答案也等于组合数 `C(m+n-2,m-1)`。可在 `O(min(m,n))` 时间、`O(1)` 空间内逐项计算。实现时使用 `long` 保存中间结果，并注意乘除次序，避免中间溢出。

## 边界与易错点

- `m = 1` 或 `n = 1` 时只有一条路径。
- 一维 DP 必须从左向右更新；反向会使用上一行的左方值，破坏转移。
- 有障碍物时第一行和第一列不能统一初始化为 `1`。
- 若题目不保证答案范围，返回值和 DP 数组应改为 `long` 或大整数。

## 可扩展变式

- 63. 不同路径 II：加入障碍物，障碍格路径数清零。
- 最小路径和（64）：把“路径数相加”改为“上方与左方最小值加当前代价”。
- 允许对角线移动：转移中加入左上方状态。
- 组合数学版：适合无障碍、规则移动的超大网格。
