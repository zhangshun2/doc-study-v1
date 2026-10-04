# LeetCode-301 删除无效的括号

- 难度：困难
- 链接：https://leetcode.cn/problems/remove-invalid-parentheses/

## 问题描述
给定一个字符串 `s`，通过删除最少数量的括号 `()` 使得字符串有效，返回所有可能的结果。非括号字符保持不变。

## 题解一：官方经典（BFS 分层删除）
- 思路：
  - 从原串开始，逐层删除一个括号生成所有可能字符串；在某一层首次出现有效字符串时即为最少删除层，返回该层的所有有效字符串。
  - 使用 `visited` 去重；有效性判定函数统计括号平衡，遇到负值直接判无效。
- 复杂度：最坏情况下状态数指数级；BFS 在首层命中有效后终止。

```java
import java.util.*;
class Solution {
    public List<String> removeInvalidParentheses(String s) {
        List<String> ans = new ArrayList<>();
        Set<String> vis = new HashSet<>();
        Deque<String> dq = new ArrayDeque<>();
        dq.offer(s); vis.add(s);
        boolean found = false;
        while (!dq.isEmpty()) {
            int size = dq.size();
            for (int t = 0; t < size; t++) {
                String cur = dq.poll();
                if (isValid(cur)) { ans.add(cur); found = true; }
                if (found) continue; // 本层命中有效，不再扩展下一层
                for (int i = 0; i < cur.length(); i++) {
                    char c = cur.charAt(i);
                    if (c != '(' && c != ')') continue;
                    String next = cur.substring(0, i) + cur.substring(i + 1);
                    if (vis.add(next)) dq.offer(next);
                }
            }
            if (found) break;
        }
        if (ans.isEmpty()) ans.add("");
        return ans;
    }
    private boolean isValid(String s) {
        int bal = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') bal++;
            else if (c == ')') {
                if (bal == 0) return false;
                bal--;
            }
        }
        return bal == 0;
    }
}
```

## 题解二：通用解法（DFS 目标删除数 + 计数剪枝）
- 标签：BFS、回溯、字符串、剪枝
- 思路：
  - 先遍历计算最少需要删除的左括号 `remL` 与右括号 `remR`（遇到多余右括号时 `remR++`，多余左括号累计为 `remL`）。
  - 再用回溯枚举保留或删除的选择，维护当前未匹配左括号数 `open`，同时限制删除次数不超标；用集合去重。

```java
import java.util.*;
class Solution2 {
    Set<String> res = new HashSet<>();
    public List<String> removeInvalidParentheses(String s) {
        int[] rm = computeRem(s);
        dfs(s, 0, rm[0], rm[1], 0, new StringBuilder());
        return new ArrayList<>(res);
    }
    private int[] computeRem(String s) {
        int remL = 0, remR = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') remL++;
            else if (c == ')') {
                if (remL > 0) remL--; else remR++;
            }
        }
        return new int[]{remL, remR};
    }
    private void dfs(String s, int i, int remL, int remR, int open, StringBuilder path) {
        if (i == s.length()) {
            if (remL == 0 && remR == 0 && open == 0) res.add(path.toString());
            return;
        }
        char c = s.charAt(i);
        int len = path.length();
        if (c == '(') {
            if (remL > 0) dfs(s, i + 1, remL - 1, remR, open, path); // 删除当前左括号
            path.append(c);
            dfs(s, i + 1, remL, remR, open + 1, path);               // 保留当前左括号
            path.setLength(len);
        } else if (c == ')') {
            if (remR > 0) dfs(s, i + 1, remL, remR - 1, open, path);  // 删除当前右括号
            if (open > 0) {                                           // 只有有未匹配左括号时才能保留右括号
                path.append(c);
                dfs(s, i + 1, remL, remR, open - 1, path);
                path.setLength(len);
            }
        } else { // 其它字符直接保留
            path.append(c);
            dfs(s, i + 1, remL, remR, open, path);
            path.setLength(len);
        }
    }
}
```

## 总结思路
- BFS 保证最少删除层次；DFS 通过目标删除量与平衡计数剪枝枚举所有合法结果。根据偏好任选其一，BFS更易写，DFS更高效可控。

## 相关标签
- BFS、回溯、字符串、剪枝