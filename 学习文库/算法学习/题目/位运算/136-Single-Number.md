---
schemaVersion: 3
type: "problem"
leetcodeId: 136
slug: "single-number"
titleCn: "只出现一次的数字"
titleEn: "Single Number"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/single-number/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "f9a952a56c214d39369940bf77ddeb461e04331e73b210e4e62977132dee2e6b"
sourceFactsSha256: "7c0ce70d1411921347d6a44307a2bc172fbd08c84858b0780bf7b2ab3f640b41"
sourceSectionHashes:
  description: "d84c9b2b3ae281a3db426382ab04f9212da56c95a734db26bd1b158c916588f1"
  examples: "d18e8b24aebcc62fe3532f5458fabbcf163154126569675b550ad817e79aef85"
  constraints: "0b863f17079a348cb3240d0247180b15d065cbeb99ccdd0fac7f664874ec688c"
  hints: "331b388b44cdabadb7f98b03284317ca50b4eb7f2b601618942b21313344acf1"
  tags: "1514ed2991512f27ae51d8c4e87837c6786c3b4e9d902768a10a4b7a6c72aad9"
  signature: "ba9d33c5dc5aa664524bcb523f26f364ea062492e03d59dc37f2aa954d5b1688"
  javaTemplate: "a7a4b88db6877c5fbb05991b91ff57e6260cf47960e709f4c13c3044913c6c3a"
primaryPattern: "位运算"
topics: ["位运算","数组"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Bit Manipulation 位运算"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 136. 只出现一次的数字 / Single Number

> **双轨入口：** [[核心模型/位运算/136-Single-Number-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`位运算`
- 清单优先级：`P1`
- 清单代表标签：`Bit Manipulation 位运算`
- LeetCode 当前标签：位运算 (Bit Manipulation)、数组 (Array)
- 官方来源：<https://leetcode.cn/problems/single-number/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`f9a952a56c214d39369940bf77ddeb461e04331e73b210e4e62977132dee2e6b`
- 主模型：异或消去成对元素

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个 **非空** 整数数组 `nums` ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。

**示例 1 ：**

**输入：**nums = [2,2,1]

**输出：**1

**示例 2 ：**

**输入：**nums = [4,1,2,1,2]

**输出：**4

**示例 3 ：**

**输入：**nums = [1]

**输出：**1

## 官方示例


官方题面未单独列出示例。

## 官方约束


- `1 <= nums.length <= 3 * 10^4`

- `-3 * 10^4 <= nums[i] <= 3 * 10^4`

- 除了某个元素只出现一次以外，其余每个元素均出现两次。

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Think about the XOR (^) operator's property.

## 学习提示（非官方）

1. 异或运算满足 `x ^ x = 0` 和 `x ^ 0 = x`。
2. 异或满足交换律与结合律，数组中元素顺序不会影响最终结果。
3. 把所有元素异或在一起，成对元素会相互抵消。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 期望 `O(n)` 时间。
- 额外空间要求 `O(1)`，因此哈希计数不是最终方案。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

设唯一元素为 `u`，其他元素为成对的 `a,a,b,b`。由于异或可任意重排和分组：

```text
a ^ a ^ b ^ b ^ u
= (a ^ a) ^ (b ^ b) ^ u
= 0 ^ 0 ^ u
= u
```

Java 的 `^` 对负数同样按二进制补码逐位计算，上述代数性质仍成立。

## 朴素方案一：逐个计数

使用 `HashMap<Integer,Integer>` 统计出现次数，再找次数为 `1` 的键。

- 时间复杂度：平均 `O(n)`。
- 空间复杂度：`O(n)`。
- 局限：违反常量额外空间要求。

## 朴素方案二：排序

排序后成对检查相邻元素，第一个无法配对的就是答案。

- 时间复杂度：`O(n log n)`。
- 空间复杂度：依排序实现而定。
- 局限：不满足线性时间，并会改变输入顺序。

## 最优方案推导

初始化 `answer = 0`，顺序遍历数组并执行 `answer ^= num`。任何成对值无论相隔多远，最终都会因交换律和结合律消为零；循环结束只留下唯一值。

无需提前知道哪个数字成对，也无需对输入排序或建立计数表。

## 正确性与不变量

处理完数组前 `i` 个元素后，`answer` 等于这 `i` 个元素的异或结果。循环更新显然保持该不变量。全部处理后，利用交换律和结合律可把所有相同的两个元素配对，每对异或为零；零不会改变剩余值，所以最终 `answer` 恰好等于只出现一次的元素。

## 复杂度

- 时间复杂度：`O(n)`，每个元素异或一次。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int singleNumber(int[] nums) {
        int answer = 0;
        for (int num : nums) {
            answer ^= num;
        }
        return answer;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public int singleNumber(int[] nums) {
        int answer = 0;
        for (int num : nums) {
            answer ^= num;
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {4, 1, 2, 1, 2};
        int answer = new Solution().singleNumber(nums);
        System.out.println("nums = " + Arrays.toString(nums));
        System.out.println("single number = " + answer);
    }
}
```

## 边界与易错点

- 异或技巧依赖“其他元素恰好出现两次”；出现三次时不能直接套用。
- 不要把异或 `^` 与逻辑或、乘方混淆；Java 中 `^` 是按位异或。
- 一个元素时，`0 ^ nums[0]` 正好得到该元素。
- 负数无需特殊处理，补码位模式会正常成对消去。
- 若题目不保证唯一答案，异或结果不再具有指定语义。

## 可扩展变式

- 137. 只出现一次的数字 II：其他元素出现三次，可统计每一位对 3 取模。
- 260. 只出现一次的数字 III：有两个唯一数，先整体异或，再按某个不同位分组。
- 找缺失数字（268）：异或所有下标和数组值，成对消去。
- 判断两个整数哪些位不同：异或后统计结果中的 `1` 位数。
