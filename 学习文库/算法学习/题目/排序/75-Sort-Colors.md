---
schemaVersion: 3
type: "problem"
leetcodeId: 75
slug: "sort-colors"
titleCn: "颜色分类"
titleEn: "Sort Colors"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/sort-colors/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "827adbc4ec1cd585135dd89db47cf9e71d7b4124254325b79725e08ef58ee19d"
sourceFactsSha256: "c134a307de94954e82675289d0d8453fc4145e65af8e2badff730bfab89bc81c"
sourceSectionHashes:
  description: "a044064529de5d82b23c8054ec43dd59b79df09fd9065f512b205417a4b5cbb3"
  examples: "3e5e8890a0a061e816756ba5b56c8885bd213680bc8b8df2a16ace4f41299c44"
  constraints: "b2675f4a0fddba13e10e9efa819f4578c442a711f7ce58dfe79c03c931bfd0b8"
  hints: "ebe310c0f9e0381d54bb3cf34b92cef2f93ac5268668e5c03265b84c1ec08dd1"
  tags: "fbe58771b443233df811eb4ff27cd087e52fd398584c87c6450cd96523de1248"
  signature: "28ce317d386e8629e17620f80503afa03b14e455d27b21d9add20f57c819b8f5"
  javaTemplate: "1bc5eb7d64c083c06f43777549119a5efdb61938aa13527a9708951e52d6819f"
primaryPattern: "排序"
topics: ["排序","数组","双指针","冒泡排序","快速排序"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Sorting 排序"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 75. 颜色分类 / Sort Colors

> **双轨入口：** [[核心模型/排序/75-Sort-Colors-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`排序`
- 清单优先级：`P0`
- 清单代表标签：`Sorting 排序`
- LeetCode 当前标签：数组 (Array)、双指针 (Two Pointers)、冒泡排序、排序 (Sorting)、快速排序
- 官方来源：<https://leetcode.cn/problems/sort-colors/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`827adbc4ec1cd585135dd89db47cf9e71d7b4124254325b79725e08ef58ee19d`
- 主模型：荷兰国旗三指针分区

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个包含红色、白色和蓝色、共 `n`**个元素的数组 `nums` ，**[原地](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95) **对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。

必须在不使用库内置的 sort 函数的情况下解决这个问题。

## 官方示例


**示例 1：**

输入：nums = [2,0,2,1,1,0]

输出：[0,0,1,1,2,2]

**解释：**

该数组包含两个 0、两个 1 和两个 2。将它们原地排序后，所有 0 排在最前面，接着是所有 1，最后是所有 2。

**示例 2：**

输入：nums = [2,0,1]

输出：[0,1,2]

**解释：**

数组中有且仅有一个 0、一个 1 和一个 2，按 0、1、2 的顺序原地排列。

## 官方约束


- `n == nums.length`

- `1 <= n <= 300`

- `nums[i]` 为 0、1 或 2

**进阶：**

- 你能想出一个仅使用常数空间的一趟扫描算法吗？

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. A rather straight forward solution is a two-pass algorithm using counting sort.
2. Iterate the array counting number of 0's, 1's, and 2's.
3. Overwrite array with the total number of 0's, then 1's and followed by 2's.

## 学习提示（非官方）

1. 把数组划分成“确定是 0、确定是 1、尚未处理、确定是 2”四段。
2. 当前值为 `2` 时与右侧交换，交换回来的值尚未检查，所以当前指针不能立即前进。
3. 当前值为 `0` 时与左侧交换，左侧交换回来的元素已经属于处理区，可以前进。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 进阶要求一次遍历、`O(1)` 额外空间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [0]
输出：[0]
```

## 核心观察

维护三个指针：

- `low`：下一个 `0` 应放的位置。
- `current`：当前待分类元素。
- `high`：下一个 `2` 应放的位置。

循环中保持四段结构：

```text
[0, low)          全是 0
[low, current)    全是 1
[current, high]   尚未分类
(high, n)         全是 2
```

## 朴素方案：计数后回写

遍历一次统计 `0`、`1`、`2` 的数量，再按数量覆盖数组。这也是正确且高效的方案。

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(1)`。
- 局限：需要两次遍历；没有展示通用的原地三路分区模型。

直接比较排序则为 `O(n log n)`，且违反不能调用排序函数的要求。

## 最优方案推导

检查 `nums[current]`：

- 为 `0`：与 `nums[low]` 交换，`low++`、`current++`。
- 为 `1`：位置已经正确，只执行 `current++`。
- 为 `2`：与 `nums[high]` 交换，`high--`，但 `current` 不动。

最后一点最关键：右边交换回来的可能是 `0`、`1` 或 `2`，必须在下一轮继续判断。

## 正确性与不变量

初始时四个区间除未分类区外均为空，不变量成立。每次操作都把当前未分类元素移动到它所属的确定区域，并至少让未分类区缩小一格：处理 `0` 扩大左侧零区，处理 `1` 扩大中间一区，处理 `2` 扩大右侧二区。操作不会破坏其他确定区域。当 `current > high` 时未分类区为空，整个数组按 `0、1、2` 排列。

## 复杂度

- 时间复杂度：`O(n)`，每轮都缩小未分类区，每个元素至多被常数次交换检查。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public void sortColors(int[] nums) {
        int low = 0;
        int current = 0;
        int high = nums.length - 1;

        while (current <= high) {
            if (nums[current] == 0) {
                swap(nums, low, current);
                low++;
                current++;
            } else if (nums[current] == 1) {
                current++;
            } else {
                swap(nums, current, high);
                high--;
            }
        }
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public void sortColors(int[] nums) {
        int low = 0;
        int current = 0;
        int high = nums.length - 1;

        while (current <= high) {
            if (nums[current] == 0) {
                swap(nums, low, current);
                low++;
                current++;
            } else if (nums[current] == 1) {
                current++;
            } else {
                swap(nums, current, high);
                high--;
            }
        }
    }

    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {2, 0, 2, 1, 1, 0};
        new Solution().sortColors(nums);
        System.out.println(Arrays.toString(nums));
    }
}
```

## 边界与易错点

- 循环条件必须是 `current <= high`，因为 `current == high` 时仍有一个元素未分类。
- 与 `high` 交换后不能 `current++`。
- 与 `low` 交换后可以前进，因为 `[low,current)` 在交换前全是 `1`，或两指针重合。
- 本题输入值仅三种；若可能有非法值，应显式校验而不是把所有其他值都当作 `2`。

## 可扩展变式

- 快速排序三路分区：把元素分成小于、等于、大于枢轴三段。
- 只有 `0` 和 `1`：可用左右双指针或计数。
- `k` 种颜色：计数排序需要 `O(k)` 空间；通用原地一次遍历更复杂。
- 将负数、零、正数三分类：同一不变量直接适用。
