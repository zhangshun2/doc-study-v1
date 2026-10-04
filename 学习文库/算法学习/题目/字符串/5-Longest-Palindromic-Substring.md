---
schemaVersion: 3
type: "problem"
leetcodeId: 5
slug: "longest-palindromic-substring"
titleCn: "最长回文子串"
titleEn: "Longest Palindromic Substring"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-palindromic-substring/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "dcffc09a04bc07adff364b533f1634862f4da7802ed1a826765e010171a29a0e"
sourceFactsSha256: "ed0fb1c22be6f57fa565940a9aa6deb3c5228e7bc635249aab898ec9654a6898"
sourceSectionHashes:
  description: "ec12a70be42a9af83e0d48822b1fcc61b6676bec94eb53e01263fb035f888329"
  examples: "4f20b95964dbc1b645341fbd7baa77af536b0fddc59caf78d9cf980f15b39b14"
  constraints: "363ada21cd7cd764720ea4489ddb447a84f6571e694b80e07eac7cf873397688"
  hints: "7e9dd858c5e0debcb8abaea667a42993c41246edaeedf493fd42262623ef93cc"
  tags: "2ef9ada1b340b43d9bea9eb74837c58ec3b2b08e7ef09346cb47aae9aa0f5635"
  signature: "226822d213adc04ae3c03878ec3ce5c96e4a84fd29c6c82a2f761be9e7d7dd97"
  javaTemplate: "47f186eaaee71a667d78cb1a148c1ced0f54d58e90c95cd4cd8bf71f71c1e64b"
primaryPattern: "字符串"
topics: ["字符串","双指针","动态规划","Manacher 算法"]
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
# 5. 最长回文子串 / Longest Palindromic Substring

> **双轨入口：** [[核心模型/字符串/5-Longest-Palindromic-Substring-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`字符串`
- 清单优先级：`P1`
- 清单代表标签：`String 字符串`
- LeetCode 当前标签：双指针 (Two Pointers)、字符串 (String)、动态规划 (Dynamic Programming)、Manacher 算法
- 官方来源：<https://leetcode.cn/problems/longest-palindromic-substring/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`dcffc09a04bc07adff364b533f1634862f4da7802ed1a826765e010171a29a0e`
- 主模型：枚举回文中心 + 双向扩展

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个字符串 `s`，找到 `s` 中最长的 回文 子串。

## 官方示例


**示例 1：**

```text
输入：s = "babad"
输出："bab"
解释："aba" 同样是符合题意的答案。
```

**示例 2：**

```text
输入：s = "cbbd"
输出："bb"
```

## 官方约束


- `1 <= s.length <= 1000`

- `s` 仅由数字和英文字母组成

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. How can we reuse a previously computed palindrome to compute a larger palindrome?
2. If “aba” is a palindrome, is “xabax” a palindrome? Similarly is “xabay” a palindrome?
3. Complexity based hint:
If we use brute-force and check whether for every start and end position a substring is a palindrome we have O(n^2) start - end pairs and O(n) palindromic checks. Can we reduce the time for palindromic checks to O(1) by reusing some previous computation.

## 学习提示（非官方）

1. 每个回文串都围绕一个中心对称。
2. 奇数长度回文的中心是一个字符，偶数长度回文的中心是两个字符之间的缝隙。
3. 从中心向两侧扩展，直到越界或字符不同。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `O(n^2)` 解法在该范围内可接受；应避免枚举子串后再逐个验证导致的 `O(n^3)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：s = "a"
输出："a"
```

## 核心观察

长度为 `L` 的字符串有 `n` 个单字符中心和 `n-1` 个双字符中心，总计 `2n-1` 个。枚举所有中心，就不会漏掉任何回文子串。对中心 `(left,right)`，只要 `s[left] == s[right]` 就继续扩张。

## 朴素方案：枚举所有子串

枚举起点和终点，再用双指针判断该子串是否回文。子串数量为 `O(n^2)`，每次验证最多 `O(n)`。

- 时间复杂度：`O(n^3)`。
- 空间复杂度：`O(1)`（不计返回字符串）。

动态规划可用 `dp[left][right]` 表示区间是否回文，时间和空间都是 `O(n^2)`。

## 推荐最优方案：中心扩展

对每个位置 `center` 做两次扩展：

- `expand(center, center)`：寻找奇数长度回文。
- `expand(center, center+1)`：寻找偶数长度回文。

扩展函数返回最大合法长度，据此计算当前回文的起止下标。

### 正确性与不变量

任意回文串都有唯一的几何中心：奇数回文落在字符上，偶数回文落在字符间。算法枚举了这两类全部中心。扩展过程中，区间 `[left+1,right-1]` 始终是以该中心为轴的回文；相邻两字符相等时扩大后仍是回文。停止时已得到该中心的最长回文。因此所有中心中的最大者就是全局最长回文。

- 时间复杂度：最坏 `O(n^2)`，如字符串全为同一字符。
- 空间复杂度：`O(1)`，不计返回结果。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public String longestPalindrome(String s) {
        int bestStart = 0;
        int bestLength = 1;

        for (int center = 0; center < s.length(); center++) {
            int oddLength = expand(s, center, center);
            int evenLength = expand(s, center, center + 1);
            int currentLength = Math.max(oddLength, evenLength);

            if (currentLength > bestLength) {
                bestLength = currentLength;
                bestStart = center - (currentLength - 1) / 2;
            }
        }
        return s.substring(bestStart, bestStart + bestLength);
    }

    private int expand(String s, int left, int right) {
        while (left >= 0 && right < s.length()
                && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public String longestPalindrome(String s) {
        int bestStart = 0;
        int bestLength = 1;

        for (int center = 0; center < s.length(); center++) {
            int oddLength = expand(s, center, center);
            int evenLength = expand(s, center, center + 1);
            int currentLength = Math.max(oddLength, evenLength);

            if (currentLength > bestLength) {
                bestLength = currentLength;
                bestStart = center - (currentLength - 1) / 2;
            }
        }
        return s.substring(bestStart, bestStart + bestLength);
    }

    private int expand(String s, int left, int right) {
        while (left >= 0 && right < s.length()
                && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.longestPalindrome("babad"));
        System.out.println(solution.longestPalindrome("cbbd"));
        System.out.println(solution.longestPalindrome("a"));
        System.out.println(solution.longestPalindrome("aaaa"));
    }
}
```

## 边界与易错点

- 不能只枚举单字符中心，否则会漏掉 `"bb"` 这类偶数回文。
- 循环停止时 `left`、`right` 已各多走一步，长度是 `right-left-1`。
- 更新起点公式为 `center - (length-1)/2`，同时适用于奇偶长度。
- 多个最长答案并存时返回任意一个即可；代码因使用 `>` 而保留较早发现者。

## 可扩展变式

- 统计所有回文子串：每次成功扩展都把计数加一。
- 最长回文子序列不要求连续，通常使用区间动态规划。
- 若需要线性时间，可学习 Manacher 算法，但实现和维护成本明显更高。
