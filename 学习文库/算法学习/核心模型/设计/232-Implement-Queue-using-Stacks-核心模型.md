---
schemaVersion: 3
type: "core-model"
leetcodeId: 232
slug: "implement-queue-using-stacks"
titleCn: "用栈实现队列"
titleEn: "Implement Queue using Stacks"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/implement-queue-using-stacks/"
sourceCheckedAt: "2026-10-04"
sourceFactsSha256: "806dd77538bf6b24b92df84d5a78797b0f3b41c22e53600e42cf05bf195a440b"
primaryPattern: "设计"
topics: ["设计","栈","队列"]
priority: "P1"
problemPath: "题目/设计/232-Implement-Queue-using-Stacks.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 232. 用栈实现队列：核心模型

> **双轨阅读：** [[题目/设计/232-Implement-Queue-using-Stacks.md|标准题解]]

## 一句话本质

把元素从输入栈整体倒进输出栈会反转一次顺序，原本最早进入的元素因此来到栈顶，可以按队列头弹出。

## 直观画面与扩题

像把一摞盘子整体搬到另一张桌上：搬运会倒序，原来最底下的盘子搬到新桌后反而在最上面。

本题不是寻找一个新的容器，而是组合已有操作。难点在于控制转移时机：如果每来一个新元素就搬运，新元素可能跑到尚未出队的旧元素前面。因此输出栈必须一次搬空，之后持续消费，直到再次为空。

## 关系重写

输入栈按到达顺序反向保存新元素；一次完整转移后，输出栈栈顶与队列头元素一一对应。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 队列元素、输入栈、输出栈、当前队头 | 输入栈按到达顺序反向保存新元素；一次完整转移后，输出栈栈顶与队列头元素一一对应。 | inStack 承接 push，outStack 提供 pop/peek，二者和为零表示空队列 | push 只进入输入栈；读取或删除前若输出栈为空，就完整倒栈一次，再操作输出栈顶 | 两个栈拼起来时，outStack 中尚未弹出的元素总是早于 inStack 中全部元素；outStack 栈顶是队头 | pop 返回并删除队头，peek 只读取队头，empty 报告两栈是否都空 |

## 最小演算

官方首例输入：`push(1), push(2), peek(), pop(), empty()`。

1. 两次 push 后 inStack 从底到顶为 [1,2]，outStack 为空。
2. peek 触发倒栈，1、2 依次弹出并压入 outStack，栈顶变成 1。
3. peek 返回 1；pop 删除 1，outStack 剩余栈顶 2。
4. 此时两个栈不全为空，empty 返回 false。

## 为什么成立

一次完整转移相当于反转一段序列，恰好把先进先出关系映射成后进先出关系。只要输出栈不空就优先服务旧元素，新 push 不会越过它们。每个元素最多搬运一次，频繁倒栈的担忧也因此消失。

## 代码映射

```text
建立 inStack 与 outStack。
push(x): 把 x 压入 inStack。
prepare(): 若 outStack 为空，循环弹出 inStack 并压入 outStack。
pop(): prepare 后弹出 outStack 栈顶。
peek(): prepare 后读取 outStack 栈顶。
empty(): 返回两个栈是否都为空。
```

## 复杂度

- 时间复杂度：push、empty 为 O(1)；pop、peek 单次最坏 O(n)，但每个元素最多转移一次，n 次操作总时间为 O(n)，均摊 O(1)。
- 空间复杂度：O(n)，两个栈共同保存全部队列元素。

## 30 秒识别信号

要求用后进先出的操作实现先进先出，并且允许把搬移成本摊到多次操作上时，考虑双栈反转。

## 最小反例与易错点

- outStack 非空时继续搬运会让新元素压住旧元素。
- pop 和 peek 都要共享同一套 prepare 逻辑，否则状态容易不一致。

## 分层入口

- [[题目/设计/232-Implement-Queue-using-Stacks.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]
