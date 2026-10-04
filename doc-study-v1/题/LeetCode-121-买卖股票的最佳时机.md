# LeetCode-121 买卖股票的最佳时机

- 难度：简单
- 链接：https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/

## 问题描述
给定数组 `prices`，表示某只股票每天的价格。你只能选择某一天买入并在未来某一天卖出，最大化利润，返回最大利润。

## 题解一：官方经典（一遍扫描维护历史最低价）
- 思路：维护迄今为止的最低买入价 `minPrice`，每天计算当日卖出可获得的利润 `prices[i]-minPrice`，更新最大值。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int maxProfit(int[] prices) {
        int min = Integer.MAX_VALUE, ans = 0;
        for (int p : prices) { min = Math.min(min, p); ans = Math.max(ans, p - min); }
        return ans;
    }
}
```

## 题解二：通用解法（DP 两状态）
- 标签：数组、贪心、动态规划
- 思路：`hold` 表示持有股票的最大收益，`cash` 表示不持有的最大收益；本题限制一次交易，等价于 `hold = -minPrice, cash = maxProfit`。

```java
class Solution {
    public int maxProfit(int[] prices) {
        int hold = Integer.MIN_VALUE, cash = 0;
        for (int p : prices) {
            hold = Math.max(hold, -p);    // 买入
            cash = Math.max(cash, hold + p); // 卖出
        }
        return cash;
    }
}
```

## 题解三：最好理解（“先找最低，再看能赚多少”）
- 直觉：持续更新历史最低买入价，然后每一天都尝试卖出，取最大利润即可。

## 总结思路
- 一遍扫描是面试标准写法；DP有助于统一多次交易等扩展问题的思路。

## 相关标签
- 数组、贪心、动态规划