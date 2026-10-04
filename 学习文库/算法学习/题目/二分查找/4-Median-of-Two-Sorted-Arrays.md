---
schemaVersion: 3
type: "problem"
leetcodeId: 4
slug: "median-of-two-sorted-arrays"
titleCn: "寻找两个正序数组的中位数"
titleEn: "Median of Two Sorted Arrays"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/median-of-two-sorted-arrays/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "56dbe1fb5b5e47613582b96ead4938bd0b7bb0cf886518dab0661ec5e45963f6"
sourceFactsSha256: "5c409108fd36de4c1b9288f353aecfa88209022dc5225b90cec7270145e575eb"
sourceSectionHashes:
  description: "889f6339882a23f52a3067e79792caba0adf42452d25101d68e03844803bc377"
  examples: "03a9484a239dd3490d38037ad92401623b1fefca79e5a6ee4e660d67f8d8b1e1"
  constraints: "3b34b40b9de43cf4c181208cdecba0df258c3d88384da4988fe1d70c32da2176"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "ff1ff0b6a2ad205092d83b6f79aaef1fadce7ab5d4d04d29aa970ae75dae7a85"
  signature: "577859706b5a653c5d1ee31d0893ea63a96139bc25b3ade763b846e60e2c1360"
  javaTemplate: "6ec88bf14f20fce8b9f2fe3b400a9162c783ce74638c800d813925029015a499"
