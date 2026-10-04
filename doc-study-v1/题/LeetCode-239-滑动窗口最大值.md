# LeetCode-239 滑动窗口最大值

- 难度：困难
- 链接：https://leetcode.cn/problems/sliding-window-maximum/

## 问题描述
给定数组 `nums` 和窗口大小 `k`，返回每个窗口的最大值。

## 题解一：官方经典（单调队列）
- 思路：使用双端队列存储下标，队列维护从大到小的单调性；每次加入元素时弹出队尾小于它的下标；队头若已出窗口（`<= i-k`）则弹出；队头即当前窗口最大值。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length; if (n == 0 || k == 0) return new int[0];
        int[] ans = new int[n - k + 1];
        Deque<Integer> dq = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
            dq.offerLast(i);
            if (dq.peekFirst() <= i - k) dq.pollFirst();
            if (i >= k - 1) ans[i - k + 1] = nums[dq.peekFirst()];
        }
        return ans;
    }
}
```

## 题解二：通用解法（大顶堆 + 延迟删除）
- 标签：数组、滑动窗口、单调队列、堆
- 思路：用堆存 `(值, 下标)`，每次取堆顶作为最大值并在需要时延迟移除过期下标；实现简单但整体 O(n log n)。

```java
import java.util.*;
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length; if (n == 0 || k == 0) return new int[0];
        int[] ans = new int[n - k + 1];
        PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> b[0]-a[0]);
        for (int i = 0; i < n; i++) {
            pq.offer(new int[]{nums[i], i});
            if (i >= k - 1) {
                while (pq.peek()[1] <= i - k) pq.poll();
                ans[i - k + 1] = pq.peek()[0];
            }
        }
        return ans;
    }
}
```

## 题解三：最好理解（“队头永远是最大且在窗口内”）
- 直觉：把不可能成为最大值的下标维护出队列，只保留递减的“候选最大值”，队头既最大又处于有效窗口。

## 总结思路
- 单调队列是最优；堆实现通用但略慢。

## 相关标签
- 数组、滑动窗口、单调队列、堆