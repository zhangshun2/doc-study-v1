---
schemaVersion: 3
type: "core-model"
leetcodeId: 224
slug: "basic-calculator"
titleCn: "基本计算器"
titleEn: "Basic Calculator"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/basic-calculator/"
sourceCheckedAt: "2026-10-04"
sourceFactsSha256: "bb971ce00e613461c2178ef08685b34a86a6ae0421814dbaac8e78682c480977"
primaryPattern: "栈"
topics: ["栈","递归","数学","字符串"]
priority: "P0"
problemPath: "题目/栈/224-Basic-Calculator.md"
deepDivePath: "建模专题/T0/224-Basic-Calculator-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 224. 基本计算器：核心模型

> **双轨阅读：** [[题目/栈/224-Basic-Calculator.md|标准题解]] · [[建模专题/T0/224-Basic-Calculator-直观建模.md|完整建模]]

## 一句话本质

括号开启一层独立求和；左括号保存外层结果与符号，右括号把内层结果作为一个带符号操作数加回外层。

## 直观画面与扩题

像做账时遇到一个子账本：先记下母账本当前余额和处理下一步的符号，把子账本算完后，再按原符号并回母账本。

本题只有加减，本来不需要普通运算符优先级栈。真正打断线性计算的是括号，因为它要求先完成一段内部表达式，再把这个整体放回外层原来的位置。所以栈保存的对象不是每个数字，而是一层尚未恢复的外层现场。

## 关系重写

左括号把当前 result 和 sign 变成父层现场；右括号把子层 result 乘父层 sign 后并回父层 result。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 字符、当前层结果、下一位数字符号、外层括号现场 | 左括号把当前 result 和 sign 变成父层现场；右括号把子层 result 乘父层 sign 后并回父层 result。 | result 表示当前层已完成部分，sign 表示下一个数字符号；两个栈保存父层现场 | 数字按 sign 累加；左括号压入现场并重置当前层；右括号弹出父层，合并当前层结果 | 处理任意字符后，result 是当前最内层括号已经求值的部分，栈中从底到顶保存所有尚未恢复的外层结果和符号 | 扫描结束后栈必为空，result 就是完整表达式值 |

## 最小演算

官方首例输入：`s = "(1+(4+5+2)-3)+(6+8)"`。

1. 最外层左括号保存 result=0、sign=1；当前层从 0、+1 开始。
2. 读入 1 后当前层为 1；遇到内部左括号，再保存父层 1 与 +1。
3. 4+5+2 得到 11，遇到右括号后并回父层，当前层变为 1+11=12。
4. 继续 -3 得到 9，再遇右括号并回最外层；随后处理 +(6+8)，最终得到 23。

## 为什么成立

括号内部的字符与外部互不影响；只要保存外层已算结果和进入括号前的符号，就可以安全地把内层当成从零开始的独立表达式。右括号到来时内层已经完整，因此一次合并即可恢复父层全部信息。

## 代码映射

```text
result=0，sign=1，并准备两个现场栈。
从左到右扫描字符。
若读到数字，解析完整数字并按 sign 累加。
若读到 '('，保存 result 与 sign，再重置当前层。
若读到 ')'，弹出现场并合并当前层结果。
否则更新 sign。扫描结束返回 result。
```

## 复杂度

- 时间复杂度：O(n)，每个字符只读取一次，数字也只解析一次。
- 空间复杂度：O(d)，d 为括号最大嵌套深度。

## 30 秒识别信号

表达式只有加减或括号，并且遇到括号时需要先完成内部、再作为一个值回到外层时，考虑保存括号现场。

## 最小反例与易错点

- 右括号只合并一层，不能用全局累加替代嵌套现场。
- 括号前的负号属于父层符号，必须先保存再进入子层。

## 分层入口

- [[题目/栈/224-Basic-Calculator.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/224-Basic-Calculator-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
