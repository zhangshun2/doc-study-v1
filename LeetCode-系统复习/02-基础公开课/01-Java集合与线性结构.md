# Java 集合与线性结构

## 1. 数组与列表

数组是一排固定长度的格子，可以用下标直接拿到某格；读取和写入为 `O(1)`。`ArrayList` 是可扩容的连续列表，按下标读写也是 `O(1)`，中间插入或删除通常要移动后面的元素。

```java
int[] values = {4, 1, 7};
int value = values[1];

List<Integer> list = new ArrayList<>();
list.add(4);                 // 尾部加入
int first = list.get(0);     // 下标读取
list.set(0, 9);              // 覆盖
list.remove(list.size() - 1);// 删除尾项
```

常见区别：`array.length` 是字段，`list.size()` 是方法。`List<Integer>` 保存对象，读取后会自动拆箱成 `int`；不要把 `null` 当作数字参与运算。

## 2. Map 与 Set

当你需要“给一个值，快速找它对应的另一条信息”时，用 `Map`。只需要知道“见没见过”时，用 `Set`。

```java
Map<Integer, Integer> indexByValue = new HashMap<>();
indexByValue.put(8, 2);
Integer index = indexByValue.get(8); // 不存在时是 null

Set<Integer> seen = new HashSet<>();
boolean newlyAdded = seen.add(8);    // 新元素为 true，已有元素为 false
```

哈希容器的主要操作平均 `O(1)`。需要按键顺序时才考虑 `TreeMap` 或 `TreeSet`（操作 `O(log n)`）。遍历 `HashMap` 的顺序没有保证。频数常写成：

```java
count.put(value, count.getOrDefault(value, 0) + 1);
```

## 3. Deque、栈和队列

栈像一摞盘子，只从最近放上的一端处理；队列像排队，先来的先处理。Java 中两者都可以用 `ArrayDeque`，不用旧的 `Stack` 类。

```java
Deque<Integer> stack = new ArrayDeque<>();
stack.push(3);             // 从头部放入
int top = stack.peek();    // 看头部，不删除
int removed = stack.pop();// 删除并返回头部

Deque<Integer> queue = new ArrayDeque<>();
queue.offerLast(3);              // 队尾加入
Integer first = queue.peekFirst();// 查看队首
Integer done = queue.pollFirst(); // 删除队首；空时返回 null
```

队列用 `offerLast` 加、`pollFirst` 出。`ArrayDeque` 两端增删均摊 `O(1)`，不允许放 `null`。需要按一层一层处理树或图时，队列保存“下一批要处理的对象”。
> 这里可以场景记忆。stack 就是打牌的史达克。放牌，看牌，拿牌，都在排队，pushpeekpop。
> queue 就是放牌方式相反的史塔克，最下面赛牌，然后最上面看牌摸牌。offerpeekpop。

## 4. 单调栈和单调队列

单调结构不是另一种 Java 容器，而是使用 `Deque` 时额外维护的顺序规则。

- 单调栈保存尚未得到答案的位置；新位置到来时，先结算被它解决的栈顶，再放入自己。
- 单调队列只保留窗口中仍有机会成为最值的候选下标；过期下标从队首移走，被新下标压过的候选从队尾移走。

先把普通栈/队列接口写熟，再学习这两条维护规则。对应题目见 [[../04-Hot100题单/02-数据结构|数据结构题单]] 中的每日温度、接雨水、滑动窗口最大值。

## 5. 常见 Java 小陷阱

- 空栈调用 `pop()` 会抛异常；循环前先检查 `isEmpty()`。
- `peek()`、`poll()` 可能返回 `null`；拆箱前保证结构非空。
- 修改集合时不要一边用增强 `for` 遍历一边删除。
- `String` 拼接循环容易产生许多临时对象；反复拼接用 `StringBuilder`。
- 用 `long` 保存可能超过 `int` 的累计和或乘积，转换要发生在乘法/加法之前。

## 关联课程

- [[02-PriorityQueue与排序比较器|堆和排序比较器]]
- [[03-位运算白话课|位运算白话课]]
- [[../03-标签公开课/Hot100标签白话指南|Hot100 标签白话指南]]
