---
schemaVersion: 3
type: "problem"
leetcodeId: 215
slug: "kth-largest-element-in-an-array"
titleCn: "数组中的第K个最大元素"
titleEn: "Kth Largest Element in an Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/kth-largest-element-in-an-array/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "8f73d3a1149d31b0acb1e740a184c6578427b346d90f56f3bfcc7eb25a289788"
sourceFactsSha256: "967606a922921e6660ca6897c5f71857d79cadb7ee47c1ece70efdee55eea582"
sourceSectionHashes:
  description: "b080c602bceba7ec85003b4b95e6a43bbc8c39e6a5094a63be85261ff3c420a7"
  examples: "d0bcf7de7d5cbf2458e4ad07764864bd0140b12cf8be771d653314824de5cb9c"
  constraints: "80c4dfb5ef01a8340609b9153eb7dbdf1b7b9b3694c2a851f35d0d2b54ff6ecd"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "486d5422a1df76e7d8710f6ac7126a5a33fb13f0475d0783833dc93f2c089110"
  signature: "737c3d6a38c1b4c0aefc7d5f106d2d05ba8585ed630b6d5a35104f9c7fa06863"
  javaTemplate: "eb1dce62d3d2c9fbc270640469139874916a75cd60d2311c5bd0242bd1a54a27"
