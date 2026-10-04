---
schemaVersion: 3
type: "problem"
leetcodeId: 34
slug: "find-first-and-last-position-of-element-in-sorted-array"
titleCn: "在排序数组中查找元素的第一个和最后一个位置"
titleEn: "Find First and Last Position of Element in Sorted Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "4e76abd4f2e10e15c370d721a31b81e09f8c0d61e2c34e7ba1a4191c274f9d33"
sourceFactsSha256: "4fae36e4ca276a41b42c38895c4c0d38872ddc4b78563dffc610a85203707502"
sourceSectionHashes:
  description: "11a8bb9f0704a89941d0060ab7366ef66c8ce1e75ed7cc85277465f5b0277a73"
  examples: "81ec0b24b6ef04675cf88c0668bf28d0f38aecc171c59c30a276d90abfdee3fb"
  constraints: "41ee6c9de206629b20a5fbe5ee807ce93afaca43ad719eaee421051d4425e359"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "627d17842be8001c5ad93db5fb84aa0fb45086f17bd41b33b5240354bef91285"
  signature: "b8bb27cbbcdb21afc9f93dc738696d35c9fcde987a7df6638e49fb23965e5b5f"
  javaTemplate: "1af8068ec7565261d318a5fddc1cf268de4d5c7d757fc1e1d48c090cb492c11c"
primaryPattern: "二分查找"
topics: ["二分查找","数组"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Binary Search 二分查找"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 34. 在排序数组中查找元素的第一个和最后一个位置 / Find First and Last Position of Element in Sorted Array

> **双轨入口：** [[核心模型/二分查找/34-Find-First-and-Last-Position-of-Element-in-Sorted-Array-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`二分查找`
- 清单优先级：`P0`
- 清单代表标签：`Binary Search 二分查找`
- LeetCode 当前标签：数组 (Array)、二分查找 (Binary Search)
- 官方来源：<https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`4e76abd4f2e10e15c370d721a31b81e09f8c0d61e2c34e7ba1a4191c274f9d33`
- 主模型：两次边界二分（lower bound / upper bound）

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个按照非递减顺序排列的整数数组 `nums`，和一个目标值 `target`。请你找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 `target`，返回 `[-1, -1]`。

你必须设计并实现时间复杂度为 `O(log n)` 的算法解决此问题。

## 官方示例


**示例 1：**

```text
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
```

**示例 2：**

```text
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
```

**示例 3：**

```text
输入：nums = [], target = 0
输出：[-1,-1]
```

## 官方约束


- `0 <= nums.length <= 10^5`

- `-10^9 <= nums[i] <= 10^9`

- `nums` 是一个非递减数组

- `-10^9 <= target <= 10^9`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 普通二分命中任意一个目标位置后不要停止，要继续向边界搜索。
2. 第一个位置是“第一个大于等于 `target` 的下标”。
3. 最后一个位置可以通过“第一个大于 `target` 的下标减一”得到。
4. 使用左闭右开区间 `[left,right)` 能统一处理空数组和答案位于 `n` 的情况。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 必须达到 `O(log n)`，找到一次后向两侧线性扩张在最坏情况下是 `O(n)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

有序数组中的同值元素形成连续区间。问题可拆成两个单调边界：

```text
first = lowerBound(target)       // 第一个 >= target
afterLast = upperBound(target)   // 第一个 > target
last = afterLast - 1
```

如果 `first == n` 或 `nums[first] != target`，目标不存在。

## 朴素方案：线性扫描或命中后扩张

从左到右记录首尾位置是 `O(n)`。普通二分找到一个目标后再向左右逐个扩张，在数组全等时仍需 `O(n)`，不满足要求。

- 时间复杂度：最坏 `O(n)`。
- 空间复杂度：`O(1)`。

## 最优方案：两次边界二分

`lowerBound` 遇到 `nums[mid] >= target` 时保留 `mid` 并向左找，否则向右；`upperBound` 遇到 `nums[mid] <= target` 时向右，否则保留 `mid` 并向左。两者最终都在 `[0,n]` 返回一个插入位置。

### 正确性与不变量

`lowerBound` 始终保持 `[0,left)` 中元素小于目标，而 `[right,n)` 中元素大于等于目标；区间收缩到空时 `left==right`，正是第一个大于等于目标的位置。`upperBound` 对称地保持左侧元素小于等于目标、右侧元素大于目标。因此当目标存在时，两边界围出的闭区间恰好包含全部目标值；不存在时的显式校验会返回 `[-1,-1]`。

- 时间复杂度：两次二分均为 `O(log n)`，总体 `O(log n)`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int[] searchRange(int[] nums, int target) {
        int first = lowerBound(nums, target);
        if (first == nums.length || nums[first] != target) {
            return new int[]{-1, -1};
        }
        int afterLast = upperBound(nums, target);
        return new int[]{first, afterLast - 1};
    }

    private int lowerBound(int[] nums, int target) {
        int left = 0;
        int right = nums.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] >= target) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    private int upperBound(int[] nums, int target) {
        int left = 0;
        int right = nums.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

public class Solution {
    public int[] searchRange(int[] nums, int target) {
        int first = lowerBound(nums, target);
        if (first == nums.length || nums[first] != target) {
            return new int[]{-1, -1};
        }
        int afterLast = upperBound(nums, target);
        return new int[]{first, afterLast - 1};
    }

    private int lowerBound(int[] nums, int target) {
        int left = 0;
        int right = nums.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] >= target) {
                right = mid;
            } else {
                left = mid + 1;
            }
        }
        return left;
    }

    private int upperBound(int[] nums, int target) {
        int left = 0;
        int right = nums.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(solution.searchRange(
                new int[]{5, 7, 7, 8, 8, 10}, 8))); // [3, 4]
        System.out.println(Arrays.toString(solution.searchRange(
                new int[]{5, 7, 7, 8, 8, 10}, 6))); // [-1, -1]
        System.out.println(Arrays.toString(solution.searchRange(
                new int[]{}, 0)));                    // [-1, -1]
    }
}
```

## 边界与易错点

- `lowerBound` 可能返回 `nums.length`，访问数组前必须检查。
- 不要用 `lowerBound(target+1)-1` 的写法处理任意 `int` 目标，`target+1` 可能溢出；单独实现 `upperBound` 更稳健。
- 左闭右开模板中 `right` 初值是 `nums.length`，循环为 `left < right`。
- 找到一个目标立即返回只能得到任意位置，无法保证是边界。

## 可扩展变式

- 目标出现次数为 `upperBound-lowerBound`。
- 有序数组插入位置就是 `lowerBound`。
- 在值域上二分答案时，也常把判定函数转换成“第一个满足条件的位置”。
