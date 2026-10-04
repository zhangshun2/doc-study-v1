---
schemaVersion: 3
type: "problem"
leetcodeId: 3
slug: "longest-substring-without-repeating-characters"
titleCn: "无重复字符的最长子串"
titleEn: "Longest Substring Without Repeating Characters"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-substring-without-repeating-characters/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "495318e9d5d0eb72c4a69d583c0cb410ab6552b072ce2989dbb305a132a53736"
sourceFactsSha256: "d60376fe12d69873855959ae0cead8bc8409683c2f73d85d07dca295da635ee6"
sourceSectionHashes:
  description: "3b80c1577aebf3d4d7fbe4af57b2a3d74788ec2d21008c459fbd024249aa704f"
  examples: "8fa5053631b7caa48bb0203f8278a8d5a48a002362ec0e2e85e2a7a71940a989"
  constraints: "7b6c5b8790b39909cc29fd58be397800868f768ab79aaf8164a23507d7a77c5d"
  hints: "c8d8c6f932d674a5ecf9f34c53465ccd3b96626e7867132831c7c6bc83c5544e"
  tags: "946cd5f352db51a9aaf1f2294bee7f74a175039977f4f6cef0e37fbffacfd20f"
  signature: "7da0988eaaf2e07df64cb9e8594dd13375360e7afd2df586cb804d08df7f099f"
  javaTemplate: "215e51d6dc8108275689a367d26bd7c3bde0c77df5c1394fd15dc5a238ea78e8"
primaryPattern: "滑动窗口"
topics: ["滑动窗口","哈希表","字符串"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Sliding Window 滑动窗口","String 字符串"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 3. 无重复字符的最长子串 / Longest Substring Without Repeating Characters

> **双轨入口：** [[核心模型/滑动窗口/3-Longest-Substring-Without-Repeating-Characters-核心模型.md|核心模型]] · [[建模专题/T0/3-Longest-Substring-Without-Repeating-Characters-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`滑动窗口`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Sliding Window 滑动窗口`、`String 字符串`
- LeetCode 当前标签：哈希表 (Hash Table)、字符串 (String)、滑动窗口 (Sliding Window)
- 官方来源：<https://leetcode.cn/problems/longest-substring-without-repeating-characters/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`495318e9d5d0eb72c4a69d583c0cb410ab6552b072ce2989dbb305a132a53736`
- 主模型：可变长度滑动窗口
- 直观建模专题：[从重复检查到维护合法连续区间](../../建模专题/T0/3-Longest-Substring-Without-Repeating-Characters-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长 子串**** **的长度。

## 官方示例


**示例 1:**

```text
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。注意 "bca" 和 "cab" 也是正确答案。
```

**示例 2:**

```text
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
```

**示例 3:**

```text
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
```

## 官方约束


- `0 <= s.length <= 10^5`

- `s` 由英文字母、数字、符号和空格组成

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. There are less than 100 unique characters. We can check all substrings with length at most 100 for example. This is a good enough approximation.

## 学习提示（非官方）

1. 维护一个始终没有重复字符的窗口 `[left, right]`。
2. 新字符若在窗口内出现过，左边界可以直接跳到其上次位置的后一位。
3. 左边界只能右移，不能被更早的重复位置拉回去。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 长度上限要求避免为每个起点重新扫描右侧的 `O(n^2)` 做法。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

当右端加入 `s[right]` 后，窗口可能只有一种冲突：这个新字符与窗口中相同字符重复。知道它最近一次出现的位置 `previous` 后，把 `left` 更新为 `max(left, previous + 1)`，窗口就重新合法。

记录最近位置比使用集合逐个删除更直接，不过两种实现都是线性复杂度。

## 朴素方案：枚举每个起点

对每个起点向右扩展，并用集合检测重复，遇到重复后停止。最坏情况如全部字符互不相同时，每个起点都扫描很远。

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(min(n, 字符集大小))`。

## 最优方案：最近位置滑动窗口

哈希表 `lastIndex` 保存字符最后出现的下标。每次处理右端字符：

1. 若它上次出现的位置不小于 `left`，令 `left = previous + 1`。
2. 更新该字符的最后位置为 `right`。
3. 用 `right - left + 1` 更新最大长度。

### 正确性与不变量

每轮结束时，窗口 `[left,right]` 中无重复字符，并且 `left` 是能使以 `right` 结尾的窗口合法的最小左边界。若当前字符在窗口内重复，任何 `left <= previous` 的窗口都非法，因此跳到 `previous+1` 是必要且最小的移动；若重复位置在窗口外，则无需移动。于是每个右端点对应的最长合法窗口都被考虑，最大值即全局答案。

- 时间复杂度：`O(n)`，每个字符作为右端点处理一次。
- 空间复杂度：`O(min(n, 字符集大小))`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> lastIndex = new HashMap<>();
        int left = 0;
        int best = 0;

        for (int right = 0; right < s.length(); right++) {
            char current = s.charAt(right);
            Integer previous = lastIndex.get(current);
            if (previous != null && previous >= left) {
                left = previous + 1;
            }
            lastIndex.put(current, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> lastIndex = new HashMap<>();
        int left = 0;
        int best = 0;

        for (int right = 0; right < s.length(); right++) {
            char current = s.charAt(right);
            Integer previous = lastIndex.get(current);
            if (previous != null && previous >= left) {
                left = previous + 1;
            }
            lastIndex.put(current, right);
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.lengthOfLongestSubstring("abcabcbb")); // 3
        System.out.println(solution.lengthOfLongestSubstring("bbbbb"));    // 1
        System.out.println(solution.lengthOfLongestSubstring("pwwkew"));  // 3
        System.out.println(solution.lengthOfLongestSubstring(""));        // 0
    }
}
```

## 边界与易错点

- `left` 必须取 `max(left, previous + 1)` 的语义，代码通过 `previous >= left` 实现。对于 `abba`，若无此判断，最后一个 `a` 会把左边界错误拉回。
- 题目要的是连续子串，不是可跳过字符的子序列。
- Java 的 `char` 是 UTF-16 代码单元；题目给定的常见字符可以直接处理。若扩展到完整 Unicode 码点，应使用 `codePoints()`。
- 空串答案是 `0`，无需特殊分支。

## 可扩展变式

- “至多包含 K 种字符”可维护字符频次并在种类过多时收缩窗口。
- “至少重复 K 次”通常不能直接套同一窗口，需要按字符种类数量分层枚举。
- 若还要返回子串，记录刷新 `best` 时的起点即可。
