---
schemaVersion: 3
type: "problem"
leetcodeId: 9
slug: "palindrome-number"
titleCn: "回文数"
titleEn: "Palindrome Number"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/palindrome-number/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "668e9d558247c7833fbdf04798e1d091b20ac0ddc0f4050a0b7e56b40d80453b"
sourceFactsSha256: "ca1cfae1e1839f6fcfa4d7d1b8a4bca65aa1cf737b673d0c623385a8ba57ec47"
sourceSectionHashes:
  description: "5d694343fdd17677e123f7e4008a96d62d7197114095b6cca83ed4265ec7db98"
  examples: "fe681893e6dee03b82b6290ba562d04b6c011342d596be83b48f492bf3977bd8"
  constraints: "e8c94647d605c9d0ccd5148d1ea2df6ff629f793c121ba39bb8da7e3bee4c73e"
  hints: "376694147b15f6753aeb2477a6964d3619c430bea1e6561ed9ebd7379d1b05aa"
  tags: "06edb80c76ca31f042e090652428b3b46f710393d25f9c95e7e75d8d60e4fd1e"
  signature: "2a8a5124ab4aa7625762eb7956aec498379ea30ba200129e01b04a100ddfb78e"
  javaTemplate: "5d7cae0a49ec3de58d56de6af4d1a3c1b97769fd55e315e914886f3361ff2cd7"
