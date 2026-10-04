---
schemaVersion: 3
type: "problem"
leetcodeId: 15
slug: "3sum"
titleCn: "三数之和"
titleEn: "3Sum"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/3sum/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "63eb6d79808da6c9139c2505d6dac316c0c0735ae8a6c02ff7866ca6673e7f37"
sourceFactsSha256: "54330425666213a6c5c5ef8ad3c7e2434110a61068dd8847e16f956f1c222acd"
sourceSectionHashes:
  description: "49740de145a3490d3b39744fd3cae4df667fce5784835e7784507f00ac57730f"
  examples: "092a86e13d1bf9cc91999e53bdb155b281b626d6214ebf49bd2b5350e0e91028"
  constraints: "1652a7159e3e2b736ac3d3f49592dbc2a4dfcf2ee48e3dd54d41b7c588435a05"
  hints: "d67caaefb28c173def890505e64b99138761141aba51092f8b6e08b72af3e1ab"
  tags: "316c5a97dc534411ef9fd2ab73ee2a9eac796899783f0ea30d16827c3307e485"
  signature: "95c6f0466f8c9f1237c904233bac7e29b760c420bc3c456dd00961e1b4103c31"
  javaTemplate: "09afe50bc55196805e48da515eb983ade851035640da658793a3b14bc9249c25"
