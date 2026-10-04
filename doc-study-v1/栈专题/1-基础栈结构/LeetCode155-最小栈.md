# LeetCode155-最小栈

# LeetCode 155 - 最小栈
## 📋 题目描述
**难度：中等**

设计一个支持 `push`，`pop`，`top` 操作，并能在常数时间内检索到最小元素的栈。

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
+ `pop`、`top` 和 `getMin` 操作总是在**非空栈**上调用
+ `push`、`pop`、`top` 和 `getMin` 最多被调用 `3 * 10^4` 次

## 🎯 解题思路
### 核心挑战
普通栈只能在 O(1) 时间内访问栈顶元素，但要在 O(1) 时间内获取最小元素，需要额外的数据结构来维护最小值信息。

### 关键洞察
1. **最小值的变化规律**：
    - 当新元素入栈时，最小值可能更新
    - 当栈顶元素出栈时，如果它是当前最小值，需要恢复到之前的最小值
2. **辅助栈的思想**：
    - 使用一个辅助栈来存储每个状态下的最小值
    - 主栈和辅助栈同步操作

### 算法思路
```plain
方法一：双栈法
- 主栈：存储所有元素
- 辅助栈：存储每个状态下的最小值

方法二：单栈法
- 在栈中存储差值，节省空间
- 通过差值计算原始值和最小值

方法三：链表法
- 每个节点存储值和当前最小值
- 形成自包含的数据结构
```

## 💻 代码实现
### 方法一：双栈法（推荐）
```java
import java.util.*;

/**
 * 使用两个栈实现最小栈
 * 主栈存储所有元素，辅助栈存储最小值
 */
public class MinStack {
    
    private Deque<Integer> dataStack;    // 主栈：存储数据
    private Deque<Integer> minStack;     // 辅助栈：存储最小值
    
    public MinStack() {
        dataStack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }
    
    public void push(int val) {
        // 主栈正常入栈
        dataStack.push(val);
        
        // 辅助栈入栈当前最小值
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        } else {
            minStack.push(minStack.peek()); // 保持最小值
        }
    }
    
    public void pop() {
        if (!dataStack.isEmpty()) {
            dataStack.pop();
            minStack.pop();
        }
    }
    
    public int top() {
        return dataStack.peek();
    }
    
    public int getMin() {
        return minStack.peek();
    }
}
```

### 方法二：优化的双栈法（空间优化）
```java
/**
 * 优化版双栈法：辅助栈只在必要时入栈
 */
public class MinStackOptimized {
    
    private Deque<Integer> dataStack;
    private Deque<Integer> minStack;
    
    public MinStackOptimized() {
        dataStack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
    }
    
    public void push(int val) {
        dataStack.push(val);
        
        // 只有当新值小于等于当前最小值时，才入辅助栈
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        }
    }
    
    public void pop() {
        if (!dataStack.isEmpty()) {
            int popped = dataStack.pop();
            
            // 如果弹出的是最小值，辅助栈也要弹出
            if (!minStack.isEmpty() && popped == minStack.peek()) {
                minStack.pop();
            }
        }
    }
    
    public int top() {
        return dataStack.peek();
    }
    
    public int getMin() {
        return minStack.peek();
    }
}
```

### 方法三：单栈差值法
```java
/**
 * 使用单栈存储差值的方法
 * 节省空间但逻辑较复杂
 */
public class MinStackDifference {
    
    private Deque<Long> stack;  // 存储差值，使用 Long 防止溢出
    private long min;           // 当前最小值
    
    public MinStackDifference() {
        stack = new ArrayDeque<>();
    }
    
    public void push(int val) {
        if (stack.isEmpty()) {
            stack.push(0L);
            min = val;
        } else {
            // 存储与当前最小值的差值
            long diff = (long) val - min;
            stack.push(diff);
            
            // 如果新值更小，更新最小值
            if (val < min) {
                min = val;
            }
        }
    }
    
    public void pop() {
        if (!stack.isEmpty()) {
            long diff = stack.pop();
            
            // 如果差值小于0，说明弹出的是最小值
            if (diff < 0) {
                min = min - diff; // 恢复之前的最小值
            }
        }
    }
    
    public int top() {
        long diff = stack.peek();
        
        if (diff < 0) {
            return (int) min; // 栈顶是最小值
        } else {
            return (int) (min + diff); // 通过差值计算原值
        }
    }
    
    public int getMin() {
        return (int) min;
    }
}
```

