---
schemaVersion: 3
type: "problem"
leetcodeId: 239
slug: "sliding-window-maximum"
titleCn: "滑动窗口最大值"
titleEn: "Sliding Window Maximum"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/sliding-window-maximum/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "f75f6afb6d338c6eae2d2fed95d418ab96375586f83e9f00f489dc5c38387a94"
sourceFactsSha256: "01cd2dc35d3e7f15e7c84aee9bfb2eb5648ebe0164ca805dcddafb408f916e6e"
sourceSectionHashes:
  description: "fdc06e6b193c82a8555e1ae26804242d60745790dd60aaaa94821ccb06ad0744"
  examples: "c71538b444b803badd8bf61739149530354d66ac048d6ca970c668ee9497403b"
  constraints: "c473c602a31e6db6c19589ae885c6611a97f0838f20ab38e0d1b7f96b57ef0ca"
  hints: "95fbf24806cfd0455f9eadc4640b1f03e908dd98263a64870a5e305a17aef513"
  tags: "69f66951bca912d73d356fe6e1372e00341b44d8633c0ed233d5c41a1728944c"
  signature: "2767034d4cfcd9a9ed1bfba2841541ea50fe37e159a82f9a7be0504ab5e9b680"
  javaTemplate: "a94e105bf7bd143e9d3f0c4ff4aa976eddd654dfe1808af67d4dc872a6919e3b"
primaryPattern: "单调结构"
topics: ["单调结构","队列","数组","滑动窗口","单调队列","堆（优先队列）","区间最值查询"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Sliding Window 滑动窗口","Queue 队列","Monotonic Queue 单调队列"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 239. 滑动窗口最大值 / Sliding Window Maximum

> **双轨入口：** [[核心模型/单调结构/239-Sliding-Window-Maximum-核心模型.md|核心模型]] · [[建模专题/T0/239-Sliding-Window-Maximum-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`单调结构`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Sliding Window 滑动窗口`、`Queue 队列`、`Monotonic Queue 单调队列`
- LeetCode 当前标签：队列 (Queue)、数组 (Array)、滑动窗口 (Sliding Window)、单调队列 (Monotonic Queue)、堆（优先队列） (Heap (Priority Queue))、区间最值查询
- 官方来源：<https://leetcode.cn/problems/sliding-window-maximum/>
- 直观建模专题：[从重复扫描到维护未来仍有资格的候选下标](../../建模专题/T0/239-Sliding-Window-Maximum-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`f75f6afb6d338c6eae2d2fed95d418ab96375586f83e9f00f489dc5c38387a94`
- **主解法**：保存下标的单调递减双端队列

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums`，有一个大小为 `k`* *的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 `k` 个数字。滑动窗口每次只向右移动一位。

返回 *滑动窗口中的最大值*。

## 官方示例


**示例 1：**

```text
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

**示例 2：**

```text
输入：nums = [1], k = 1
输出：[1]
```

## 官方约束


- `1 <= nums.length <= 10^5`

- `-10^4 <= nums[i] <= 10^4`

- `1 <= k <= nums.length`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. How about using a data structure such as deque (double-ended queue)?
2. The queue size need not be the same as the window’s size.
3. Remove redundant elements and the queue should store only elements that need to be considered.

## 学习提示（非官方）

1. 队列应保存下标而不是只保存值，才能判断元素是否已经离开窗口。
2. 新元素进入时，队尾所有不大于它的元素以后都不可能成为最大值，可以删除。
3. 队首始终是当前窗口最大值的下标。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [9,11], k = 2
输出：[11]
```

## 核心观察

某个旧元素若不大于刚进入的新元素，那么新元素更大且离开窗口更晚，旧元素从此再无成为窗口最大值的机会。删除所有这类“被支配”的下标后，候选值从队首到队尾严格递减。

## 朴素方案

每个窗口扫描 `k` 个元素求最大值，时间 `O(nk)`。用大顶堆可达 `O(n log n)`，通过延迟删除清理过期下标；可行但没有利用窗口每次只变动两个元素的结构。

## 最优方案推导

遍历右端下标 `right`：

1. 若队首下标 `< right - k + 1`，说明已离开窗口，从队首删除。
2. 队尾值 `<= nums[right]` 时不断删除队尾。
3. 把 `right` 加入队尾。
4. 当 `right >= k - 1` 时，队首值就是一个完整窗口的答案。

相等值删除旧下标是安全的，因为新下标生命周期更长。

## 正确性与不变量

每轮处理后保持：

1. 队列中的下标严格递增，且全部位于当前窗口。
2. 对应的数组值严格递减。
3. 所有被删除的队尾元素都被一个更晚且不小的元素支配，不可能成为未来最大值。

因此队首既是未过期候选中值最大的，也是当前窗口真实最大值。每个窗口输出队首即正确。

## 复杂度

- **时间复杂度**：`O(n)`；每个下标至多入队一次、从队首或队尾出队一次。
- **空间复杂度**：`O(k)`，队列最多保存一个窗口内的下标。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int[] answer = new int[nums.length - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        int answerIndex = 0;

        for (int right = 0; right < nums.length; right++) {
            int windowLeft = right - k + 1;
            while (!deque.isEmpty() && deque.peekFirst() < windowLeft) {
                deque.pollFirst();
            }
            while (!deque.isEmpty()
                    && nums[deque.peekLast()] <= nums[right]) {
                deque.pollLast();
            }
            deque.offerLast(right);

            if (right >= k - 1) {
                answer[answerIndex++] = nums[deque.peekFirst()];
            }
        }
        return answer;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int[] answer = new int[nums.length - k + 1];
        Deque<Integer> deque = new ArrayDeque<>();
        int answerIndex = 0;

        for (int right = 0; right < nums.length; right++) {
            int windowLeft = right - k + 1;
            while (!deque.isEmpty() && deque.peekFirst() < windowLeft) {
                deque.pollFirst();
            }
            while (!deque.isEmpty()
                    && nums[deque.peekLast()] <= nums[right]) {
                deque.pollLast();
            }
            deque.offerLast(right);

            if (right >= k - 1) {
                answer[answerIndex++] = nums[deque.peekFirst()];
            }
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(solution.maxSlidingWindow(
                new int[]{1, 3, -1, -3, 5, 3, 6, 7}, 3)));
        System.out.println(Arrays.toString(solution.maxSlidingWindow(
                new int[]{1}, 1)));
        System.out.println(Arrays.toString(solution.maxSlidingWindow(
                new int[]{9, 11}, 2)));
    }
}
```

## 边界与易错点

- 过期判断是 `< windowLeft`；等于左边界的下标仍在窗口中。
- 输出数组长度是 `n - k + 1`。
- 存下标才能同时访问值和判断有效期。
- `k == 1` 时每个元素都是答案；模板无需特殊处理。
- 维护的是“递减值队列”；求最小值时改为递增。

## 可扩展变式

- 滑动窗口最小值：将队尾比较改为 `>=`。
- 同时输出最大最小值：维护两个单调队列。
- 允许窗口大小动态变化：仍可清理过期下标，但需明确左右边界移动规则。
- 最短子数组和至少为 K 且允许负数：前缀和上使用单调队列，队列语义不同。
