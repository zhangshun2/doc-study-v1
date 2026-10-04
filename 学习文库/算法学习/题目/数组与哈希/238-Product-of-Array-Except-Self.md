---
schemaVersion: 3
type: "problem"
leetcodeId: 238
slug: "product-of-array-except-self"
titleCn: "除了自身以外数组的乘积"
titleEn: "Product of Array Except Self"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/product-of-array-except-self/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "896ff275fd4d361e76611bc72f06deb54e0f59cfc6aa15fa23a85d51cf09b7db"
sourceFactsSha256: "fa3260ef4dccb3742fa42c3f1ee4864fbc229159dcb345dc8152931450f00fa2"
sourceSectionHashes:
  description: "963357c84782488a0b2b256e1d6656a86a9e89b04c6cef6e3c0c8bd2036798cd"
  examples: "18abb024871f9e36847af12132d1eed364d5b0eea1b1dc56c0050dcc0e4d7733"
  constraints: "ccec775d32398d5ac161ed2d4785abc8cac5eb241394a543324e0f328c33879b"
  hints: "e22fdfb337e02c2a298d6074316ebd42fdcb526f1592834bd1bf7622f0872cb7"
  tags: "08044c56993fd5d8606f8da5c3e8800c30098596ccc95866088e95764f41b2a3"
  signature: "c1a71387b902b886962bd7d8fc6ce9f93e94e91682e82b60b815b1f1e6d70478"
  javaTemplate: "0a2e3dcc3b0dba37368e3a0f708b78658480f2eaa921b93e3282284ad5da93c7"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","数组","前缀和"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Prefix Sum 前缀和"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 238. 除了自身以外数组的乘积 / Product of Array Except Self

> **双轨入口：** [[核心模型/数组与哈希/238-Product-of-Array-Except-Self-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`数组与哈希`
- 清单优先级：`P1`
- 清单代表标签：`Prefix Sum 前缀和`
- LeetCode 当前标签：数组 (Array)、前缀和 (Prefix Sum)
- 官方来源：<https://leetcode.cn/problems/product-of-array-except-self/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`896ff275fd4d361e76611bc72f06deb54e0f59cfc6aa15fa23a85d51cf09b7db`
- **主解法**：前缀积输出数组 + 后缀积变量

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums`，返回 数组 `answer` ，其中 `answer[i]` 等于 `nums` 中除了 `nums[i]` 之外其余各元素的乘积 。

题目数据 **保证** 数组 `nums`之中任意元素的全部前缀元素和后缀的乘积都在  **32 位** 整数范围内。

请 **不要使用除法，**且在 `O(n)` 时间复杂度内完成此题。

## 官方示例


**示例 1:**

```text
输入: nums = [1,2,3,4]
输出: [24,12,8,6]
```

**示例 2:**

```text
输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]
```

## 官方约束


- `2 <= nums.length <= 10^5`

- `-30 <= nums[i] <= 30`

- 输入 **保证** 数组 `answer[i]` 在  **32 位** 整数范围内

**进阶：**你可以在 `O(1)` 的额外空间复杂度内完成这个题目吗？（ 出于对空间复杂度分析的目的，输出数组 **不被视为 **额外空间。）

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Think how you can efficiently utilize prefix and suffix products to calculate the product of all elements except self for each index. Can you pre-compute the prefix and suffix products in linear time to avoid redundant calculations?
2. Can you minimize additional space usage by reusing memory or modifying the input array to store intermediate results?

## 学习提示（非官方）

1. `answer[i]` 可以拆成左边所有元素乘积乘以右边所有元素乘积。
2. 第一遍把“左侧乘积”直接写进输出数组。
3. 第二遍从右向左，用一个变量累计“右侧乘积”。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 进阶：除返回数组外，仅使用 `O(1)` 额外空间；输出数组不计入额外空间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [0,0]
输出：[0,0]
```

## 核心观察

对位置 `i`：

```text
answer[i] = 左侧元素 nums[0..i-1] 的乘积
          * 右侧元素 nums[i+1..n-1] 的乘积
          = prefixBefore(i) * suffixAfter(i)
```

左右两部分互不包含自身，天然避开除法，也能正确处理零。

## 朴素方案

对每个 `i` 遍历数组并跳过自身，时间 `O(n^2)`。先求总乘积再除以 `nums[i]` 虽为 `O(n)`，但违反禁止除法且遇到零无法直接处理。显式建立 `prefix[]`、`suffix[]` 可以 `O(n)` 时间，但额外空间是 `O(n)`。

## 最优方案推导

第一遍从左到右，令 `answer[i]` 等于 `i` 左侧全部元素乘积。初始化左侧空积为 `1`。

第二遍从右到左，维护 `suffix` 为 `i` 右侧全部元素乘积：先执行 `answer[i] *= suffix`，再执行 `suffix *= nums[i]`。顺序不能颠倒，否则会错误地把自身乘入。

## 正确性与不变量

第一遍处理位置 `i` 前，累计变量是 `nums[0..i)` 的乘积，所以写入的正是左侧积。

第二遍处理位置 `i` 前，`suffix` 是 `nums(i..n)` 即 `nums[i+1..n-1]` 的乘积。输出中原有左侧积，乘上 `suffix` 后恰为除自身外所有元素的乘积。更新后不变量对下一个位置成立。因此每个答案均正确。

## 复杂度

- **时间复杂度**：`O(n)`，两次线性扫描。
- **空间复杂度**：`O(1)` 额外空间，不计必须返回的 `answer` 数组。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] answer = new int[nums.length];
        int prefix = 1;
        for (int index = 0; index < nums.length; index++) {
            answer[index] = prefix;
            prefix *= nums[index];
        }

        int suffix = 1;
        for (int index = nums.length - 1; index >= 0; index--) {
            answer[index] *= suffix;
            suffix *= nums[index];
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
    public int[] productExceptSelf(int[] nums) {
        int[] answer = new int[nums.length];
        int prefix = 1;
        for (int index = 0; index < nums.length; index++) {
            answer[index] = prefix;
            prefix *= nums[index];
        }

        int suffix = 1;
        for (int index = nums.length - 1; index >= 0; index--) {
            answer[index] *= suffix;
            suffix *= nums[index];
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(solution.productExceptSelf(
                new int[]{1, 2, 3, 4}))); // [24, 12, 8, 6]
        System.out.println(Arrays.toString(solution.productExceptSelf(
                new int[]{-1, 1, 0, -3, 3}))); // [0, 0, 9, 0, 0]
        System.out.println(Arrays.toString(solution.productExceptSelf(
                new int[]{0, 0}))); // [0, 0]
    }
}
```

## 边界与易错点

- 空集合的乘积定义为 `1`，因此 `prefix`、`suffix` 初值都必须是 `1`。
- 第二遍必须先乘 `suffix`，再把当前 `nums[i]` 纳入后缀积。
- 不需要单独判断零：前后缀积自然覆盖一个零和多个零。
- 题目保证 32 位范围；若移植到更大约束，应将中间量和输出改为 `long`。

## 可扩展变式

- 允许除法：需分类讨论零的数量；没有零时可用总积除自身。
- 求除自身外的和：可用总和减自身；乘法问题因零和禁除法更有代表性。
- 矩阵每格除自身外乘积：先展平或做全局前后缀遍历。
- 乘积取模：相同前后缀方法适用，注意负数标准化与乘法溢出。
