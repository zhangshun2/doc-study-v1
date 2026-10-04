---
schemaVersion: 3
type: "java-api"
titleCn: "PriorityQueue 与 Comparator"
topics: ["Java API","堆","排序","比较器"]
sourceUrl: "https://docs.oracle.com/javase/8/docs/api/java/util/PriorityQueue.html"
sourceCheckedAt: "2026-09-12"
priority: "P2"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
relatedProblems: [23,56,215,347]
---

# PriorityQueue / Comparator

## 典型场景

| 需求 | 构造方向 |
| --- | --- |
| 每次取最小值 | `new PriorityQueue<>()` |
| 每次取最大值 | 使用反向比较器 |
| 维护最大的 K 个数 | 大小为 K 的小顶堆 |
| 维护最小的 K 个数 | 大小为 K 的大顶堆 |
| 合并多个有序序列 | 堆中保存当前最小头节点或下标 |

Java 的 `PriorityQueue` 默认是小顶堆，`peek` 和 `poll` 都面向当前最小元素。

## 构造方式

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
PriorityQueue<int[]> byDistance =
        new PriorityQueue<>(Comparator.comparingInt(cell -> cell[0]));
```

泛型类型不能是基本类型。需要同时保存值、来源或下标时，使用 `int[]`、自定义对象或封装后的 `Map.Entry`。

## 常用操作

| 操作 | 写法 | 返回或副作用 |
| --- | --- | --- |
| 加入 | `offer(value)` | 成功返回 `true` |
| 查看队首 | `peek()` | 空堆返回 `null` |
| 删除队首 | `poll()` | 空堆返回 `null`，否则返回最小值或比较器定义的队首 |
| 大小 | `size()` | 当前元素数 |
| 是否为空 | `isEmpty()` | 不删除元素 |

`add` 与 `offer` 都可加入，但容量无限制时通常使用 `offer`。`remove()` 无参版本与 `poll()` 都删除队首，区别是空堆时前者抛异常。

## 返回值语义

- `peek()` 返回堆顶但不删除；为空时返回 `null`。
- `poll()` 返回并删除堆顶；为空时返回 `null`。
- `size()` 表示当前候选数量，不表示已经删除的历史元素数。
- 堆只保证队首是最值，不保证整个迭代顺序恰好有序。

## 空值与装箱

`PriorityQueue` 不允许插入 `null`。`PriorityQueue<Integer>` 中元素会围绕 `Integer` 自动装箱和拆箱。若堆顶取出后要与 `int` 运算，先确认堆非空或返回值非 `null`。

## Comparator 规则

比较器 `compare(a,b)` 必须满足：

- 返回负数表示 `a` 排在 `b` 前。
- 返回 0 表示两者在此排序关系中相等。
- 返回正数表示 `a` 排在 `b` 后。
- 必须保持自反、反对称和传递；不要写成可能溢出的 `a - b`，优先使用 `Integer.compare(a,b)`。

`PriorityQueue` 是稳定性的例外：它不保证相等元素按插入顺序取出。若相等元素的先后会影响正确性，需要在比较器中继续比较一个唯一顺序字段，例如下标或节点编号。

## 迭代修改陷阱

不要在 `for (int value : heap)` 遍历时修改堆。需要按优先级逐个处理时，用 `while (!heap.isEmpty()) { ... heap.poll(); }`。直接调用 `remove(Object)` 删除任意元素是 `O(n)`，也不能依靠它维护复杂状态。

## 复杂度

- `offer` 和 `poll` 为 `O(log n)`。
- `peek` 为 `O(1)`。
- 线性建堆为 `O(n)`，逐个插入为 `O(n log n)`。
- 任意查找或删除对象为 `O(n)`。
- 空间复杂度为 `O(n)`。

## 关联题目

- [[题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md|215. 数组中的第 K 个最大元素]]：小顶堆维护前 K 大。
- [[题目/堆与选择/347-Top-K-Frequent-Elements.md|347. 前 K 个高频元素]]：频次映射加小顶堆。
- [[题目/堆与选择/23-Merge-k-Sorted-Lists.md|23. 合并 K 个升序链表]]：堆保存每个链表当前头节点。
- [[题目/排序/56-Merge-Intervals.md|56. 合并区间]]：排序和比较器的实际使用。

## 官方文档

- [PriorityQueue](https://docs.oracle.com/javase/8/docs/api/java/util/PriorityQueue.html)
- [Comparator](https://docs.oracle.com/javase/8/docs/api/java/util/Comparator.html)
