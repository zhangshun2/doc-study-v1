---
schemaVersion: 3
type: "problem"
leetcodeId: 209
slug: "minimum-size-subarray-sum"
titleCn: "长度最小的子数组"
titleEn: "Minimum Size Subarray Sum"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/minimum-size-subarray-sum/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "9c6595054cab2c5b020d4f5cec4af96b7b1c2bf49824d0ae1c59290696fbfcc9"
sourceFactsSha256: "d00e4a27c91b276049bc1396e3a449196e674ff55434bbf1f69ea5891955884b"
sourceSectionHashes:
  description: "ce62b621d1c18c3f4497095425b9a0d97f19adb54752ef8afeabb006775586a3"
  examples: "656fe7c25cf773f1afc859d2670ef65ebe2976a71cff40559474f2b84f6bbcff"
  constraints: "68934289a29f6355df6de60e15fe4c1a117d99f54c2920cb97ca0c4df7a12d08"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "d8202844a516cc4d58aea985041589d616c3cb0aa45d8d6afbb4144aa54bdee5"
  signature: "804ebaa89d8f670e8ac27b7d375c4a81bec9c651823c8bd9e675c5e8d9a50544"
  javaTemplate: "2915077e15f8b8dad94734527770a047bbd80616aa6abfce1c604a72c04648bb"
primaryPattern: "滑动窗口"
topics: ["滑动窗口","数组","二分查找","前缀和"]
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
# 209. 长度最小的子数组 / Minimum Size Subarray Sum

> **双轨入口：** [[核心模型/滑动窗口/209-Minimum-Size-Subarray-Sum-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`滑动窗口`
- 清单优先级：`P1`
- 清单代表标签：`Prefix Sum 前缀和`
- LeetCode 当前标签：数组 (Array)、二分查找 (Binary Search)、前缀和 (Prefix Sum)、滑动窗口 (Sliding Window)
- 官方来源：<https://leetcode.cn/problems/minimum-size-subarray-sum/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`9c6595054cab2c5b020d4f5cec4af96b7b1c2bf49824d0ae1c59290696fbfcc9`
- **主解法**：同向双指针 / 滑动窗口

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个含有 `n`** **个正整数的数组和一个正整数 `target`**。**

找出该数组中满足其总和大于等于****`target`****的长度最小的 **子数组** `[nums_l, nums_l+1, ..., nums_r-1, nums_r]` ，并返回其长度**。**如果不存在符合条件的子数组，返回 `0` 。

## 官方示例


**示例 1：**

```text
输入：target = 7, nums = [2,3,1,2,4,3]
输出：2
解释：子数组 [4,3] 是该条件下的长度最小的子数组。
```

**示例 2：**

```text
输入：target = 4, nums = [1,4,4]
输出：1
```

**示例 3：**

```text
输入：target = 11, nums = [1,1,1,1,1,1,1,1]
输出：0
```

## 官方约束


- `1 <= target <= 10^9`

- `1 <= nums.length <= 10^5`

- `1 <= nums[i] <= 10^4`

**进阶：**

- 如果你已经实现**`O(n)` 时间复杂度的解法, 请尝试设计一个 `O(n log(n))` 时间复杂度的解法。

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 固定右边界时，只要窗口和已经达标，就尽量移动左边界缩短窗口。
2. 正数保证：右移右边界时和只会增加，右移左边界时和只会减少。
3. 用 `long` 保存窗口和，能让写法更适合约束扩大后的场景。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

元素全为正，窗口和对左右指针具有单调性。右指针扩张是为了首次达到目标；达到后，左指针不断收缩，找到以当前右端点结尾的最短合法窗口。两个指针都只向右走，无需回退。

## 朴素方案

枚举所有起点与终点并逐项求和为 `O(n^3)`；利用前缀和可将每个区间和降为 `O(1)`，但仍有 `O(n^2)` 个区间。进一步利用前缀和递增，可对每个起点二分终点，达到 `O(n log n)`，仍不如线性窗口。

## 最优方案推导

维护窗口 `[left, right]` 和 `windowSum`：

1. 右端加入 `nums[right]`。
2. 当 `windowSum >= target` 时，当前窗口合法，更新最短长度。
3. 移除 `nums[left]` 并令 `left++`，继续尝试更短窗口。
4. 和不足后，再扩张右端。

收缩必须使用 `while` 而不是 `if`，因为一次扩张后可能连续缩短多次。

## 正确性与不变量

每轮外层结束前，算法已检查所有右端点不超过 `right` 的潜在最优合法窗口。对固定 `right`，收缩循环依次检查所有仍合法的左端点，并在下一次收缩将使窗口不合法时停止；最后一个合法状态正是该右端点下的最短窗口。

由于正数保证被移除的左端点不可能在未来某个更右端点下产生比当前保留左端点更短的窗口而需要回退，因此不漏解。

## 复杂度

- **时间复杂度**：`O(n)`，每个元素最多被右指针加入一次、被左指针移除一次。
- **空间复杂度**：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int minimumLength = Integer.MAX_VALUE;
        long windowSum = 0;

        for (int right = 0; right < nums.length; right++) {
            windowSum += nums[right];
            while (windowSum >= target) {
                minimumLength = Math.min(minimumLength, right - left + 1);
                windowSum -= nums[left];
                left++;
            }
        }
        return minimumLength == Integer.MAX_VALUE ? 0 : minimumLength;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        int minimumLength = Integer.MAX_VALUE;
        long windowSum = 0;

        for (int right = 0; right < nums.length; right++) {
            windowSum += nums[right];
            while (windowSum >= target) {
                minimumLength = Math.min(minimumLength, right - left + 1);
                windowSum -= nums[left];
                left++;
            }
        }
        return minimumLength == Integer.MAX_VALUE ? 0 : minimumLength;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.minSubArrayLen(7,
                new int[]{2, 3, 1, 2, 4, 3})); // 2
        System.out.println(solution.minSubArrayLen(4,
                new int[]{1, 4, 4})); // 1
        System.out.println(solution.minSubArrayLen(11,
                new int[]{1, 1, 1, 1, 1, 1, 1, 1})); // 0
    }
}
```

## 边界与易错点

- 无解时返回 `0`，不是 `Integer.MAX_VALUE`。
- 长度公式是 `right - left + 1`。
- 收缩条件为 `>= target`，不能写成 `> target`。
- 数组含负数时单调性失效，不能直接用这个窗口模板。
- 题目清单突出前缀和；本题在正数约束下滑动窗口是更优的线性解。

## 可扩展变式

- 要求 `O(n log n)`：构造严格递增的前缀和，对每个起点二分第一个满足差值的终点。
- 数组允许负数：使用前缀和 + 单调队列（LeetCode 862）。
- 求和不超过上限的最长子数组：正数条件下可用相似窗口，调整更新时机。
- 在线数据流：窗口可边读边处理，只需保存当前窗口中的值以便移除。
