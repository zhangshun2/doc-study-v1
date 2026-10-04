# LeetCode-17 电话号码的字母组合

- 难度：中等
- 链接：https://leetcode.cn/problems/letter-combinations-of-a-phone-number/

## 问题描述
给定仅包含数字 `2-9` 的字符串，返回所有它能表示的字母组合。数字到字母的映射与电话按键相同。

## 题解一：官方经典（回溯枚举）
- 思路：使用回溯，按位选择当前数字对应的所有字母，将选择加入路径后递归到下一位；当路径长度等于输入长度时加入答案。
- 复杂度：设每位最多 4 个字母，长度为 `n`，时间近似 O(4^n)，空间 O(n) 路径栈。

```java
import java.util.*;
class Solution {
    private static final String[] MAP = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    List<String> ans = new ArrayList<>();
    String digits;
    public List<String> letterCombinations(String digits) {
        this.digits = digits;
        if (digits == null || digits.length() == 0) return ans;
        backtrack(0, new StringBuilder());
        return ans;
    }
    private void backtrack(int idx, StringBuilder path) {
        if (idx == digits.length()) { ans.add(path.toString()); return; }
        int d = digits.charAt(idx) - '0';
        String letters = MAP[d];
        for (int i = 0; i < letters.length(); i++) {
            path.append(letters.charAt(i));
            backtrack(idx + 1, path);
            path.deleteCharAt(path.length() - 1);
        }
    }
}
```

## 题解二：通用解法（队列迭代）
- 标签：回溯、枚举、队列
- 思路：用队列层层扩展，每次取出队头字符串与当前数字的所有字母拼接，入队下一层，直至处理完所有位。

```java
import java.util.*;
class Solution {
    private static final String[] MAP = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    public List<String> letterCombinations(String digits) {
        List<String> ans = new ArrayList<>();
        if (digits == null || digits.length() == 0) return ans;
        Deque<String> q = new ArrayDeque<>();
        q.offer("");
        for (int i = 0; i < digits.length(); i++) {
            int d = digits.charAt(i) - '0';
            String letters = MAP[d];
            int size = q.size();
            for (int k = 0; k < size; k++) {
                String cur = q.poll();
                for (int j = 0; j < letters.length(); j++) {
                    q.offer(cur + letters.charAt(j));
                }
            }
        }
        ans.addAll(q);
        return ans;
    }
}
```

## 总结思路
- 回溯写法更直接，迭代队列适合作为非递归替代；二者复杂度等价。

## 相关标签
- 回溯、枚举、字符串