### 方法四：链表节点法
```java
/**
 * 使用链表节点，每个节点存储值和当前最小值
 */
public class MinStackLinkedList {
    
    private Node head;
    
    private static class Node {
        int val;
        int min;
        Node next;
        
        Node(int val, int min, Node next) {
            this.val = val;
            this.min = min;
            this.next = next;
        }
    }
    
    public MinStackLinkedList() {
        head = null;
    }
    
    public void push(int val) {
        if (head == null) {
            head = new Node(val, val, null);
        } else {
            int currentMin = Math.min(val, head.min);
            head = new Node(val, currentMin, head);
        }
    }
    
    public void pop() {
        if (head != null) {
            head = head.next;
        }
    }
    
    public int top() {
        return head.val;
    }
    
    public int getMin() {
        return head.min;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
| 操作 | 双栈法 | 差值法 | 链表法 |
| --- | --- | --- | --- |
| **push** | O(1) | O(1) | O(1) |
| **pop** | O(1) | O(1) | O(1) |
| **top** | O(1) | O(1) | O(1) |
| **getMin** | O(1) | O(1) | O(1) |


### 空间复杂度
| 方法 | 空间复杂度 | 说明 |
| --- | --- | --- |
| **双栈法** | O(n) | 两个栈，最坏情况下都存储 n 个元素 |
| **优化双栈** | O(n) | 辅助栈最多存储 n 个元素 |
| **差值法** | O(n) | 单栈，但需要额外的 min 变量 |
| **链表法** | O(n) | 每个节点额外存储 min 值 |


## 🎨 可视化演示
### 双栈法演示
```java
/**
 * 带可视化输出的最小栈
 */
public class VisualMinStack {
    
    private Deque<Integer> dataStack;
    private Deque<Integer> minStack;
    
    public VisualMinStack() {
        dataStack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
        System.out.println("🏗️  初始化最小栈");
        printState();
    }
    
    public void push(int val) {
        System.out.printf("\n📥 Push %d\n", val);
        
        dataStack.push(val);
        
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
            System.out.printf("   新的最小值: %d\n", val);
        } else {
            minStack.push(minStack.peek());
            System.out.printf("   保持最小值: %d\n", minStack.peek());
        }
        
        printState();
    }
    
    public void pop() {
        if (dataStack.isEmpty()) {
            System.out.println("\n❌ 栈为空，无法弹出");
            return;
        }
        
        int popped = dataStack.pop();
        minStack.pop();
        
        System.out.printf("\n📤 Pop %d\n", popped);
        printState();
    }
    
    public int top() {
        if (dataStack.isEmpty()) {
            throw new RuntimeException("栈为空");
        }
        
        int topVal = dataStack.peek();
        System.out.printf("\n🔝 Top: %d\n", topVal);
        return topVal;
    }
    
    public int getMin() {
        if (minStack.isEmpty()) {
            throw new RuntimeException("栈为空");
        }
        
        int minVal = minStack.peek();
        System.out.printf("\n⬇️  Min: %d\n", minVal);
        return minVal;
    }
    
    private void printState() {
        System.out.println("   ┌─────────────────┐");
        System.out.println("   │  数据栈  │ 最小栈 │");
        System.out.println("   ├─────────────────┤");
        
        List<Integer> dataList = new ArrayList<>(dataStack);
        List<Integer> minList = new ArrayList<>(minStack);
        
        int maxSize = Math.max(dataList.size(), minList.size());
        
        for (int i = 0; i < maxSize; i++) {
            String dataStr = i < dataList.size() ? 
                String.format("%4d", dataList.get(i)) : "    ";
            String minStr = i < minList.size() ? 
                String.format("%4d", minList.get(i)) : "    ";
            
            System.out.printf("   │   %s   │  %s   │\n", dataStr, minStr);
        }
        
        if (maxSize == 0) {
            System.out.println("   │   空    │   空   │");
        }
        
        System.out.println("   └─────────────────┘");
    }
    
    public static void main(String[] args) {
        VisualMinStack minStack = new VisualMinStack();
        
        // 模拟题目示例
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);
        minStack.getMin();
        minStack.pop();
        minStack.top();
        minStack.getMin();
    }
}
```

### 操作序列演示
```plain
🏗️  初始化最小栈
   ┌─────────────────┐
   │  数据栈  │ 最小栈 │
   ├─────────────────┤
   │   空    │   空   │
   └─────────────────┘

📥 Push -2
   新的最小值: -2
   ┌─────────────────┐
   │  数据栈  │ 最小栈 │
   ├─────────────────┤
   │   -2   │   -2   │
   └─────────────────┘

📥 Push 0
   保持最小值: -2
   ┌─────────────────┐
   │  数据栈  │ 最小栈 │
   ├─────────────────┤
   │    0   │   -2   │
   │   -2   │   -2   │
   └─────────────────┘

📥 Push -3
   新的最小值: -3
   ┌─────────────────┐
   │  数据栈  │ 最小栈 │
   ├─────────────────┤
   │   -3   │   -3   │
   │    0   │   -2   │
   │   -2   │   -2   │
   └─────────────────┘

