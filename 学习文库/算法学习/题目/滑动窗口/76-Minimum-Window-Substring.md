---
schemaVersion: 3
type: "problem"
leetcodeId: 76
slug: "minimum-window-substring"
titleCn: "最小覆盖子串"
titleEn: "Minimum Window Substring"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/minimum-window-substring/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "cc6bb2b9ecea550af7adf67ff70e55730702331171353f0bb0e49b2da973e8de"
sourceFactsSha256: "d6923b53db5be884732c19a7c0c7621a8bad8cd6c59ba7186a29362b7ad51927"
sourceSectionHashes:
  description: "8f7e7e51ec16d32e6f6aabcd0e722b4a1b1a92462ffc0dadf866248a6906a88e"
  examples: "b2d005d90bd3214e6f3120315deb2ede96a3208a0fe52ccecba656e4c4d44ec3"
  constraints: "8a348daaa5711446a49d8da4e464dc6539c0ff8211e064e29f8403cbd830da1c"
  hints: "f21dfc052b6c64e50922a8e88134614c8edc4faacf7753025dbea73423989133"
  tags: "946cd5f352db51a9aaf1f2294bee7f74a175039977f4f6cef0e37fbffacfd20f"
  signature: "3ea47544f30c43b2f9482755a19ff040d997098cee0fdf5fc69b12d731662cd1"
  javaTemplate: "d98c1fa5c990db2d06c9e2ae6f6b7f0cdf4349dfba1437f25bd251d12b89e0ca"
