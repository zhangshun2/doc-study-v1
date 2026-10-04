---
schemaVersion: 3
type: "problem"
leetcodeId: 20
slug: "valid-parentheses"
titleCn: "有效的括号"
titleEn: "Valid Parentheses"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/valid-parentheses/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "44f6f258b852802debfb31dade445d1a73400dd3f3b87dbf2f03601872555ae1"
sourceFactsSha256: "03c24c94303d51b4769bcada015b9342ab32b95ea5e1e6d6ac3c9fa5742629e2"
sourceSectionHashes:
  description: "5038aeba2e559b0b322787a5c641ec6bc4365c5b311784449b6969a982a8b516"
  examples: "ff0ff4192f2a907b5c14d26deab24ef43e9556b95210161efddbf351f00a1a72"
  constraints: "3f8416461f91bd6a25e3d3af6d6d8b67c8d9b1bc2037abb182690f83b4c2c3c2"
  hints: "2212f51b28c61cfa6f3d73fc942f711f1372815e576f4112b7ca4c22f2e8e381"
  tags: "ea380972fddf126a6a06b6dd023d5ac30749b0739fc4edd06c53959c958a6683"
  signature: "0906d2946d5c91869b6e4a796bb87a5798c4185797aea33880bfd94eafd1e1bf"
  javaTemplate: "acdae391d0962626384a2019d17c44154f8bb37fa8db6320c14806445f819f1a"
primaryPattern: "栈"
topics: ["栈","字符串","括号序列"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Stack 栈"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 20. 有效的括号 / Valid Parentheses

> **双轨入口：** [[核心模型/栈/20-Valid-Parentheses-核心模型.md|核心模型]] · [[建模专题/T0/20-Valid-Parentheses-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`
- LeetCode 当前标签：栈 (Stack)、字符串 (String)、括号序列
- 官方来源：<https://leetcode.cn/problems/valid-parentheses/>
- 直观建模专题：[从“反复消去合法对”到“维护未完成闭合约定”](../../建模专题/T0/20-Valid-Parentheses-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`44f6f258b852802debfb31dade445d1a73400dd3f3b87dbf2f03601872555ae1`
- 主模型：栈保存尚未匹配的结束符

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个只包括 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s` ，判断字符串是否有效。

有效字符串需满足：

- 左括号必须用相同类型的右括号闭合。

- 左括号必须以正确的顺序闭合。

- 每个右括号都有一个对应的相同类型的左括号。

## 官方示例


**示例 1：**

输入：s = "()"

输出：true

**示例 2：**

输入：s = "()[]{}"

输出：true

**示例 3：**

输入：s = "(]"

输出：false

**示例 4：**

输入：s = "([])"

输出：true

**示例 5：**

输入：s = "([)]"

输出：false

## 官方约束


- `1 <= s.length <= 10^4`

- `s` 仅由括号 `'()[]{}'` 组成

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Use a stack of characters.
2. When you encounter an opening bracket, push it to the top of the stack.
3. When you encounter a closing bracket, check if the top of the stack was the opening for it. If yes, pop it from the stack. Otherwise, return false.

## 学习提示（非官方）

1. 最后遇到、但尚未闭合的左括号，必须最先闭合，这是后进先出。
2. 遇到左括号时，可以把它对应的右括号压栈；遇到右括号时直接比较栈顶。
3. 扫描中不能从空栈弹出，扫描结束后栈也必须为空。
4. 奇数长度字符串一定无效，可提前返回。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

嵌套结构天然符合栈：`([{}])` 中 `{` 最晚打开却最早关闭。与其压入左括号后再写映射判断，不如在遇到左括号时压入“未来期望看到的右括号”。这样右括号分支只需做一次相等比较。

## 朴素方案：反复替换成对括号

不断把字符串中的 `()`、`[]`、`{}` 替换为空，直至不能变化，最后检查是否为空。它容易理解，但每轮替换会扫描和创建新字符串，深度嵌套时需要多轮。

- 时间复杂度：最坏 `O(n^2)`。
- 空间复杂度：`O(n)`。

仅统计三类括号数量也不正确，因为 `([)]` 的数量平衡但顺序非法。

## 最优方案：一次扫描栈

遇到左括号时压入对应右括号，遇到右括号时：

1. 若栈为空，说明它没有左括号，返回 `false`。
2. 弹出栈顶，若不等于当前字符，说明类型或顺序错误，返回 `false`。
3. 扫描结束后只有栈为空才有效。

### 正确性与不变量

处理完任意前缀后，栈从底到顶保存该前缀中尚未闭合的左括号所期望的右括号，栈顶是下一次必须最先出现的结束符。左括号分支维持该不变量；右括号若与栈顶不同就不可能形成合法嵌套，若相同则恰好完成最近一对匹配。最终栈空等价于所有打开的括号均已闭合。

- 时间复杂度：`O(n)`。
- 空间复杂度：最坏 `O(n)`，如全部是左括号。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public boolean isValid(String s) {
        if (s.length() % 2 == 1) {
            return false;
        }

        Deque<Character> expectedClosings = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char current = s.charAt(i);
            if (current == '(') {
                expectedClosings.push(')');
            } else if (current == '[') {
                expectedClosings.push(']');
            } else if (current == '{') {
                expectedClosings.push('}');
            } else if (expectedClosings.isEmpty()
                    || expectedClosings.pop() != current) {
                return false;
            }
        }
        return expectedClosings.isEmpty();
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class Solution {
    public boolean isValid(String s) {
        if (s.length() % 2 == 1) {
            return false;
        }

        Deque<Character> expectedClosings = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char current = s.charAt(i);
            if (current == '(') {
                expectedClosings.push(')');
            } else if (current == '[') {
                expectedClosings.push(']');
            } else if (current == '{') {
                expectedClosings.push('}');
            } else if (expectedClosings.isEmpty()
                    || expectedClosings.pop() != current) {
                return false;
            }
        }
        return expectedClosings.isEmpty();
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.isValid("()"));     // true
        System.out.println(solution.isValid("()[]{}")); // true
        System.out.println(solution.isValid("(]"));     // false
        System.out.println(solution.isValid("([)]"));   // false
        System.out.println(solution.isValid("{[]}"));   // true
    }
}
```

## 边界与易错点

- 不能只看括号数量，类型与嵌套顺序同样重要。
- 遇到右括号时必须先判断空栈，避免 `NoSuchElementException`。
- 扫描完仍有左括号，例如 `"(("`，必须返回 `false`。
- Java 推荐 `ArrayDeque` 作为栈，不推荐旧的 `Stack` 类。

## 可扩展变式

- 含普通字符的表达式可在扫描时忽略非括号字符。
- 需要报告错误位置时，在栈中保存括号和下标的二元信息。
- “最长有效括号”需要栈保存下标或使用动态规划，不只是布尔匹配。
- 编译器的块结构、函数调用与表达式求值也使用同样的栈模型。
