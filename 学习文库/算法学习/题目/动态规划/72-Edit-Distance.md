---
schemaVersion: 3
type: "problem"
leetcodeId: 72
slug: "edit-distance"
titleCn: "编辑距离"
titleEn: "Edit Distance"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/edit-distance/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "63317bbfbad0793fc267d5754924ebba57da320e2b4245340717a3c498ad0bbc"
sourceFactsSha256: "b75d25569208671c52ad174890774d9439da8c5b0ccef7813fcf2ff6d632cf0d"
sourceSectionHashes:
  description: "b9c2e32afb9cb79b4d35a35aec63577a14634df82b316378d6f94584752610e6"
  examples: "26516ea515c3f91e665b0c97eac0b153229494cbdcb12feecc565b9549dd52b1"
  constraints: "93aa5148c9c25b3c091f939aa3b25edbc589876c579f74ae8ece13caa7da5d0f"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0c3725f3a9eda160d1531ea68892a11b576f4018ad825e6ead3e3fd5c3b4acf3"
  signature: "d724fb20941b3588823880728ffe7807a851a9e1eeb26449d053364050da05f3"
  javaTemplate: "3487bd9f17f98b5493ea49860e019013c662a0fe7fae44f08b889f0e24900f9b"
primaryPattern: "动态规划"
topics: ["动态规划","字符串"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["String 字符串"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 72. 编辑距离 / Edit Distance

> **双轨入口：** [[核心模型/动态规划/72-Edit-Distance-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P1`
- 清单代表标签：`String 字符串`
- LeetCode 当前标签：字符串 (String)、动态规划 (Dynamic Programming)
- 官方来源：<https://leetcode.cn/problems/edit-distance/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`63317bbfbad0793fc267d5754924ebba57da320e2b4245340717a3c498ad0bbc`
- 主模型：二维前缀动态规划

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你两个单词 `word1` 和 `word2`， *请返回将 `word1` 转换成 `word2` 所使用的最少操作数*  。

你可以对一个单词进行如下三种操作：

- 插入一个字符

- 删除一个字符

- 替换一个字符

## 官方示例


**示例 1：**

```text
输入：word1 = "horse", word2 = "ros"
输出：3
解释：
horse -> rorse (将 'h' 替换为 'r')
rorse -> rose (删除 'r')
rose -> ros (删除 'e')
```

**示例 2：**

```text
输入：word1 = "intention", word2 = "execution"
输出：5
解释：
intention -> inention (删除 't')
inention -> enention (将 'i' 替换为 'e')
enention -> exention (将 'n' 替换为 'x')
exention -> exection (将 'n' 替换为 'c')
exection -> execution (插入 'u')
```

## 官方约束


- `0 <= word1.length, word2.length <= 500`

- `word1` 和 `word2` 由小写英文字母组成

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 不要直接描述“整个字符串怎么变”，改为研究两个前缀之间的最小编辑次数。
2. 若当前末尾字符相同，不需要为这两个字符增加操作。
3. 若不同，最后一步只能是插入、删除或替换，分别对应三个相邻状态。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `500 x 500` 的状态表可接受，目标时间为 `O(mn)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：word1 = "", word2 = "abc"
输出：3
解释：需要依次插入 a、b、c。
```

## 核心观察

定义 `dp[i][j]` 为把 `word1` 的前 `i` 个字符转换成 `word2` 的前 `j` 个字符的最少操作数。

若 `word1[i-1] == word2[j-1]`：

```text
dp[i][j] = dp[i - 1][j - 1]
```

若不同，考虑最后一次操作：

```text
删除 word1 末字符：dp[i - 1][j] + 1
插入 word2 末字符：dp[i][j - 1] + 1
替换两个末字符：  dp[i - 1][j - 1] + 1
```

取三者最小值。

## 朴素方案：递归枚举操作

从两个字符串末尾出发，字符不同时递归尝试三种操作。相同的 `(i,j)` 状态会被不同操作序列反复计算，最坏呈指数增长。记忆化搜索能消除重复，复杂度变为 `O(mn)`，但递归栈和边界处理相对隐蔽。

- 朴素时间复杂度：指数级。
- 记忆化时间复杂度：`O(mn)`。
- 记忆化空间复杂度：`O(mn)`，另有递归栈。

## 最优方案推导

建立 `(m+1) x (n+1)` 表，多出的第 `0` 行和第 `0` 列表示空前缀：

- `dp[i][0] = i`：把长度 `i` 的前缀全部删除。
- `dp[0][j] = j`：向空串插入 `j` 个字符。

之后从左上到右下填表，因为每个状态依赖上方、左方和左上方。

## 正确性与不变量

对于 `dp[i][j]`，若末字符相同，任何最优转换都可保留它们，只需解决较短前缀。若末字符不同，最优方案的最后一步必属于题目允许的插入、删除、替换之一；去掉这最后一步后恰好对应三个相邻子问题。取三者最小值覆盖全部可能且不会遗漏最优解。按行填表时，所有依赖状态均已正确，因此归纳得到 `dp[m][n]` 正确。

## 复杂度

- 时间复杂度：`O(mn)`。
- 空间复杂度：`O(mn)`；只求距离时可压缩到 `O(min(m,n))`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    int delete = dp[i - 1][j];
                    int insert = dp[i][j - 1];
                    int replace = dp[i - 1][j - 1];
                    dp[i][j] = 1 + Math.min(replace, Math.min(delete, insert));
                }
            }
        }
        return dp[m][n];
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public int minDistance(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    int delete = dp[i - 1][j];
                    int insert = dp[i][j - 1];
                    int replace = dp[i - 1][j - 1];
                    dp[i][j] = 1 + Math.min(replace, Math.min(delete, insert));
                }
            }
        }
        return dp[m][n];
    }
}

public class Main {
    public static void main(String[] args) {
        String word1 = "horse";
        String word2 = "ros";
        int answer = new Solution().minDistance(word1, word2);
        System.out.println("word1 = " + word1);
        System.out.println("word2 = " + word2);
        System.out.println("edit distance = " + answer);
    }
}
```

## 边界与易错点

- `dp` 下标是前缀长度，字符串字符下标要减 `1`。
- 空字符串的初始化是编辑距离定义的重要组成部分。
- “插入”对应 `dp[i][j-1]`：先变成目标较短前缀，再插入目标末字符。
- 只压缩为一维时必须额外保存更新前的左上角值。
- 本实现返回最少次数，不恢复具体操作序列；恢复序列需要从右下角回溯状态表。

## 可扩展变式

- 各操作代价不同：在三个转移分支上加各自权重。
- 只允许插入和删除：与最长公共子序列有直接关系。
- 恢复编辑脚本：记录转移来源或从完整 DP 表反向推导。
- Damerau-Levenshtein 距离：额外允许交换相邻字符。
