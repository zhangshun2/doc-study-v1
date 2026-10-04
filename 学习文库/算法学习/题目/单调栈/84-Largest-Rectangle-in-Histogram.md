---
schemaVersion: 3
type: "problem"
leetcodeId: 84
slug: "largest-rectangle-in-histogram"
titleCn: "柱状图中最大的矩形"
titleEn: "Largest Rectangle in Histogram"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/largest-rectangle-in-histogram/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "07507caef42068adb86a95e1034afdc2ea46c821cd93627181d1ac56b6a8f5d1"
sourceFactsSha256: "753498798efd0ec98ef4d7e7574de7d027d2ed446ceed78f0d3b76503072c4b4"
sourceSectionHashes:
  description: "ba8ec9d343f2e76d149b4fadcd7e5748c85b8e46b59390c9007d57eb9949f42b"
  examples: "9fad1924d0f7fe006fed2c4c9c1ddcf93bac75ae7c884ea27b9086fbf30ebb7a"
  constraints: "31c8fd032832a79ed4409fbaa256437334bc9f216ed58e2872bf1eaa95f9f37e"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "08f686d285d93c6cf77c6f462fe9d0be07f9e10a331267e5f374dae5ad733a09"
  signature: "d83744c1add04581c03d744428feb9298f2e4550aaedbcc7f6b53fe4264d6e13"
  javaTemplate: "213df7119b646620ac73e735d2416b17e10ca342832bdb28b60d9de4c1bbeb91"
primaryPattern: "单调栈"
topics: ["单调栈","栈","数组","区间最值查询"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Monotonic Stack 单调栈"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 84. 柱状图中最大的矩形 / Largest Rectangle in Histogram

> **双轨入口：** [[核心模型/单调栈/84-Largest-Rectangle-in-Histogram-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`单调栈`
- 清单优先级：`P0`
- 清单代表标签：`Monotonic Stack 单调栈`
- LeetCode 当前标签：栈 (Stack)、数组 (Array)、单调栈 (Monotonic Stack)、区间最值查询
- 官方来源：<https://leetcode.cn/problems/largest-rectangle-in-histogram/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`07507caef42068adb86a95e1034afdc2ea46c821cd93627181d1ac56b6a8f5d1`
- 主模型：单调递增下标栈

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定 *n* 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。

## 官方示例


**示例 1:**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)

```text
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg)

```text
输入： heights = [2,4]
输出： 4
```

## 官方约束


- `1 <= heights.length <=10^5`

- `0 <= heights[i] <= 10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 以某根柱子高度为矩形高度时，只需找到左右两侧第一个严格更矮的柱子。
2. 维护柱高单调不降的下标栈；遇到更矮柱时，栈顶柱子的右边界被确定。
3. 弹栈之后的新栈顶是左侧第一个更矮的位置，宽度不是简单的 `i - popped`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `n` 可达 `10^5`，目标为 `O(n)` 时间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：heights = [0]
输出：0
```

## 核心观察

对于被弹出的下标 `middle`：

- 当前下标 `i` 是它右侧第一个更矮柱子的位置。
- 弹出后新的栈顶 `leftLess` 是它左侧第一个更矮柱子的位置。
- 因而高度 `heights[middle]` 能延伸的宽度为 `i - leftLess - 1`。

使用虚拟下标 `-1` 作为左哨兵，并在遍历到 `i == n` 时令当前高度为 `0`，统一清空栈中剩余柱子。

## 朴素方案：以每根柱子向两边扩展

对每个下标向左、向右寻找第一个更矮柱子，再计算最大宽度。严格递增或递减数组中，每次可能扫描很远。

- 时间复杂度：最坏 `O(n^2)`。
- 空间复杂度：`O(1)`。
- 重复点：相邻柱子寻找边界时会反复经过同一段柱子。

也可预计算左右边界，用两个数组做到 `O(n)` 时间和 `O(n)` 空间；单调栈可以在一次扫描中完成结算。

## 最优方案推导

栈中保存尚未找到右侧更矮柱子的下标，柱高保持单调不降。当当前高度小于栈顶高度时：

1. 弹出栈顶 `middle`，当前下标就是其右边界。
2. 新栈顶就是其左边界。
3. 计算 `heights[middle] * (i - stack.peek() - 1)`。
4. 持续弹出，直到单调性恢复，再压入当前下标。

相等高度可以都保留。较早的相等柱最终获得更大宽度，仍能得到正确最大值。

## 正确性与不变量

栈内下标递增、对应高度单调不降，且其中每根柱子尚未遇到右侧第一个更矮值。遇到更矮的当前柱时，所有高于它的栈顶都首次获得右边界；弹出后栈顶由于单调性是左侧最近的严格更矮位置。因此计算的是以该柱高度能达到的最大矩形，不可能通过继续向两边扩展获得更大宽度。每根柱子最终都被结算一次，取最大即全局答案。

## 复杂度

- 时间复杂度：`O(n)`，每个下标至多入栈一次、出栈一次。
- 空间复杂度：`O(n)`，最坏递增数组全部入栈。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1);
        int best = 0;

        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = i == heights.length ? 0 : heights[i];
            while (stack.peek() != -1
                    && heights[stack.peek()] > currentHeight) {
                int height = heights[stack.pop()];
                int width = i - stack.peek() - 1;
                best = Math.max(best, height * width);
            }
            stack.push(i);
        }
        return best;
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
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1);
        int best = 0;

        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = i == heights.length ? 0 : heights[i];
            while (stack.peek() != -1
                    && heights[stack.peek()] > currentHeight) {
                int height = heights[stack.pop()];
                int width = i - stack.peek() - 1;
                best = Math.max(best, height * width);
            }
            stack.push(i);
        }
        return best;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] heights = {2, 1, 5, 6, 2, 3};
        int answer = new Solution().largestRectangleArea(heights);
        System.out.println("heights = " + Arrays.toString(heights));
        System.out.println("largest area = " + answer);
    }
}
```

## 边界与易错点

- 宽度公式是 `i - stack.peek() - 1`，其中栈顶是在弹出后读取。
- 末尾需要哨兵高度 `0`，否则递增数组中的柱子不会被结算。
- 不要用 `heights[i]` 访问 `i == heights.length` 的虚拟位置。
- 高度可以为 `0`；压入多个零不影响正确性。
- 当前约束下面积不超过 `10^9`；若范围扩大，面积应使用 `long`。

## 可扩展变式

- 85. 最大矩形：逐行把二进制矩阵转成柱状图，再调用本题算法。
- 42. 接雨水：单调栈弹出时计算凹槽面积。
- 739. 每日温度：弹栈时计算下一个更大元素的距离。
- 求每个元素左右第一个更小值：分别扫描或在一次弹栈时记录边界。
