---
相关文档导航:
  - [字符串专题导航](../字符串专题/导航.md)
  - [学习顺序 - 字符串专题](../字符串专题/学习顺序 - 字符串专题.md)
  - [微模板与易错点卡片](../字符串专题/删除无效括号/微模板与易错点卡片.md)
  - [模板索引：回溯与 BFS](../学习方法/模板索引.md#回溯与 bfs)
---
# LeetCode-301 删除无效括号

- 难度：困难
- 链接：https://leetcode.cn/problems/remove-invalid-parentheses/

## 问题描述
给你一个由若干括号和字母组成的字符串 `s`，删除最小数量的无效括号，使得输入的字符串有效。返回所有可能的结果。答案可以按任意顺序返回。

例如：
- 输入：`"()())()"` → 输出：`["(())()","()()()"]`
- 输入：`"(a)())()"` → 输出：`["(a())()","(a)()()"]`
- 输入：`")("` → 输出：`[""]`

## 题解一：BFS（层次遍历，保证删除最少）
- 思路：
  1. 使用 BFS 逐层删除括号，每一层尝试删除一个字符
  2. 第一次找到有效字符串时，该层所有有效字符串即为答案（保证删除数量最少）
  3. 使用 Set 去重，避免重复计算
- 复杂度：时间 O(2^n)，空间 O(2^n)

```java
import java.util.*;
class Solution {
    public List<String> removeInvalidParentheses(String s) {
        List<String> result = new ArrayList<>();
        if (s == null) return result;
        
        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();
        queue.offer(s);
        visited.add(s);
        
        boolean found = false;
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                String cur = queue.poll();
                if (isValid(cur)) {
                    result.add(cur);
                    found = true;
                }
                if (found) continue;
                
                for (int j = 0; j < cur.length(); j++) {
                    if (cur.charAt(j) != '(' && cur.charAt(j) != ')') continue;
                    String next = cur.substring(0, j) + cur.substring(j + 1);
                    if (!visited.contains(next)) {
                        visited.add(next);
                        queue.offer(next);
                    }
                }
            }
            if (found) break;
        }
        
        return result;
    }
    
    private boolean isValid(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') count++;
            else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
}
```

## 题解二：回溯 + 剪枝
- 思路：
  1. 先统计需要删除的左右括号数量
  2. 回溯尝试删除，剪枝：连续相同括号只删除第一个，避免重复
  3. 删除够数量后验证有效性
- 复杂度：时间 O(2^n)，空间 O(n)

```java
import java.util.*;
class Solution {
    List<String> result = new ArrayList<>();
    
    public List<String> removeInvalidParentheses(String s) {
        int lRemove = 0, rRemove = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') lRemove++;
            else if (c == ')') {
                if (lRemove > 0) lRemove--;
                else rRemove++;
            }
        }
        backtrack(s, 0, lRemove, rRemove);
        return result;
    }
    
    private void backtrack(String s, int start, int lRemove, int rRemove) {
        if (lRemove == 0 && rRemove == 0) {
            if (isValid(s)) result.add(s);
            return;
        }
        
        for (int i = start; i < s.length(); i++) {
            if (i > start && s.charAt(i) == s.charAt(i - 1)) continue; // 去重剪枝
            
            char c = s.charAt(i);
            if (lRemove > 0 && c == '(') {
                backtrack(s.substring(0, i) + s.substring(i + 1), i, lRemove - 1, rRemove);
            } else if (rRemove > 0 && c == ')') {
                backtrack(s.substring(0, i) + s.substring(i + 1), i, lRemove, rRemove - 1);
            }
        }
    }
    
    private boolean isValid(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') count++;
            else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
}
```

## 总结思路
- BFS 保证删除最少，适合求所有最优解
- 回溯需要预先计算删除数量，剪枝是关键
- 验证有效性的核心：左括号数始终 >= 右括号数，最终相等

## 相关标签
- 字符串、回溯、BFS、括号匹配
