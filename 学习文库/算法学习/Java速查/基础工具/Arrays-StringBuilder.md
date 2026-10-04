---
schemaVersion: 3
type: "java-api"
titleCn: "Arrays 与 StringBuilder"
topics: ["Java API","数组","字符串"]
sourceUrl: "https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html"
sourceCheckedAt: "2026-09-12"
priority: "P2"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
relatedProblems: [3,5,14,34,49,72,124,215,322,1249]
---

# Arrays / StringBuilder

## 典型场景

| 需求 | 常用工具 |
| --- | --- |
| 数组填充初始值 | `Arrays.fill` |
| 排序数组或对象数组 | `Arrays.sort` |
| 复制固定长度数组 | `Arrays.copyOf` / `Arrays.copyOfRange` |
| 判断两个数组内容相等 | `Arrays.equals` |
| 在有序数组中查找值 | `Arrays.binarySearch` |
| 高频拼接字符串 | `StringBuilder` |
| 反转或修改字符序列 | `StringBuilder.reverse` / `setCharAt` |

`String` 不可变，循环中反复 `s = s + x` 会创建许多中间字符串。需要逐步构造结果时改用 `StringBuilder`。

## 构造方式

```java
int[] dp = new int[amount + 1];
Arrays.fill(dp, amount + 1);

StringBuilder path = new StringBuilder();
StringBuilder reversed = new StringBuilder(text).reverse();
```

`StringBuilder()` 默认容量足够小场景；已知结果长度时可以传预期容量。容量只是性能提示，不影响正确性。

## 常用操作

| 类型 | 操作 | 说明 |
| --- | --- | --- |
| 数组 | `Arrays.fill(array, value)` | 原地覆盖全部元素 |
| 数组 | `Arrays.sort(array)` | 基本类型升序，原地排序 |
| 数组 | `Arrays.sort(objects, comparator)` | 对象数组按比较器排序 |
| 数组 | `Arrays.copyOf(array, newLength)` | 返回新数组，可加长或截短 |
| 数组 | `Arrays.binarySearch(array, key)` | 仅对已经升序排序的数组有效 |
| 字符串 | `builder.append(value)` | 追加并返回 builder |
| 字符串 | `builder.charAt(index)` | 读取指定位置 |
| 字符串 | `builder.setCharAt(index, ch)` | 原地替换字符 |
| 字符串 | `builder.deleteCharAt(index)` | 删除一个字符 |
| 字符串 | `builder.toString()` | 生成不可变字符串快照 |

## 返回值语义

- `Arrays.sort`、`Arrays.fill` 原地修改并返回 `void`。
- `Arrays.copyOf` 返回新数组，原数组不变。
- `Arrays.binarySearch` 找到时返回某一次命中的下标，不保证是第一个或最后一个；未找到时返回 `-(插入点)-1`。
- `StringBuilder.append` 返回同一个 builder，便于链式调用，但它不是新对象。
- `StringBuilder.toString()` 复制当前内容；后续修改 builder 不会改变已经生成的字符串。

## 空值与装箱

数组声明为 `Integer[]` 时才允许元素为 `null`；`int[]` 的默认值是 0。不要把“默认 0”误当成“尚未计算”，需要哨兵时应显式 `Arrays.fill`。自动装箱的 `Integer[]` 进行 `Arrays.sort` 时自然顺序可处理 `null` 之外的元素，但算法代码通常优先使用基本类型数组避免额外对象。

## 常见边界

- `Arrays.binarySearch` 的前提是数组已经按同一比较规则升序排序。
- `new int[n]` 的所有元素默认为 0，布尔数组默认为 `false`。
- `StringBuilder` 的 `deleteCharAt` 是 `O(n)`，但在回溯中只删除末位时可用 `deleteCharAt(length-1)`。
- 比较数组内容不能用 `array1 == array2`，必须用 `Arrays.equals`。

## 迭代修改陷阱

不要在增强 `for` 遍历数组时改变数组长度，因为数组长度固定。`Arrays.asList(array)` 返回的是固定长度视图，`add`、`remove` 会抛 `UnsupportedOperationException`；需要可变列表时使用 `new ArrayList<>(Arrays.asList(array))`。遍历 `StringBuilder` 时修改其长度也会造成下标错位，删除和扩展应在明确的索引循环中完成。

## 复杂度

- `Arrays.fill`、`Arrays.equals`：`O(n)`。
- 基本类型数组排序：平均和典型实现为 `O(n log n)`，额外空间取决于排序实现。
- `Arrays.copyOf`：`O(n)`。
- `Arrays.binarySearch`：`O(log n)`。
- `StringBuilder.append` 均摊 `O(1)`，`toString` 为 `O(n)`。

## 关联题目

- [[题目/数组与哈希/49-Group-Anagrams.md|49. 字母异位词分组]]：字符计数与键构造。
- [[题目/动态规划/322-Coin-Change.md|322. 零钱兑换]]：数组填充不可达哨兵。
- [[题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md|215. 数组中的第 K 个最大元素]]：原地数组操作。
- [[题目/字符串/14-Longest-Common-Prefix.md|14. 最长公共前缀]]：逐字符构造公共结果。
- [[题目/动态规划/72-Edit-Distance.md|72. 编辑距离]]：多维数组状态。
- [[题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md|1249. 移除无效的括号]]：用布尔标记过滤字符，再用 StringBuilder 一次构造结果。

## 官方文档

- [Arrays](https://docs.oracle.com/javase/8/docs/api/java/util/Arrays.html)
- [StringBuilder](https://docs.oracle.com/javase/8/docs/api/java/lang/StringBuilder.html)
- [String](https://docs.oracle.com/javase/8/docs/api/java/lang/String.html)
