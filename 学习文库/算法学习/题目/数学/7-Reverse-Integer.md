---
schemaVersion: 3
type: "problem"
leetcodeId: 7
slug: "reverse-integer"
titleCn: "整数反转"
titleEn: "Reverse Integer"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/reverse-integer/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "99f5832a46a9c83a3b4ff8cd4b4fadd868b277ea61daa3423fdbe2fa50109bb7"
sourceFactsSha256: "84e0d08c126d506418c2f429bacb538f2fadf8151ac4bff4064e443867e61aa8"
sourceSectionHashes:
  description: "d58f5695a9d0b0c1040a5cc1ab3070de2fb7388a207a68c4e37b92169301200a"
  examples: "af0613aebafb9c7d840d26e4c7eb79a699a92938c13ef81dcbdcc5dfe76afa13"
  constraints: "e97e3a4d47ae415bf486be21fcd551f033cdf0ecd06fae730ae4984c8bc2e731"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "06edb80c76ca31f042e090652428b3b46f710393d25f9c95e7e75d8d60e4fd1e"
  signature: "9761ff5cb4ecfb99f272b742dd1bf1538bef684b51740c097a4d27447a700cdc"
  javaTemplate: "10789ded01f9f1a68e09521fad58cfe29b0f9b3aa57821bb2ca2fd19eeef8c3e"
primaryPattern: "数学"
topics: ["数学"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Math 数学"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 7. 整数反转 / Reverse Integer

> **双轨入口：** [[核心模型/数学/7-Reverse-Integer-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`数学`
- 清单优先级：`P1`
- 清单代表标签：`Math 数学`
- LeetCode 当前标签：数学 (Math)
- 官方来源：<https://leetcode.cn/problems/reverse-integer/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`99f5832a46a9c83a3b4ff8cd4b4fadd868b277ea61daa3423fdbe2fa50109bb7`
- 主模型：逐位取模 + 写入前溢出检查

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个 32 位的有符号整数 `x` ，返回将 `x` 中的数字部分反转后的结果。

如果反转后整数超过 32 位的有符号整数的范围 `[−2^31,  2^31 − 1]` ，就返回 0。

**假设环境不允许存储 64 位整数（有符号或无符号）。**

## 官方示例


**示例 1：**

```text
输入：x = 123
输出：321
```

**示例 2：**

```text
输入：x = -123
输出：-321
```

**示例 3：**

```text
输入：x = 120
输出：21
```

**示例 4：**

```text
输入：x = 0
输出：0
```

## 官方约束


- `-2^31 <= x <= 2^31 - 1`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. `x % 10` 取得末位，`x / 10` 删除末位。
2. 新结果为 `reversed * 10 + digit`，必须在执行乘法和加法之前判断是否溢出。
3. Java 的整数除法向零截断，负数也可以直接按同一逻辑处理。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 目标时间复杂度为数字位数级别，即 `O(log10 |x|)`；空间应为 `O(1)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

每次把原数最后一位弹出，再压入结果末尾：

```text
digit = x % 10
x /= 10
reversed = reversed * 10 + digit
```

真正难点是最后一行可能在判断前已经溢出。设上界为 `MAX`：若 `reversed > MAX/10`，乘 10 必溢出；若等于 `MAX/10`，则只有 `digit <= MAX%10` 才安全。下界同理。

## 朴素方案：字符串反转或使用 long

可先提取符号，把绝对值转字符串并反转，再解析为 `long`。但 `Math.abs(Integer.MIN_VALUE)` 本身就会溢出，而且题目明确禁止 64 位整数。这种方案依赖异常或更宽类型兜底，没有解决核心问题。

- 时间复杂度：`O(log |x|)`。
- 空间复杂度：`O(log |x|)`。
- 局限：违反题设环境限制。

## 最优方案：纯 int 的数学反转

在每次写入新数字前，用除法边界判断。Java 中：

```text
Integer.MAX_VALUE / 10 = 214748364，末位上限为 7
Integer.MIN_VALUE / 10 = -214748364，末位下限为 -8
```

### 正确性与不变量

每轮开始时，`reversed` 是已从原数末尾取出的所有数字按反向顺序组成的整数，`x` 是尚未处理的高位部分。取出 `digit` 并安全追加后，该关系继续成立。预检查精确排除了大于最大值或小于最小值的两类情况。循环结束时没有剩余数字，因此 `reversed` 就是所求反转值。

- 时间复杂度：`O(log10 |x|)`，最多处理 10 位。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int reverse(int x) {
        int reversed = 0;

        while (x != 0) {
            int digit = x % 10;
            x /= 10;

            if (reversed > Integer.MAX_VALUE / 10
                    || (reversed == Integer.MAX_VALUE / 10
                    && digit > Integer.MAX_VALUE % 10)) {
                return 0;
            }
            if (reversed < Integer.MIN_VALUE / 10
                    || (reversed == Integer.MIN_VALUE / 10
                    && digit < Integer.MIN_VALUE % 10)) {
                return 0;
            }

            reversed = reversed * 10 + digit;
        }
        return reversed;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public int reverse(int x) {
        int reversed = 0;

        while (x != 0) {
            int digit = x % 10;
            x /= 10;

            if (reversed > Integer.MAX_VALUE / 10
                    || (reversed == Integer.MAX_VALUE / 10
                    && digit > Integer.MAX_VALUE % 10)) {
                return 0;
            }
            if (reversed < Integer.MIN_VALUE / 10
                    || (reversed == Integer.MIN_VALUE / 10
                    && digit < Integer.MIN_VALUE % 10)) {
                return 0;
            }

            reversed = reversed * 10 + digit;
        }
        return reversed;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.reverse(123));          // 321
        System.out.println(solution.reverse(-123));         // -321
        System.out.println(solution.reverse(120));          // 21
        System.out.println(solution.reverse(1_534_236_469)); // 0
    }
}
```

## 边界与易错点

- 不要对 `x` 先取绝对值，`Integer.MIN_VALUE` 的绝对值无法用 `int` 表示。
- Java 中 `-123 % 10 == -3`、`-123 / 10 == -12`，因此正负数可统一处理。
- 末尾的零反转后自然消失，无需特殊删除。
- 边界判断必须出现在 `reversed * 10 + digit` 之前。

## 可扩展变式

- 回文数可以只反转后一半数字，既避免字符串也更易控制溢出。
- 任意进制反转时，把除数和模数 `10` 改为 `base`，并重新计算边界。
- 若题目允许 64 位类型，可用 `long` 简化检查，但仍应明确最终范围。
