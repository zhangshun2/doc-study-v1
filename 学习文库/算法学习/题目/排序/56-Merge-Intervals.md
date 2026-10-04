---
schemaVersion: 3
type: "problem"
leetcodeId: 56
slug: "merge-intervals"
titleCn: "合并区间"
titleEn: "Merge Intervals"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/merge-intervals/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "1e38974de587578f75aa3bd186d6ad591714f04ea1f287a6cb34d189cf35a734"
sourceFactsSha256: "288c6343904b13a72ff52e5eeab227a15eb96577b8fd5fd1baf849e63d94ddf0"
sourceSectionHashes:
  description: "2c385bfe5e7eeaf24104c886ba406c353deb27b96770ac034a40522fe154f27c"
  examples: "c6b562ece04910b485d95f66ff0474e1f6bdc61338e469d27801f81c69f8a35d"
  constraints: "5a106c56632e99d5a33e299e09a5de63d04276ad258eebc326b53b11090257df"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "411190fe64aad93808f795689e71ef3912fad775ea95fffdea7603e867ee106d"
  signature: "1ceed6b4db0b37d3f122aaca1c21ac6cd1d10fe46b9f3a175c58fec71e315ddc"
  javaTemplate: "2b54fecb949c5b2c680f3141ef1640f7626e135d537301422f24ff97c87f259b"
primaryPattern: "排序"
topics: ["排序","数组","快速排序"]
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
# 56. 合并区间 / Merge Intervals

> **双轨入口：** [[核心模型/排序/56-Merge-Intervals-核心模型.md|核心模型]] · [[建模专题/T0/56-Merge-Intervals-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`排序`
- 清单优先级：`P0`
- 清单代表标签：`Sorting 排序`
- LeetCode 当前标签：数组 (Array)、排序 (Sorting)、快速排序
- 官方来源：<https://leetcode.cn/problems/merge-intervals/>
- 直观建模专题：[从“反复比较任意两段”到“维护一个未封口合并块”](../../建模专题/T0/56-Merge-Intervals-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`1e38974de587578f75aa3bd186d6ad591714f04ea1f287a6cb34d189cf35a734`
- 主模型：按左端点排序后线性合并

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [start_i, end_i]` 。请你合并所有重叠的区间，并返回 *一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间* 。

## 官方示例


**示例 1：**

```text
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
```

**示例 2：**

```text
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
```

**示例 3：**

```text
输入：intervals = [[4,7],[1,4]]
输出：[[1,7]]
解释：区间 [1,4] 和 [4,7] 可被视为重叠区间。
```

## 官方约束


- `1 <= intervals.length <= 10^4`

- `intervals[i].length == 2`

- `0 <= start_i <= end_i <= 10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 区间按左端点升序后，后一个区间只需与当前合并结果的最后一个比较。
2. 重叠条件是 `nextStart <= currentEnd`，不是严格小于。
3. 重叠时左端点不变，右端点更新为两者最大值。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 排序是主要成本，目标时间复杂度为 `O(n log n)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：intervals = [[1,4],[2,3]]
输出：[[1,4]]
解释：第二个区间完全被第一个区间包含。
```

## 核心观察

排序后，尚未处理区间的左端点不会比当前区间更小。设当前合并区间为 `[L,R]`，下一个为 `[a,b]`：

- `a <= R`：两个区间重叠或相接，合并成 `[L,max(R,b)]`。
- `a > R`：后续区间的左端点只会更大，因此 `[L,R]` 不会再与后面重叠，可以安全输出。

## 朴素方案：反复两两合并

不断扫描所有区间对，发现重叠就删除两个旧区间并加入合并结果，直到没有变化。一次合并可能触发重新扫描。

- 时间复杂度：最坏 `O(n^2)`，若动态数组删除和移动也计入，代价更高。
- 空间复杂度：通常 `O(n)`。
- 局限：没有利用区间左端点的有序性。

## 最优方案推导

先按左端点排序，将第一个区间作为当前候选：

1. 与候选重叠时扩张候选的右端点。
2. 不重叠时输出候选，并让新区间成为候选。
3. 遍历结束后加入最后一个候选。

下面使用两个整数保存候选并在输出时创建数组，避免输出结果与输入子数组共享引用。

## 正确性与不变量

处理前 `i` 个排序区间后，结果列表中的区间互不重叠并完整覆盖这 `i` 个区间；当前候选是唯一可能与下一个区间重叠的部分。因为左端点有序，当下一区间与候选不重叠时，它也不可能与更早且已经封闭的区间重叠。每一步合并或输出都保持该不变量，最终结果完整且两两不重叠。

## 复杂度

- 时间复杂度：`O(n log n)`，排序占主导，扫描为 `O(n)`。
- 空间复杂度：`O(n)` 用于返回结果；Java 对对象数组排序还可能使用线性辅助空间。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> merged = new ArrayList<>();
        int currentStart = intervals[0][0];
        int currentEnd = intervals[0][1];

        for (int i = 1; i < intervals.length; i++) {
            int nextStart = intervals[i][0];
            int nextEnd = intervals[i][1];
            if (nextStart <= currentEnd) {
                currentEnd = Math.max(currentEnd, nextEnd);
            } else {
                merged.add(new int[] {currentStart, currentEnd});
                currentStart = nextStart;
                currentEnd = nextEnd;
            }
        }
        merged.add(new int[] {currentStart, currentEnd});
        return merged.toArray(new int[merged.size()][]);
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> merged = new ArrayList<>();
        int currentStart = intervals[0][0];
        int currentEnd = intervals[0][1];

        for (int i = 1; i < intervals.length; i++) {
            int nextStart = intervals[i][0];
            int nextEnd = intervals[i][1];
            if (nextStart <= currentEnd) {
                currentEnd = Math.max(currentEnd, nextEnd);
            } else {
                merged.add(new int[] {currentStart, currentEnd});
                currentStart = nextStart;
                currentEnd = nextEnd;
            }
        }
        merged.add(new int[] {currentStart, currentEnd});
        return merged.toArray(new int[merged.size()][]);
    }
}

public class Main {
    public static void main(String[] args) {
        int[][] intervals = {{1, 3}, {2, 6}, {8, 10}, {15, 18}};
        int[][] answer = new Solution().merge(intervals);
        System.out.println(Arrays.deepToString(answer));
    }
}
```

## 边界与易错点

- 相接区间要合并，因此条件为 `nextStart <= currentEnd`。
- 完全包含时，右端点必须取 `max`，不能直接赋为 `nextEnd`。
- 循环结束后要把最后一个候选加入结果。
- 比较器使用 `Integer.compare`，避免大整数相减溢出。
- `Arrays.sort` 会改变输入排列；若调用方要求输入不变，应先深复制。

## 可扩展变式

- 57. 插入区间：输入已有序且互不重叠，可边扫描边插入。
- 435. 无重叠区间：按右端点排序，贪心保留结束最早的区间。
- 252/253. 会议室：判断冲突或计算最大同时会议数。
- 区间交集（986）：两个有序区间列表使用双指针。
