---
schemaVersion: 3
type: "problem"
leetcodeId: 287
slug: "find-the-duplicate-number"
titleCn: "寻找重复数"
titleEn: "Find the Duplicate Number"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/find-the-duplicate-number/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "a65273f0499cd050712bf93e1319780f04585dc6ea5e0a035424efbd5683d89b"
sourceFactsSha256: "40d8542d22206458b7ab6ebb5c11c3e79f418ec8db3cf1a030a3219fa1cef516"
sourceSectionHashes:
  description: "343289bd70870b17464ec6a5183a3026634e4a94892e215c3e8efb2fba5043fa"
  examples: "44db0e661c06b9a1ca9ae386fc64efab495940383e802bf897d360b0e440f229"
  constraints: "3bed0333274a25d3a781eb2781b87892171f765a07006efdc32c73216f1f5500"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "22717d32071180a0d62f6454db1429ede055914ef23cf37db237245a6fcf7958"
  signature: "df612c7bee54ea07e9b0b0230928faf0a4f4989bdc57764c3d6baf16aab152ae"
  javaTemplate: "d18ad9e7854f1b1d22bd5a8a3ae466b6c3f35155ba0a50080cda0d6ad94c56fa"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","位运算","数组","双指针","二分查找","Floyd 判圈算法","抽屉原理"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Bit Manipulation 位运算"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 287. 寻找重复数 / Find the Duplicate Number

> **双轨入口：** [[核心模型/数组与哈希/287-Find-the-Duplicate-Number-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`数组与哈希`
- 清单优先级：`P1`
- 清单代表标签：`Bit Manipulation 位运算`
- LeetCode 当前标签：位运算 (Bit Manipulation)、数组 (Array)、双指针 (Two Pointers)、二分查找 (Binary Search)、Floyd 判圈算法、抽屉原理
- 官方来源：<https://leetcode.cn/problems/find-the-duplicate-number/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`a65273f0499cd050712bf93e1319780f04585dc6ea5e0a035424efbd5683d89b`
- **主解法**：Floyd 快慢指针判环

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个包含 `n + 1` 个整数的数组 `nums` ，其数字都在 `[1, n]` 范围内（包括 `1` 和 `n`），可知至少存在一个重复的整数。

假设 `nums` 只有 **一个重复的整数** ，返回 **这个重复的数** 。

你设计的解决方案必须 **不修改** 数组 `nums` 且只用常量级 `O(1)` 的额外空间。

## 官方示例


**示例 1：**

```text
输入：nums = [1,3,4,2,2]
输出：2
```

**示例 2：**

```text
输入：nums = [3,1,3,4,2]
输出：3
```

**示例 3 :**

```text
输入：nums = [3,3,3,3,3]
输出：3
```

## 官方约束


- `1 <= n <= 10^5`

- `nums.length == n + 1`

- `1 <= nums[i] <= n`

- `nums` 中 **只有一个整数** 出现 **两次或多次** ，其余整数均只出现 **一次**

进阶：

- 如何证明 `nums` 中至少存在一个重复的数字?

- 你可以设计一个线性级时间复杂度 `O(n)` 的解决方案吗？

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 将数组下标看作节点，将 `i -> nums[i]` 看作一条有向边。
2. 值始终在 `[1,n]`，从下标 0 出发会不断进入合法下标且最终成环。
3. 重复值意味着至少两个不同下标指向同一个节点，该节点正是环入口。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 不允许修改 `nums`，且只用常量额外空间。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

函数图中每个节点只有一个后继。数组有 `n + 1` 个位置但值只有 `n` 种，根据抽屉原理存在重复指向。从 0 沿 `nums[index]` 前进，会形成“链尾 + 环”。重复数就是环入口，可用 Floyd 算法在 `O(1)` 空间找到。

## 朴素方案

- 哈希集合记录已见元素：`O(n)` 时间、`O(n)` 空间，不满足空间要求。
- 排序后找相邻重复：`O(n log n)` 且会修改输入；复制后排序又需 `O(n)` 空间。
- 对每个值计数：`O(n)` 额外空间。
- 按值域二分计数可在 `O(n log n)` 时间、`O(1)` 空间完成，是不使用判环时的稳妥方案。

## 最优方案推导

第一阶段找相遇点：慢指针每次走一步 `slow = nums[slow]`，快指针每次走两步 `fast = nums[nums[fast]]`。两者必在环内相遇。

第二阶段找入口：令一个指针回到 0，两个指针都每次走一步，再次相遇的位置就是环入口，也就是重复数。

初始化采用 `slow = nums[0]`、`fast = nums[0]` 并用 `do-while`，确保指针至少移动一次。

## 正确性与不变量

设从起点到环入口距离为 `a`，入口到首次相遇点距离为 `b`，环长为 `c`。相遇时慢指针走了 `a+b`，快指针走了其两倍，二者路程差是若干整环：

```text
2(a+b) - (a+b) = a+b = k*c
```

所以 `a = k*c - b`，即从相遇点再走 `a` 步恰好绕到入口。从 0 出发的指针也在 `a` 步到入口，两者必在那里相遇。环入口因多条边指向它，对应唯一重复值。

## 复杂度

- **时间复杂度**：`O(n)`。
- **空间复杂度**：`O(1)`。
- **输入影响**：不修改数组。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0];
        int fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        int finder = nums[0];
        while (finder != slow) {
            finder = nums[finder];
            slow = nums[slow];
        }
        return finder;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0];
        int fast = nums[0];
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);

        int finder = nums[0];
        while (finder != slow) {
            finder = nums[finder];
            slow = nums[slow];
        }
        return finder;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.findDuplicate(
                new int[]{1, 3, 4, 2, 2})); // 2
        System.out.println(solution.findDuplicate(
                new int[]{3, 1, 3, 4, 2})); // 3
        System.out.println(solution.findDuplicate(
                new int[]{3, 3, 3, 3, 3})); // 3
    }
}
```

## 边界与易错点

- 这里的“节点”是数组下标，下一节点是数组值，不是在普通链表上操作。
- 二阶段起点可一致使用 `nums[0]`；若采用另一套以 0 为起点的初始化，公式和代码要成套，避免混搭。
- 题目保证值在 `[1,n]`，所以 `nums[nums[fast]]` 不越界。
- 不能通过把访问过的元素改为负数来标记，那会违反“不修改数组”。
- 清单把本题列在位运算；位计数也可解，但 Floyd 在本约束下更简洁。

## 可扩展变式

- 链表环入口：同一个 Floyd 两阶段模板。
- 只允许多次扫描、不允许随机访问：Floyd 依赖按值跳转，不适用于纯流式输入。
- 找全部重复数：唯一重复的函数图模型不再直接适用，需哈希、排序或原地标记等其他方案。
- 值域计数二分：统计 `<= mid` 的元素数是否大于 `mid`，利用抽屉原理缩小答案范围。
