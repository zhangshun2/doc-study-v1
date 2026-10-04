# LeetCode-394 字符串解码

- 难度：中等
- 链接：https://leetcode.cn/problems/decode-string/

## 问题描述
给定形如 `k[encoded_string]` 的编码字符串，`k` 为正整数，按规则展开并返回结果。支持嵌套与多位数字。

## 题解一：官方经典（栈模拟）
- 思路：遇数字解析倍数；遇 `[` 入栈当前倍数与已构造字符串；遇 `]` 弹栈并重复拼接；其他字符直接追加。
- 复杂度：时间 O(n)，空间 O(n)。

```java
import java.util.*;
class Solution {
    public String decodeString(String s) {
        Deque<Integer> kSt = new ArrayDeque<>();
        Deque<StringBuilder> strSt = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int k = 0;
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) k = k * 10 + (c - '0');
            else if (c == '[') { kSt.push(k); strSt.push(cur); k = 0; cur = new StringBuilder(); }
            else if (c == ']') {
                int times = kSt.pop(); StringBuilder prev = strSt.pop();
                for (int i = 0; i < times; i++) prev.append(cur);
                cur = prev;
            } else cur.append(c);
        }
        return cur.toString();
    }
}
```

## 题解二：通用解法（递归解析 + 全局索引）
- 标签：栈、递归、字符串
- 思路：用递归遇 `[` 进入子问题，遇 `]` 返回；用全局索引在同一数组上行走。

```java
class Solution {
    private int i;
    public String decodeString(String s) { i = 0; return parse(s.toCharArray()); }
    private String parse(char[] a) {
        StringBuilder cur = new StringBuilder(); int k = 0;
        while (i < a.length && a[i] != ']') {
            if (Character.isDigit(a[i])) { k = k * 10 + (a[i] - '0'); i++; }
            else if (a[i] == '[') { i++; String t = parse(a); for (int c = 0; c < k; c++) cur.append(t); k = 0; }
            else { cur.append(a[i++]); }
        }
        if (i < a.length && a[i] == ']') i++;
        return cur.toString();
    }
}
```

## 题解三：最好理解（“层层展开”）
- 直觉：每见到一层 `[...]` 就把它当作子串处理，展开后回到上一层再继续拼接。

## 总结思路
- 栈法与递归法都很直观；处理多位数字与嵌套是关键。

## 相关标签
- 栈、递归、字符串