primaryPattern: "二分查找"
topics: ["二分查找","数组","分治"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Binary Search 二分查找","Divide and Conquer 分治"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 4. 寻找两个正序数组的中位数 / Median of Two Sorted Arrays

> **双轨入口：** [[核心模型/二分查找/4-Median-of-Two-Sorted-Arrays-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`二分查找`
- 清单优先级：`P0`
- 清单代表标签：`Binary Search 二分查找`、`Divide and Conquer 分治`
- LeetCode 当前标签：数组 (Array)、二分查找 (Binary Search)、分治 (Divide and Conquer)
- 官方来源：<https://leetcode.cn/problems/median-of-two-sorted-arrays/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`56dbe1fb5b5e47613582b96ead4938bd0b7bb0cf886518dab0661ec5e45963f6`
- 主模型：在较短数组上二分寻找合法分割线

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定两个大小分别为 `m` 和 `n` 的正序（从小到大）数组 `nums1` 和 `nums2`。请你找出并返回这两个正序数组的 **中位数** 。

算法的时间复杂度应该为 `O(log (m+n))` 。

## 官方示例


**示例 1：**

```text
输入：nums1 = [1,3], nums2 = [2]
输出：2.00000
解释：合并数组 = [1,2,3] ，中位数 2
```

**示例 2：**

```text
输入：nums1 = [1,2], nums2 = [3,4]
输出：2.50000
解释：合并数组 = [1,2,3,4] ，中位数 (2 + 3) / 2 = 2.5
```

## 官方约束


- `nums1.length == m`

- `nums2.length == n`

- `0 <= m <= 1000`

- `0 <= n <= 1000`

- `1 <= m + n <= 2000`

- `-10^6 <= nums1[i], nums2[i] <= 10^6`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 将合并序列切成左右两部分，使左半部分元素个数为 `(m+n+1)/2`。
2. 如果在数组 A 中取 `i` 个元素放左边，则数组 B 必须取 `j = half-i` 个。
3. 合法分割满足 `A左最大 <= B右最小` 且 `B左最大 <= A右最小`。
4. 始终在较短数组上二分，才能保证分割下标有效并获得 `O(log(min(m,n)))`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 题目明确要求 `O(log(m+n))`，直接合并的 `O(m+n)` 不满足进阶限制。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

不需要真的合并数组，只需要找到中位数两侧的边界。设分割后左右部分分别为：

```text
A: [0 ... i-1] | [i ... m-1]
B: [0 ... j-1] | [j ... n-1]
```

只要左侧总数正确，并且两个左侧最大值都不大于两个右侧最小值，整个左半部分就不大于右半部分。中位数只由四个边界值决定。

## 朴素方案：归并到新数组

像归并排序一样合并两个数组，再按总长度取中间值。

- 时间复杂度：`O(m+n)`。
- 空间复杂度：`O(m+n)`；若只走到中间可降到 `O(1)` 空间。
- 局限：没有达到题目要求的对数时间。

## 最优方案：分割线二分

在短数组 A 中二分 `i`，由左侧元素总数确定 `j`。使用 `Integer.MIN_VALUE` 和 `Integer.MAX_VALUE` 表示分割位于数组边缘时不存在的边界。

- 若 `aLeft > bRight`，A 左侧拿多了，`high = i - 1`。
- 若 `bLeft > aRight`，A 左侧拿少了，`low = i + 1`。
- 否则找到合法分割。

### 正确性与不变量

二分始终搜索所有可能的 A 左侧长度。`aLeft > bRight` 时，任何更大的 `i` 只会让 `aLeft` 不减、`bRight` 不增，均不可能合法，因此可以排除右半区；另一种不等式同理可排除左半区。找到合法分割时，左侧数量正确且所有左侧值不大于所有右侧值，中位数公式因此成立。

- 时间复杂度：`O(log(min(m,n)))`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.length;
        int n = nums2.length;
        int half = (m + n + 1) / 2;
        int low = 0;
        int high = m;

        while (low <= high) {
            int i = low + (high - low) / 2;
            int j = half - i;

            int aLeft = i == 0 ? Integer.MIN_VALUE : nums1[i - 1];
            int aRight = i == m ? Integer.MAX_VALUE : nums1[i];
            int bLeft = j == 0 ? Integer.MIN_VALUE : nums2[j - 1];
            int bRight = j == n ? Integer.MAX_VALUE : nums2[j];

            if (aLeft > bRight) {
                high = i - 1;
            } else if (bLeft > aRight) {
                low = i + 1;
            } else {
                int leftMax = Math.max(aLeft, bLeft);
                if ((m + n) % 2 == 1) {
                    return leftMax;
                }
                int rightMin = Math.min(aRight, bRight);
                return ((double) leftMax + rightMin) / 2.0;
            }
        }
        throw new IllegalArgumentException("Input arrays must be sorted");
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.length;
        int n = nums2.length;
        int half = (m + n + 1) / 2;
        int low = 0;
        int high = m;

        while (low <= high) {
            int i = low + (high - low) / 2;
            int j = half - i;

            int aLeft = i == 0 ? Integer.MIN_VALUE : nums1[i - 1];
            int aRight = i == m ? Integer.MAX_VALUE : nums1[i];
            int bLeft = j == 0 ? Integer.MIN_VALUE : nums2[j - 1];
            int bRight = j == n ? Integer.MAX_VALUE : nums2[j];

            if (aLeft > bRight) {
                high = i - 1;
            } else if (bLeft > aRight) {
                low = i + 1;
            } else {
                int leftMax = Math.max(aLeft, bLeft);
                if ((m + n) % 2 == 1) {
                    return leftMax;
                }
                int rightMin = Math.min(aRight, bRight);
                return ((double) leftMax + rightMin) / 2.0;
            }
        }
        throw new IllegalArgumentException("Input arrays must be sorted");
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.findMedianSortedArrays(
                new int[]{1, 3}, new int[]{2}));
        System.out.println(solution.findMedianSortedArrays(
                new int[]{1, 2}, new int[]{3, 4}));
        System.out.println(solution.findMedianSortedArrays(
                new int[]{}, new int[]{1}));
    }
}
```

## 边界与易错点

- 必须确保 A 是短数组，否则 `j` 可能越界。
- 左侧元素个数用 `(total+1)/2`，这样奇数长度时多出的一个归左侧，中位数就是 `leftMax`。
- 偶数求平均时先转 `double`，通用工程输入下可避免整数加法溢出。
- 哨兵只参与比较，不代表数组中真的加入了元素。

## 可扩展变式

- 求两个有序数组第 `k` 小元素，可每次排除约 `k/2` 个候选。
- 多个有序数组的中位数可结合值域二分与“小于等于某值的数量”统计。
- 流式数据中位数通常用一个大根堆与一个小根堆动态维护。
