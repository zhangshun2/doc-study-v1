---
schemaVersion: 3
type: "core-model"
leetcodeId: 301
slug: "remove-invalid-parentheses"
titleCn: "删除无效的括号"
titleEn: "Remove Invalid Parentheses"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/remove-invalid-parentheses/"
sourceCheckedAt: "2026-10-04"
sourceFactsSha256: "e0f38664dac0301af3ef63935562e088a2bbe22ab1020c49e053fd40bd3e9679"
primaryPattern: "回溯"
topics: ["回溯","广度优先搜索","字符串"]
priority: "P0"
problemPath: "题目/回溯/301-Remove-Invalid-Parentheses.md"
deepDivePath: "建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 301. 删除无效的括号：核心模型

> **双轨阅读：** [[题目/回溯/301-Remove-Invalid-Parentheses.md|标准题解]] · [[建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md|完整建模]]

## 一句话本质

每个字符串都是删除图上的节点，删除一个括号是一层边；第一次到达合法节点的那一层就是最少删除方案。

## 直观画面与扩题

像从一个词开始每次改掉一个字母，第一次走到目标词的最短路径；这里每次只删一个括号，合法字符串就是目标。

题目要求所有最优答案，因此不能只保留一条搜索路径。BFS 的价值不是遍历得快，而是层号直接表示已删除数量，让我们知道何时必须停止。去重则保证不同删除顺序得到的同一字符串只被解释一次。

## 关系重写

字符串 A 删除一个括号得到 B 时，A 与 B 之间存在一条搜索边；初始字符串到合法节点的最短路径长度就是最少删除数。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 括号字符串、删一个括号后的邻接状态、删除层数、合法判定 | 字符串 A 删除一个括号得到 B 时，A 与 B 之间存在一条搜索边；初始字符串到合法节点的最短路径长度就是最少删除数。 | 队列保存某一删除层的字符串，visited 保存所有已发现字符串 | 逐层取出字符串，合法的加入答案，不合法的删除一个括号并生成未访问的下一层候选 | 处理到第 d 层前，visited 中的合法结果若尚未出现，说明少于 d 次删除不可能得到有效字符串 | 第一次出现有效字符串的整层结果全部加入答案后立即停止 |

## 最小演算

官方首例输入：`s = "()())()"`。

1. 第 0 层只有 ()())()，检查后无效，继续删除一个括号。
2. 第 1 层候选包括删掉不同右括号得到的结果，但没有合法字符串。
3. 第 2 层生成 (())() 与 ()()() 等候选，检查发现它们都合法。
4. 整层合法结果加入答案；不再扩展到第 3 层，因为它们已是最少删除。

## 为什么成立

BFS 的层号等于从原字符串到当前字符串的最少删除次数。若第 d 层首次出现合法字符串，则所有更少删除的字符串都已检查失败，而同一层每个合法结果都恰好删除了 d 个括号，所以得到全部最优解。

## 代码映射

```text
queue 放入原串，visited 记录原串。
while queue 非空且尚未找到合法层:
    记录本层长度。
    处理本层每个字符串。
    若合法，加入答案并标记 found。
    若本层未 found，删除一个括号生成下一层。
返回答案。
```

## 复杂度

- 时间复杂度：最坏为 O(n * 2^n)，其中 n 为括号数量，因为每个字符串要生成 O(n) 个删除候选并做 O(n) 有效性检查。
- 空间复杂度：O(2^n * n)，visited 和队列最坏保存指数数量的字符串。

## 30 秒识别信号

题目要求最少次数操作后的所有结果，且一次操作可以自然生成相邻状态时，考虑按层 BFS。

## 最小反例与易错点

- 不能发现首个合法字符串就立刻返回，它会漏掉同层其他答案。
- 不能等出队时才去重，否则重复状态会先占满队列。

## 分层入口

- [[题目/回溯/301-Remove-Invalid-Parentheses.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]]
