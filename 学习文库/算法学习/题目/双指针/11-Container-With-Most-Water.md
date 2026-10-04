---
schemaVersion: 3
type: "problem"
leetcodeId: 11
slug: "container-with-most-water"
titleCn: "盛最多水的容器"
titleEn: "Container With Most Water"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/container-with-most-water/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "ab88d24e356091a35a8cd2cd4b2f9c82d6914392848c100738fa704b9a34b577"
sourceFactsSha256: "829357544b8af653c7cb84a6b9c8fefc1b5d49f71fb9174d3e6f414574f39f62"
sourceSectionHashes:
  description: "c1088ed0345bbc0323728d8a47a3e52fbd0e2213a254683496ec6a1278c9234a"
  examples: "a7728f63e1fff26dc7e4ac9d78fde6de6366af9b8924d4def496c57b3ae233c8"
  constraints: "f77c567c41a8444cdaa3ed9a071a6a739ac1488c4c209f74950772f0faa5a034"
  hints: "f6807e12eaf4daf39aff8461b5b1752dc94f031cd8c26073985da1309e4e2514"
  tags: "25b44688c95072ff8891f9cd20712f9076325c5c27d317d86cc02819f7ecfa8b"
  signature: "5c2451b722b757109575ed884d5ee0eab511b91eafe1d1b8350624f2e000377d"
  javaTemplate: "72a4c399ef062ffe215983c921d83f191e046547f375531401acffcdc063809b"
primaryPattern: "双指针"
topics: ["双指针","贪心","数组"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Two Pointers 双指针","Greedy 贪心"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 11. 盛最多水的容器 / Container With Most Water

> **双轨入口：** [[核心模型/双指针/11-Container-With-Most-Water-核心模型.md|核心模型]] · [[建模专题/T0/11-Container-With-Most-Water-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`双指针`
- 清单优先级：`P0`
- 清单代表标签：`Two Pointers 双指针`、`Greedy 贪心`
- LeetCode 当前标签：贪心 (Greedy)、数组 (Array)、双指针 (Two Pointers)
- 官方来源：<https://leetcode.cn/problems/container-with-most-water/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`ab88d24e356091a35a8cd2cd4b2f9c82d6914392848c100738fa704b9a34b577`
- 主模型：左右双指针排除不可能更优的边界

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个长度为 `n` 的整数数组 `height` 。有 `n` 条垂线，第 `i` 条线的两个端点是 `(i, 0)` 和 `(i, height[i])` 。

找出其中的两条线，使得它们与 `x` 轴共同构成的容器可以容纳最多的水。

返回容器可以储存的最大水量。

**说明：**你不能倾斜容器。

## 官方示例


**示例 1：**

![Official problem illustration](https://aliyun-lc-upload.oss-cn-hangzhou.aliyuncs.com/aliyun-lc-upload/uploads/2018/07/25/question_11.jpg)

```text
输入：[1,8,6,2,5,4,8,3,7]
输出：49
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。
```

**示例 2：**

```text
输入：height = [1,1]
输出：1
```

## 官方约束


- `n == height.length`

- `2 <= n <= 10^5`

- `0 <= height[i] <= 10^4`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. If you simulate the problem, it will be O(n^2) which is not efficient.
2. Try to use two-pointers. Set one pointer to the left and one to the right of the array. Always move the pointer that points to the lower line.
3. How can you calculate the amount of water at each step?

## 学习提示（非官方）

1. 一对边界的面积是 `(right-left) * min(height[left],height[right])`。
2. 从最宽的容器开始考察。
3. 若移动较高边界，宽度变小且短板不可能升高；该方向不可能得到更大面积。
4. 因此每次移动较短边界，尝试寻找更高的短板。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `n` 达到 `10^5`，枚举所有边界对的 `O(n^2)` 会超时。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：height = [1,8,6,2,5,4,8,3,7]
输出：49
解释：选择下标 1 和 8，高度下限为 7，宽度为 7，面积为 7 * 7 = 49。
```

## 核心观察

面积同时受宽度和短板控制。左右指针初始拥有最大宽度。假设 `height[left] <= height[right]`，保持 `left` 不动而把 `right` 左移：新宽度更小，新高度仍不超过 `height[left]`，所以面积一定不超过当前面积。于是所有以当前 `left` 为左边界、右端位于内部的方案都可一次排除，应移动 `left`。

## 朴素方案：枚举所有边界对

两层循环枚举 `left < right`，按公式计算并更新最大面积。

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(1)`。
- 局限：`10^5` 个元素时最多约 50 亿对。

## 最优方案：相向双指针

指针从两端开始，每轮先计算当前面积，然后移动高度较小的一侧。相等时移动任意一侧都不会漏掉更优解；代码选择移动右侧。

### 正确性与不变量

当前区间外的边界组合均已被证明不可能优于已记录答案。每轮若左边较短，所有使用该左边界和更靠内右边界的容器，宽度更小且高度上限不变，因此都不可能超过当前容器，可以安全排除左边界。右边较短时对称成立。算法不断安全排除一个边界，直至所有候选均已计算或被支配，`best` 即全局最优值。

- 时间复杂度：`O(n)`，每个指针最多移动 `n-1` 次。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int best = 0;

        while (left < right) {
            int width = right - left;
            int limitedHeight = Math.min(height[left], height[right]);
            best = Math.max(best, width * limitedHeight);

            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return best;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int best = 0;

        while (left < right) {
            int width = right - left;
            int limitedHeight = Math.min(height[left], height[right]);
            best = Math.max(best, width * limitedHeight);

            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.maxArea(
                new int[]{1, 8, 6, 2, 5, 4, 8, 3, 7})); // 49
        System.out.println(solution.maxArea(new int[]{1, 1})); // 1
        System.out.println(solution.maxArea(new int[]{4, 3, 2, 1, 4})); // 16
    }
}
```

## 边界与易错点

- 高度用 `min`，不是 `max`；水会从较短边界溢出。
- 宽度是下标差 `right-left`，不是元素个数 `right-left+1`。
- 必须移动短板；“移动高板保留短板”没有增大高度上限的可能。
- 这道题求两个边界之间的一整块面积，与“接雨水”逐列累加不是同一问题。

## 可扩展变式

- 返回最佳边界下标时，在更新 `best` 的同时记录 `left`、`right`。
- 接雨水同样使用双指针，但维护的是左右历史最大高度并逐列结算。
- 若横坐标并非等距，宽度改为 `x[right]-x[left]`，排除证明仍可沿用。