primaryPattern: "滑动窗口"
topics: ["滑动窗口","哈希表","字符串"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Sliding Window 滑动窗口"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 76. 最小覆盖子串 / Minimum Window Substring

> **双轨入口：** [[核心模型/滑动窗口/76-Minimum-Window-Substring-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`滑动窗口`
- 清单优先级：`P0`
- 清单代表标签：`Sliding Window 滑动窗口`
- LeetCode 当前标签：哈希表 (Hash Table)、字符串 (String)、滑动窗口 (Sliding Window)
- 官方来源：<https://leetcode.cn/problems/minimum-window-substring/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`cc6bb2b9ecea550af7adf67ff70e55730702331171353f0bb0e49b2da973e8de`
- 主模型：可变长度滑动窗口与字符欠账

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定两个字符串 `s` 和 `t`，长度分别是 `m` 和 `n`，返回 s 中的 **最短窗口 子串**，使得该子串包含 `t` 中的每一个字符（**包括重复字符**）。如果没有这样的子串，返回空字符串* *`""`。

测试用例保证答案唯一。

## 官方示例


**示例 1：**

```text
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
```

**示例 2：**

```text
输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。
```

**示例 3:**

```text
输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。
```

## 官方约束


- `m == s.length`

- `n == t.length`

- `1 <= m, n <= 10^5`

- `s` 和 `t` 由英文字母组成

**进阶：**你能设计一个在 `O(m + n)` 时间内解决此问题的算法吗？

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Use two pointers to create a window of letters in s, which would have all the characters from t.
2. Expand the right pointer until all the characters of t are covered.
3. Once all the characters are covered, move the left pointer and ensure that all the characters are still covered to minimize the subarray size.
4. Continue expanding the right and left pointers until you reach the end of s.

## 学习提示（非官方）

1. 右指针负责把字符纳入窗口，直到窗口合法。
2. 窗口合法后，左指针负责删除冗余字符，直到再删一步就不合法。
3. 可维护“还缺多少个字符实例”，而不是每次扫描整个计数表判断是否合法。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `n` 达到 `10^5`，枚举所有子串会超时。
- 目标应为线性扫描，允许用字符计数表占常数或字符集大小的空间。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

用 `need[c]` 表示当前窗口还欠字符 `c` 几个。初始根据 `t` 计数，并令 `missing = t.length()`。

右端加入字符 `c` 时：

- 若 `need[c] > 0`，这个字符偿还了一笔欠账，`missing--`。
- 无论是否欠缺，都执行 `need[c]--`；负数表示窗口中有冗余。

当 `missing == 0` 时窗口合法。左端移出字符 `c` 前执行 `need[c]++`；若结果大于 `0`，说明移走的是必需字符，窗口重新非法，`missing++`。

## 朴素方案：枚举所有子串

枚举左、右边界，并为每个子串统计是否覆盖 `t`。直接做法可能达到 `O(n^3)`；增量维护每个左边界的计数仍需 `O(n^2)` 个窗口。`n = 100000` 时不可行。

问题的重复在于相邻窗口共享绝大多数字符，滑动窗口只处理进入和离开的两个字符。

## 最优方案推导

1. 右指针逐字符扩张，并更新欠账。
2. 一旦 `missing == 0`，当前窗口覆盖了 `t`，记录其长度。
3. 在合法期间不断右移左指针，寻找同一右端点下最短的合法窗口。
4. 移出必需字符后窗口非法，回到扩张阶段。

左右指针都只向右移动，每个字符最多进入和离开窗口一次。

## 正确性与不变量

任意时刻 `need[c]` 等于 `t` 对字符 `c` 的需求量减去当前窗口中的数量，`missing` 等于所有正欠账之和。故 `missing == 0` 当且仅当窗口覆盖 `t`。固定右端点时，内层循环不断收缩左端，检查了以该右端点结尾的所有可能最优合法窗口；第一次变非法后，更右的左端也不可能合法。遍历所有右端点并取最短，得到全局最小覆盖。

## 复杂度

- 时间复杂度：`O(|s| + |t|)`，两个指针各最多走过 `s` 一次。
- 空间复杂度：`O(1)`，题目限定英文字母，使用固定大小数组；推广到任意字符集时为 `O(字符种类数)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public String minWindow(String s, String t) {
        if (t.length() > s.length()) {
            return "";
        }

        int[] need = new int[128];
        for (int i = 0; i < t.length(); i++) {
            need[t.charAt(i)]++;
        }

        int missing = t.length();
        int left = 0;
        int bestStart = 0;
        int bestLength = Integer.MAX_VALUE;

        for (int right = 0; right < s.length(); right++) {
            char entering = s.charAt(right);
            if (need[entering] > 0) {
                missing--;
            }
            need[entering]--;

            while (missing == 0) {
                int windowLength = right - left + 1;
                if (windowLength < bestLength) {
                    bestLength = windowLength;
                    bestStart = left;
                }

                char leaving = s.charAt(left);
                need[leaving]++;
                if (need[leaving] > 0) {
                    missing++;
                }
                left++;
            }
        }

        return bestLength == Integer.MAX_VALUE
                ? ""
                : s.substring(bestStart, bestStart + bestLength);
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public String minWindow(String s, String t) {
        if (t.length() > s.length()) {
            return "";
        }

        int[] need = new int[128];
        for (int i = 0; i < t.length(); i++) {
            need[t.charAt(i)]++;
        }

        int missing = t.length();
        int left = 0;
        int bestStart = 0;
        int bestLength = Integer.MAX_VALUE;

        for (int right = 0; right < s.length(); right++) {
            char entering = s.charAt(right);
            if (need[entering] > 0) {
                missing--;
            }
            need[entering]--;

            while (missing == 0) {
                int windowLength = right - left + 1;
                if (windowLength < bestLength) {
                    bestLength = windowLength;
                    bestStart = left;
                }

                char leaving = s.charAt(left);
                need[leaving]++;
                if (need[leaving] > 0) {
                    missing++;
                }
                left++;
            }
        }

        return bestLength == Integer.MAX_VALUE
                ? ""
                : s.substring(bestStart, bestStart + bestLength);
    }
}

public class Main {
    public static void main(String[] args) {
        String s = "ADOBECODEBANC";
        String t = "ABC";
        String answer = new Solution().minWindow(s, t);
        System.out.println("minimum window = " + answer);
    }
}
```

## 边界与易错点

- 重复字符必须按数量覆盖，不能只用 `Set`。
- `need[c] < 0` 表示冗余，不代表错误。
- 更新最优答案必须发生在移出左端字符之前。
- Java 的 `substring` 右边界不包含，因此使用 `bestStart + bestLength`。
- 固定数组大小 `128` 依赖题目只含英文字母；任意 Unicode 文本应改用 `Map<Character,Integer>` 或按码点处理。

## 可扩展变式

- 3. 无重复字符的最长子串：合法条件变为窗口内无重复。
- 438. 找到字符串中所有字母异位词：使用固定长度窗口。
- 567. 字符串的排列：判断是否存在一个完全匹配频次的窗口。
- 最短覆盖序列：若要求保持 `t` 中字符顺序，需要动态规划或双向扫描。
