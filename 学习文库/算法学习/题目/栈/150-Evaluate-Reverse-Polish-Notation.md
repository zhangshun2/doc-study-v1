---
schemaVersion: 3
type: "problem"
leetcodeId: 150
slug: "evaluate-reverse-polish-notation"
titleCn: "逆波兰表达式求值"
titleEn: "Evaluate Reverse Polish Notation"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/evaluate-reverse-polish-notation/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "9be4fbdd8577e17f2eb9bb8f65c80f0bec0fb9ad01aa3bf025453b13393dc498"
sourceFactsSha256: "6debbec6bbb1423b395a4327b01cbf1625a9615a74eddb96de1d5895a89b037a"
sourceSectionHashes:
  description: "2394f64efe224fbe0c511d1b2b8d7e5453710bf0f0dbbb92aa170010cb7996b6"
  examples: "74b0e9f998a91b211576f2e9b7d78dd4bec4df961cdafc72ffacd1f27d2e4fe3"
  constraints: "778b8f44f864f4fc336f7c9c145c7548c3302f6a2055a3a80c69d51b18d57378"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0745550be22d6e07e2c62dddf5b57ae36a80b12fe8112f90bf231b91d711d687"
  signature: "7f3d09a95e19b693211c2c0c53d7ffe2b600a83fd3b47b1c57b1372fee776ac2"
  javaTemplate: "cbd9446686ea1d667c0d86f704813ff2edf801232cd2bba02f4cc0ee7449d34d"
