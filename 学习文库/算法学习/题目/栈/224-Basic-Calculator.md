---
schemaVersion: 3
type: "problem"
leetcodeId: 224
slug: "basic-calculator"
titleCn: "基本计算器"
titleEn: "Basic Calculator"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/basic-calculator/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "88d18712de398667bba05b634f5c6260c1ef8bff7d9261965a4abba28ef26a88"
sourceFactsSha256: "bb971ce00e613461c2178ef08685b34a86a6ae0421814dbaac8e78682c480977"
sourceSectionHashes:
  description: "34ac5e8803fcdbde93116b377978ea3c299bfe556a0f6c8996ebe0f059cb0e56"
  examples: "1b3b5428ffd8a3e925bef8ed2dfb2f360d8224ee739ca15681de9ffdea7743b1"
  constraints: "c805707b5f169e22a1f145f49cb58937a62380b8fdf8104c9e8c80d9409ac757"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0554f00f243191e00ffde9a011083758c2e07c70825949e3e677a259ac2a63e5"
  signature: "7b149bf160fe5cdc12c54a97965d0927b738828ebc68704abedbdc4264171d06"
  javaTemplate: "f198a2af5509329f52318a6f88d3cdfcfc8f1465e510f11df2478442144c3c5d"
primaryPattern: "栈"
topics: ["栈","递归","数学","字符串"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Stack 栈","Recursion 递归","Math 数学"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 224. 基本计算器 / Basic Calculator

> **双轨入口：** [[核心模型/栈/224-Basic-Calculator-核心模型.md|核心模型]] · [[建模专题/T0/224-Basic-Calculator-直观建模.md|完整建模]]

## 题目信息

- 官方难度：`Hard`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`、`Recursion 递归`、`Math 数学`
- LeetCode 当前标签：栈 (Stack)、递归 (Recursion)、数学 (Math)、字符串 (String)
- 官方来源：<https://leetcode.cn/problems/basic-calculator/>
- 直观建模专题：[完整推导](../../建模专题/T0/224-Basic-Calculator-直观建模.md)
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`88d18712de398667bba05b634f5c6260c1ef8bff7d9261965a4abba28ef26a88`
- **主解法**：括号现场栈

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个字符串表达式 `s` ，请你实现一个基本计算器来计算并返回它的值。

注意:不允许使用任何将字符串作为数学表达式计算的内置函数，比如 `eval()` 。

## 官方示例

**示例 1：**

```text
输入：s = "1 + 1"
输出：2
```

**示例 2：**

```text
输入：s = " 2-1 + 2 "
输出：3
```

**示例 3：**

```text
输入：s = "(1+(4+5+2)-3)+(6+8)"
输出：23
```

## 官方约束

- `1 <= s.length <= 3 * 10^5`

- `s` 由数字、`'+'`、`'-'`、`'('`、`')'`、和 `' '` 组成

- `s` 表示一个有效的表达式

- `'+'` 不能用作一元运算(例如， `"+1"` 和 `"+(2 + 3)"` 无效)

- `'-'` 可以用作一元运算(即 `"-1"` 和 `"-(2 + 3)"` 是有效的)

- 输入中不存在两个连续的操作符

- 每个数字和运行的计算将适合于一个有符号的 32位 整数

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 只有加减时，表达式可以从左到右累加；括号改变的是每层计算的起点。
2. 遇到左括号时保存外层已有结果和括号前符号，然后从零开始计算内层。
3. 遇到右括号时把内层结果乘以外层符号，再加回保存的外层结果。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：O(n)，每个字符只读取一次，数字也只解析一次。
- 空间复杂度目标：O(d)，d 为括号最大嵌套深度。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

加减表达式可以边扫描边合并；括号不是为了优先级重新排序，而是在当前位置开启一个独立的子表达式。

## 朴素方案

可先把表达式转换为抽象语法树或后缀表达式，再统一求值；这能处理更完整的运算符集合，但本题只有加减和括号，构建额外结构会引入不必要的优先级与转换状态。

## 最优方案：单栈保存括号外现场

维护当前层 result 和下一个数字的 sign。数字解析完整后，按 sign 加入 result。遇到左括号，把外层 result 和外层 sign 压栈，再把当前层重置为 0 和正号；遇到右括号，先得到当前层结果，再弹出外层现场，用 外层结果 + 外层符号 * 当前层结果 合并。一元负号自然表现为括号或数字前的 sign=-1。

### 正确性与不变量

在不含括号的任意连续片段中，从左到右累加配合当前 sign 与普通加减意义一致。每遇到左括号，当前 result 和 sign 正好完整描述括号左侧的外层现场，可以暂停并保存。括号内部独立计算结束后，它作为外层的一个带符号操作数合并返回；嵌套括号通过同样规则逐层弹出，因此最终结果唯一且正确。

## 复杂度

- **时间复杂度**：O(n)，每个字符只读取一次，数字也只解析一次。
- **空间复杂度**：O(d)，d 为括号最大嵌套深度。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int calculate(String s) {
        Deque<Integer> outerResult = new ArrayDeque<>();
        Deque<Integer> outerSign = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        int index = 0;

        while (index < s.length()) {
            char current = s.charAt(index);
            if (Character.isDigit(current)) {
                int number = 0;
                while (index < s.length()
                        && Character.isDigit(s.charAt(index))) {
                    number = number * 10 + (s.charAt(index) - '0');
                    index++;
                }
                result += sign * number;
                continue;
            }
            if (current == '+') {
                sign = 1;
            } else if (current == '-') {
                sign = -1;
            } else if (current == '(') {
                outerResult.push(result);
                outerSign.push(sign);
                result = 0;
                sign = 1;
            } else if (current == ')') {
                result = outerResult.pop()
                        + outerSign.pop() * result;
            }
            index++;
        }
        return result;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int calculate(String s) {
        Deque<Integer> outerResult = new ArrayDeque<>();
        Deque<Integer> outerSign = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        int index = 0;

        while (index < s.length()) {
            char current = s.charAt(index);
            if (Character.isDigit(current)) {
                int number = 0;
                while (index < s.length()
                        && Character.isDigit(s.charAt(index))) {
                    number = number * 10 + (s.charAt(index) - '0');
                    index++;
                }
                result += sign * number;
                continue;
            }
            if (current == '+') {
                sign = 1;
            } else if (current == '-') {
                sign = -1;
            } else if (current == '(') {
                outerResult.push(result);
                outerSign.push(sign);
                result = 0;
                sign = 1;
            } else if (current == ')') {
                result = outerResult.pop()
                        + outerSign.pop() * result;
            }
            index++;
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.calculate("1 + 1"));
        System.out.println(solution.calculate(" 2-1 + 2 "));
        System.out.println(solution.calculate(
                "(1+(4+5+2)-3)+(6+8)"));
        System.out.println(solution.calculate("-(2-3)"));
    }
}
```

## 边界与易错点

- 空格必须跳过，不能当作数字或运算符。
- 多位数字要累积解析，解析结束后当前下标仍要停留在最后一个数字字符。
- 左括号前的负号要一并保存；否则 -(1+2) 会丢掉外层取反。

## 可扩展变式

- 加入乘法除法时，需要再引入优先级栈或先转换为后缀表达式。
- 递归下降法使用函数调用栈表达同样的括号现场。
