---
schemaVersion: 3
type: "core-model"
leetcodeId: 7
slug: "reverse-integer"
titleCn: "整数反转"
titleEn: "Reverse Integer"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/reverse-integer/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "84e0d08c126d506418c2f429bacb538f2fadf8151ac4bff4064e443867e61aa8"
primaryPattern: "数学"
topics: ["数学"]
priority: "P1"
problemPath: "题目/数学/7-Reverse-Integer.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 7. 整数反转：核心模型

> **双轨阅读：** [[题目/数学/7-Reverse-Integer.md|标准题解]]

## 一句话本质

每次把原数最后一位弹出，再压入结果末尾： digit = x % 10 x /= 10 reversed = reversed * 10 + digit 真正难点是最后一行可能在判断前已经溢出。设上界为 MAX：若 reversed > MAX/10，乘 10 必溢出；若等于 MAX/10，则只有 digit <= MAX%10 才安全。下界同理。

## 直观画面与扩题

像逐位拆开十进制计数器，每次只处理当前最低位，同时守住溢出边界。

在本题中，对象是 **整数位、反转过程或比较边界**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：每次把原数最后一位弹出，再压入结果末尾： digit = x % 10 x /= 10 reversed = reversed * 10 + digit 真正难点是最后一行可能在判断前已经溢出。设上界为 MAX：若 reversed > MAX/10，乘 10 必溢出；若等于 MAX/10，则只有 digit <= MAX%10 才安全。下界同理。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 整数位、反转过程或比较边界 | 把题目翻译成一条可执行关系：每次把原数最后一位弹出，再压入结果末尾： digit = x % 10 x /= 10 reversed = reversed * 10 + digit 真正难点是最后一行可能在判断前已经溢出。 | 在每次写入新数字前，用除法边界判断。Java 中： Integer.MAX_VALUE / 10 = 214748364，末位上限为 7 | 在每次写入新数字前，用除法边界判断。 | 每轮开始时，reversed 是已从原数末尾取出的所有数字按反向顺序组成的整数，x 是尚未处理的高位部分。 | 每轮开始时，reversed 是已从原数末尾取出的所有数字按反向顺序组成的整数，x 是尚未处理的高位部分。 |

## 最小演算

官方首例输入：`x = 123`，输出：`321`。

1. **初始状态：** 在每次写入新数字前，用除法边界判断。
2. **触发事件：** 在每次写入新数字前，用除法边界判断。
3. **结束条件：** 每轮开始时，reversed 是已从原数末尾取出的所有数字按反向顺序组成的整数，x 是尚未处理的高位部分。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮开始时，reversed 是已从原数末尾取出的所有数字按反向顺序组成的整数，x 是尚未处理的高位部分。取出 digit 并安全追加后，该关系继续成立。预检查精确排除了大于最大值或小于最小值的两类情况。循环结束时没有剩余数字，因此 reversed 就是所求反转值。

## 代码映射

```text
1. 在每次写入新数字前，用除法边界判断。
2. Java 中：
3. 在每次写入新数字前，用除法边界判断。Java 中： Integer.MAX_VALUE / 10 = 214748364，末位上限为 7
```

## 复杂度

- 时间复杂度：O(log10 |x|)，最多处理 10 位。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`数学`
- 切入点：x % 10 取得末位，x / 10 删除末位。

## 最小反例与易错点

- 不要对 x 先取绝对值，Integer.MIN_VALUE 的绝对值无法用 int 表示。
- Java 中 -123 % 10 == -3、-123 / 10 == -12，因此正负数可统一处理。

## 分层入口

- [[题目/数学/7-Reverse-Integer.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
