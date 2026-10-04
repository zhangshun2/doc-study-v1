---
schemaVersion: 3
type: "problem"
leetcodeId: 169
slug: "majority-element"
titleCn: "多数元素"
titleEn: "Majority Element"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/majority-element/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "5f3d519528552f51ceb26f56d849350f83fc39a0c25db8ceb89efca46d79273b"
sourceFactsSha256: "f4b192d33ee938da62f1e7a17cac42d054eac57ad4860753bf24378c42384cce"
sourceSectionHashes:
  description: "56057bdd4a3353fe70eb7ba28ebeea81798a991f5a4cc842ffe6da336f763474"
  examples: "1cd633ee0690114941cb148e288a1fe89fd4b3e0c036b53256b484365d397651"
  constraints: "05b56e657f7366598f0bb6a1c31cb6dc6950cccb58bc56b48d144e2633ab323a"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "a224555416a76648724f2d9ee0ca44235a4181bed6fecf01a16c0570583c4c5d"
  signature: "78a34e93607e3236efcd4452b523be4fc600a68b058df4cf69743801dc54334a"
  javaTemplate: "b40312ca4d0b73043539b01226c1cc885660f1121944e961ab019b9165179291"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","数组","哈希表","分治","计数","排序","摩尔投票算法"]
priority: "P2"
checklistPriorities: ["P2"]
checklistTags: ["Counting 计数"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 169. 多数元素 / Majority Element

> **双轨入口：** [[核心模型/数组与哈希/169-Majority-Element-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`数组与哈希`
- 清单优先级：`P2`
- 清单代表标签：`Counting 计数`
- LeetCode 当前标签：数组 (Array)、哈希表 (Hash Table)、分治 (Divide and Conquer)、计数 (Counting)、排序 (Sorting)、摩尔投票算法
- 官方来源：<https://leetcode.cn/problems/majority-element/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`5f3d519528552f51ceb26f56d849350f83fc39a0c25db8ceb89efca46d79273b`
- **主解法**：Boyer-Moore 投票算法

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个大小为 `n`**的数组 `nums` ，返回其中的多数元素。多数元素是指在数组中出现次数 **大于** `⌊ n/2 ⌋` 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

## 官方示例


**示例 1：**

```text
输入：nums = [3,2,3]
输出：3
```

**示例 2：**

```text
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

## 官方约束


- `n == nums.length`

- `1 <= n <= 5 * 10^4`

- `-10^9 <= nums[i] <= 10^9`

- 输入保证数组中一定有一个多数元素。

**进阶：**尝试设计时间复杂度为 O(n)、空间复杂度为 O(1) 的算法解决此问题。

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 哈希计数很直接，但需要额外空间。
2. 将一个多数元素与一个非多数元素配对消去，多数元素最终仍会剩下。
3. 票数归零时，当前已处理前缀的影响可以整体抵消，重新选择候选人即可。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 进阶要求：线性时间、`O(1)` 额外空间。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [1]
输出：1
```

## 核心观察

多数元素的数量超过其他所有元素数量之和。任意删除两个不同的元素，不会改变剩余数组中的多数元素身份。Boyer-Moore 算法在线完成这种“异类配对抵消”。

## 朴素方案

- 双重循环统计每个值的次数：`O(n^2)` 时间、`O(1)` 空间。
- 哈希表计数：`O(n)` 时间、`O(n)` 空间，容易实现但没有满足进阶空间要求。
- 排序后返回 `nums[n / 2]`：`O(n log n)` 时间；多数元素必覆盖中点。

## 最优方案推导

维护 `candidate` 和 `votes`：

- `votes == 0` 时，把当前元素设为新候选人。
- 当前元素等于候选人则 `votes++`，否则 `votes--`。

票数表示在已经处理、尚未完全抵消的元素中，候选人的净优势。由于真正多数元素总数严格超过一半，它不可能被所有其他元素完全抵消，最终候选人必是它。

## 正确性与不变量

扫描过程中，可以把已处理前缀划分为若干对“值不同的已抵消元素”和 `votes` 个值为 `candidate` 的未抵消元素。当票数归零时，该前缀全部配对抵消，对后续多数判断没有影响。

对完整数组删除任意数量的异值对后，原多数元素仍至少剩一个。最终未抵消元素全等于 `candidate`，因此候选人就是题目保证存在的多数元素。

## 复杂度

- **时间复杂度**：`O(n)`，仅扫描一次。
- **空间复杂度**：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int majorityElement(int[] nums) {
        int candidate = 0;
        int votes = 0;
        for (int num : nums) {
            if (votes == 0) {
                candidate = num;
            }
            votes += (num == candidate) ? 1 : -1;
        }
        return candidate;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public int majorityElement(int[] nums) {
        int candidate = 0;
        int votes = 0;
        for (int num : nums) {
            if (votes == 0) {
                candidate = num;
            }
            votes += (num == candidate) ? 1 : -1;
        }
        return candidate;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] first = {3, 2, 3};
        int[] second = {2, 2, 1, 1, 1, 2, 2};
        System.out.println(Arrays.toString(first) + " -> "
                + solution.majorityElement(first));
        System.out.println(Arrays.toString(second) + " -> "
                + solution.majorityElement(second));
    }
}
```

## 边界与易错点

- `votes == 0` 时要先更新候选人，再根据当前元素加票。
- 算法第一轮只能产生“候选人”。本题因保证多数元素存在，可以直接返回。
- 若题目不保证存在，需要第二轮统计候选人次数并验证是否大于 `n / 2`。
- 多数的定义是“严格大于一半”，不是大于等于一半。

## 可扩展变式

- 找出现次数大于 `n / 3` 的元素：维护两个候选人与两组票数，最后二次验证。
- 一般的 `n / k`：最多维护 `k - 1` 个候选人，即 Misra-Gries 算法。
- 流式数据：投票算法可单遍处理，但若不保证多数存在，验证需要重放数据或额外计数能力。
