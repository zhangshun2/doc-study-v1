# LeetCode-155-最小栈

# LeetCode 155 - 最小栈
## 题目描述
**难度：中等**

设计一个支持 `push` ，`pop` ，`top` 操作，并能在常数时间内检索到最小元素的栈。

实现 `MinStack` 类:

+ `MinStack()` 初始化堆栈对象。
+ `void push(int val)` 将元素val推入堆栈。
+ `void pop()` 删除堆栈顶部的元素。
+ `int top()` 获取堆栈顶部的元素。
+ `int getMin()` 获取堆栈中的最小元素。

### 示例
```plain
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // 返回 -3
minStack.pop();
minStack.top();    // 返回 0
minStack.getMin(); // 返回 -2
```

### 约束条件
+ `-2^31 <= val <= 2^31 - 1`
+ `pop`、`top` 和 `getMin` 操作总是在 **非空栈** 上调用
+ `push`、`pop`、`top` 和 `getMin` 最多被调用 `3 * 10^4` 次

## 解题思路
这道题的核心挑战是：**如何在 O(1) 时间内获取栈中的最小元素**。

关键问题：

1. 栈的特性是后进先出，我们只能访问栈顶元素
2. 当栈顶元素被弹出后，我们需要知道剩余元素中的最小值
3. 所有操作都要求 O(1) 时间复杂度

### 方法一：辅助栈（推荐）
#### 核心思想
使用两个栈：

+ **主栈**：存储所有元素
+ **辅助栈**：存储每个状态下的最小值

#### 关键设计
+ 每次 `push` 时，同时向辅助栈压入当前的最小值
+ 每次 `pop` 时，同时从辅助栈弹出对应的最小值
+ `getMin` 直接返回辅助栈的栈顶元素

#### 图解分析
```plain
操作序列: push(-2) -> push(0) -> push(-3) -> getMin() -> pop() -> top() -> getMin()

步骤1: push(-2)
主栈:    [-2]
辅助栈:  [-2]  (当前最小值是-2)

步骤2: push(0)  
主栈:    [-2, 0]
辅助栈:  [-2, -2]  (当前最小值仍是-2)

步骤3: push(-3)
主栈:    [-2, 0, -3]
辅助栈:  [-2, -2, -3]  (当前最小值是-3)

步骤4: getMin()
返回辅助栈栈顶: -3

步骤5: pop()
主栈:    [-2, 0]      (弹出-3)
辅助栈:  [-2, -2]     (弹出-3对应的最小值)

步骤6: top()
返回主栈栈顶: 0

步骤7: getMin()
返回辅助栈栈顶: -2
```

### 方法二：单栈优化
#### 核心思想
只使用一个栈，但存储的不是原始值，而是与当前最小值的差值。

#### 关键设计
+ 用一个变量 `min` 记录当前最小值
+ 栈中存储 `val - min` 的差值
+ 通过差值的正负性判断是否需要更新最小值

## 代码实现
### 方法一：辅助栈解法（推荐）
```java
class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new LinkedList<Integer>();
        minStack = new LinkedList<Integer>();
    }
    
    public void push(int val) {
        stack.push(val);
        // 辅助栈存储当前状态下的最小值
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        } else {
            minStack.push(minStack.peek());
        }
    }
    
    public void pop() {
        stack.pop();
        minStack.pop();
    }
    
    public int top() {
        return stack.peek();
    }
    
    public int getMin() {
        return minStack.peek();
    }
}
```

### 方法二：优化的辅助栈（空间优化）
```java
class MinStack {
    private Deque<Integer> stack;
    private Deque<Integer> minStack;

    public MinStack() {
        stack = new LinkedList<Integer>();
        minStack = new LinkedList<Integer>();
    }
    
    public void push(int val) {
        stack.push(val);
        // 只在新的最小值时才压入辅助栈
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }
    }
    
    public void pop() {
        // 如果弹出的是最小值，同时从辅助栈弹出
        if (stack.peek().equals(minStack.peek())) {
            minStack.pop();
        }
        stack.pop();
    }
    
    public int top() {
        return stack.peek();
    }
    
    public int getMin() {
        return minStack.peek();
    }
}
```

