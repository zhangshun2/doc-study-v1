---
schemaVersion: 3
type: "java-api"
titleCn: "Math 与位运算"
topics: ["Java API","数学","位运算"]
sourceUrl: "https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html"
sourceCheckedAt: "2026-09-12"
priority: "P2"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
relatedProblems: [7,9,136,191,338,371]
---

# Math / 位运算

## 典型场景

| 需求 | 常用写法 |
| --- | --- |
| 取较小或较大值 | `Math.min(a,b)` / `Math.max(a,b)` |
| 取绝对值 | `Math.abs(value)` |
| 判断奇偶 | `(value & 1) == 1` |
| 取最低有效位 | `value & 1` |
| 去掉最低的 1 位 | `value & (value - 1)` |
| 找只出现一次的数 | 全部异或 |
| 快速乘除 2 的幂 | `value << k` / `value >> k` |
| 提取一片二进制位 | 先右移，再按掩码 `&` |

位运算适合表达独立开关、奇偶、二进制计数和成对抵消。普通数值范围比较仍应优先写清楚，不能为了技巧压缩可读性。

## 构造方式与常用运算

```java
int smaller = Math.min(first, second);
int largest = Math.max(best, candidate);
int absolute = Math.abs(value);

boolean isOdd = (value & 1) == 1;
int lowestBit = value & -value;
int withoutLowestBit = value & (value - 1);
int xorAccumulator = 0;
xorAccumulator ^= value;
```

## 运算符语义

| 运算符 | 含义 | 示例 |
| --- | --- | --- |
| `&` | 按位与，两位都为 1 才得 1 | `6 & 3 == 2` |
| `|` | 按位或，任一位为 1 就得 1 | `4 | 1 == 5` |
| `^` | 按位异或，不同得 1 | `5 ^ 1 == 4` |
| `~` | 按位取反 | `~0 == -1` |
| `<<` | 左移，低位补 0 | `3 << 1 == 6` |
| `>>` | 有符号右移，高位补符号位 | `-8 >> 1 == -4` |
| `>>>` | 无符号右移，高位补 0 | 适合处理二进制位模式 |

异或性质是 `x ^ x == 0`、`x ^ 0 == x`，并且满足交换律和结合律，因此相同的数出现两次会相互抵消。

## 返回值语义

- `Math.max`、`Math.min` 返回两个参数中的较大或较小值。
- `Math.abs(Integer.MIN_VALUE)` 仍是 `Integer.MIN_VALUE`，因为对应的正数超出 `int` 范围。
- 位运算符的优先级低于比较运算符；条件中必须加括号，例如写 `(value & 1) == 1`。
- 移位距离只使用右侧操作数的低 5 位处理 `int`，低 6 位处理 `long`。

## 空值与装箱

`Math.max`、`Math.min` 和位运算符的参数是基本数值类型；传入 `Integer` 会自动拆箱，值为 `null` 时抛 `NullPointerException`。涉及大数时使用 `long`，例如 `mid = left + (right - left) / 2` 或先转 `long` 再计算，避免 `int` 加法溢出。

## 常见误区与陷阱

- `>>` 会保留符号，负数右移后仍可能为负；只想移动位模式时使用 `>>>`。
- `Math.abs(a - b)` 在 `a - b` 超出 `int` 范围时可能先溢出；必要时转 `long`。
- 判断负数奇偶时，`value % 2` 可能得到 `-1`；`(value & 1) == 1` 对负奇数同样成立。
- 异或只适合出现次数具有成对关系的计数；出现三次或要求频次时不能直接套用。

## 迭代修改陷阱

位运算的直接对象是不可变基本数值或 `Integer`，不存在原地修改集合的迭代陷阱。真正容易出错的是复合状态：用多个位同时表示多个开关时，修改某一位要先用 `value | mask` 置位、`value & ~mask` 清零，不能直接对整个状态赋值。循环中更新 `value` 时先写清每一步的位含义。

## 复杂度

- `Math.min`、`Math.max`、`Math.abs`：`O(1)`。
- 单个位运算和移位：`O(1)`。
- 逐位扫描一个整数：`O(w)`，`w` 是二进制位数，`int` 通常为 32。
- 使用位运算只需要常数个标量时，额外空间为 `O(1)`。

## 关联题目

- [[题目/位运算/136-Single-Number.md|136. 只出现一次的数字]]：异或消除成对元素。
- [[题目/数学/7-Reverse-Integer.md|7. 整数反转]]：溢出边界判断。
- [[题目/数学/9-Palindrome-Number.md|9. 回文数]]：逐位构造和比较。

## 官方文档

- [Math](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html)
- [Integer](https://docs.oracle.com/javase/8/docs/api/java/lang/Integer.html)