⬇️  Min: -3

📤 Pop -3
   ┌─────────────────┐
   │  数据栈  │ 最小栈 │
   ├─────────────────┤
   │    0   │   -2   │
   │   -2   │   -2   │
   └─────────────────┘

🔝 Top: 0

⬇️  Min: -2
```

## 🧪 测试用例
### 基础功能测试
```java
public class MinStackTest {
    
    @Test
    public void testBasicOperations() {
        MinStack minStack = new MinStack();
        
        // 测试空栈
        assertTrue(minStack.isEmpty());
        
        // 测试单个元素
        minStack.push(5);
        assertEquals(5, minStack.top());
        assertEquals(5, minStack.getMin());
        
        // 测试多个元素
        minStack.push(3);
        minStack.push(7);
        assertEquals(7, minStack.top());
        assertEquals(3, minStack.getMin());
        
        // 测试弹出操作
        minStack.pop();
        assertEquals(3, minStack.top());
        assertEquals(3, minStack.getMin());
    }
    
    @Test
    public void testMinimumTracking() {
        MinStack minStack = new MinStack();
        
        // 递减序列
        minStack.push(3);
        minStack.push(2);
        minStack.push(1);
        assertEquals(1, minStack.getMin());
        
        minStack.pop();
        assertEquals(2, minStack.getMin());
        
        minStack.pop();
        assertEquals(3, minStack.getMin());
    }
    
    @Test
    public void testDuplicateMinimums() {
        MinStack minStack = new MinStack();
        
        minStack.push(1);
        minStack.push(1);
        minStack.push(2);
        assertEquals(1, minStack.getMin());
        
        minStack.pop();
        assertEquals(1, minStack.getMin());
        
        minStack.pop();
        assertEquals(1, minStack.getMin());
    }
    
    @Test
    public void testNegativeNumbers() {
        MinStack minStack = new MinStack();
        
        minStack.push(-2);
        minStack.push(0);
        minStack.push(-3);
        
        assertEquals(-3, minStack.getMin());
        minStack.pop();
        assertEquals(0, minStack.top());
        assertEquals(-2, minStack.getMin());
    }
}
```

### 性能测试
```java
public class MinStackPerformanceTest {
    
    @Test
    public void testLargeDataSet() {
        MinStack minStack = new MinStack();
        int n = 100000;
        
        long startTime = System.nanoTime();
        
        // 大量入栈操作
        for (int i = 0; i < n; i++) {
            minStack.push(i % 1000);
        }
        
        // 大量查询最小值
        for (int i = 0; i < 1000; i++) {
            minStack.getMin();
        }
        
        // 大量出栈操作
        for (int i = 0; i < n; i++) {
            minStack.pop();
        }
        
        long endTime = System.nanoTime();
        double duration = (endTime - startTime) / 1_000_000.0;
        
        System.out.printf("处理 %d 个操作耗时: %.2f ms\n", n * 3, duration);
        assertTrue(duration < 1000); // 应该在1秒内完成
    }
    
    @Test
    public void compareImplementations() {
        int n = 50000;
        Random random = new Random(42);
        
        // 生成测试数据
        int[] data = new int[n];
        for (int i = 0; i < n; i++) {
            data[i] = random.nextInt(10000);
        }
        
        // 测试双栈法
        long time1 = testImplementation(new MinStack(), data);
        
        // 测试优化双栈法
        long time2 = testImplementation(new MinStackOptimized(), data);
        
        // 测试差值法
        long time3 = testImplementation(new MinStackDifference(), data);
        
        // 测试链表法
        long time4 = testImplementation(new MinStackLinkedList(), data);
        
        System.out.printf("双栈法: %.2f ms\n", time1 / 1_000_000.0);
        System.out.printf("优化双栈法: %.2f ms\n", time2 / 1_000_000.0);
        System.out.printf("差值法: %.2f ms\n", time3 / 1_000_000.0);
        System.out.printf("链表法: %.2f ms\n", time4 / 1_000_000.0);
    }
    
