# LeetCode-309 最佳买卖股票时机含冷冻期

- 难度：中等
- 链接：https://leetcode.cn/problems/best-time-to-buy-and-sell-stock-with-cooldown/

## 问题描述
给定价格数组 `prices`，你可以多次买卖，但卖出后有一天的冷冻期，求最大利润。

## 题解一：官方经典（状态机DP）
- 思路：维护三状态：`hold`（持有）、`sold`（当天卖出）、`rest`（不持有且非卖出当天）。
  - 转移：
    - `newHold = max(hold, rest - price)`
    - `newSold = hold + price`
    - `newRest = max(rest, sold)`
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int maxProfit(int[] prices) {
        int hold = Integer.MIN_VALUE / 2, sold = 0, rest = 0;
        for (int p : prices) {
            int newHold = Math.max(hold, rest - p);
            int newSold = hold + p;
            int newRest = Math.max(rest, sold);
            hold = newHold; sold = newSold; rest = newRest;
        }
        return Math.max(sold, rest);
    }
}
```

## 题解二：通用解法（滚动变量 buy/sell）
- 标签：动态规划、状态机
- 思路：常见实现用 `buy/sell/prevSell` 三变量，语义与上面状态机一致。

## 总结思路
- 用状态机明晰冷冻期约束；滚动变量简化实现。

## 相关标签
- 动态规划、股票、状态机