---
schemaVersion: 3
type: "problem"
leetcodeId: 49
slug: "group-anagrams"
titleCn: "字母异位词分组"
titleEn: "Group Anagrams"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/group-anagrams/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "32eb1a3b8905d39dd5b14ee96c18216202374a7bf98c9e78a1daf298ebe48652"
sourceFactsSha256: "ce2f2b184b8d18071def77c679e5296c4c0254fe73be0603457d23d1e7842a75"
sourceSectionHashes:
  description: "bc77cf25ad6d5a32205d9650bfe295418a6df1dea3520ca4d3b31498307b11ee"
  examples: "f87908dfe4331255b289a6f93ddff37eb08659aeb46c6ed7574906daf47cc5f5"
  constraints: "dd0fb29e6ab70fcbd9b7f711f6015f5aea362038e7fe9280c84c3a31ebab5e83"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "3605fd3553e0594af6ef76ef1c5288153441303045f62168125b5e750d0b90bd"
  signature: "2eb51680a1a4baafdac789c90957da3e254453b59b478d95c3ced94482ecdc37"
  javaTemplate: "03270e64abbd87b118cc1cdd34ecd76d036a6fb49d78261a8730e13e652f03e9"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","数组","哈希表","字符串","排序"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Hash Table 哈希表"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 49. 字母异位词分组 / Group Anagrams

> **双轨入口：** [[核心模型/数组与哈希/49-Group-Anagrams-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`数组与哈希`
- 清单优先级：`P0`
- 清单代表标签：`Hash Table 哈希表`
- LeetCode 当前标签：数组 (Array)、哈希表 (Hash Table)、字符串 (String)、排序 (Sorting)
- 官方来源：<https://leetcode.cn/problems/group-anagrams/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`32eb1a3b8905d39dd5b14ee96c18216202374a7bf98c9e78a1daf298ebe48652`
- 主模型：字符频次签名 + 哈希分组

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

## 官方示例


**示例 1:**

**输入:** strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

**输出:**[["bat"],["nat","tan"],["ate","eat","tea"]]

**解释：**

- 在 strs 中没有字符串可以通过重新排列来形成 `"bat"`。

- 字符串 `"nat"` 和 `"tan"` 是字母异位词，因为它们可以重新排列以形成彼此。

- 字符串 `"ate"` ，`"eat"` 和 `"tea"` 是字母异位词，因为它们可以重新排列以形成彼此。

**示例 2:**

**输入:** strs = [""]

**输出:**[[""]]

**示例 3:**

**输入:** strs = ["a"]

**输出:**[["a"]]

## 官方约束


- `1 <= strs.length <= 10^4`

- `0 <= strs[i].length <= 100`

- `strs[i]` 仅包含小写字母

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 异位词排序后会得到相同字符串，例如 `eat`、`tea` 都变成 `aet`。
2. 因为字符集固定为 26 个小写字母，也可用每个字母的出现次数作为签名，省去排序。
3. 频次数值之间必须有分隔符，否则不同计数可能拼成相同文本。
4. 使用 `computeIfAbsent` 可以自然地创建并追加分组。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

分组问题的核心不是两两比较，而是设计“规范化键”：同组对象的键相同，不同组对象的键不同。对于本题，26 维字符频次向量正好完整描述一个单词的字母多重集合。

例如 `abb` 的签名开头是 `#1#2#0...`，`bab` 也得到完全相同的签名。

## 朴素方案：逐组比较

维护已有分组，每来一个字符串，就与各组代表逐一判断是否为异位词。每次判断还要计数或排序，组数多时会趋近二次复杂度。

- 时间复杂度：最坏约 `O(m^2 * L)`，`m` 为字符串数、`L` 为平均长度。
- 空间复杂度：`O(mL)` 保存结果。

常见合格方案是把每个字符串排序后作为键，时间为 `O(sum(L_i log L_i))`。

## 最优方案：计数签名哈希

对每个字符串创建长度 26 的计数数组，扫描字符后按固定字母顺序序列化为带分隔符的键。哈希表从键映射到该组字符串列表。

### 正确性与不变量

两个小写字符串是字母异位词，当且仅当它们对每个字母的出现次数都相等。签名按固定次序无损编码这 26 个计数，因此异位词必然得到相同键，非异位词至少一个计数不同而得到不同键。每个字符串按其唯一签名加入对应列表，所以最终分组既完整又互斥。

- 时间复杂度：`O(T + 26m)`，`T` 为所有字符串字符总数；固定字符集下通常记为 `O(T)`。
- 空间复杂度：`O(T + 26m)`，包括结果引用和哈希键；不计输出时哈希结构仍与输入规模同阶。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groupsBySignature = new HashMap<>();

        for (String word : strs) {
            int[] counts = new int[26];
            for (int i = 0; i < word.length(); i++) {
                counts[word.charAt(i) - 'a']++;
            }

            StringBuilder signature = new StringBuilder();
            for (int count : counts) {
                signature.append('#').append(count);
            }

            groupsBySignature
                    .computeIfAbsent(signature.toString(), key -> new ArrayList<>())
                    .add(word);
        }

        return new ArrayList<>(groupsBySignature.values());
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groupsBySignature = new HashMap<>();

        for (String word : strs) {
            int[] counts = new int[26];
            for (int i = 0; i < word.length(); i++) {
                counts[word.charAt(i) - 'a']++;
            }

            StringBuilder signature = new StringBuilder();
            for (int count : counts) {
                signature.append('#').append(count);
            }

            groupsBySignature
                    .computeIfAbsent(signature.toString(), key -> new ArrayList<>())
                    .add(word);
        }

        return new ArrayList<>(groupsBySignature.values());
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.groupAnagrams(
                new String[]{"eat", "tea", "tan", "ate", "nat", "bat"}));
        System.out.println(solution.groupAnagrams(new String[]{""}));
        System.out.println(solution.groupAnagrams(new String[]{"a"}));
    }
}
```

## 边界与易错点

- 空字符串的 26 个计数全为 0，所有空字符串应属于同一组。
- 不能把计数直接无分隔拼接，例如计数 `1,11` 与 `11,1` 可能产生含糊键；`#` 消除了边界歧义。
- 返回顺序没有要求，不能依赖 `HashMap` 的迭代顺序编写测试。
- 计数数组方案依赖“小写英文字母”约束；若字符集任意，应排序字符或使用字符到频次的映射。

## 可扩展变式

- 判断两个字符串是否互为异位词，只需比较频次数组，无需建立分组哈希表。
- 支持 Unicode 时，可按 Unicode 码点排序，或用 `Map<Integer,Integer>` 构造规范签名。
- 数据量极大时可按签名做外部分桶，再对每个桶独立处理。
- 若只需要每组数量，可把映射值从列表改为计数器。
