---
schemaVersion: 3
type: "problem"
leetcodeId: 139
slug: "word-break"
titleCn: "单词拆分"
titleEn: "Word Break"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/word-break/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "30e951a3ee9b4b15177cb35c83e3ce780089b96f436bc5c42c58b0265e5113ff"
sourceFactsSha256: "02ee6740f1f4f8d241d5b64f9ad7d36ec6d743e2df55fbcffc4fc286e29983f4"
sourceSectionHashes:
  description: "4dd6fdfb265b7d3358b7068262f624c706e2b0f68d6c0fad931361fd567c1840"
  examples: "89ba74270f2d2dd7d99aac154411381596711439976257128044de71f23c434a"
  constraints: "d36461be5ddcd24ee8bc3fb9ca3d49fe879418f8020e975eaff6395450733e89"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0d44aa1e371427e7512d2f1107030218c632f7546bb913f35cb96734bc5742cd"
  signature: "b878135dc1c8df8ae0bb215f43bf630dfd536136144d2f1ee750d4b2587f1a08"
  javaTemplate: "54c493c1c3131cbd93eb513a4afb7386ade7a290d66bd72149559d55e1aa19b8"
primaryPattern: "动态规划"
topics: ["动态规划","字典树","记忆化","数组","哈希表","字符串","Brute-Force Search"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Trie 字典树","Memoization 记忆化"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 139. 单词拆分 / Word Break

> **双轨入口：** [[核心模型/动态规划/139-Word-Break-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P1`
- 清单代表标签：`Trie 字典树`、`Memoization 记忆化`
- LeetCode 当前标签：字典树 (Trie)、记忆化 (Memoization)、数组 (Array)、哈希表 (Hash Table)、字符串 (String)、动态规划 (Dynamic Programming)、Brute-Force Search
- 官方来源：<https://leetcode.cn/problems/word-break/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`30e951a3ee9b4b15177cb35c83e3ce780089b96f436bc5c42c58b0265e5113ff`
- **主解法**：动态规划；等价解法为记忆化搜索

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个字符串 `s` 和一个字符串列表 `wordDict` 作为字典。如果可以利用字典中出现的一个或多个单词拼接出 `s` 则返回 `true`。

**注意：**不要求字典中出现的单词全部都使用，并且字典中的单词可以重复使用。

## 官方示例


**示例 1：**

```text
输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以由 "leet" 和 "code" 拼接成。
```

**示例 2：**

```text
输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以由 "apple" "pen" "apple" 拼接成。
     注意，你可以重复使用字典中的单词。
```

**示例 3：**

```text
输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false
```

## 官方约束


- `1 <= s.length <= 300`

- `1 <= wordDict.length <= 1000`

- `1 <= wordDict[i].length <= 20`

- `s` 和 `wordDict[i]` 仅由小写英文字母组成

- `wordDict` 中的所有字符串 **互不相同**

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 不要直接问“整个字符串是否在字典中”，而要问“某个前缀能否被拆分”。
2. 若前 `i` 个字符已经可拆分，只要 `s[i..j)` 是字典单词，前 `j` 个字符也可拆分。
3. 字典单词最长只有 20，可以限制枚举的切分长度。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

字符串的切分选择看似很多，但后续是否成功只与“当前处理到哪个下标”有关，而与此前如何切分无关。这说明问题具有重复子问题与最优子结构，可以用布尔动态规划压缩搜索状态。

定义 `dp[i]`：`s` 的前 `i` 个字符，即 `s[0..i)`，是否能由字典单词拼出。空前缀天然可拆分，所以 `dp[0] = true`。

## 朴素方案：枚举所有切分

从下标 0 出发，尝试每个可能的结束位置；若当前片段在字典中，递归处理剩余字符串。每个字符间隙都可能切或不切，最坏接近 `O(2^n)` 个切分组合；相同起点会被重复求解。加入 `memo[start]` 后会变成记忆化搜索，复杂度降为多项式。

## 最优方案推导

对每个前缀终点 `i`，枚举最后一个单词的起点 `j`：

```text
dp[i] = 存在某个 j，使 dp[j] == true 且 s[j..i) 在字典中
```

实际实现中，从已经可达的 `i` 向后扩展最多 `maxWordLength` 个字符，可以避免无意义的长片段。字典用 `HashSet`，平均 `O(1)` 判断单词是否存在。

## 正确性与不变量

处理下标 `i` 时，不变量是：`dp[0..i]` 已准确表示对应前缀是否可拆分。

- 若算法设置 `dp[end] = true`，则存在可拆分前缀 `s[0..i)`，且 `s[i..end)` 在字典中，两者拼接后 `s[0..end)` 必然可拆分。
- 若 `s[0..end)` 存在合法拆分，取其最后一个单词的起点 `i`，则 `dp[i]` 必为 `true`，算法枚举到该单词时一定会设置 `dp[end]`。

因此 `dp[n]` 当且仅当整个字符串可以拆分。

## 复杂度

- **时间复杂度**：设 `n = s.length()`，最长单词长度为 `L`，至多检查 `nL` 个片段；Java 生成子串还需复制字符，严格上界为 `O(nL^2)`。本题 `L <= 20`，通常写作 `O(nL)`。
- **空间复杂度**：`O(n + D)`，`dp` 占 `O(n)`，哈希集合存储字典字符总量 `D`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.HashSet;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> words = new HashSet<>(wordDict);
        int maxLength = 0;
        for (String word : wordDict) {
            maxLength = Math.max(maxLength, word.length());
        }

        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true;
        for (int start = 0; start < s.length(); start++) {
            if (!dp[start]) {
                continue;
            }
            int maxEnd = Math.min(s.length(), start + maxLength);
            for (int end = start + 1; end <= maxEnd; end++) {
                if (words.contains(s.substring(start, end))) {
                    dp[end] = true;
                }
            }
        }
        return dp[s.length()];
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.HashSet;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        Set<String> words = new HashSet<>(wordDict);
        int maxLength = 0;
        for (String word : wordDict) {
            maxLength = Math.max(maxLength, word.length());
        }

        boolean[] dp = new boolean[s.length() + 1];
        dp[0] = true;
        for (int start = 0; start < s.length(); start++) {
            if (!dp[start]) {
                continue;
            }
            int maxEnd = Math.min(s.length(), start + maxLength);
            for (int end = start + 1; end <= maxEnd; end++) {
                if (words.contains(s.substring(start, end))) {
                    dp[end] = true;
                }
            }
        }
        return dp[s.length()];
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.wordBreak(
                "leetcode", Arrays.asList("leet", "code"))); // true
        System.out.println(solution.wordBreak(
                "applepenapple", Arrays.asList("apple", "pen"))); // true
        System.out.println(solution.wordBreak(
                "catsandog", Arrays.asList("cats", "dog", "sand", "and", "cat"))); // false
    }
}
```

## 边界与易错点

- `dp` 长度必须是 `n + 1`，其中 `dp[0]` 代表空前缀。
- 题目允许重复使用同一个字典单词，不要在使用后删除它。
- `substring(start, end)` 的右边界不包含 `end`。
- 贪心选择最长或最短单词都不可靠，例如 `s = "cars"`、字典为 `["car", "ca", "rs"]`。

## 可扩展变式

- 输出一种合法拆分：记录 `previous[end] = start`，从 `n` 反向恢复。
- 统计拆分方案数：把布尔 `dp` 改为计数数组。
- 字典很大且需要避免创建子串：使用 Trie 从每个可达起点沿字符向后匹配。
- 要求最少单词数：令 `dp[i]` 表示拼出前缀的最少单词数。