### 方法三：单栈差值法
```java
class MinStack {
    private Deque<Long> stack;
    private long min;

    public MinStack() {
        stack = new LinkedList<Long>();
    }
    
    public void push(int val) {
        if (stack.isEmpty()) {
            stack.push(0L);
            min = val;
        } else {
            // 存储与当前最小值的差值
            stack.push((long)val - min);
            if (val < min) {
                min = val;
            }
        }
    }
    
    public void pop() {
        if (stack.isEmpty()) return;
        
        long pop = stack.pop();
        // 如果差值小于0，说明弹出的是最小值，需要恢复之前的最小值
        if (pop < 0) {
            min = min - pop;
        }
    }
    
    public int top() {
        long top = stack.peek();
        // 如果差值小于0，说明栈顶是最小值
        if (top < 0) {
            return (int)min;
        } else {
            return (int)(top + min);
        }
    }
    
    public int getMin() {
        return (int)min;
    }
}
```

### 方法四：链表实现
```java
class MinStack {
    private Node head;
    
    private class Node {
        int val;
        int min;
        Node next;
        
        Node(int val, int min, Node next) {
            this.val = val;
            this.min = min;
            this.next = next;
        }
    }

    public MinStack() {
        
    }
    
    public void push(int val) {
        if (head == null) {
            head = new Node(val, val, null);
        } else {
            head = new Node(val, Math.min(val, head.min), head);
        }
    }
    
    public void pop() {
        head = head.next;
    }
    
    public int top() {
        return head.val;
    }
    
    public int getMin() {
        return head.min;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **所有方法**：所有操作都是 O(1)

### 空间复杂度
+ **辅助栈方法**：O(n)，需要额外的辅助栈
+ **优化辅助栈**：O(n)，最坏情况下仍需要 O(n) 空间
+ **单栈差值法**：O(n)，只使用一个栈
+ **链表实现**：O(n)，每个节点存储额外的最小值信息

## 关键点总结
### 1. 设计思路对比
| 方法 | 优点 | 缺点 | 适用场景 |
| --- | --- | --- | --- |
| 辅助栈 | 思路简单，易理解 | 空间使用较多 | 面试推荐 |
| 优化辅助栈 | 空间稍有优化 | 逻辑稍复杂 | 空间敏感场景 |
| 单栈差值法 | 空间最优 | 理解困难，有溢出风险 | 高级优化 |
| 链表实现 | 结构清晰 | 额外的指针开销 | 特定需求 |


### 2. 辅助栈的核心思想
+ **状态保存**：每个状态都保存对应的最小值
+ **同步操作**：主栈和辅助栈同步进行 push/pop
+ **空间换时间**：用额外空间换取 O(1) 的查询时间

### 3. 单栈差值法的精髓
+ **相对存储**：存储相对于最小值的差值
+ **信息编码**：通过差值的正负性编码额外信息
+ **状态恢复**：通过差值计算恢复原始值和历史最小值

### 4. 常见错误
+ **忘记同步操作**：主栈和辅助栈必须同步
+ **边界条件**：空栈时的特殊处理
+ **数据溢出**：单栈差值法中的整数溢出问题
+ **相等值处理**：多个相同最小值的正确处理

## 扩展思考
### 1. 变种问题
+ **最大栈**：获取栈中最大元素
+ **最小队列**：在队列中实现类似功能
+ **滑动窗口最小值**：LeetCode 239 的变种

### 2. 优化方向
+ **内存优化**：减少辅助栈的空间使用
+ **缓存优化**：对频繁访问的最小值进行缓存
+ **并发安全**：多线程环境下的线程安全实现

### 3. 实际应用
+ **监控系统**：实时获取指标的最小值
+ **数据流处理**：流式数据的最小值跟踪
+ **算法优化**：其他算法中需要快速获取最小值的场景

### 4. 解法选择建议
+ **面试推荐**：辅助栈方法，思路清晰，易于解释
+ **生产环境**：根据具体的空间和时间要求选择
+ **学习目的**：建议都掌握，体现不同的设计思想

### 5. 设计模式体现
+ **装饰器模式**：在原有栈的基础上增加最小值功能
+ **策略模式**：不同的实现方法可以看作不同的策略
+ **组合模式**：多个数据结构的组合使用

### 6. 面试要点
+ **时间复杂度要求**：必须是 O(1)
+ **空间权衡**：讨论不同方法的空间使用
+ **边界处理**：空栈、单元素等特殊情况
+ **扩展性**：如何扩展到最大栈、最小队列等

这道题是栈应用的经典设计题，通过它可以深入理解数据结构设计中的权衡思想和优化技巧！



> 更新: 2025-09-19 00:54:30  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/f4330e75943aa7fabf1f652452fb7a17>