primaryPattern: "堆与选择"
topics: ["堆与选择","数组","分治","快速选择","排序","堆（优先队列）"]
priority: "P0"
checklistPriorities: ["P0","P2"]
checklistTags: ["Sorting 排序","Heap (Priority Queue) 堆","Quickselect 快速选择"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 215. 数组中的第K个最大元素 / Kth Largest Element in an Array

> **双轨入口：** [[核心模型/堆与选择/215-Kth-Largest-Element-in-an-Array-核心模型.md|核心模型]] · [[建模专题/T0/215-Kth-Largest-Element-in-an-Array-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`堆与选择`
- 清单优先级：`P0`、`P2`
- 清单代表标签：`Sorting 排序`、`Heap (Priority Queue) 堆`、`Quickselect 快速选择`
- LeetCode 当前标签：数组 (Array)、分治 (Divide and Conquer)、快速选择 (Quickselect)、排序 (Sorting)、堆（优先队列） (Heap (Priority Queue))
- 官方来源：<https://leetcode.cn/problems/kth-largest-element-in-an-array/>
- 直观建模专题：[从反复找最大值到维护前 k 名的入选门槛](../../建模专题/T0/215-Kth-Largest-Element-in-an-Array-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`8f73d3a1149d31b0acb1e740a184c6578427b346d90f56f3bfcc7eb25a289788`
- **主解法**：随机化快速选择

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。

请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。

你必须设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

## 官方示例


**示例 1:**

```text
输入: [3,2,1,5,6,4], k = 2
输出: 5
```

**示例 2:**

```text
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
```

## 官方约束


- `1 <= k <= nums.length <= 10^5`

- `-10^4 <= nums[i] <= 10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 第 `k` 大等价于升序下标 `nums.length - k` 的元素。
2. 快排分区后，枢轴所在位置已经是其最终排序位置；只需继续处理目标所在的一侧。
3. 随机选择枢轴可以降低恶意有序输入触发最坏情况的概率。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [3,2,1,5,6,4], k = 2
输出：5
```

### 补充用例 2

```text
输入：nums = [3,2,3,1,2,4,5,5,6], k = 4
输出：4
```

### 补充用例 3

```text
输入：nums = [-1,-1], k = 2
输出：-1
```

## 核心观察

完整排序做了太多工作。本题只关心一个排名。分区操作将枢轴放到最终位置，并使左侧不大于枢轴、右侧大于枢轴。比较枢轴位置与目标下标，就能丢弃另一半候选区域。

## 朴素方案

- 排序后取 `nums[n-k]`：`O(n log n)` 时间。
- 维护大小为 `k` 的小顶堆：`O(n log k)` 时间、`O(k)` 空间，适合数据流或不能修改输入。
- 对每个元素统计比它大的数量：`O(n^2)`。

## 最优方案推导

将目标转为升序索引 `target = n - k`。在区间 `[left,right]` 中：

1. 随机选枢轴并与末尾交换。
2. 把所有 `<= pivot` 的元素交换到前部。
3. 把枢轴放在分界点 `pivotIndex`。
4. 若等于 `target` 就返回；目标更小则缩小右界，否则增大左界。

用循环代替递归，可避免递归栈。

## 正确性与不变量

每次分区结束后：`pivotIndex` 左侧元素均 `<= pivot`，右侧元素均 `> pivot`，所以枢轴在整个数组有序后的最终位置就是 `pivotIndex`。

若目标下标小于枢轴位置，目标不可能在右侧；反之亦然。每轮保留必含目标的区间且严格缩小，最终目标位置被选为枢轴并返回，其值即第 `k` 大。

## 复杂度

- **时间复杂度**：随机化后期望 `O(n)`；极端连续选到最差枢轴时最坏 `O(n^2)`。
- **空间复杂度**：`O(1)`，原地迭代分区。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.concurrent.ThreadLocalRandom;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        int target = nums.length - k;
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int pivotIndex = partition(nums, left, right);
            if (pivotIndex == target) {
                return nums[pivotIndex];
            }
            if (pivotIndex < target) {
                left = pivotIndex + 1;
            } else {
                right = pivotIndex - 1;
            }
        }
        throw new IllegalStateException("Target index must be reachable");
    }

    private int partition(int[] nums, int left, int right) {
        int randomIndex = ThreadLocalRandom.current().nextInt(left, right + 1);
        swap(nums, randomIndex, right);
        int pivot = nums[right];
        int store = left;

        for (int index = left; index < right; index++) {
            if (nums[index] <= pivot) {
                swap(nums, store, index);
                store++;
            }
        }
        swap(nums, store, right);
        return store;
    }

    private void swap(int[] nums, int first, int second) {
        int temp = nums[first];
        nums[first] = nums[second];
        nums[second] = temp;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.concurrent.ThreadLocalRandom;

class Solution {
    public int findKthLargest(int[] nums, int k) {
        int target = nums.length - k;
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int pivotIndex = partition(nums, left, right);
            if (pivotIndex == target) {
                return nums[pivotIndex];
            }
            if (pivotIndex < target) {
                left = pivotIndex + 1;
            } else {
                right = pivotIndex - 1;
            }
        }
        throw new IllegalStateException("Target index must be reachable");
    }

    private int partition(int[] nums, int left, int right) {
        int randomIndex = ThreadLocalRandom.current().nextInt(left, right + 1);
        swap(nums, randomIndex, right);
        int pivot = nums[right];
        int store = left;

        for (int index = left; index < right; index++) {
            if (nums[index] <= pivot) {
                swap(nums, store, index);
                store++;
            }
        }
        swap(nums, store, right);
        return store;
    }

    private void swap(int[] nums, int first, int second) {
        int temp = nums[first];
        nums[first] = nums[second];
        nums[second] = temp;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.findKthLargest(
                new int[]{3, 2, 1, 5, 6, 4}, 2)); // 5
        System.out.println(solution.findKthLargest(
                new int[]{3, 2, 3, 1, 2, 4, 5, 5, 6}, 4)); // 4
        System.out.println(solution.findKthLargest(
                new int[]{-1, -1}, 2)); // -1
    }
}
```

## 边界与易错点

- 第 `k` 大的升序下标是 `n - k`，不是 `k - 1`。
- 重复元素不去重；使用 `<= pivot` 仍然正确。
- 快速选择会打乱原数组；若调用方需保留，先复制。
- `nextInt(left, right + 1)` 的上界不包含，故需加一。
- 若要求严格最坏 `O(n)`，可用 median-of-medians，但实现和常数更复杂。

## 可扩展变式

- 数据流第 `k` 大：维护大小为 `k` 的小顶堆。
- 求最小的 `k` 个元素：快速选择目标下标 `k - 1`，再截取前 `k` 项。
- Top K 高频元素：先统计频率，再对频率快速选择或使用桶排序。
- 多次排名查询：一次排序更合适；快速选择适合少量查询。
