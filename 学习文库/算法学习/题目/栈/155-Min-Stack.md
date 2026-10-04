---
schemaVersion: 3
type: "problem"
leetcodeId: 155
slug: "min-stack"
titleCn: "最小栈"
titleEn: "Min Stack"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/min-stack/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "4e78464937a222853112ce95b59e23df64401e0cc84efc83da86b13894543a94"
sourceFactsSha256: "77ddb740d257d6d8ced461d34848f581945a2d805ea84e15f78f58f6fa1a9c68"
sourceSectionHashes:
  description: "4231866f58ff251709a9b6cc9e089ad24d662f17d8ae64ccd7a9b0a84d6bf192"
  examples: "3337fe1a27a16c93498b8546c84ea79a1dbe3360ba509772916154456e1897a9"
  constraints: "6194a1ec4a07fb7788189a2ffc643fc9b8f171b8f24dfe5707e8ce492a85fd37"
  hints: "04ce67319c1305f1fc2e536b53f1c43e34d133510acecdba339b95078fdf442b"
  tags: "ebc33298de8a00abb0eced0f8aae7b1e4d352703615e73a3fbc457a0de2b41fc"
  signature: "a9c3adf895223f0c4802c94adc4b0db59e894ed9897b3c81a01fdf652db887a4"
  javaTemplate: "61305362ec407927415e813ba47118042414ce791041d31894fefbabf9f54aa8"
primaryPattern: "栈"
topics: ["栈","设计"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Stack 栈","Design 设计题"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 155. 最小栈 / Min Stack

> **双轨入口：** [[核心模型/栈/155-Min-Stack-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`栈`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Stack 栈`、`Design 设计题`
- LeetCode 当前标签：栈 (Stack)、设计 (Design)
- 官方来源：<https://leetcode.cn/problems/min-stack/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`4e78464937a222853112ce95b59e23df64401e0cc84efc83da86b13894543a94`
- **主解法**：同步辅助栈

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

设计一个支持 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类:

- `MinStack()` 初始化堆栈对象。

- `void push(int value)` 将元素 `value` 推入堆栈。

- `void pop()` 删除堆栈顶部的元素。

- `int top()` 获取堆栈顶部的元素。

- `int getMin()` 获取堆栈中的最小元素。

## 官方示例


**示例 1:**

```text
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.getMin();   --> 返回 -2.
```

## 官方约束


- `-2^31 <= val <= 2^31 - 1`

- `pop`、`top` 和 `getMin` 操作总是在 **非空栈** 上调用

- `push`, `pop`, `top`, and `getMin`最多被调用 `3 * 10^4` 次

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Consider each node in the stack having a minimum value. (Credits to @aakarshmadhavan)

## 学习提示（非官方）

1. 当前最小值被弹出后，需要立刻知道“此前的最小值”。
2. 对每一层数据，都同步保存压入该层之后的最小值。
3. 遇到与当前最小值相等的值也必须记录，否则重复最小值会出错。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：["MinStack", "push", "push", "push", "getMin", "pop", "getMin"]
参数：[[], [2], [1], [1], [], [], []]
输出：[null, null, null, null, 1, null, 1]
解释：弹出一个最小值 1 后，栈中仍有另一个 1。
```

## 核心观察

普通栈只能访问栈顶，扫描求最小值为 `O(n)`。关键是把每个历史时刻的最小值随栈状态一同保存。数据栈第 `i` 层存实际值，最小栈第 `i` 层存前 `i` 层的最小值，两个栈严格同步。

## 朴素方案

仅使用一个栈，`getMin()` 时遍历全部元素，时间为 `O(n)`。或者维护单个 `min` 变量，但最小元素弹出后无法恢复上一个最小值，除非再次扫描。

## 最优方案推导

压入 `val` 时，同时向最小栈压入：

```text
min(val, 之前的最小值)
```

弹出时两个栈一起弹。于是最小栈栈顶永远对应当前数据栈的最小值。也可只在 `val <= currentMin` 时记录最小值，但同步栈写法更不易出错。

## 正确性与不变量

不变量：两个栈大小相等，且 `minimums[i]` 是 `values[0..i]` 的最小值。

初始时两个栈为空。不变量对压栈成立，因为新最小值正是 `min(旧最小值, val)`；同步弹栈后，新的栈顶恢复上一层保存的最小值。因此任意时刻 `getMin()` 返回值都正确。

## 复杂度

- **时间复杂度**：构造、`push`、`pop`、`top`、`getMin` 均为 `O(1)`。
- **空间复杂度**：`O(n)`，两个栈各保存至多 `n` 个整数。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MinStack {
    private final Deque<Integer> values = new ArrayDeque<>();
    private final Deque<Integer> minimums = new ArrayDeque<>();

    public MinStack() {
    }

    public void push(int val) {
        values.push(val);
        if (minimums.isEmpty()) {
            minimums.push(val);
        } else {
            minimums.push(Math.min(val, minimums.peek()));
        }
    }

    public void pop() {
        values.pop();
        minimums.pop();
    }

    public int top() {
        return values.peek();
    }

    public int getMin() {
        return minimums.peek();
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Deque;

class MinStack {
    private final Deque<Integer> values = new ArrayDeque<>();
    private final Deque<Integer> minimums = new ArrayDeque<>();

    public MinStack() {
    }

    public void push(int val) {
        values.push(val);
        if (minimums.isEmpty()) {
            minimums.push(val);
        } else {
            minimums.push(Math.min(val, minimums.peek()));
        }
    }

    public void pop() {
        values.pop();
        minimums.pop();
    }

    public int top() {
        return values.peek();
    }

    public int getMin() {
        return minimums.peek();
    }
}

public class Main {
    public static void main(String[] args) {
        MinStack stack = new MinStack();
        stack.push(-2);
        stack.push(0);
        stack.push(-3);
        System.out.println(stack.getMin()); // -3
        stack.pop();
        System.out.println(stack.top());    // 0
        System.out.println(stack.getMin()); // -2
    }
}
```

## 边界与易错点

- 重复最小值必须正确处理；同步保存每层最小值天然解决此问题。
- `ArrayDeque` 不允许 `null`，本题只存整数，不受影响。
- 题目保证查询时非空；工程实现可自行增加 `NoSuchElementException` 或 Optional 语义。
- 不要用 `Stack<Integer>` 作为新代码首选，`ArrayDeque` 通常更轻量。

## 可扩展变式

- 最大栈：同步维护前缀最大值。
- 同时查询最小和最大：增加一个最大辅助栈。
- 节省常数空间：用一个栈保存 `val - min` 的差值，但必须用 `long` 防止整数溢出。
- 持久化最小栈：每次操作生成不可变节点，天然保存历史版本。
