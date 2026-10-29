# PriorityQueue 与排序比较器

## 1. 堆解决什么问题

如果一堆候选会不断加入，而每次只需要最快拿到当前最大或最小的一个，没必要每次把所有候选重新排序。优先队列让队首始终是当前优先级最高的候选。

Java `PriorityQueue` 默认是小顶堆：`peek()` 查看最小项，`poll()` 删除并返回最小项。堆内其他元素不保证整体有序。

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(8);
minHeap.offer(3);
minHeap.peek(); // 3
minHeap.poll(); // 删除并返回 3

PriorityQueue<Integer> maxHeap =
        new PriorityQueue<>((a, b) -> Integer.compare(b, a));
```

加入和取出均为 `O(log n)`，查看队首为 `O(1)`。要维护最大的 K 个数，通常保留容量 K 的小顶堆：新数加入后若大小超过 K，就移走最小者。

## 2. 比较器怎么读

`compare(a, b)` 的结果小于 0，表示 `a` 排在 `b` 前；等于 0 表示排序规则认为二者并列；大于 0 表示 `a` 排在 `b` 后。

```java
int[][] intervals = {{4, 7}, {1, 3}, {2, 5}};
Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
```

这里比较的是每个区间的起点，起点小的在前。避免写 `a[0] - b[0]`，因为减法可能溢出。多字段排序可以继续比较第二字段：

```java
Arrays.sort(intervals, (a, b) -> {
    int byStart = Integer.compare(a[0], b[0]);
    if (byStart != 0) return byStart;
    return Integer.compare(a[1], b[1]);
});
```

## 3. 排序什么时候值得先做

排序花费 `O(n log n)`，但会让后续关系更容易看见：相邻重复值放在一起、区间按起点排列、双指针有明确的移动方向。先说明排序后数据多了什么性质，再决定是否排序；排序本身不会自动证明后续选择正确。

Java 常用：

```java
Arrays.sort(intArray);               // 原地升序
Collections.sort(list);              // List 升序
list.sort(Comparator.reverseOrder());// 对象列表降序
```

基本类型数组可直接使用 `Arrays.sort`。对象数组和列表能传比较器。

## 4. 小顶堆与大顶堆的方向

不要只背“第 K 大用小顶堆”。要说出堆里留的是什么：如果堆里最多留 K 个目前最大的候选，那么最小的那个正是下一次可能被挤走的边界，所以堆顶必须是小值。

若堆里保存多个有序链表当前节点，堆顶则应是全体当前节点中最小的那个，因为它是下一项全局输出。

## 关联课程

- [[../04-Hot100题单/01-排序|排序与区间题单]]
- [[../04-Hot100题单/02-数据结构|数据结构题单]]
