---
schemaVersion: 3
type: "java-api"
titleCn: "Deque 与 Stack"
topics: ["Java API","栈","队列","双端队列"]
sourceUrl: "https://docs.oracle.com/javase/8/docs/api/java/util/Deque.html"
sourceCheckedAt: "2026-09-12"
priority: "P2"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
relatedProblems: [20,32,102,127,150,155,200,207,224,232,239,394,1249]
---

# Deque / Stack

## 典型场景

| 需求 | 推荐写法 |
| --- | --- |
| 后进先出，最近对象先处理 | `Deque<T> stack = new ArrayDeque<>();` |
| 先进先出，按发现顺序处理 | `Queue<T> queue = new ArrayDeque<>();` |
| 两端都能加入或删除 | 直接使用 `Deque<T>` |
| 滑动窗口维护单调候选 | 用 `Deque<Integer>` 保存下标 |

算法代码优先使用 `ArrayDeque`，不要使用同步的 `java.util.Stack`。需要 `null` 元素时不能用 `ArrayDeque`，因为它不允许 `null`。

## 构造方式

```java
Deque<Integer> stack = new ArrayDeque<>();
Queue<int[]> queue = new ArrayDeque<>();
Deque<Integer> window = new ArrayDeque<>();
```

`Deque` 是接口，`ArrayDeque` 是实现。方法参数或局部变量按所需能力声明为 `Deque` 或 `Queue`。

## 常用操作

| 目的 | 队列方法 | 栈方法 | 空结构时 |
| --- | --- | --- | --- |
| 加入 | `offerLast(x)` | `push(x)` | 返回 `false` 或抛异常 |
| 查看头部 | `peekFirst()` | `peek()` | 返回 `null` |
| 查看尾部 | `peekLast()` | 不常用 | 返回 `null` |
| 删除头部 | `pollFirst()` | `pop()` | `poll` 返回 `null`，`pop` 抛异常 |
| 删除尾部 | `pollLast()` | 不常用 | 返回 `null` |

推荐成对使用 `offerLast` / `pollFirst` 表示队列，使用 `offerFirst` / `pollFirst` 表示栈。`add`、`remove`、`element` 在空结构或容量受限时抛异常；`offer`、`poll`、`peek` 更适合算法控制流。

## 返回值语义

- `pollFirst()` 返回被删除元素；为空时返回 `null`。
- `peekFirst()` 不删除元素；为空时返回 `null`。
- `pop()` 等同 `removeFirst()`，为空时抛 `NoSuchElementException`。
- `push()` 等同 `addFirst()`，加入头端。
- 在 `ArrayDeque` 中，头端是下一次 `pollFirst` 或 `pop` 所在的一端。

## 空值与装箱

`ArrayDeque` 不允许 `null`。`Deque<Integer>` 保存的是 `Integer`，自动装箱后的 `null` 仍不能加入。若问题中 `0` 是合法值，应使用返回 `null` 的 `poll` 后再拆箱，或先用 `isEmpty` 判断，不能用“取到 0”表示空。

## 迭代修改陷阱

不要在增强 `for` 遍历双端队列时从两端删除元素。算法需要检查前沿并修改结构时，应显式写 `while (!deque.isEmpty())`，在循环体内调用 `poll`、`push` 或 `offer`。使用迭代器时只能通过 `iterator.remove()` 删除当前元素。

## 复杂度

- `ArrayDeque` 的两端插入和删除均摊 `O(1)`。
- `peek` 为 `O(1)`。
- 查找任意元素为 `O(n)`。
- 空间复杂度为 `O(n)`。

## 关联题目

- [[题目/栈/20-Valid-Parentheses.md|20. 有效的括号]]：最近未匹配左括号。
- [[题目/栈/32-Longest-Valid-Parentheses.md|32. 最长有效括号]]：未匹配下标栈同时提供配对与区间边界。
- [[题目/栈/150-Evaluate-Reverse-Polish-Notation.md|150. 逆波兰表达式求值]]：操作数栈按后缀顺序合并子表达式。
- [[题目/图与搜索/200-Number-of-Islands.md|200. 岛屿数量]]：DFS 显式栈。
- [[题目/图与搜索/207-Course-Schedule.md|207. 课程表]]：拓扑排序队列。
- [[题目/栈/224-Basic-Calculator.md|224. 基本计算器]]：栈保存括号外层的计算结果与符号现场。
- [[题目/设计/232-Implement-Queue-using-Stacks.md|232. 用栈实现队列]]：输入栈与输出栈通过延迟转移实现先进先出。
- [[题目/单调结构/239-Sliding-Window-Maximum.md|239. 滑动窗口最大值]]：双端单调队列。
- [[题目/栈/394-Decode-String.md|394. 字符串解码]]：嵌套现场入栈与结算。
- [[题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md|1249. 移除无效的括号]]：下标栈找出无法配对的括号位置。

## 官方文档

- [Deque](https://docs.oracle.com/javase/8/docs/api/java/util/Deque.html)
- [ArrayDeque](https://docs.oracle.com/javase/8/docs/api/java/util/ArrayDeque.html)
- [Queue](https://docs.oracle.com/javase/8/docs/api/java/util/Queue.html)
