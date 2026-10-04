---
schemaVersion: 3
type: "problem"
leetcodeId: 33
slug: "search-in-rotated-sorted-array"
titleCn: "搜索旋转排序数组"
titleEn: "Search in Rotated Sorted Array"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/search-in-rotated-sorted-array/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "20df2be1d0b62e2502b4e7a10c9ec27a18c7845515726727744eb4aae03948fb"
sourceFactsSha256: "4ca0d92f6ff1a8f1224dd4b852b24a4b88fd7396ca40c7d40f58d2c424c4638e"
sourceSectionHashes:
  description: "8718246d164ad43dd90f76481f959ffcc6166bfaff41e65c611ceb2a8715af4b"
  examples: "bd50b96cae2ecedae2785c3a4dcad642bf789ee3c8bd53400084a3027421c044"
  constraints: "ee8145e9ad075c20fe590a9b18c9abeb0a915d343fec6d3953691d1fe0638526"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "627d17842be8001c5ad93db5fb84aa0fb45086f17bd41b33b5240354bef91285"
  signature: "db80a0fefc8e2f37f14975f4c2729dc95a875b485e11ef7abaefac0853abed9f"
  javaTemplate: "c0b901bb35c29a818930dad470b557c749988d2334f4c4a80cd7da31becc3c8d"
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
# 33. 搜索旋转排序数组 / Search in Rotated Sorted Array

> **双轨入口：** [[核心模型/二分查找/33-Search-in-Rotated-Sorted-Array-核心模型.md|核心模型]] · [[建模专题/T0/33-Search-in-Rotated-Sorted-Array-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`二分查找`
- 清单优先级：`P0`
- 清单代表标签：`Binary Search 二分查找`
- LeetCode 当前标签：数组 (Array)、二分查找 (Binary Search)
- 官方来源：<https://leetcode.cn/problems/search-in-rotated-sorted-array/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`20df2be1d0b62e2502b4e7a10c9ec27a18c7845515726727744eb4aae03948fb`
- 主模型：二分判断哪一半有序，再排除不含目标的一半
- 直观建模专题：[从整体旋转到每轮至少一半有序](../../建模专题/T0/33-Search-in-Rotated-Sorted-Array-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

整数数组 `nums` 按升序排列，数组中的值 **互不相同** 。

在传递给函数之前，`nums` 在预先未知的某个下标 `k`（`0 <= k < nums.length`）上进行了 **向左旋转**，使数组变为 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]`（下标 **从 0 开始** 计数）。例如， `[0,1,2,4,5,6,7]` 下标 `3` 上向左旋转后可能变为 `[4,5,6,7,0,1,2]` 。

给你 **旋转后** 的数组 `nums` 和一个整数 `target` ，如果 `nums` 中存在这个目标值 `target` ，则返回它的下标，否则返回 `-1` 。

你必须设计一个时间复杂度为 `O(log n)` 的算法解决此问题。

## 官方示例


**示例 1：**

```text
输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
```

**示例 2：**

```text
输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
```

**示例 3：**

```text
输入：nums = [1], target = 0
输出：-1
```

## 官方约束


- `1 <= nums.length <= 5000`

- `-10^4 <= nums[i] <= 10^4`

- `nums` 中的每个值都 **独一无二**

- 题目数据保证 `nums` 在预先未知的某个下标上进行了旋转

- `-10^4 <= target <= 10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 任意二分区间中，以 `mid` 分割后至少有一半仍然有序。
2. 用 `nums[left] <= nums[mid]` 判断左半段是否有序。
3. 确定有序半段后，可以用边界比较判断 `target` 是否位于其中。
4. 目标不在该有序半段，就去另一半；每轮都排除一半候选。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 必须达到 `O(log n)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

旋转只制造了一个“下降断点”。一个区间被中点切开时，断点最多落在其中一半，所以另一半必然保持有序。只要找出有序的一半，就能判断目标是否在这个值域中，从而恢复二分的排除能力。

## 朴素方案：线性扫描

从头到尾比较每个元素，找到目标返回下标。

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(1)`。
- 局限：没有满足对数时间要求。

也可先二分找旋转点，再做一次普通二分，仍为 `O(log n)`；但需要两个阶段。

## 最优方案：一次改造二分

每轮先检查 `nums[mid]`。若左半有序，判断 `target` 是否满足 `nums[left] <= target < nums[mid]`；满足就收缩到左半，否则去右半。若右半有序，则使用 `nums[mid] < target <= nums[right]` 对称判断。

### 正确性与不变量

循环开始时，如果目标存在，它一定在闭区间 `[left,right]`。因为元素互异，左右至少一半可明确为有序。若目标值落在有序半段的闭开值域内，则它只能位于该半段；否则它不可能位于该半段，可以安全排除。每轮保留的区间仍满足不变量且长度至少减半。命中时返回正确下标，区间为空则证明目标不存在。

- 时间复杂度：`O(log n)`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }

            if (nums[left] <= nums[mid]) {
                if (nums[left] <= target && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                if (nums[mid] < target && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        return -1;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (nums[mid] == target) {
                return mid;
            }

            if (nums[left] <= nums[mid]) {
                if (nums[left] <= target && target < nums[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                if (nums[mid] < target && target <= nums[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.search(
                new int[]{4, 5, 6, 7, 0, 1, 2}, 0)); // 4
        System.out.println(solution.search(
                new int[]{4, 5, 6, 7, 0, 1, 2}, 3)); // -1
        System.out.println(solution.search(new int[]{1}, 0)); // -1
        System.out.println(solution.search(new int[]{1, 3}, 3)); // 1
    }
}
```

## 边界与易错点

- 区间是闭区间，因此循环条件为 `left <= right`。
- 判断左半有序要用 `<=`，确保单元素区间被正确归类。
- 值域边界一端用 `<=`、靠近 `mid` 的一端用 `<`，因为 `mid` 已单独检查。
- 本题元素互异；若允许重复值，如 `[1,0,1,1,1]`，仅靠两端与中点可能无法判断哪半有序，最坏会退化到线性。

## 可扩展变式

- 先找旋转数组最小值，再根据目标值选择普通二分区间。
- 含重复元素的旋转数组搜索需要在三者相等时收缩边界。
- 求旋转次数等价于寻找最小元素的下标。
