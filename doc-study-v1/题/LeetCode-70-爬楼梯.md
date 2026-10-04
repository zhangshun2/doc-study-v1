# LeetCode-70 爬楼梯

- 难度：简单
- 链接：https://leetcode.cn/problems/climbing-stairs/

## 问题描述
每次可以爬一阶或两阶，问到达第 `n` 阶共有多少种不同的方法。

## 题解一：官方经典（斐波那契型DP）
- 思路：`f(n) = f(n-1) + f(n-2)`，初值 `f(1)=1, f(2)=2`。可用 O(1) 空间滚动计算。
- 复杂度：时间 O(n)，空间 O(1)。

```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int a = 1, b = 2; // f(1), f(2)
        for (int i = 3; i <= n; i++) {
            int c = a + b; a = b; b = c;
        }
        return b;
    }
}
```

## 题解二：通用解法（矩阵快速幂）
- 标签：动态规划、斐波那契、快速幂
- 思路：斐波那契可用矩阵幂加速到 O(log n)，适合非常大的 `n`（此题一般不需要）。

```java
class Solution2 {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        long[][] M = {{1,1},{1,0}};
        long[][] R = pow(M, n - 2);
        long f2 = 2, f1 = 1;
        return (int)(R[0][0] * f2 + R[0][1] * f1);
    }
    private long[][] mul(long[][] A, long[][] B) {
        return new long[][]{
            {A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]},
            {A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]}
        };
    }
    private long[][] pow(long[][] M, int k) {
        long[][] R = {{1,0},{0,1}};
        while (k > 0) {
            if ((k & 1) == 1) R = mul(R, M);
            M = mul(M, M); k >>= 1;
        }
        return R;
    }
}
```

## 总结思路
- 本题最适合滚动DP；快速幂是斐波那契的通用加速技巧，了解即可。

## 相关标签
- 动态规划、斐波那契、快速幂