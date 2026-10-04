# LeetCode-22 括号生成

- 难度：中等
- 链接：https://leetcode.cn/problems/generate-parentheses/

## 问题描述
给定 `n`，生成由 `n` 对括号组成的所有合法括号序列。合法定义为任意前缀中左括号数不少于右括号数，最终左右括号数相等。

## 题解一：官方经典（回溯 + 约束）
- 思路：使用两个计数 `left` 与 `right` 表示当前已放置的左、右括号：
  - 若 `left < n` 可以放一个 `(`；
  - 若 `right < left` 可以放一个 `)`；
  - 当 `left == right == n` 加入答案。
- 复杂度：答案个数为卡特兰数 `C_n`，时间 O(C_n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    List<String> ans = new ArrayList<>();
    public List<String> generateParenthesis(int n) {
        backtrack(n, 0, 0, new StringBuilder());
        return ans;
    }
    private void backtrack(int n, int left, int right, StringBuilder path) {
        if (left == n && right == n) { ans.add(path.toString()); return; }
        if (left < n) { path.append('('); backtrack(n, left + 1, right, path); path.deleteCharAt(path.length() - 1); }
        if (right < left) { path.append(')'); backtrack(n, left, right + 1, path); path.deleteCharAt(path.length() - 1); }
    }
}
```

## 题解二：通用解法（DP构造）
- 标签：回溯、卡特兰数、DP
- 思路：利用递推：`S_n = '(' + S_i + ')' + S_{n-1-i}` 的笛卡尔积组合（`i=0..n-1`），实现所有构造；回溯更直观，DP适合理解结构。

## 总结思路
- 约束回溯是首选模板；DP构造可作为思维补充与验证。

## 相关标签
- 回溯、构造、卡特兰数