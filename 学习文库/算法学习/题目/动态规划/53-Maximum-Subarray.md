---
schemaVersion: 3
type: "problem"
leetcodeId: 53
slug: "maximum-subarray"
titleCn: "最大子数组和"
titleEn: "Maximum Subarray"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/maximum-subarray/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "754da07fe14887e8e25531ffb64c92cd2b3f49838cc445c83ee9ec91ece31f71"
sourceFactsSha256: "a50e13b9fc2f7998def4e76c16e28793a1251c6a3425ab49b51340ae767649a6"
sourceSectionHashes:
  description: "fd44980f98711233f9855c56dbf7022b2add9e06adf6080d1ade9a4e63374891"
  examples: "88c4dd9b2611541e326541503dd7e322152603265c1075d4c08fc01362cab675"
  constraints: "f3a680980a59a1e7add33ffda366c03b992c267b834a54efe8971c4145ed5458"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "f8870c07d439560962285e08e59c5da5c68c100c64a4b8480ef15714d9f0b322"
  signature: "9cf7a3f3a47beda43c810a339074fa1e0635499563b752227bd2943fcbba260d"
  javaTemplate: "19be4bca18aa43efdc1b6bc21a1afcacd2748b53eb1917a982c845b1ae325180"
primaryPattern: "动态规划"
topics: ["动态规划","数组","分治"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Array 数组","Divide and Conquer 分治"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 53. 最大子数组和 / Maximum Subarray

> **双轨入口：** [[核心模型/动态规划/53-Maximum-Subarray-核心模型.md|核心模型]] · [[建模专题/T0/53-Maximum-Subarray-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`动态规划`
- 清单优先级：`P0`
- 清单代表标签：`Array 数组`、`Divide and Conquer 分治`
- LeetCode 当前标签：数组 (Array)、分治 (Divide and Conquer)、动态规划 (Dynamic Programming)
- 官方来源：<https://leetcode.cn/problems/maximum-subarray/>
- 直观建模专题：[从枚举所有连续区间到结算“必须在当前位置结束”](../../建模专题/T0/53-Maximum-Subarray-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`754da07fe14887e8e25531ffb64c92cd2b3f49838cc445c83ee9ec91ece31f71`
- 主模型：线性动态规划 / Kadane 算法

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

**子数组**是数组中的一个连续部分。

## 官方示例


**示例 1：**

```text
输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

**示例 2：**

```text
输入：nums = [1]
输出：1
```

**示例 3：**

```text
输入：nums = [5,4,-1,7,8]
输出：23
```

## 官方约束


- `1 <= nums.length <= 10^5`

- `-10^4 <= nums[i] <= 10^4`

**进阶：**如果你已经实现复杂度为 `O(n)` 的解法，尝试使用更为精妙的 **分治法** 求解。

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 先不要问“最大子数组从哪里开始”，先问“以位置 `i` 结尾的最大子数组和是多少”。
2. 到达 `nums[i]` 时只有两种选择：接到前一个最优结尾后面，或者从当前元素重新开始。
3. 如果前面的累加和是负数，继续携带它只会让当前结果更小。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- `n` 可达 `10^5`，目标应为 `O(n)` 时间；`O(n^2)` 枚举会超时。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

定义 `dp[i]` 为必须以 `nums[i]` 结尾的非空连续子数组的最大和。一个以 `i` 结尾的连续子数组，要么只有 `nums[i]`，要么把 `nums[i]` 接到某个以 `i - 1` 结尾的子数组后面：

```text
dp[i] = max(nums[i], dp[i - 1] + nums[i])
```

全局答案不一定在最后一个位置结束，所以还要维护所有 `dp[i]` 的最大值。

## 朴素方案：枚举左右边界

固定左端点 `left`，向右累加每个 `right` 并更新最大和。复用区间和可把三重枚举降为两重枚举。

```java
int best = Integer.MIN_VALUE;
for (int left = 0; left < nums.length; left++) {
    int sum = 0;
    for (int right = left; right < nums.length; right++) {
        sum += nums[right];
        best = Math.max(best, sum);
    }
}
```

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(1)`。
- 局限：当 `n = 100000` 时区间数量约为五十亿，无法通过。

## 最优方案推导

令 `current` 表示上一轮的 `dp[i - 1]`。处理当前值 `num` 时执行：

```text
current = max(num, current + num)
best = max(best, current)
```

由于 `dp[i]` 只依赖 `dp[i - 1]`，不需要保存整个数组。这种状态压缩写法通常称为 Kadane 算法。

对 `[-2,1,-3,4,-1,2,1,-5,4]`，`current` 依次是 `-2, 1, -2, 4, 3, 5, 6, 1, 5`，其中最大值为 `6`。

## 正确性与不变量

遍历到下标 `i` 后保持两个不变量：

1. `current` 等于所有以 `i` 结尾的非空连续子数组中的最大和。
2. `best` 等于下标区间 `[0,i]` 内所有非空连续子数组的最大和。

第一个不变量成立，因为任何以 `i` 结尾的连续子数组只能“从 `i` 开始”或“由以 `i-1` 结尾的子数组扩展”。第二个不变量通过 `best = max(best, current)` 保持。遍历结束时，`best` 就是整个数组的答案。

## 复杂度

- 时间复杂度：`O(n)`，每个元素只处理一次。
- 空间复杂度：`O(1)`，只使用两个状态变量。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public int maxSubArray(int[] nums) {
        int current = nums[0];
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return best;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

class Solution {
    public int maxSubArray(int[] nums) {
        int current = nums[0];
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            current = Math.max(nums[i], current + nums[i]);
            best = Math.max(best, current);
        }
        return best;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        int answer = new Solution().maxSubArray(nums);
        System.out.println("nums = " + Arrays.toString(nums));
        System.out.println("maximum subarray sum = " + answer);
    }
}
```

## 边界与易错点

- 全为负数时答案是最大的那个负数，不能把 `best` 初始化为 `0`。
- `current` 表示必须以当前位置结尾，`best` 才是全局答案，两者不能混用。
- 子数组要求连续；如果可以跳过中间元素，就变成了子序列问题。
- 若题目扩大数值范围，应将累加变量改成 `long`。

## 可扩展变式

- 返回最大子数组的左右下标：重启时记录新起点，刷新 `best` 时保存区间。
- 最大环形子数组和（918）：比较普通最大子数组与“总和减最小子数组”。
- 最大子数组乘积（152）：负数会交换最大与最小，需要同时维护两个状态。
- 分治解法：答案位于左半、右半或跨越中点，可用于理解 Divide and Conquer 标签。
