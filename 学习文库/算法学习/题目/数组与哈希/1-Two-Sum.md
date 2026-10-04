---
schemaVersion: 3
type: "problem"
leetcodeId: 1
slug: "two-sum"
titleCn: "两数之和"
titleEn: "Two Sum"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/two-sum/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "4c6ba0618a3b754548bfb16490a192e6982a51f15e135b7b5a8e909941e856c6"
sourceFactsSha256: "ce3444f65ce7ee4a8b6d6c1639effa34f65e8c96eccb217dbcd6ad3eb8f9a175"
sourceSectionHashes:
  description: "0fb4bf1258abc0b408ed7c9c9bf86516ed52aee03ddbc1080545f4c09cb835a6"
  examples: "eb6879470c656f30b0628d9083a3248711bd91f4d35c4f6f6d55d023f68dd431"
  constraints: "95df0f000a3d009347b2320a673b97ff2231ce7768a1abc139ddf1223e375863"
  hints: "d011acbb1ced56bc1018511c4ff0338ec737ddf3baf817712648aba35e53f8f9"
  tags: "9b3250254798d10b9bcfd41f3bcf6e206774feb626a2c04923b2b370d8e880d9"
  signature: "968c5b091291cbdca780232c1a3979d2260ff932316b092b63541d635c1378df"
  javaTemplate: "c50bec4149f19bf493fb3d5a0ef374dbfae2805f9f4ed64f9d7be96f3ccb9074"
primaryPattern: "数组与哈希"
topics: ["数组与哈希","数组","哈希表"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Array 数组","Hash Table 哈希表"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 1. 两数之和 / Two Sum

> **双轨入口：** [[核心模型/数组与哈希/1-Two-Sum-核心模型.md|核心模型]] · [[建模专题/T0/1-Two-Sum-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`数组与哈希`
- 清单优先级：`P0`
- 清单代表标签：`Array 数组`、`Hash Table 哈希表`
- LeetCode 当前标签：数组 (Array)、哈希表 (Hash Table)
- 官方来源：<https://leetcode.cn/problems/two-sum/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`4c6ba0618a3b754548bfb16490a192e6982a51f15e135b7b5a8e909941e856c6`
- 主模型：一次遍历 + 哈希表记录历史信息
- 直观建模专题：[从两数关系到补数查询](../../建模专题/T0/1-Two-Sum-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出 **和为目标值***`target`*  的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

## 官方示例


**示例 1：**

```text
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```text
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

**示例 3：**

```text
输入：nums = [3,3], target = 6
输出：[0,1]
```

## 官方约束


- `2 <= nums.length <= 10^4`

- `-10^9 <= nums[i] <= 10^9`

- `-10^9 <= target <= 10^9`

- **只会存在一个有效答案**

**进阶：**你可以想出一个时间复杂度小于 `O(n^2)` 的算法吗？

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. A really brute force way would be to search for all possible pairs of numbers but that would be too slow. Again, it's best to try out brute force solutions just for completeness. It is from these brute force solutions that you can come up with optimizations.
2. So, if we fix one of the numbers, say `x`, we have to scan the entire array to find the next number `y` which is `value - x` where value is the input parameter. Can we change our array somehow so that this search becomes faster?
3. The second train of thought is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?

## 学习提示（非官方）

1. 固定一个数 `nums[i]` 后，另一个数必须是 `target - nums[i]`。
2. 与其向右扫描补数，不如记录已经扫描过的数字。
3. 哈希表应保存“数值 -> 下标”，先查询再写入，才能避免同一个元素被使用两次。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 目标应优于检查所有数对的 `O(n^2)` 解法，通常要求做到 `O(n)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

题目不是让我们枚举所有组合，而是在每个位置询问：它需要的补数是否已经出现。扫描到 `nums[i]` 时，若 `target - nums[i]` 位于历史哈希表中，就立即得到了唯一答案。

先查后放非常关键。例如 `nums = [3,3]`，扫描第二个 `3` 时才能匹配第一个 `3`；扫描第一个时不能匹配自己。

## 朴素方案：双重循环

枚举左下标 `i`，再枚举 `j > i`，检查两数之和。它直观且额外空间为常数，但最坏要检查 `n(n-1)/2` 个数对。

- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(1)`

## 最优方案：一次遍历哈希表

维护 `indexByValue`，其中只存当前位置左侧已经访问过的元素。

1. 计算 `need = target - nums[i]`。
2. 查询 `need` 是否已出现；若出现，返回历史下标与 `i`。
3. 若没有出现，把 `nums[i] -> i` 放入表中。

### 正确性与不变量

循环开始处理下标 `i` 时，哈希表恰好包含区间 `[0, i)` 中元素的值和下标。如果答案的右端点是 `i`，其左端点一定在该表中，查询补数必然找到它。反之，只有当 `nums[old] + nums[i] == target` 时才返回，因此结果一定有效。题目保证唯一解，所以最终必然返回。

- 时间复杂度：平均 `O(n)`；哈希查询和写入平均为 `O(1)`。
- 空间复杂度：`O(n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> indexByValue = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            Integer previousIndex = indexByValue.get(need);
            if (previousIndex != null) {
                return new int[]{previousIndex, i};
            }
            indexByValue.put(nums[i], i);
        }
        throw new IllegalArgumentException("No valid pair");
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> indexByValue = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            Integer previousIndex = indexByValue.get(need);
            if (previousIndex != null) {
                return new int[]{previousIndex, i};
            }
            indexByValue.put(nums[i], i);
        }
        throw new IllegalArgumentException("No valid pair");
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(
                solution.twoSum(new int[]{2, 7, 11, 15}, 9)));
        System.out.println(Arrays.toString(
                solution.twoSum(new int[]{3, 2, 4}, 6)));
        System.out.println(Arrays.toString(
                solution.twoSum(new int[]{3, 3}, 6)));
    }
}
```

## 边界与易错点

- 不能先放入当前元素再查询，否则 `target == 2 * nums[i]` 时可能使用同一下标两次。
- 数组允许重复值，不能用只表示“是否存在”的集合代替“值到下标”的映射。
- 数值范围内两数和可能到 `2 * 10^9`，仍在 `int` 范围内；当前约束下 `target - nums[i]` 也不会越过约 `±2 * 10^9`。
- LeetCode 保证有解；工程代码若没有该保证，应约定无解返回值或抛出异常。

## 可扩展变式

- 数组有序时可改用左右双指针，空间降为 `O(1)`。
- 要返回所有不重复数对时，需要处理重复值与输出去重。
- 三数之和可通过“排序 + 固定一个数 + 双指针”把三层枚举降到 `O(n^2)`。
