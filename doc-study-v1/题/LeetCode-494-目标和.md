---
相关文档导航:
  - [动态规划专题导航](../动态规划专题/导航.md)
  - [学习顺序 - 动态规划专题](../动态规划专题/学习顺序 - 动态规划专题.md)
  - [微模板与易错点卡片](../动态规划专题/目标和/微模板与易错点卡片.md)
  - [模板索引：背包问题](../学习方法/模板索引.md#背包问题)
---
# LeetCode-494 目标和

- 难度：中等
- 链接：https://leetcode.cn/problems/target-sum/

## 问题描述
给你一个非负整数数组 `nums` 和一个整数 `target`。向数组中的每个整数前添加 `'+'` 或 `'-'`，然后串联起所有整数，构造一个表达式。返回可以通过上述方法构造的、运算结果等于 `target` 的不同表达式的数目。

例如：
- 输入：`nums = [1,1,1,1,1], target = 3` → 输出：`5`
- 输入：`nums = [1], target = 1` → 输出：`1`

## 题解一：动态规划（0-1 背包变形）
- 思路：
  1. 设正数和为 P，负数和为 N，则 P - N = target，P + N = sum
  2. 解得 P = (sum + target) / 2，问题转化为：从 nums 中选若干数使其和为 P 的方案数
  3. 使用 0-1 背包 DP：`dp[j]` 表示和为 j 的方案数
- 复杂度：时间 O(n * sum)，空间 O(sum)

```java
class Solution {
    public int findTargetSumWays(int[] nums, int target) {
        int sum = 0;
        for (int num : nums) sum += num;
        
        // 边界条件检查
        if (target > sum || target < -sum) return 0;
        if ((sum + target) % 2 != 0) return 0;
        
        int positive = (sum + target) / 2;
        int[] dp = new int[positive + 1];
        dp[0] = 1;
        
        for (int num : nums) {
            for (int j = positive; j >= num; j--) {
                dp[j] += dp[j - num];
            }
        }
        
        return dp[positive];
    }
}
```

## 题解二：回溯（暴力枚举）
- 思路：对每个数字尝试加或减，递归枚举所有可能，统计结果等于 target 的数量
- 复杂度：时间 O(2^n)，空间 O(n)

```java
class Solution {
    int count = 0;
    
    public int findTargetSumWays(int[] nums, int target) {
        backtrack(nums, 0, 0, target);
        return count;
    }
    
    private void backtrack(int[] nums, int index, int currentSum, int target) {
        if (index == nums.length) {
            if (currentSum == target) count++;
            return;
        }
        
        backtrack(nums, index + 1, currentSum + nums[index], target);
        backtrack(nums, index + 1, currentSum - nums[index], target);
    }
}
```

## 题解三：记忆化搜索（带缓存的回溯）
- 思路：在回溯基础上，用 Map 缓存 `(index, currentSum)` 的结果，避免重复计算
- 复杂度：时间 O(n * sum)，空间 O(n * sum)

```java
import java.util.*;
class Solution {
    Map<String, Integer> memo = new HashMap<>();
    
    public int findTargetSumWays(int[] nums, int target) {
        return dfs(nums, 0, 0, target);
    }
    
    private int dfs(int[] nums, int index, int currentSum, int target) {
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        String key = index + "," + currentSum;
        if (memo.containsKey(key)) return memo.get(key);
        
        int add = dfs(nums, index + 1, currentSum + nums[index], target);
        int subtract = dfs(nums, index + 1, currentSum - nums[index], target);
        
        memo.put(key, add + subtract);
        return memo.get(key);
    }
}
```

## 总结思路
- 本质是 0-1 背包问题的变形
- 数学转换是关键：将正负号选择转换为子集和问题
- DP 最优，回溯适合理解但会超时（除非加记忆化）

## 相关标签
- 动态规划、回溯、0-1 背包、数学
