---
schemaVersion: 3
type: "problem"
leetcodeId: 32
slug: "longest-valid-parentheses"
titleCn: "最长有效括号"
titleEn: "Longest Valid Parentheses"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/longest-valid-parentheses/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "7a4ad0fb4128f43f0a2847aad4c47a96346b3f12dcc0e7bdef6efed5d8dda3a2"
sourceFactsSha256: "eac3e76563b2fcb07a1d8de3ba76cad6a9f7595df8f681f939bef76ca16903fd"
sourceSectionHashes:
  description: "20839bc21a07a22334ffc6ccec8e80bcd71992eb4c0d68ab75df76f1664c2517"
  examples: "74a04c238eefdf29ae336b9a7242700195c51b294d7483bb65bb61c62c3a6f20"
  constraints: "e43d11fe27b11663997c3f2e13182c661256adca807f4a6d58cfd1461415aa57"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "084fc4ccd34a331ffd0c719aca27e058929ff5c1b5865778ec59d2d17b7b6daf"
  signature: "61ef827a9ae24fd7e4d53321b750eb57bb0578bdc9521cccb88d31b182b8cc22"
  javaTemplate: "7d76c1e7dd456e89c0de5e9fdaf2b6e9182136bcef3af3e13e1775f0db7e139e"
primaryPattern: "栈"
topics: ["栈","字符串","动态规划","括号序列"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Stack 栈","Dynamic Programming 动态规划"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 32. 最长有效括号 / Longest Valid Parentheses

> **双轨入口：** [[核心模型/栈/32-Longest-Valid-Parentheses-核心模型.md|核心模型]] · [[建模专题/T0/32-Longest-Valid-Parentheses-直观建模.md|完整建模]]

## 题目信息

- 官方难度：`Hard`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`、`Dynamic Programming 动态规划`
- LeetCode 当前标签：栈 (Stack)、字符串 (String)、动态规划 (Dynamic Programming)、括号序列
- 官方来源：<https://leetcode.cn/problems/longest-valid-parentheses/>
- 直观建模专题：[完整推导](../../建模专题/T0/32-Longest-Valid-Parentheses-直观建模.md)
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`7a4ad0fb4128f43f0a2847aad4c47a96346b3f12dcc0e7bdef6efed5d8dda3a2`
- **主解法**：未匹配位置栈

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个只包含 `'('` 和 `')'` 的字符串，找出最长有效（格式正确且连续）括号 子串 的长度。

左右括号匹配，即每个左括号都有对应的右括号将其闭合的字符串是格式正确的，比如 `"(()())"`。

## 官方示例

**示例 1：**

```text
输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"
```

**示例 2：**

```text
输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
```

**示例 3：**

```text
输入：s = ""
输出：0
```

## 官方约束

- `0 <= s.length <= 3 * 10^4`

- `s[i]` 为 `'('` 或 `')'`

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 直接枚举所有子串会重复检查大量前缀；栈只需要保存尚未配对的括号位置。
2. 初始压入 -1，把“当前有效段从下标 0 开始”也统一成一个可计算的基准。
3. 每遇到一个无法配对的右括号，它右侧才可能开始新的有效段。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：O(n)，每个字符只处理一次，每个下标最多入栈和出栈一次。
- 空间复杂度目标：O(n)，最坏情况字符串全部是左括号。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

有效括号段只会在两种边界之间出现：最近一个未匹配括号之后，以及当前扫描位置之前。若把每个未匹配右括号的下标也留在栈里，栈顶就是当前有效段左侧的第一条边界。

## 朴素方案

可以枚举每个起点和终点，再用一次扫描判断子串是否有效；共有 O(n^2) 个区间，每个区间最坏检查 O(n)，因此为 O(n^3)。也可以定义 dp[i] 为以 i 结尾的最长有效长度，时间 O(n)，但需要分别处理 ...() 与 ...)) 两种转移。

## 最优方案：索引栈：把未匹配位置变成区间边界

栈不保存括号字符，只保存尚未结算的下标。初始放入 -1。遇到左括号时压入其下标；遇到右括号时先弹出栈顶，表示尝试完成最近匹配。若弹出后栈为空，说明这个右括号没有可配对的左括号，于是把它的下标压入，作为后续有效段的新基准。若栈不为空，则当前下标减去新的栈顶，就是以当前字符结尾的最长有效段长度。

### 正确性与不变量

处理任意前缀后，栈中保存的是尚未匹配的左括号下标；当存在未匹配右括号时，栈底还会保留最近一个无法匹配的右括号下标。因此栈顶始终是当前有效段左边界之前的位置。成功匹配一个右括号时，区间长度恰好覆盖从该边界之后的全部成对内容；没有可匹配左括号时，新基准左侧内容不可能再与未来字符组成有效段。取遍所有结束位置的最大值即全局最长长度。

## 复杂度

- **时间复杂度**：O(n)，每个字符只处理一次，每个下标最多入栈和出栈一次。
- **空间复杂度**：O(n)，最坏情况字符串全部是左括号。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int longestValidParentheses(String s) {
        int best = 0;
        Deque<Integer> unmatched = new ArrayDeque<>();
        unmatched.push(-1);

        for (int index = 0; index < s.length(); index++) {
            if (s.charAt(index) == '(') {
                unmatched.push(index);
            } else {
                unmatched.pop();
                if (unmatched.isEmpty()) {
                    unmatched.push(index);
                } else {
                    best = Math.max(best, index - unmatched.peek());
                }
            }
        }
        return best;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int longestValidParentheses(String s) {
        int best = 0;
        Deque<Integer> unmatched = new ArrayDeque<>();
        unmatched.push(-1);

        for (int index = 0; index < s.length(); index++) {
            if (s.charAt(index) == '(') {
                unmatched.push(index);
            } else {
                unmatched.pop();
                if (unmatched.isEmpty()) {
                    unmatched.push(index);
                } else {
                    best = Math.max(best, index - unmatched.peek());
                }
            }
        }
        return best;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.longestValidParentheses("(()"));
        System.out.println(solution.longestValidParentheses(")()())"));
        System.out.println(solution.longestValidParentheses(""));
        System.out.println(solution.longestValidParentheses("()(())"));
    }
}
```

## 边界与易错点

- 空字符串应返回 0，初始哨兵 -1 使循环自然跳过。
- 栈为空时不能直接计算长度，应把当前右括号下标作为新基准。
- 长度用下标差计算，不再额外加一，因为栈顶本身位于有效区间之外。

## 可扩展变式

- 动态规划把 dp[i] 解释为以 i 结尾的最长有效后缀。
- 双向计数扫描可以用 O(1) 额外空间求最长长度，但不能直接定位区间。
