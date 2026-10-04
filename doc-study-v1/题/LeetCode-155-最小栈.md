# LeetCode-155 最小栈

- 难度：中等
- 链接：https://leetcode.cn/problems/min-stack/

## 问题描述
设计一个支持 `push/pop/top/getMin` 的栈，`getMin` 返回栈中最小值，且各操作均为 O(1)。

## 题解一：官方经典（双栈）
- 思路：数据栈存元素；最小栈同步存当前最小值，入栈时比较更新，出栈时同步弹出。
- 复杂度：操作均摊 O(1)。

```java
import java.util.*;
class MinStack {
    private Deque<Integer> st = new ArrayDeque<>();
    private Deque<Integer> min = new ArrayDeque<>();
    public void push(int x) {
        st.push(x);
        if (min.isEmpty() || x <= min.peek()) min.push(x);
    }
    public void pop() {
        int x = st.pop(); if (!min.isEmpty() && x == min.peek()) min.pop();
    }
    public int top() { return st.peek(); }
    public int getMin() { return min.peek(); }
}
```

## 题解二：通用解法（单栈存对）
- 标签：栈、数据结构
- 思路：栈元素为 `(val, curMin)`，每次入栈记录当下最小值；出栈即可恢复。

```java
import java.util.*;
class MinStack {
    private static class Node { int v, m; Node(int v,int m){this.v=v;this.m=m;} }
    private Deque<Node> st = new ArrayDeque<>();
    public void push(int x) {
        int m = st.isEmpty() ? x : Math.min(x, st.peek().m);
        st.push(new Node(x, m));
    }
    public void pop() { st.pop(); }
    public int top() { return st.peek().v; }
    public int getMin() { return st.peek().m; }
}
```

## 题解三：最好理解（“当前最小”随入栈更新）
- 直觉：每次入栈都更新到当前最小，出栈时自然恢复到之前的最小值。

## 总结思路
- 双栈更直观；单栈更紧凑。注意等值入栈时的处理。

## 相关标签
- 栈、数据结构