---
schemaVersion: 3
type: "java-api"
titleCn: "Map 与 Set"
topics: ["Java API","哈希表","集合"]
sourceUrl: "https://docs.oracle.com/javase/8/docs/api/java/util/Map.html"
sourceCheckedAt: "2026-09-12"
priority: "P2"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
relatedProblems: [1,3,49,128,146,169,207,239,301,347,560]
---

# Map / Set

## 典型场景

| 需求 | 推荐结构 | 原因 |
| --- | --- | --- |
| 值到下标、值到次数、前缀和到次数 | `HashMap<K,V>` | 按键快速建立映射 |
| 只判断是否出现、是否访问过 | `HashSet<E>` | 只保存键，不关心重复次数 |
| 需要按键排序后遍历 | `TreeMap<K,V>` | 迭代顺序按键比较器确定 |
| 需要去重后按顺序遍历 | `TreeSet<E>` | 元素按比较规则保持有序 |

算法题默认先考虑 `HashMap` 和 `HashSet`。只有题目明确依赖键的排序、范围查询或第一个大于某键的元素时，才改用树结构。

## 构造方式

```java
Map<String, Integer> countByWord = new HashMap<>();
Set<Integer> visited = new HashSet<>();
Map<Integer, List<Integer>> graph = new HashMap<>();
```

需要确定性遍历顺序时使用 `LinkedHashMap`，需要按键排序时使用 `TreeMap`。算法题一般不依赖 `HashMap` 的遍历顺序。

## 常用操作

| 操作 | 写法 | 返回语义 |
| --- | --- | --- |
| 读取 | `map.get(key)` | 不存在时返回 `null` |
| 安全读取 | `map.getOrDefault(key, 0)` | 不存在时返回提供的默认值 |
| 写入或覆盖 | `map.put(key, value)` | 返回该键原来的值，没有则返回 `null` |
| 没有才写入 | `map.putIfAbsent(key, value)` | 原有值存在时不覆盖 |
| 删除 | `map.remove(key)` | 返回被删除的值，没有则返回 `null` |
| 是否含键 | `map.containsKey(key)` | 只检查键，不读取值 |
| 遍历键值 | `for (Map.Entry<K,V> e : map.entrySet())` | 每个条目读取一次 |
| 集合添加 | `set.add(value)` | 新元素返回 `true`，已存在返回 `false` |

频次统计可写：

```java
countByWord.put(word, countByWord.getOrDefault(word, 0) + 1);
```

## 返回值语义

`Map.get` 返回 `null` 同时表示“键不存在”和“键存在且值为 null”。如果值类型允许 `null`，必须用 `containsKey` 区分。算法代码通常把值定义为 `Integer`、`List` 等非空对象，从源头避免歧义。

## 空值与装箱

- `HashMap` 允许一个 `null` 键和多个 `null` 值；`TreeMap` 是否允许 `null` 键取决于比较器。
- `Map<Integer,Integer>` 的泛型值必须是 `Integer`。取出后与 `int` 比较或运算时会自动拆箱，此时若结果为 `null` 会抛出 `NullPointerException`。
- 判断“补数是否出现”时，可把 `Integer previous = map.get(need);` 放在 `if (previous != null)` 中，再自动拆箱。
- 小整数缓存只是实现细节，不能用 `==` 比较两个 `Integer` 的值；对象值比较用 `equals`，需要数值比较时先转成基本类型。

## 迭代修改陷阱

使用增强 `for` 遍历 `map.keySet()`、`entrySet()` 或 `set` 时直接 `remove` 可能抛出 `ConcurrentModificationException`。安全做法是使用迭代器的 `iterator.remove()`，或 Java 8 的 `map.entrySet().removeIf(...)` / `set.removeIf(...)`。需要同时判断并删除时，不要一边遍历一边 `put` 新键。

## 复杂度

- `HashMap`、`HashSet` 的 `get`、`put`、`add`、`remove` 在哈希分布合理时平均为 `O(1)`，最坏可退化为 `O(n)`。
- 一次完整遍历为 `O(n)`。
- `TreeMap`、`TreeSet` 的主要操作为 `O(log n)`，完整遍历为 `O(n)`。
- 空间复杂度均为 `O(n)`。

## 关联题目

- [[题目/数组与哈希/1-Two-Sum.md|1. 两数之和]]：值到下标。
- [[题目/数组与哈希/49-Group-Anagrams.md|49. 字母异位词分组]]：规范化键到分组。
- [[题目/数组与哈希/560-Subarray-Sum-Equals-K.md|560. 和为 K 的子数组]]：前缀和到历史频次。
- [[题目/图与搜索/207-Course-Schedule.md|207. 课程表]]：邻接表与入度状态。
- [[题目/设计/146-LRU-Cache.md|146. LRU 缓存]]：哈希索引与链表节点协作。
- [[题目/回溯/301-Remove-Invalid-Parentheses.md|301. 删除无效的括号]]：访问集合阻止同一删除结果从不同路径重复入队。

## 官方文档

- [Map](https://docs.oracle.com/javase/8/docs/api/java/util/Map.html)
- [HashMap](https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html)
- [Set](https://docs.oracle.com/javase/8/docs/api/java/util/Set.html)
- [HashSet](https://docs.oracle.com/javase/8/docs/api/java/util/HashSet.html)