primaryPattern: "栈"
topics: ["栈","数组","数学"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Stack 栈","Array 数组","Math 数学"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 150. 逆波兰表达式求值 / Evaluate Reverse Polish Notation

> **双轨入口：** [[核心模型/栈/150-Evaluate-Reverse-Polish-Notation-核心模型.md|核心模型]]

## 题目信息

- 官方难度：`Medium`
- 主归档题型：`栈`
- 清单优先级：`P0`
- 清单代表标签：`Stack 栈`、`Array 数组`、`Math 数学`
- LeetCode 当前标签：栈 (Stack)、数组 (Array)、数学 (Math)
- 官方来源：<https://leetcode.cn/problems/evaluate-reverse-polish-notation/>
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`9be4fbdd8577e17f2eb9bb8f65c80f0bec0fb9ad01aa3bf025453b13393dc498`
- **主解法**：操作数栈

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个字符串数组 `tokens` ，表示一个根据 [逆波兰表示法](https://baike.baidu.com/item/%E9%80%86%E6%B3%A2%E5%85%B0%E5%BC%8F/128437) 表示的算术表达式。

请你计算该表达式。返回一个表示表达式值的整数。

**注意：**

- 有效的算符为 `'+'`、`'-'`、`'*'` 和 `'/'` 。

- 每个操作数（运算对象）都可以是一个整数或者另一个表达式。

- 两个整数之间的除法总是 **向零截断** 。

- 表达式中不含除零运算。

- 输入是一个根据逆波兰表示法表示的算术表达式。

- 答案及所有中间计算结果可以用 **32 位** 整数表示。

## 官方示例

**示例 1：**

```text
输入：tokens = ["2","1","+","3","*"]
输出：9
解释：该算式转化为常见的中缀算术表达式为：((2 + 1) * 3) = 9
```

**示例 2：**

```text
输入：tokens = ["4","13","5","/","+"]
输出：6
解释：该算式转化为常见的中缀算术表达式为：(4 + (13 / 5)) = 6
```

**示例 3：**

```text
输入：tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
输出：22
解释：该算式转化为常见的中缀算术表达式为：
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
```

## 官方约束

- `1 <= tokens.length <= 10^4`

- `tokens[i]` 是一个算符（`"+"`、`"-"`、`"*"` 或 `"/"`），或是在范围 `[-200, 200]` 内的一个整数

**逆波兰表达式：**

逆波兰表达式是一种后缀表达式，所谓后缀就是指算符写在后面。

- 平常使用的算式则是一种中缀表达式，如 `( 1 + 2 ) * ( 3 + 4 )` 。

- 该算式的逆波兰表达式写法为 `( ( 1 2 + ) ( 3 4 + ) * )` 。

逆波兰表达式主要有以下两个优点：

- 去掉括号后表达式无歧义，上式即便写成 `1 2 + 3 4 + *`也可以依据次序计算出正确结果。

- 适合用栈操作运算：遇到数字则入栈；遇到算符则取出栈顶两个数字进行计算，并将结果压入栈中

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 后缀表达式没有括号，运算顺序已经由 token 排列决定。
2. 运算符总作用于此前最近两个尚未合并的完整子表达式。
3. 减法和除法必须按弹出顺序还原左右操作数。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：O(n)，每个 token 只读取和计算一次。
- 空间复杂度目标：O(n)，栈中最多保存线性数量的中间表达式值。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

逆波兰表达式从左到右隐藏了括号：每读到一个运算符，它恰好合并此前最近完成的两个子表达式。栈顶天然保存这两个结果。

## 朴素方案

可以递归寻找表达式根节点，但需要先确定哪一段属于左子树、哪一段属于右子树；对数组做线性切分后递归也可行，却增加了边界状态和重复解释 token 的成本。

## 最优方案：一次扫描操作数栈

遇到数字时解析整数并压栈。遇到运算符时弹出栈顶作为右操作数，再弹出新的栈顶作为左操作数，计算后把结果压回。扫描结束时，整个表达式已经合并成一个值，栈顶就是答案。

### 正确性与不变量

每个数字本身代表一个完整子表达式。每次遇到运算符时，栈顶两个值恰是以该运算符为根的两个已求值子树；按照后缀顺序弹出右、左操作数并计算，就把这两棵子树合并为一棵。归纳可知扫描到任意前缀时，栈中保存的是该前缀无法再局部合并的完整子表达式；最终只剩一个值即原表达式结果。

## 复杂度

- **时间复杂度**：O(n)，每个 token 只读取和计算一次。
- **空间复杂度**：O(n)，栈中最多保存线性数量的中间表达式值。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> values = new ArrayDeque<>();

        for (String token : tokens) {
            if (isOperator(token)) {
                int right = values.pop();
                int left = values.pop();
                values.push(apply(left, right, token));
            } else {
                values.push(Integer.parseInt(token));
            }
        }
        return values.pop();
    }

    private boolean isOperator(String token) {
        return token.length() == 1
                && "+-*/".indexOf(token.charAt(0)) >= 0;
    }

    private int apply(int left, int right, String operator) {
        if ("+".equals(operator)) {
            return left + right;
        }
        if ("-".equals(operator)) {
            return left - right;
        }
        if ("*".equals(operator)) {
            return left * right;
        }
        return left / right;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> values = new ArrayDeque<>();

        for (String token : tokens) {
            if (isOperator(token)) {
                int right = values.pop();
                int left = values.pop();
                values.push(apply(left, right, token));
            } else {
                values.push(Integer.parseInt(token));
            }
        }
        return values.pop();
    }

    private boolean isOperator(String token) {
        return token.length() == 1
                && "+-*/".indexOf(token.charAt(0)) >= 0;
    }

    private int apply(int left, int right, String operator) {
        if ("+".equals(operator)) {
            return left + right;
        }
        if ("-".equals(operator)) {
            return left - right;
        }
        if ("*".equals(operator)) {
            return left * right;
        }
        return left / right;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.evalRPN(
                new String[]{"2", "1", "+", "3", "*"}));
        System.out.println(solution.evalRPN(
                new String[]{"4", "13", "5", "/", "+"}));
        System.out.println(solution.evalRPN(new String[]{
                "10", "6", "9", "3", "+", "-11", "*",
                "/", "*", "17", "+", "5", "+"
        }));
        System.out.println(solution.evalRPN(
                new String[]{"3", "4", "-"}));
    }
}
```

## 边界与易错点

- 负数 token 例如 -11 要先用 Integer.parseInt 解析，不能按单字符判断。
- 除法按 Java 整数规则向零截断，不能用 Math.floorDiv，后者向负无穷取整。
- 运算符判断不能只看首字符，否则负数字符串可能被误判。

## 可扩展变式

- 中缀表达式求值通常还需要处理运算符优先级和括号现场。
- 编译器可把中缀表达式先转换为后缀，再用同一模型求值。
