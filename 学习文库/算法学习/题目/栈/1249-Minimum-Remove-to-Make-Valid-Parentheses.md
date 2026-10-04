---
schemaVersion: 3
type: "problem"
leetcodeId: 1249
slug: "minimum-remove-to-make-valid-parentheses"
titleCn: "移除无效的括号"
titleEn: "Minimum Remove to Make Valid Parentheses"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "a6e3f73b61a0551bef250f09492d87de34c0411915a08a9e768a12fa173beb57"
sourceFactsSha256: "23deedc21ab67304f7c9b9fe28c6a16d1315a17238bae272f8a4dd9621506b0b"
sourceSectionHashes:
  description: "9168f06d8ad0c074cd47d51f030370513c6fea0f561e39125c1c09243ad105c6"
  examples: "6bf090f58deb0e28ed636e1390df1316c32fd83422f89c3242ac54d244bc26fd"
  constraints: "aedf5826d24b4fae731aa68c191f1ad228ee967a1f0ded243e9f51b992b3658c"
  hints: "645ed93a532fc7581cd5fbcadbf0ef8c723752e28ba91fa771c2aa2761ade007"
  tags: "d1264e00749d6eee994311100a0b3b22ab372468f255e08d443be28855a492f8"
  signature: "5a3de95b3a9fd97b784cc4dde6f9fe4b7df8f9c500ed88eca49d71a24beb0e03"
  javaTemplate: "9a8e0d4f231e34a1a7cbdcd30525d72c17242a08206b50c495773f317ec6680e"
primaryPattern: "栈"
topics: ["栈","字符串"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Stack 栈","String 字符串"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 1249. 移除无效的括号 / Minimum Remove to Make Valid Parentheses

> **双轨入口：** [[核心模型/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses-核心模型.md|核心模型]]

## 题目信息

- 官方难度：`Medium`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`、`String 字符串`
- LeetCode 当前标签：栈 (Stack)、字符串 (String)
- 官方来源：<https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/>
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`a6e3f73b61a0551bef250f09492d87de34c0411915a08a9e768a12fa173beb57`
- **主解法**：标记无效括号

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个由 `'('`、`')'` 和小写字母组成的字符串 `s`。

你需要从字符串中删除最少数目的 `'('` 或者 `')'` （可以删除任意位置的括号)，使得剩下的「括号字符串」有效。

请返回任意一个合法字符串。

有效「括号字符串」应当符合以下 **任意一条 **要求：

- 空字符串或只包含小写字母的字符串

- 可以被写作 `AB`（`A` 连接 `B`）的字符串，其中 `A` 和 `B` 都是有效「括号字符串」

- 可以被写作 `(A)` 的字符串，其中 `A` 是一个有效的「括号字符串」

## 官方示例

**示例 1：**

```text
输入：s = "lee(t(c)o)de)"
输出："lee(t(c)o)de"
解释："lee(t(co)de)" , "lee(t(c)ode)" 也是一个可行答案。
```

**示例 2：**

```text
输入：s = "a)b(c)d"
输出："ab(c)d"
```

**示例 3：**

```text
输入：s = "))(("
输出：""
解释：空字符串也是有效的
```

## 官方约束

- `1 <= s.length <= 10^5`

- `s[i]` 可能是 `'('`、`')'` 或英文小写字母

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Each prefix of a balanced parentheses has a number of open parentheses greater or equal than closed parentheses, similar idea with each suffix.
2. Check the array from left to right, remove characters that do not meet the property mentioned above, same idea in backward way.

## 学习提示（非官方）

1. 从左到右无法匹配的右括号一定无效；扫描结束后栈内剩余左括号也一定无效。
2. 先记录无效位置，再统一构建结果，不会误删可以参与后续匹配的左括号。
3. 任意一个最少删除结果都可行，因此无需枚举组合。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：O(n)，两次线性扫描。
- 空间复杂度目标：O(n)，最坏保存全部左括号下标与布尔标记。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

有效括号要求任意前缀中左括号数量不少于右括号。扫描过程中所有无法匹配的右括号，以及结束后仍留在栈里的左括号，就是必须删除的最小集合。

## 朴素方案

可以枚举要删除的括号子集，再检查剩余字符串是否有效，保留删除数最少的组合。其数量为 O(2^n)，还可能在已经不可能成为最优解时继续搜索。

## 最优方案：一次标记无效括号，再一次构建结果

第一遍扫描只记录左括号下标。遇到右括号时，若栈非空就弹出最近的左括号，表示两者匹配；若栈为空，则当前右括号没有对应左括号，直接标记为无效。扫描结束后，栈中剩余下标都是未被匹配的左括号，也标记为无效。第二遍按原顺序拼接未标记字符。

### 正确性与不变量

遇到右括号时，若左侧还有未匹配左括号，弹出最近者即可形成合法嵌套；若没有，则无论保留哪个字符都无法让这个右括号合法。第一遍结束后还在栈中的左括号右侧没有足够右括号，也必须删除。其余弹掉的括号都有配对关系，且嵌套顺序由栈保证，所以删除标记集合后得到的字符串有效；任何无效括号不删除都不可能形成有效结果，因此删除数量也最少。

## 复杂度

- **时间复杂度**：O(n)，两次线性扫描。
- **空间复杂度**：O(n)，最坏保存全部左括号下标与布尔标记。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String minRemoveToMakeValid(String s) {
        Deque<Integer> openIndices = new ArrayDeque<>();
        boolean[] invalid = new boolean[s.length()];

        for (int index = 0; index < s.length(); index++) {
            char current = s.charAt(index);
            if (current == '(') {
                openIndices.push(index);
            } else if (current == ')') {
                if (openIndices.isEmpty()) {
                    invalid[index] = true;
                } else {
                    openIndices.pop();
                }
            }
        }
        while (!openIndices.isEmpty()) {
            invalid[openIndices.pop()] = true;
        }

        StringBuilder answer = new StringBuilder();
        for (int index = 0; index < s.length(); index++) {
            if (!invalid[index]) {
                answer.append(s.charAt(index));
            }
        }
        return answer.toString();
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String minRemoveToMakeValid(String s) {
        Deque<Integer> openIndices = new ArrayDeque<>();
        boolean[] invalid = new boolean[s.length()];

        for (int index = 0; index < s.length(); index++) {
            char current = s.charAt(index);
            if (current == '(') {
                openIndices.push(index);
            } else if (current == ')') {
                if (openIndices.isEmpty()) {
                    invalid[index] = true;
                } else {
                    openIndices.pop();
                }
            }
        }
        while (!openIndices.isEmpty()) {
            invalid[openIndices.pop()] = true;
        }

        StringBuilder answer = new StringBuilder();
        for (int index = 0; index < s.length(); index++) {
            if (!invalid[index]) {
                answer.append(s.charAt(index));
            }
        }
        return answer.toString();
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.minRemoveToMakeValid(
                "lee(t(c)o)de)"));
        System.out.println(solution.minRemoveToMakeValid("a)b(c)d"));
        System.out.println(solution.minRemoveToMakeValid("))(("));
        System.out.println(solution.minRemoveToMakeValid("(a(b)c)"));
    }
}
```

## 边界与易错点

- 字母直接保留，不参与匹配也不加入无效集合。
- 空字符串本身有效，构建结果自然为空。
- 匹配右括号时只能删除一个左括号，不能一次清空栈。

## 可扩展变式

- 两次计数扫描可用 O(1) 栈空间删除多余右括号和多余额左括号。
- 若要求字典序最小的最优结果，标记法还需要额外选择规则。
