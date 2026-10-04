---
schemaVersion: 3
type: "core-model"
leetcodeId: 1249
slug: "minimum-remove-to-make-valid-parentheses"
titleCn: "移除无效的括号"
titleEn: "Minimum Remove to Make Valid Parentheses"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/"
sourceCheckedAt: "2026-10-04"
sourceFactsSha256: "23deedc21ab67304f7c9b9fe28c6a16d1315a17238bae272f8a4dd9621506b0b"
primaryPattern: "栈"
topics: ["栈","字符串"]
priority: "P0"
problemPath: "题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 1249. 移除无效的括号：核心模型

> **双轨阅读：** [[题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md|标准题解]]

## 一句话本质

扫描时匹配成功的括号都保留，无法配对的右括号和最终剩余左括号恰好构成必须删除的最小集合。

## 直观画面与扩题

像检查一串门锁：遇到关门时若有可用的最近钥匙就配掉；没有钥匙的门和结束时仍未使用的钥匙都属于坏零件。

本题只要求返回任意一个最优结果，因此不需要枚举方案。关键是把“最少删除”转化为“哪些括号注定无法参与任何合法匹配”。一次栈扫描可以完整找出这两类括号，之后只需过滤。

## 关系重写

右括号优先匹配最近未配对左括号；匹配失败的右括号和扫描结束时剩余左括号都必须删除。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 括号字符、字符下标、未匹配左括号、无效位置标记 | 右括号优先匹配最近未配对左括号；匹配失败的右括号和扫描结束时剩余左括号都必须删除。 | 栈保存尚未匹配左括号下标，boolean 数组标记无效位置 | 左括号入栈；右括号能配则弹栈，否则标记；扫描结束后剩余栈元素全部标记 | 第一遍处理任意前缀后，栈中下标都是仍未找到右括号的左侧括号，标记位置都是已经证明无法保留的字符 | 第二遍跳过所有标记位置，拼接出的字符串就是最小删除结果 |

## 最小演算

官方首例输入：`s = "lee(t(c)o)de)"`。

1. 依次匹配括号；最后一个多余右括号出现时栈为空，于是标记它的下标。
2. 继续之前的左括号都已经和更早右括号配对，结束时栈为空。
3. 第二遍保留字母和全部已匹配括号，跳过标记的末尾右括号。
4. 得到 lee(t(c)o)de，删除数量为 1。

## 为什么成立

栈匹配的括号满足最近闭合和前缀平衡要求，因此保留它们不会互相冲突。无法匹配的右括号左侧没有可用左括号，剩余左括号右侧也没有可配右括号，这两类字符在任何有效结果中都不能保留，删除它们既必要又充分。

## 代码映射

```text
建立左括号下标栈和 invalid 数组。
从左到右扫描字符。
遇到 '(' 压入下标。
遇到 ')'：栈空则标记，否则弹出一个左括号。
扫描结束后标记栈中剩余左括号。
再次扫描，拼接所有未标记字符并返回。
```

## 复杂度

- 时间复杂度：O(n)，两次线性扫描。
- 空间复杂度：O(n)，最坏保存全部左括号下标与布尔标记。

## 30 秒识别信号

题目只要任意一个最少删除结果，并允许保留普通字符时，用栈标记无效括号通常比枚举更直接。

## 最小反例与易错点

- 不能在第一次遇到多余右括号时立即从构建结果中删除后就忘记记录位置；统一标记更清晰。
- 剩余左括号必须在扫描结束后再处理，不能在中间提前删除。

## 分层入口

- [[题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/集合/Map-Set.md|Map / Set]]
