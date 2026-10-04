# LeetCode-448 找到所有数组中消失的数字

- 难度：简单
- 链接：https://leetcode.cn/problems/find-all-numbers-disappeared-in-an-array/

## 问题描述
给定一个包含 `1..n` 的整数数组，其中某些元素出现了两次，某些元素出现了一次。找出所有没有出现在数组中的数字。

## 题解一：官方经典（原地标记法）
- 思路：遍历数组，令 `idx = abs(nums[i]) - 1`，将 `nums[idx]` 置为负表示该数字出现过；二次遍历收集值仍为正的位置 `i+1` 即为缺失数字。
- 复杂度：时间 O(n)，空间 O(1)（不计输出）。

```java
import java.util.*;
class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        for (int x : nums) {
            int idx = Math.abs(x) - 1;
            if (nums[idx] > 0) nums[idx] = -nums[idx];
        }
        List<Integer> res = new ArrayList<>();
        for (int i = 0; i < nums.length; i++) if (nums[i] > 0) res.add(i + 1);
        return res;
    }
}
```

## 题解二：通用解法（布尔数组标记）
- 标签：数组、原地标记、哈希
- 思路：用布尔数组标记出现过的数字，再扫描收集缺失位置；空间 O(n)。

```java
import java.util.*;
class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        boolean[] seen = new boolean[nums.length + 1];
        for (int x : nums) seen[x] = true;
        List<Integer> res = new ArrayList<>();
        for (int i = 1; i <= nums.length; i++) if (!seen[i]) res.add(i);
        return res;
    }
}
```

## 题解三：最好理解（“出现过就打勾，没勾的就是缺失”）
- 直觉：用数组自身或额外空间做出现标记，最后统计没被标记的数字。

## 总结思路
- 原地标记更优；布尔数组更直观但占空间。

## 相关标签
- 数组、原地标记、哈希