---
schemaVersion: 3
type: "problem"
leetcodeId: 300
slug: "longest-increasing-subsequence"
titleCn: "最长递增子序列"
titleEn: "Longest Increasing Subsequence"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-increasing-subsequence/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "7be1570726409ee041690df5817dea8e4f9e1b8a0ee4b44f45c52656a23f2629"
sourceFactsSha256: "ff921defc4f92f3d8b9ff5649695ed01a2ee2d85957d59e3be6f267495a26012"
sourceSectionHashes:
  description: "7946e0d3935ccabab3eee729abe5d27750026122916c79f986310b15ac467f6a"
  examples: "a6f4f08e37db2654b1dc4079f8676d738cacf1210c2cf7b810f7892539833b69"
  constraints: "02def401580033377cb1b121268920bb18be35c8221608f78896e7ec92a90879"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "208e92b3af6d48e91d4859f9105a532ae000e4c8c8f7255284e30a2bbc7aff74"
  signature: "8a04e03a9111a8af8ef2f1f5f4ce9d59b64e9374edcdfa7fb3c40abcc8667ab8"
  javaTemplate: "b6750132ab62fa73d07fb6f646c5704c69f0000d540ae17b41ff4eaa8b58740b"
primaryPattern: "动态规划"
topics: ["动态规划","数组","二分查找","最长上升子序列"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Dynamic Programming 动态规划"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 300. 最长递增子序列 / Longest Increasing Subsequence

> **双轨入口：** [[核心模型/动态规划/300-Longest-Increasing-Subsequence-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P0`
- 清单代表标签：`Dynamic Programming 动态规划`
- LeetCode 当前标签：数组 (Array)、二分查找 (Binary Search)、动态规划 (Dynamic Programming)、最长上升子序列
- 官方来源：<https://leetcode.cn/problems/longest-increasing-subsequence/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`7be1570726409ee041690df5817dea8e4f9e1b8a0ee4b44f45c52656a23f2629`
- **主解法**：贪心维护结尾值 + 二分查找

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。

**子序列 **是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列。

## 官方示例


**示例 1：**

```text
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
```

**示例 2：**

```text
输入：nums = [0,1,0,3,2,3]
输出：4
```

**示例 3：**

```text
输入：nums = [7,7,7,7,7,7,7]
输出：1
```

## 官方约束


- `1 <= nums.length <= 2500`

- `-10^4 <= nums[i] <= 10^4`

进阶：

- 你能将算法的时间复杂度降低到 `O(n log(n))` 吗?

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 基础 DP：`dp[i]` 表示以 `nums[i]` 结尾的 LIS 长度。
2. 对固定长度的递增子序列，结尾越小，未来越容易接上新元素。
3. 维护每种长度的最小结尾，结尾数组本身有序，可二分更新。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 要求严格递增，相等元素不能延长序列。
- 子序列不要求连续，但必须保持原相对顺序。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

若已经存在两个长度同为 `L` 的递增子序列，结尾分别为 6 和 10，那么结尾为 6 的序列不会比结尾为 10 的更差。只保留最小结尾即可为未来留出最大空间。

令 `tails[i]` 表示长度为 `i+1` 的递增子序列能够取得的最小结尾值。`tails` 严格递增。

## 朴素方案

枚举所有子序列有 `2^n` 种。经典 `O(n^2)` 动态规划对每个 `i` 枚举 `j < i`：若 `nums[j] < nums[i]`，用 `dp[j] + 1` 更新 `dp[i]`。它在本题约束下可通过，也是理解状态转移的重要基线。

## 最优方案推导

逐个处理 `num`，在 `tails[0..size)` 中查找第一个 `>= num` 的位置 `left`（lower bound）：

- 找到则用 `num` 替换 `tails[left]`，让该长度的结尾尽可能小。
- 若 `left == size`，说明 `num` 大于所有结尾，可以把最长长度扩展一。

替换不一定对应同一条真实子序列，但 `size` 始终是当前前缀的 LIS 长度。

## 正确性与不变量

处理完任意前缀后，`tails[i]` 是该前缀内所有长度为 `i+1` 的严格递增子序列中的最小结尾。

对新值 `num`，第一个 `>= num` 的位置之前所有结尾都小于 `num`，故可以从长度 `left` 的序列扩展出长度 `left+1`；用 `num` 更新该长度不会丢失更优选择。后面位置不能由 `num` 合法产生更长长度。若没有这样的结尾，最长序列可扩展。归纳得 `size` 等于 LIS 长度。

## 复杂度

- **时间复杂度**：`O(n log n)`，每个元素做一次二分。
- **空间复杂度**：`O(n)`，保存 `tails`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;

        for (int num : nums) {
            int left = 0;
            int right = size;
            while (left < right) {
                int middle = left + (right - left) / 2;
                if (tails[middle] < num) {
                    left = middle + 1;
                } else {
                    right = middle;
                }
            }
            tails[left] = num;
            if (left == size) {
                size++;
            }
        }
        return size;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;

        for (int num : nums) {
            int left = 0;
            int right = size;
            while (left < right) {
                int middle = left + (right - left) / 2;
                if (tails[middle] < num) {
                    left = middle + 1;
                } else {
                    right = middle;
                }
            }
            tails[left] = num;
            if (left == size) {
                size++;
            }
        }
        return size;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.lengthOfLIS(
                new int[]{10, 9, 2, 5, 3, 7, 101, 18})); // 4
        System.out.println(solution.lengthOfLIS(
                new int[]{0, 1, 0, 3, 2, 3})); // 4
        System.out.println(solution.lengthOfLIS(
                new int[]{7, 7, 7, 7, 7, 7, 7})); // 1
    }
}
```

## 边界与易错点

- 严格递增需要找第一个 `>= num` 的位置；若找第一个 `> num`，会把相等值错误地延长。
- `tails` 通常不是某一条真实 LIS，不能直接当作答案序列输出。
- 二分区间采用左闭右开 `[0,size)`，循环条件是 `left < right`。
- 只有插入位置等于 `size` 时才增加长度。

## 可扩展变式

- 输出一条 LIS：额外记录每个元素的前驱下标和各长度当前末尾下标，再回溯。
- 最长非递减子序列：二分第一个 `> num` 的位置（upper bound）。
- 最长二维递增序列：先按一维排序，另一维转化为 LIS；同值排序规则需谨慎。
- 统计 LIS 个数：使用 `O(n^2)` 的长度数组和计数数组，或线段树优化。
