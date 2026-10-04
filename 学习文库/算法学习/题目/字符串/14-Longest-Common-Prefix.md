---
schemaVersion: 3
type: "problem"
leetcodeId: 14
slug: "longest-common-prefix"
titleCn: "最长公共前缀"
titleEn: "Longest Common Prefix"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/longest-common-prefix/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "ea1517bd84fbf7824a27c4bf2f1a48166bc89d084c0554ce86eb0de07b54a241"
sourceFactsSha256: "5784a90eda5f1a7fd946f5860a1813f52202dcfca84dd0e52115cb9b7bf8acfd"
sourceSectionHashes:
  description: "9a3f06e3615cef86c787d9ff471f8ee2e716babffde356aa632c317b117e5bc5"
  examples: "6ec5da332e5d1b1945a1fbdeb442297cffcf7b5d335d0836bad3286bc812d14e"
  constraints: "241d330b71224cf45664949f85bb8e2ab72063808a0a428302cb8f073b5848d0"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "12085fa63a089642051e8e89f13b46606b959e8fe66d1bea1b940dcfaf1b9d3f"
  signature: "62c3e5661c546f0f4b206e5d404d8d593b304158d27ea9175561948c53ccbcde"
  javaTemplate: "726695d5f5b4f2f72d486fa35ba7ad5e31e48f646bcf77762e51d2fae8f9f077"
primaryPattern: "字符串"
topics: ["字符串","字典树","数组"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Trie 字典树"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 14. 最长公共前缀 / Longest Common Prefix

> **双轨入口：** [[核心模型/字符串/14-Longest-Common-Prefix-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`字符串`
- 清单优先级：`P1`
- 清单代表标签：`Trie 字典树`
- LeetCode 当前标签：字典树 (Trie)、数组 (Array)、字符串 (String)
- 官方来源：<https://leetcode.cn/problems/longest-common-prefix/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`ea1517bd84fbf7824a27c4bf2f1a48166bc89d084c0554ce86eb0de07b54a241`
- 主模型：纵向字符扫描；Trie 是批量前缀查询的扩展模型

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

编写一个函数来查找字符串数组中的最长公共前缀。

如果不存在公共前缀，返回空字符串 `""`。

## 官方示例


**示例 1：**

```text
输入：strs = ["flower","flow","flight"]
输出："fl"
```

**示例 2：**

```text
输入：strs = ["dog","racecar","car"]
输出：""
解释：输入不存在公共前缀。
```

## 官方约束


- `1 <= strs.length <= 200`

- `0 <= strs[i].length <= 200`

- `strs[i]` 如果非空，则仅由小写英文字母组成

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 以第一个字符串为基准，按列比较同一位置的字符。
2. 某个字符串长度不足，或者某列字符不同，就可以立即结束。
3. 如果只有一次查询，构建 Trie 会增加不必要的对象开销；若有大量前缀操作，Trie 才更有价值。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：strs = ["a"]
输出："a"
```

## 核心观察

公共前缀在首次不一致的位置后不可能恢复。假设第 `column` 列是第一个不一致位置，那么答案必然恰好是基准字符串的 `[0,column)`。所以不需要排序或构建复杂结构，只需从左到右逐列验证。

## 朴素方案：逐个缩短候选前缀

令候选前缀初始为第一个字符串。对后续字符串，若它不以候选开头，就不断删掉候选末尾字符。这一做法正确，但反复创建子串或执行 `startsWith` 会重复比较字符。

- 时间复杂度：最坏可达 `O(S * L)` 的重复比较，具体取决于实现；`S` 为总字符数、`L` 为前缀长度。
- 空间复杂度：取决于子串创建，最坏 `O(L)`。

## 最优方案：纵向扫描

枚举第一个字符串的每个字符位置，再与其余所有字符串的同一位置比较。一旦越界或不同，返回此前区间。

### 正确性与不变量

开始检查第 `column` 列前，区间 `[0,column)` 已被证明是所有字符串的公共前缀。若任一字符串在该列不存在或字符不同，任何长度大于 `column` 的前缀都不可能公共，因此立即返回是正确的。若全部相同，不变量扩展到 `[0,column+1)`。完整扫描后，第一个字符串本身就是公共前缀，且不可能有更长答案。

- 时间复杂度：`O(S)`，`S` 为实际检查的字符总数，最坏为所有字符串长度总和。
- 空间复杂度：`O(1)`，不计返回字符串。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public String longestCommonPrefix(String[] strs) {
        String first = strs[0];

        for (int column = 0; column < first.length(); column++) {
            char expected = first.charAt(column);
            for (int row = 1; row < strs.length; row++) {
                if (column >= strs[row].length()
                        || strs[row].charAt(column) != expected) {
                    return first.substring(0, column);
                }
            }
        }
        return first;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public String longestCommonPrefix(String[] strs) {
        String first = strs[0];

        for (int column = 0; column < first.length(); column++) {
            char expected = first.charAt(column);
            for (int row = 1; row < strs.length; row++) {
                if (column >= strs[row].length()
                        || strs[row].charAt(column) != expected) {
                    return first.substring(0, column);
                }
            }
        }
        return first;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.longestCommonPrefix(
                new String[]{"flower", "flow", "flight"})); // fl
        System.out.println(solution.longestCommonPrefix(
                new String[]{"dog", "racecar", "car"}));    // 空串
        System.out.println(solution.longestCommonPrefix(
                new String[]{"interspecies", "interstellar", "interstate"}));
    }
}
```

## 边界与易错点

- 任一字符串为空，公共前缀立即为空；纵向扫描会自然处理。
- 题目保证数组至少一个元素，若工程输入可能为空，需要先约定返回值。
- 公共“前缀”必须从索引 0 开始，不是最长公共子串。
- Java `substring(0,0)` 合法并返回空字符串。

## 可扩展变式

- 大量字符串插入、前缀计数和自动补全可使用 Trie。
- 对非常多且很长的字符串，可用分治：分别求两半公共前缀再合并。
- 最长公共子串和最长公共子序列通常使用动态规划，不能直接使用本题方法。
