---
schemaVersion: 3
type: "problem"
leetcodeId: 394
slug: "decode-string"
titleCn: "字符串解码"
titleEn: "Decode String"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/decode-string/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "b28c5573a3b8d241d0efc6f1aec6d349eff633faf39730073e80d6d7fc457dc1"
sourceFactsSha256: "c7e4cf68f9c555fe0db0eb04593c0cb91d40e6b2811b6da9b9f409bb29e934a5"
sourceSectionHashes:
  description: "862e9bf50c7a2b949f9a82b5844c6b732cdb21b626f66a15207af9a467cc50dc"
  examples: "df2818bd717f9c9b9fbf41f29e3f3abfce76c46609e34eddfe3a5f8d0cad918e"
  constraints: "ee0384554972944d672898154b002a9eac1efe0807c4dc3749cad1c4328e4bfd"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "08bf2080a20cf58e66ab3ac59839be48b676afc033bd3f49c8ea79af9142f51a"
  signature: "72f76310ddea028be1190ea17296be2d35f5abfcb8ec9304e09ecf2a9779bc9b"
  javaTemplate: "5f3e1c297ceefe719a8c4d0752677b0f24426257119529785edffcacb1940f90"
primaryPattern: "栈"
topics: ["栈","递归","字符串"]
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
# 394. 字符串解码 / Decode String

> **双轨入口：** [[核心模型/栈/394-Decode-String-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`
- LeetCode 当前标签：栈 (Stack)、递归 (Recursion)、字符串 (String)
- 官方来源：<https://leetcode.cn/problems/decode-string/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`b28c5573a3b8d241d0efc6f1aec6d349eff633faf39730073e80d6d7fc457dc1`
- **主解法**：数字栈 + 前缀字符串栈

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: `k[encoded_string]`，表示其中方括号内部的 `encoded_string` 正好重复 `k` 次。注意 `k` 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 `k` ，例如不会出现像 `3a` 或 `2[4]` 的输入。

测试用例保证输出的长度不会超过 `10^5`。

## 官方示例


**示例 1：**

```text
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

**示例 2：**

```text
输入：s = "3[a2[c]]"
输出："accaccacc"
```

**示例 3：**

```text
输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
```

**示例 4：**

```text
输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"
```

## 官方约束


- `1 <= s.length <= 30`

- `s` 由小写英文字母、数字和方括号 `'[]'` 组成

- `s` 保证是一个 **有效** 的输入。

- `s` 中所有整数的取值范围为 `[1, 300]`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 遇到 `[` 时，需要保存进入这一层之前的前缀和重复次数。
2. 遇到 `]` 时，当前构建器就是本层已经解码的内容。
3. 数字必须按 `repeat = repeat * 10 + digit` 累积，不能逐位当作独立次数。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

嵌套括号天然符合后进先出：最内层编码最先闭合和展开。进入新层时将外层现场压栈；退出时弹出现场，把当前片段重复指定次数并接到外层前缀。

## 朴素方案

反复用正则表达式寻找最内层的“重复次数加方括号片段”并替换，虽然可以工作，但每轮会重新扫描和复制字符串，嵌套或输出很大时可能接近 `O(outputLength * nesting)`，也难以优雅处理多位数字。递归下降同样可达线性，是另一种好方案，但需维护共享下标。

## 最优方案推导

维护 `current`（当前层字符串）、`repeat`（正在读取的次数）、两个栈：

- 数字：累计到 `repeat`。
- 字母：追加到 `current`。
- `[`：压入 `repeat` 和当前 `current`，随后清空它们进入新层。
- `]`：弹出次数和外层前缀，把当前层重复后接到外层，成为新的 `current`。

遍历结束后的 `current` 即完整答案。

## 正确性与不变量

扫描任意前缀后，栈中从底到顶依次保存所有尚未闭合层的“外层已解码前缀 + 重复次数”，`current` 保存最内层正在构建的已解码内容。

普通字符和数字显然保持不变量；`[` 保存现场并进入新层；`]` 按编码定义完整展开最内层，再恢复外层现场。括号合法保证栈操作匹配。扫描结束时没有未闭合层，`current` 因而是整个字符串的解码结果。

## 复杂度

- **时间复杂度**：`O(|s| + |answer|)`，每个输入字符解析一次，每个输出字符至少需要被生成一次。嵌套拼接有复制常数，题目输出上限保证可控。
- **空间复杂度**：`O(|answer| + depth)`，字符串构建结果及嵌套栈。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String decodeString(String s) {
        Deque<Integer> repeatStack = new ArrayDeque<>();
        Deque<StringBuilder> prefixStack = new ArrayDeque<>();
        StringBuilder current = new StringBuilder();
        int repeat = 0;

        for (int index = 0; index < s.length(); index++) {
            char character = s.charAt(index);
            if (Character.isDigit(character)) {
                repeat = repeat * 10 + (character - '0');
            } else if (character == '[') {
                repeatStack.push(repeat);
                prefixStack.push(current);
                repeat = 0;
                current = new StringBuilder();
            } else if (character == ']') {
                int times = repeatStack.pop();
                StringBuilder outer = prefixStack.pop();
                for (int count = 0; count < times; count++) {
                    outer.append(current);
                }
                current = outer;
            } else {
                current.append(character);
            }
        }
        return current.toString();
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String decodeString(String s) {
        Deque<Integer> repeatStack = new ArrayDeque<>();
        Deque<StringBuilder> prefixStack = new ArrayDeque<>();
        StringBuilder current = new StringBuilder();
        int repeat = 0;

        for (int index = 0; index < s.length(); index++) {
            char character = s.charAt(index);
            if (Character.isDigit(character)) {
                repeat = repeat * 10 + (character - '0');
            } else if (character == '[') {
                repeatStack.push(repeat);
                prefixStack.push(current);
                repeat = 0;
                current = new StringBuilder();
            } else if (character == ']') {
                int times = repeatStack.pop();
                StringBuilder outer = prefixStack.pop();
                for (int count = 0; count < times; count++) {
                    outer.append(current);
                }
                current = outer;
            } else {
                current.append(character);
            }
        }
        return current.toString();
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.decodeString("3[a]2[bc]"));
        System.out.println(solution.decodeString("3[a2[c]]"));
        System.out.println(solution.decodeString("2[abc]3[cd]ef"));
        System.out.println(solution.decodeString("12[z]"));
    }
}
```

## 边界与易错点

- 多位次数必须逐位累积，`12[a]` 不是 1 次后 2 次。
- `[` 后必须把 `repeat` 重置为 0，并为当前层创建新构建器。
- 用循环追加当前片段，避免不可变字符串反复执行 `+` 拼接；该写法在 Java 17 中可直接运行。
- 解码顺序不能反：应为“外层前缀 + 当前片段重复若干次”。
- 输入虽短，输出可能很长，应使用 `StringBuilder`，不要循环做不可变字符串 `+` 拼接。

## 可扩展变式

- 递归下降解析：函数解析到对应 `]` 后返回，代码能更直接对应文法。
- 输入可能非法：增加括号、次数、非法字符和输出上限验证。
- 只查询解码长度：无需构造字符串，栈中保存长度并注意溢出。
- 输出可能极大：以迭代器或流的形式惰性展开，而不是一次性构造全部文本。
