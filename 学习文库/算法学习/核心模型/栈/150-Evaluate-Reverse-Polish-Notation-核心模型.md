---
schemaVersion: 3
type: "core-model"
leetcodeId: 150
slug: "evaluate-reverse-polish-notation"
titleCn: "逆波兰表达式求值"
titleEn: "Evaluate Reverse Polish Notation"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/evaluate-reverse-polish-notation/"
sourceCheckedAt: "2026-10-04"
sourceFactsSha256: "6debbec6bbb1423b395a4327b01cbf1625a9615a74eddb96de1d5895a89b037a"
primaryPattern: "栈"
topics: ["栈","数组","数学"]
priority: "P0"
problemPath: "题目/栈/150-Evaluate-Reverse-Polish-Notation.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 150. 逆波兰表达式求值：核心模型

> **双轨阅读：** [[题目/栈/150-Evaluate-Reverse-Polish-Notation.md|标准题解]]

## 一句话本质

每个运算符都负责合并栈顶两个已经求值的子表达式；压回结果后，这段表达式对上层而言又变成一个数字。

## 直观画面与扩题

像把散落的积木两两拼成新积木：运算符到来时，只取最近两块已经拼好的结果，合成后再放回桌面。

后缀表达式把人类习惯的括号和优先级改写成了顺序。因此不需要比较运算符优先级，也不需要保存操作符栈；问题只剩“最近两个完整结果在哪里”。这个访问模式正是后进先出，而真正容易错的是左右操作数顺序。

## 关系重写

每个运算符的左操作数是第二近的完整结果，右操作数是最新一轮计算后留在栈顶的完整结果。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| token、已求值的子表达式、待合并的中间结果 | 每个运算符的左操作数是第二近的完整结果，右操作数是最新一轮计算后留在栈顶的完整结果。 | Deque<Integer> values，保存尚未被上层运算符合并的表达式值 | 数字 token 解析后入栈；运算符 token 弹出右值和左值，计算后压回一个新的表达式值 | 扫描到任意前缀后，栈中每个值都对应一个已经完整求值、但尚未被后续运算符合并的子表达式 | 全部 token 处理完后，栈中唯一的整数就是表达式值 |

## 最小演算

官方首例输入：`tokens = ["4","13","5","/","+"]`。

1. 依次压入 4、13、5，栈顶是最近的完整子表达式 5。
2. 遇到 /，弹出右操作数 5，再弹出左操作数 13，计算 13/5 得到 2 并压回。
3. 栈变成 [4, 2]；遇到 +，弹出右操作数 2 和左操作数 4。
4. 计算 4+2 得到 6；扫描结束，栈顶 6 就是答案。

## 为什么成立

后缀表示法保证运算符出现时，它需要的两个子表达式都已经计算完毕。栈顶顺序与表达式的右、左子树顺序一致，所以连续弹出两次不会漏掉任何待处理子树，也不会提前合并外层运算。

## 代码映射

```text
建立空的整数栈。
从左到右读取 token。
若 token 是数字，解析后压栈。
否则弹出 right，再弹出 left。
按 token 计算并压回结果。
所有 token 处理完后返回栈顶。
```

## 复杂度

- 时间复杂度：O(n)，每个 token 只读取和计算一次。
- 空间复杂度：O(n)，栈中最多保存线性数量的中间表达式值。

## 30 秒识别信号

输入已经按无括号、无歧义的运算顺序排列，且每个操作符只依赖最近两个完整结果时，考虑操作数栈。

## 最小反例与易错点

- 先弹出的是右侧操作数，减法和除法不能反过来。
- 负号只属于数字 token，不属于运算符；解析顺序要覆盖多位数和负数。

## 分层入口

- [[题目/栈/150-Evaluate-Reverse-Polish-Notation.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]