    private long testImplementation(Object minStack, int[] data) {
        long startTime = System.nanoTime();
        
        // 使用反射调用方法（简化示例）
        try {
            Method push = minStack.getClass().getMethod("push", int.class);
            Method getMin = minStack.getClass().getMethod("getMin");
            Method pop = minStack.getClass().getMethod("pop");
            
            for (int val : data) {
                push.invoke(minStack, val);
                getMin.invoke(minStack);
            }
            
            for (int i = 0; i < data.length; i++) {
                pop.invoke(minStack);
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        return System.nanoTime() - startTime;
    }
}
```

## 🔧 变体问题
### 1. 最大栈
```java
/**
 * 支持获取最大值的栈
 */
public class MaxStack {
    
    private Deque<Integer> dataStack;
    private Deque<Integer> maxStack;
    
    public MaxStack() {
        dataStack = new ArrayDeque<>();
        maxStack = new ArrayDeque<>();
    }
    
    public void push(int val) {
        dataStack.push(val);
        
        if (maxStack.isEmpty() || val >= maxStack.peek()) {
            maxStack.push(val);
        } else {
            maxStack.push(maxStack.peek());
        }
    }
    
    public void pop() {
        if (!dataStack.isEmpty()) {
            dataStack.pop();
            maxStack.pop();
        }
    }
    
    public int top() {
        return dataStack.peek();
    }
    
    public int getMax() {
        return maxStack.peek();
    }
}
```

### 2. 同时支持最小值和最大值的栈
```java
/**
 * 同时维护最小值和最大值的栈
 */
public class MinMaxStack {
    
    private Deque<Integer> dataStack;
    private Deque<Integer> minStack;
    private Deque<Integer> maxStack;
    
    public MinMaxStack() {
        dataStack = new ArrayDeque<>();
        minStack = new ArrayDeque<>();
        maxStack = new ArrayDeque<>();
    }
    
    public void push(int val) {
        dataStack.push(val);
        
        // 维护最小值栈
        if (minStack.isEmpty() || val <= minStack.peek()) {
            minStack.push(val);
        } else {
            minStack.push(minStack.peek());
        }
        
        // 维护最大值栈
        if (maxStack.isEmpty() || val >= maxStack.peek()) {
            maxStack.push(val);
        } else {
            maxStack.push(maxStack.peek());
        }
    }
    
    public void pop() {
        if (!dataStack.isEmpty()) {
            dataStack.pop();
            minStack.pop();
            maxStack.pop();
        }
    }
    
    public int top() {
        return dataStack.peek();
    }
    
    public int getMin() {
        return minStack.peek();
    }
    
    public int getMax() {
        return maxStack.peek();
    }
}
```

### 3. 支持删除最小值的栈
```java
/**
 * 支持删除最小值操作的栈
 */
public class MinStackWithRemove {
    
    private List<Integer> data;
    private List<Integer> minIndices; // 存储最小值的索引
    
    public MinStackWithRemove() {
        data = new ArrayList<>();
        minIndices = new ArrayList<>();
    }
    
    public void push(int val) {
        data.add(val);
        
        // 更新最小值索引
        if (minIndices.isEmpty() || val <= data.get(minIndices.get(minIndices.size() - 1))) {
            minIndices.add(data.size() - 1);
        }
    }
    
    public void pop() {
        if (!data.isEmpty()) {
            int lastIndex = data.size() - 1;
            data.remove(lastIndex);
            
            // 如果弹出的是最小值，更新最小值索引
            if (!minIndices.isEmpty() && minIndices.get(minIndices.size() - 1) == lastIndex) {
                minIndices.remove(minIndices.size() - 1);
            }
        }
    }
    
    public int top() {
        return data.get(data.size() - 1);
    }
    
    public int getMin() {
        int minIndex = minIndices.get(minIndices.size() - 1);
        return data.get(minIndex);
    }
    
    public void removeMin() {
        if (!minIndices.isEmpty()) {
            int minIndex = minIndices.remove(minIndices.size() - 1);
            data.remove(minIndex);
            
            // 更新后续索引
            for (int i = 0; i < minIndices.size(); i++) {
                if (minIndices.get(i) > minIndex) {
                    minIndices.set(i, minIndices.get(i) - 1);
                }
            }
        }
    }
}
```

## 💡 解题技巧总结
### 1. 设计思路
+ **辅助数据结构**：使用额外的栈来维护最小值信息
+ **同步操作**：主栈和辅助栈的操作要保持同步
+ **状态一致性**：确保任何时候都能正确获取最小值

### 2. 优化策略
+ **空间优化**：辅助栈只在必要时存储数据
+ **时间优化**：所有操作都保持 O(1) 时间复杂度
+ **代码简洁性**：选择最易理解和维护的实现方式

### 3. 常见陷阱
+ **边界条件**：空栈时的操作处理
+ **重复最小值**：正确处理相同最小值的情况
+ **整数溢出**：差值法中需要考虑溢出问题

### 4. 扩展应用
+ **最大栈**：类似思路实现最大值查询
+ **范围查询**：扩展到查询任意范围的最值
+ **多维最值**：在多个维度上维护最值信息

最小栈是栈数据结构的经典扩展应用，它展示了如何通过辅助数据结构来增强基本数据结构的功能，这种设计思想在很多算法问题中都有应用！



> 更新: 2025-09-19 00:53:55  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/3491d025523af424a986e0860f07a056>