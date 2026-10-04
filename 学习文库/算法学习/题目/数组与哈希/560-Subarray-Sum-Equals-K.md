---
schemaVersion: 3
type: "problem"
leetcodeId: 560
slug: "subarray-sum-equals-k"
titleCn: "和为 K 的子数组"
titleEn: "Subarray Sum Equals K"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/subarray-sum-equals-k/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "6f6e05266c57c5c41226e0b0cf1b61e647c6e5171bd7049a70a4a0ee74c5249e"
sourceFactsSha256: "1708db4719789bf75357d28017d9f5af765db4b18b5597235445665ccb921ae8"
sourceSectionHashes:
  description: "ee5903d9f7ef7256d717dbda738592ab7d6ac883a9d350bf43763128452b7895"
  examples: "4ee8a35665b2982cea199b6c2cadde236bf13c93d03dc70106bdb920c41f5e31"
  constraints: "de92e0712c736558bf23a4f447fa096b97f3566794995c534a686fd9518ea1fb"
  hints: "49f3dbcb18160132878b115769c8111964259330c3b894a1ef22729524caafe3"
  tags: "a5f94c48ea736b10557a597c4c389c12faa7ea66d6d1071c99eeeebdf754eb5a"
  signature: "aaa4922f2eb419bcfb052b1067d85fa7de96f24ac9c5de3996e6c9aded5db545"
  javaTemplate: "6dea27a944e68a502c26a40edf6f282eea284ec8a9eea776aff65e2ffda908e1"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","数组","哈希表","前缀和"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Hash Table 哈希表","Prefix Sum 前缀和"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 560. 和为 K 的子数组 / Subarray Sum Equals K

> **双轨入口：** [[核心模型/数组与哈希/560-Subarray-Sum-Equals-K-核心模型.md|核心模型]] · [[建模专题/T0/560-Subarray-Sum-Equals-K-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`数组与哈希`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Hash Table 哈希表`、`Prefix Sum 前缀和`
- LeetCode 当前标签：数组 (Array)、哈希表 (Hash Table)、前缀和 (Prefix Sum)
- 官方来源：<https://leetcode.cn/problems/subarray-sum-equals-k/>
- 直观建模专题：[从“枚举每一段”到“查询历史前缀状态”](../../建模专题/T0/560-Subarray-Sum-Equals-K-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`6f6e05266c57c5c41226e0b0cf1b61e647c6e5171bd7049a70a4a0ee74c5249e`
- **主解法**：前缀和频次哈希表

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` 和一个整数 `k` ，请你统计并返回 *该数组中和为 `k`** **的子数组的个数 *。

子数组是数组中元素的连续非空序列。

## 官方示例


**示例 1：**

```text
输入：nums = [1,1,1], k = 2
输出：2
```

**示例 2：**

```text
输入：nums = [1,2,3], k = 3
输出：2
```

## 官方约束


- `1 <= nums.length <= 2 * 10^4`

- `-1000 <= nums[i] <= 1000`

- `-10^7 <= k <= 10^7`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Will Brute force work here? Try to optimize it.
2. Can we optimize it by using some extra space?
3. What about storing sum frequencies in a hash table? Will it be useful?
4. sum(i,j)=sum(0,j)-sum(0,i), where sum(i,j) represents the sum of all the elements from index i to j-1.

Can we use this property to optimize it.

## 学习提示（非官方）

1. 令 `prefix[i]` 表示前 `i` 个元素之和，区间 `[left,right]` 的和是两个前缀和之差。
2. 当前前缀和为 `sum` 时，需要此前出现过 `sum - k`。
3. 哈希表保存前缀和的出现次数，而不是只保存是否出现。
4. 初始放入 `0 -> 1`，用于统计从下标 0 开始的合法子数组。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [1,-1,0], k = 0
输出：3
解释：[1,-1]、[0]、[1,-1,0] 均满足条件。
```

## 核心观察

若扫描到下标 `right` 时前缀和为 `sum`，某个更早前缀和为 `previous`，则其后连续区间和为：

```text
sum - previous = k  <=>  previous = sum - k
```

因此只需知道 `sum-k` 在此前出现了多少次；每一次出现对应一个不同起点。

## 朴素方案

枚举所有起点和终点并逐项求和为 `O(n^3)`。用前缀和数组可在 `O(1)` 求区间和，将总时间降为 `O(n^2)`、空间 `O(n)`。由于存在负数，窗口和对指针移动不单调，普通滑动窗口会漏解。

## 最优方案推导

初始化 `frequency.put(0,1)`、`prefix=0`、`answer=0`。逐个读取元素：

1. 更新 `prefix += num`。
2. 把 `frequency[prefix-k]` 加到答案。
3. 再将当前 `prefix` 的频次加一。

必须先查询再记录当前前缀，否则在 `k=0` 时会把空子数组错误计入。

## 正确性与不变量

处理当前元素前，哈希表准确记录从空前缀到上一个位置为止的所有前缀和频次。当前以该位置为右端点、和为 `k` 的子数组，与此前值为 `prefix-k` 的前缀一一对应，所以增加该频次既不漏也不重。随后记录当前前缀，为后续右端点服务。不变量归纳保持，最终答案是全部合法子数组数。

## 复杂度

- **时间复杂度**：期望 `O(n)`，每个元素进行常数次哈希操作。
- **空间复杂度**：`O(n)`，最坏每个前缀和都不同。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> frequency = new HashMap<>();
        frequency.put(0, 1);
        int prefix = 0;
        int answer = 0;

        for (int num : nums) {
            prefix += num;
            answer += frequency.getOrDefault(prefix - k, 0);
            frequency.merge(prefix, 1, Integer::sum);
        }
        return answer;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> frequency = new HashMap<>();
        frequency.put(0, 1);
        int prefix = 0;
        int answer = 0;

        for (int num : nums) {
            prefix += num;
            answer += frequency.getOrDefault(prefix - k, 0);
            frequency.merge(prefix, 1, Integer::sum);
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.subarraySum(
                new int[]{1, 1, 1}, 2)); // 2
        System.out.println(solution.subarraySum(
                new int[]{1, 2, 3}, 3)); // 2
        System.out.println(solution.subarraySum(
                new int[]{1, -1, 0}, 0)); // 3
    }
}
```

## 边界与易错点

- 初始化 `0 -> 1` 不可缺少，否则漏掉从数组起点开始的区间。
- 存频次而不是布尔值；同一前缀和可能多次出现，每次都对应不同起点。
- 先查后存，避免把长度为 0 的区间计入。
- 负数使滑动窗口失效，不要套用“和超了就缩左端”的模板。
- 当前约束下 `int` 足够；若数组和值范围扩大，应使用 `long` 作为前缀和及 map 键。

## 可扩展变式

- 求和为 `k` 的最长子数组：哈希表保存每个前缀和首次出现下标。
- 判断是否存在：哈希集合保存此前前缀和，命中即可返回。
- 二维矩阵和为 `k` 的子矩阵数：压缩行区间为一维数组，再应用本模板。
- 和能被 `k` 整除：统计前缀和模 `k` 的频次，并规范化负余数。
