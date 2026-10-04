---
schemaVersion: 3
type: "core-model"
leetcodeId: 9
slug: "palindrome-number"
titleCn: "回文数"
titleEn: "Palindrome Number"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/palindrome-number/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "ca1cfae1e1839f6fcfa4d7d1b8a4bca65aa1cf737b673d0c623385a8ba57ec47"
primaryPattern: "数学"
topics: ["数学"]
priority: "P1"
problemPath: "题目/数学/9-Palindrome-Number.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 9. 回文数：核心模型

> **双轨阅读：** [[题目/数学/9-Palindrome-Number.md|标准题解]]

## 一句话本质

完整反转可能接近溢出，而判断回文只需要比较前后两半。例如 1221： x=1221, reversedHalf=0 x=122, reversedHalf=1 x=12, reversedHalf=12 -> 两半相等

## 直观画面与扩题

像逐位拆开十进制计数器，每次只处理当前最低位，同时守住溢出边界。

在本题中，对象是 **整数位、反转过程或比较边界**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：完整反转可能接近溢出，而判断回文只需要比较前后两半。例如 1221： x=1221, reversedHalf=0 x=122, reversedHalf=1 x=12, reversedHalf=12 -> 两半相等

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 整数位、反转过程或比较边界 | 把题目翻译成一条可执行关系：完整反转可能接近溢出，而判断回文只需要比较前后两半。例如 1221： x=1221, reversedHalf=0 x=122, reversedHalf=1 x=12, reversedHalf=12 -> 两半相等 | 先排除负数和非零末位零。不断从 x 末尾取一位加入 reversedHalf，直到 x <= reversedHalf。 | 不断从 x 末尾取一位加入 reversedHalf，直到 x <= reversedHalf。 | 每轮后，x 保存原数尚未处理的高位前缀，reversedHalf 保存已取出低位后缀的反转。 | 每轮后，x 保存原数尚未处理的高位前缀，reversedHalf 保存已取出低位后缀的反转。 |

## 最小演算

官方首例输入：`x = 121`，输出：`true`。

1. **初始状态：** 先排除负数和非零末位零。
2. **触发事件：** 不断从 x 末尾取一位加入 reversedHalf，直到 x <= reversedHalf。
3. **结束条件：** 每轮后，x 保存原数尚未处理的高位前缀，reversedHalf 保存已取出低位后缀的反转。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮后，x 保存原数尚未处理的高位前缀，reversedHalf 保存已取出低位后缀的反转。停止时后缀位数不小于前缀位数。偶数位回文要求二者完全相等；奇数位回文只多出中间数字，它位于 reversedHalf 的末位，除以 10 后应与前缀相等。这两个条件也只会接受真正对称的数字。

## 代码映射

```text
1. 先排除负数和非零末位零。
2. 不断从 x 末尾取一位加入 reversedHalf，直到 x <= reversedHalf。
3. 最后判断：
```

## 复杂度

- 时间复杂度：O(log10 |x|)，约处理数字位数的一半。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`数学`
- 切入点：负数一定不是回文数。

## 最小反例与易错点

- 0 是回文数，排除末位零时要加 x != 0。
- 负号没有对称位置，所以所有负数直接为 false。

## 分层入口

- [[题目/数学/9-Palindrome-Number.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