primaryPattern: "双指针"
topics: ["双指针","数组","排序"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Two Pointers 双指针"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 15. 三数之和 / 3Sum

> **双轨入口：** [[核心模型/双指针/15-Three-Sum-核心模型.md|核心模型]] · [[建模专题/T0/15-Three-Sum-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`双指针`
- 清单优先级：`P0`
- 清单代表标签：`Two Pointers 双指针`
- LeetCode 当前标签：数组 (Array)、双指针 (Two Pointers)、排序 (Sorting)
- 官方来源：<https://leetcode.cn/problems/3sum/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`63eb6d79808da6c9139c2505d6dac316c0c0735ae8a6c02ff7866ca6673e7f37`
- 主模型：排序 + 固定一个数 + 相向双指针 + 去重
- 直观建模专题：[从三重枚举到有序空间中的双指针](../../建模专题/T0/15-Three-Sum-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` ，判断是否存在三元组 `[nums[i], nums[j], nums[k]]` 满足 `i != j`、`i != k` 且 `j != k` ，同时还满足 `nums[i] + nums[j] + nums[k] == 0` 。请你返回所有和为 `0` 且不重复的三元组。

**注意：**答案中不可以包含重复的三元组。

## 官方示例


**示例 1：**

```text
输入：nums = [-1,0,1,2,-1,-4]
输出：[[-1,-1,2],[-1,0,1]]
解释：
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0 。
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0 。
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0 。
不同的三元组是 [-1,0,1] 和 [-1,-1,2] 。
注意，输出的顺序和三元组的顺序并不重要。
```

**示例 2：**

```text
输入：nums = [0,1,1]
输出：[]
解释：唯一可能的三元组和不为 0 。
```

**示例 3：**

```text
输入：nums = [0,0,0]
输出：[[0,0,0]]
解释：唯一可能的三元组和为 0 。
```

## 官方约束


- `3 <= nums.length <= 3000`

- `-10^5 <= nums[i] <= 10^5`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. So, we essentially need to find three numbers x, y, and z such that they add up to the given value. If we fix one of the numbers say x, we are left with the two-sum problem at hand!
2. For the two-sum problem, if we fix one of the numbers, say x, we have to scan the entire array to find the next number y, which is value - x where value is the input parameter. Can we change our array somehow so that this search becomes faster?
3. The second train of thought for two-sum is, without changing the array, can we use additional space somehow? Like maybe a hash map to speed up the search?

## 学习提示（非官方）

1. 排序后固定第一个数，剩余问题变成在右侧有序区间中找两数之和。
2. 和太小就移动左指针，和太大就移动右指针。
3. 固定数和双指针都必须跳过重复值。
4. 排序后若固定数已经大于 0，后续不可能再凑出 0。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 目标是把三层枚举的 `O(n^3)` 降到 `O(n^2)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

排序同时解决两件事：双指针可以按和的大小定向移动，相同值也会相邻便于去重。固定 `nums[first]` 后，需要在 `(first,n)` 中寻找和为 `-nums[first]` 的两个数。

## 朴素方案：三层循环与集合去重

枚举所有下标三元组，和为 0 时把三个值排序后放入集合去重。

- 时间复杂度：`O(n^3)`，不计每个三元组常数级排序。
- 空间复杂度：`O(答案数量)`。
- 局限：`n=3000` 时组合数过大。

也可固定一数后用哈希表做两数之和，达到 `O(n^2)`，但输出去重更繁琐。

## 最优方案：排序与双指针

排序后枚举 `first`。若与前一个固定值相同就跳过。设置 `left=first+1`、`right=n-1`：

- 三数和小于 0：`left++`。
- 三数和大于 0：`right--`。
- 等于 0：记录答案，两端都移动，并跳过各自重复值。

### 正确性与不变量

固定 `first` 后，双指针区间内尚未排除所有可能配对。若当前和小于 0，因为数组有序，保持左值而缩小右指针只会让和更小，所以必须增大左值；和大于 0 时对称地必须减小右值。这些移动不会跳过解。每个固定值和命中后的相邻重复值都只处理一次，因此既找到全部数值组合，也不产生重复三元组。

- 时间复杂度：排序 `O(n log n)`，扫描 `O(n^2)`，总体 `O(n^2)`。
- 空间复杂度：忽略排序实现栈和答案为 `O(1)`；Java `Arrays.sort(int[])` 的辅助空间由实现决定，通常可视为 `O(log n)` 调用栈级别。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> answer = new ArrayList<>();

        for (int first = 0; first < nums.length - 2; first++) {
            if (nums[first] > 0) {
                break;
            }
            if (first > 0 && nums[first] == nums[first - 1]) {
                continue;
            }

            int left = first + 1;
            int right = nums.length - 1;
            while (left < right) {
                int sum = nums[first] + nums[left] + nums[right];
                if (sum < 0) {
                    left++;
                } else if (sum > 0) {
                    right--;
                } else {
                    answer.add(Arrays.asList(
                            nums[first], nums[left], nums[right]));
                    int leftValue = nums[left];
                    int rightValue = nums[right];
                    while (left < right && nums[left] == leftValue) {
                        left++;
                    }
                    while (left < right && nums[right] == rightValue) {
                        right--;
                    }
                }
            }
        }
        return answer;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> answer = new ArrayList<>();

        for (int first = 0; first < nums.length - 2; first++) {
            if (nums[first] > 0) {
                break;
            }
            if (first > 0 && nums[first] == nums[first - 1]) {
                continue;
            }

            int left = first + 1;
            int right = nums.length - 1;
            while (left < right) {
                int sum = nums[first] + nums[left] + nums[right];
                if (sum < 0) {
                    left++;
                } else if (sum > 0) {
                    right--;
                } else {
                    answer.add(Arrays.asList(
                            nums[first], nums[left], nums[right]));
                    int leftValue = nums[left];
                    int rightValue = nums[right];
                    while (left < right && nums[left] == leftValue) {
                        left++;
                    }
                    while (left < right && nums[right] == rightValue) {
                        right--;
                    }
                }
            }
        }
        return answer;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.threeSum(
                new int[]{-1, 0, 1, 2, -1, -4}));
        System.out.println(solution.threeSum(new int[]{0, 1, 1}));
        System.out.println(solution.threeSum(new int[]{0, 0, 0, 0}));
    }
}
```

## 边界与易错点

- 只对结果使用 `Set` 而不在扫描中去重，会产生大量无效重复工作。
- 固定值去重条件是与前一个比较；不能无条件与后一个比较，否则可能漏解。
- 命中后左右指针都要移动，并跳过相同值。
- 本题约束下三数和在 `int` 范围内；若元素范围扩大，应使用 `long sum`。
- 排序会修改输入数组；若调用方要求保留，应先复制。

## 可扩展变式

- 三数之和最接近：不收集等值组合，而是维护与目标差值最小的和。
- 四数之和：固定两层后使用双指针，复杂度 `O(n^3)`，并注意 `long` 溢出。
- 通用 K 数之和可排序后递归降维，底层使用两数双指针。