primaryPattern: "数学"
topics: ["数学"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Math 数学"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 9. “回文数”是指：从左往右读和从右往左读都一样的数字。

> **双轨入口：** [[核心模型/数学/9-Palindrome-Number-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`数学`
- 清单优先级：`P1`
- 清单代表标签：`Math 数学`
- LeetCode 当前标签：数学 (Math)
- 官方来源：<https://leetcode.cn/problems/palindrome-number/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`668e9d558247c7833fbdf04798e1d091b20ac0ddc0f4050a0b7e56b40d80453b`
- 主模型：只反转数字的后一半

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数 `x` ，如果 `x` 是一个回文整数，返回 `true` ；否则，返回 `false` 。

回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

- 例如，`121` 是回文，而 `123` 不是。

## 官方示例


**示例 1：**

```text
输入：x = 121
输出：true
```

**示例 2：**

```text
输入：x = -121
输出：false
解释：从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。
```

**示例 3：**

```text
输入：x = 10
输出：false
解释：从右向左读, 为 01 。因此它不是一个回文数。
```

## 官方约束


- `-2^31 <= x <= 2^31 - 1`

**进阶：**你能不将整数转为字符串来解决这个问题吗？

## 输入值范围能提示什么

### `x` 在 32 位整数范围内

常见思路：

- 位运算
- 枚举二进制位，最多 32 位
- 不断除以 `2` 或 `10`
- 二分答案，最多约 32 次
- 数字拆位、整数反转、快速幂
- 使用 `long long` / `long` 保存中间结果

例如整数平方根：

```text
答案范围是 [0, x]
```

可以二分，复杂度为：

```text
O(log x) <= O(31)
```

但实现 `mid * mid` 时仍然要防止溢出，可以写成：

```cpp
mid <= x / mid
```

而不是：

```cpp
mid * mid <= x
```

### 值域很小

例如：

```text
0 <= nums[i] <= 100
```

这提示可以考虑：

- 计数数组
- 桶排序
- 状态压缩
- 用值域代替元素数量
- 前缀计数

如果有 `n = 10^5` 个数，但每个数都在 `[0, 100]`，有时不需要排序 `O(n log n)`，统计 101 个桶即可做到 `O(n + 100)`。

### 值域很大但元素数量少

例如：

```text
n <= 10^5
-10^9 <= nums[i] <= 10^9
```

不能创建一个覆盖整个值域的数组，此时通常考虑：

- 哈希表
- 排序
- 坐标压缩
- 平衡树
- 离散化

---

## 根据 `n` 倒推时间复杂度

这是 LeetCode 中更常见、更有效的倒推方法。下面是比较实用的经验表，不是绝对规则：

| 输入规模 `n` | 通常可接受的复杂度 | 常见思路 |
|---:|---:|---|
| `n <= 10` | `O(n!)`、部分指数算法 | 全排列、回溯 |
| `n <= 20` | `O(2^n)` | 状态压缩 DP、子集枚举、回溯 |
| `n <= 40` | `O(2^(n/2))` | 折半搜索 |
| `n <= 100` | `O(n^3)` | 区间 DP、Floyd、三重枚举 |
| `n <= 1,000` | `O(n^2)` | 二维 DP、枚举两端点 |
| `n <= 10^4` | 较轻的 `O(n^2)` 或 `O(n sqrt n)` | 视语言和常数而定 |
| `n <= 10^5` | `O(n log n)` | 排序、二分、堆、树状数组、线段树 |
| `n <= 10^6` | `O(n)` 或较轻的 `O(n log n)` | 双指针、滑窗、前缀和、哈希 |
| `n >= 10^7` | `O(n)` 也需注意常数和内存 | 原地扫描、位图、数学方法 |
| `n` 达到 `10^9` | `O(log n)` 或 `O(1)` | 二分、快速幂、数学推导 |
| `n` 达到 `10^18` | `O(log n)` | 快速幂、数位 DP、数学规律 |

大致可以把在线评测允许的基本操作次数理解为 `10^7～10^8` 量级，但语言、服务器、常数和数据结构都会显著影响结果。

---

## 看到数据范围时的思考顺序

### 1. 先区分“元素数量”和“元素值域”

```text
n <= 10^5
nums[i] <= 10^9
```

其中：

- `n` 决定遍历、排序、DP 的复杂度上限
- `nums[i]` 的范围决定能否使用桶、数组索引、位运算，以及是否会溢出

### 2. 计算暴力算法的操作数量

假如 `n = 10^5`：

```text
O(n^2) = 10^10
```

基本不可行。

于是需要寻找：

```text
O(n log n) ≈ 1.7 × 10^6
O(n)       = 10^5
```

这时自然会想到：

- 排序
- 哈希
- 双指针
- 滑动窗口
- 单调栈
- 前缀和
- 二分
- 堆

### 3. 看答案或状态空间是否很小

例如：

```text
n <= 10^5
答案范围 <= 10^9
```

如果存在单调性，可以二分答案：

```text
O(n log 10^9) ≈ 30n
```

虽然答案值达到十亿，但二分只需要约 30 次。

### 4. 看特殊数字是否在暗示算法

常见暗示包括：

| 数据特征 | 可能思路 |
|---|---|
| `n <= 20` | 状态压缩、子集枚举 |
| `n <= 40` | 折半搜索 |
| 值域 `[0, 10^5]` | 计数、桶、筛法 |
| 数值达到 `10^9` | 二分答案、哈希、数学 |
| 数值达到 `10^18` | 快速幂、公式、数位 DP |
| 字符种类只有 26 个 | 定长数组、位掩码 |
| 矩阵边长 `<= 200` | 二维 DP、图算法 |
| 图中边权为 `0/1` | 0-1 BFS |
| 边权非负 | Dijkstra |
| 数据是树，`n <= 10^5` | DFS、树形 DP、倍增 |
| 多次区间查询 | 前缀和、树状数组、线段树 |
| 多次判断连通性 | 并查集 |

---

## `-2^31` 这个边界的额外陷阱

很多题故意给出这个范围来测试边界处理：

```cpp
int x = INT_MIN;
-x;          // 可能溢出
abs(x);      // 可能溢出
x / -1;      // 数学结果为 2^31，超出 int
```

不同语言表现不同：

- C++：有符号整数溢出可能导致未定义行为。
- Java：`int` 溢出会按二进制补码回绕。
- Python：整数可自动扩展，通常不会溢出，但题目可能要求结果必须处于 32 位范围内。
- JavaScript：普通 `Number` 是双精度浮点数，32 位范围可以精确表示，但位运算会将数转换为 32 位整数。

所以，当题目明确写出 32 位边界时，往往要主动检查：

```text
加法会不会溢出？
乘法会不会溢出？
取负数会不会溢出？
中间结果是否需要更宽的类型？
结果超界时应该返回什么？
```

最核心的理解是：

> `n` 的范围主要用于倒推时间复杂度；`x` 或 `nums[i]` 的范围主要用于判断值域算法、二进制位数、数学性质和溢出风险。

大佬所谓“从数据范围倒推算法”，本质上就是先用数量级排除不可能的复杂度，再结合数据结构、值域和题目性质缩小到几类候选算法。


**进阶：**你能不将整数转为字符串来解决这个问题吗？

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Beware of overflow when you reverse the integer.

## 学习提示（非官方）

1. 负数一定不是回文数。
2. 除 `0` 外，末位为 `0` 的数不可能回文，因为其首位不可能是 `0`。
3. 当“反转的后半部分”大于等于“尚未处理的前半部分”时，可以停止。
4. 奇数位数字中间那一位不影响对称，可用 `/10` 去掉。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 进阶要求是不把整数转换成字符串。
- 最优方案只处理约一半数字，时间为 `O(log10 |x|)`，空间为 `O(1)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

完整反转可能接近溢出，而判断回文只需要比较前后两半。例如 `1221`：

```text
x=1221, reversedHalf=0
x=122,  reversedHalf=1
x=12,   reversedHalf=12  -> 两半相等
```

对于 `12321`，停止时 `x=12`、`reversedHalf=123`，去掉中间位后 `123/10=12`。

## 朴素方案：转换为字符串

把整数转成字符串，用左右指针比较字符。实现简单且通常足够，但使用了与数字位数成正比的字符串空间，且没有利用数值结构。

- 时间复杂度：`O(log |x|)`。
- 空间复杂度：`O(log |x|)`。

另一个朴素数学方案是完整反转数字，可能面对溢出问题。

## 最优方案：反转后一半

先排除负数和非零末位零。不断从 `x` 末尾取一位加入 `reversedHalf`，直到 `x <= reversedHalf`。最后判断：

```text
x == reversedHalf              // 偶数位
x == reversedHalf / 10         // 奇数位，忽略中间位
```

### 正确性与不变量

每轮后，`x` 保存原数尚未处理的高位前缀，`reversedHalf` 保存已取出低位后缀的反转。停止时后缀位数不小于前缀位数。偶数位回文要求二者完全相等；奇数位回文只多出中间数字，它位于 `reversedHalf` 的末位，除以 10 后应与前缀相等。这两个条件也只会接受真正对称的数字。

- 时间复杂度：`O(log10 |x|)`，约处理数字位数的一半。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }

        int reversedHalf = 0;
        while (x > reversedHalf) {
            reversedHalf = reversedHalf * 10 + x % 10;
            x /= 10;
        }

        return x == reversedHalf || x == reversedHalf / 10;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }

        int reversedHalf = 0;
        while (x > reversedHalf) {
            reversedHalf = reversedHalf * 10 + x % 10;
            x /= 10;
        }

        return x == reversedHalf || x == reversedHalf / 10;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.isPalindrome(121));   // true
        System.out.println(solution.isPalindrome(-121));  // false
        System.out.println(solution.isPalindrome(10));    // false
        System.out.println(solution.isPalindrome(12321)); // true
        System.out.println(solution.isPalindrome(0));     // true
    }
}
```

## 边界与易错点

- `0` 是回文数，排除末位零时要加 `x != 0`。
- 负号没有对称位置，所以所有负数直接为 `false`。
- 奇数位必须比较 `x == reversedHalf / 10`，否则 `121` 会被误判。
- 只反转一半后，`reversedHalf` 不会超过完整 `int` 输入的安全范围。

## 可扩展变式

- 判断字符串回文可用左右双指针，并按需忽略标点和大小写。
- 判断链表回文可用快慢指针找中点、反转后半链表再比较。
- 回文构造、最近回文数等题需要进一步处理进位和位数变化。
