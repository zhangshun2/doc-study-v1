# LeetCode-20 有效的括号

- 难度：简单
- 链接：https://leetcode.cn/problems/valid-parentheses/

## 问题描述
给定只包含 `()[]{}` 的字符串，判断是否为有效括号序列：每个左括号都能以正确顺序匹配相同类型的右括号。

## 题解一：官方经典（栈 + 映射）
- 思路：遇到左括号入栈，遇到右括号检查栈顶是否为对应左括号；最后栈为空即有效。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public boolean isValid(String s) {
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') st.push(c);
            else {
                if (st.isEmpty()) return false;
                char t = st.pop();
                if (c == ')' && t != '(') return false;
                if (c == ']' && t != '[') return false;
                if (c == '}' && t != '{') return false;
            }
        }
        return st.isEmpty();
    }
}
```

## 题解二：通用解法（栈存“期望右括号”）
- 标签：栈、字符串、模拟
- 思路：左括号时压入期望的右括号；右括号时直接与栈顶比对。

```java
import java.util.*;
class Solution {
    public boolean isValid(String s) {
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') st.push(')');
            else if (c == '[') st.push(']');
            else if (c == '{') st.push('}');
            else if (st.isEmpty() || st.pop() != c) return false;
        }
        return st.isEmpty();
    }
}
```

## 题解三：最好理解（逐字符匹配）
- 直觉：右括号只能匹配最近的未匹配左括号，用栈即可；最后栈必须清空。

## 总结思路
- 两种写法本质一致；“期望右括号”写法更简洁，减少映射判断。

## 相关标签
- 栈、字符串、模拟