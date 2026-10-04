---
schemaVersion: 3
type: "problem"
leetcodeId: 232
slug: "implement-queue-using-stacks"
titleCn: "用栈实现队列"
titleEn: "Implement Queue using Stacks"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/implement-queue-using-stacks/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "843cff336a2f4a45fc239ceaf825dfd71db8ba8f29144abd1109bc27605fc7ca"
sourceFactsSha256: "806dd77538bf6b24b92df84d5a78797b0f3b41c22e53600e42cf05bf195a440b"
sourceSectionHashes:
  description: "4a35deb79cfd3fab9d0177ef4702ffc505d5b81d9fe1aa69afbe4b6d71e1c0ba"
  examples: "096f7def5f56eb3c3aea9a155836583b7f64c8df9135d5431b52483619e745b6"
  constraints: "41ec6f2da1e107366a77cbc1f46fadaad5498cd69af665bc9b3fa0374105bd30"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "066888ad208ad7ada192d7f0b775abb223584cda01a42f1f051c21a00bafe083"
  signature: "a2e43ab22eeb442d0dba8242b97837e8df331235b1384bfd4db665df671ee775"
  javaTemplate: "3d14852d085f0cf445d9cc36b7ff6adf403f7784f167a9cd2ff8f5524c1c4f98"
primaryPattern: "设计"
topics: ["设计","栈","队列"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Stack 栈","Design 设计题","Queue 队列"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 232. 用栈实现队列 / Implement Queue using Stacks

> **双轨入口：** [[核心模型/设计/232-Implement-Queue-using-Stacks-核心模型.md|核心模型]]

## 题目信息

- 官方难度：`Easy`
- 主归档题型：`设计`
- 清单优先级：`P1`
- 清单代表标签：`Stack 栈`、`Design 设计题`、`Queue 队列`
- LeetCode 当前标签：栈 (Stack)、设计 (Design)、队列 (Queue)
- 官方来源：<https://leetcode.cn/problems/implement-queue-using-stacks/>
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`843cff336a2f4a45fc239ceaf825dfd71db8ba8f29144abd1109bc27605fc7ca`
- **主解法**：输入栈与输出栈

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（`push`、`pop`、`peek`、`empty`）：

实现 `MyQueue` 类：

- `void push(int x)` 将元素 x 推到队列的末尾

- `int pop()` 从队列的开头移除并返回元素

- `int peek()` 返回队列开头的元素

- `boolean empty()` 如果队列为空，返回 `true` ；否则，返回 `false`

**说明：**

- 你 **只能** 使用标准的栈操作 —— 也就是只有 `push to top`, `peek/pop from top`, `size`, 和 `is empty` 操作是合法的。

- 你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。

## 官方示例

**示例 1：**

```text
输入：
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 1, 1, false]

解释：
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

## 官方约束

- `1 <= x <= 9`

- 最多调用 `100` 次 `push`、`pop`、`peek` 和 `empty`

- 假设所有操作都是有效的 （例如，一个空的队列不会调用 `pop` 或者 `peek` 操作）

**进阶：**

- 你能否实现每个操作均摊时间复杂度为 `O(1)` 的队列？换句话说，执行 `n` 个操作的总时间复杂度为 `O(n)` ，即使其中一个操作可能花费较长时间。

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 入队顺序与出队顺序相反；若让元素整体反转一次，最早元素就会来到栈顶。
2. 输出栈不为空时不能把输入栈的新元素搬进去，否则会插到旧元素前面。
3. 每个元素一生只从输入栈搬到输出栈一次，因此总时间仍为线性。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：push、empty 为 O(1)；pop、peek 单次最坏 O(n)，但每个元素最多转移一次，n 次操作总时间为 O(n)，均摊 O(1)。
- 空间复杂度目标：O(n)，两个栈共同保存全部队列元素。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

一个栈把元素反转一次就会变成相反顺序。输入栈保存新到达元素，输出栈保存已经反转、可直接作为队头的元素。

## 朴素方案

每次 push 都把新元素放到栈底可以维持队列顺序，但需要反复倒栈，单个操作最坏 O(n)。每次都找最底部元素也会重复搬运已有数据。

## 最优方案：延迟转移的双栈结构

push 只把新元素压入 inStack。pop 或 peek 前检查 outStack：只有 outStack 为空时，才把 inStack 的全部元素逐个弹出并压入 outStack。这次整体反转后，最早进入 inStack 的元素位于 outStack 栈顶，随后 pop、peek 都直接操作 outStack。

### 正确性与不变量

当 outStack 非空时，其栈顶正是尚未出队元素中最早进入者；新 push 的元素在输入栈中，不可能比已转移元素更早出队。当 outStack 为空时，一次完整转移把 inStack 的入栈顺序反转，使最早元素到达栈顶，同时保持其余元素的先后关系。因此每次 pop 和 peek 都符合队列语义，empty 只需检查两个栈。

## 复杂度

- **时间复杂度**：push、empty 为 O(1)；pop、peek 单次最坏 O(n)，但每个元素最多转移一次，n 次操作总时间为 O(n)，均摊 O(1)。
- **空间复杂度**：O(n)，两个栈共同保存全部队列元素。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MyQueue {
    private final Deque<Integer> inStack = new ArrayDeque<>();
    private final Deque<Integer> outStack = new ArrayDeque<>();

    public MyQueue() {
    }

    public void push(int x) {
        inStack.push(x);
    }

    public int pop() {
        moveIfNeeded();
        return outStack.pop();
    }

    public int peek() {
        moveIfNeeded();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    private void moveIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MyQueue {
    private final Deque<Integer> inStack = new ArrayDeque<>();
    private final Deque<Integer> outStack = new ArrayDeque<>();

    public MyQueue() {
    }

    public void push(int x) {
        inStack.push(x);
    }

    public int pop() {
        moveIfNeeded();
        return outStack.pop();
    }

    public int peek() {
        moveIfNeeded();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    private void moveIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        MyQueue queue = new MyQueue();
        queue.push(1);
        queue.push(2);
        System.out.println(queue.peek());
        System.out.println(queue.pop());
        System.out.println(queue.empty());
        queue.push(3);
        System.out.println(queue.pop());
        System.out.println(queue.empty());
    }
}
```

## 边界与易错点

- 必须延迟转移：outStack 非空时转移会破坏旧元素的出队顺序。
- empty 要同时检查两个栈，不能只看某一个栈。
- 题目保证空队列不会调用 pop 或 peek，但实现仍应尊重队列契约。

## 可扩展变式

- 可用 LinkedList 实现同一逻辑，但 ArrayDeque 更轻量。
- 用栈模拟队列的逆问题是队列模拟栈，可用一个队列旋转完成。
