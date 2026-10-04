# LeetCode 232 - 用栈实现队列
## 📋 题目描述
**难度：简单**

请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（`push`、`pop`、`peek`、`empty`）：

实现 `MyQueue` 类：

+ `void push(int x)` 将元素 x 推到队列的末尾
+ `int pop()` 从队列的开头移除并返回元素
+ `int peek()` 返回队列开头的元素
+ `boolean empty()` 如果队列为空，返回 `true` ；否则，返回 `false`

**说明：**

+ 你 **只能** 使用标准的栈操作 —— 也就是只有 `push to top`, `peek/pop from top`, `size`, 和 `is empty` 操作是合法的。
+ 你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。

### 示例
```plain
输入：
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 1, 1, false]

解释：
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

### 约束条件
+ `1 <= x <= 9`
+ 最多调用 `100` 次 `push`、`pop`、`peek` 和 `empty`
+ 假设所有操作都是有效的 （例如，一个空的队列不会调用 `pop` 或者 `peek` 操作）

### 进阶
你能否实现每个操作均摊时间复杂度为 `O(1)` 的队列？换句话说，执行 `n` 个操作的总时间复杂度为 `O(n)` ，即使其中一个操作可能花费较长时间。

## 🎯 解题思路
### 核心问题分析
这是一个经典的**双栈协作问题**。关键在于：

1. 栈是后进先出（LIFO），队列是先进先出（FIFO）
2. 需要用两个栈来模拟队列的行为
3. 一个栈负责入队，另一个栈负责出队

### 双栈协作原理
```plain
核心思想：
- 输入栈（inStack）：负责接收新元素
- 输出栈（outStack）：负责弹出元素
- 当需要出队时，如果输出栈为空，将输入栈的所有元素转移到输出栈

数据流向：
push: 元素 -> 输入栈
pop/peek: 输出栈 -> 元素（如果输出栈为空，先从输入栈转移）

关键观察：
- 元素从输入栈转移到输出栈时，顺序会反转
- 这正好实现了FIFO的效果
```

### 算法步骤
```plain
1. 初始化两个栈：inStack 和 outStack
2. push操作：直接将元素压入 inStack
3. pop/peek操作：
   - 如果 outStack 不为空，直接从 outStack 操作
   - 如果 outStack 为空，将 inStack 的所有元素转移到 outStack
   - 然后从 outStack 操作
4. empty操作：两个栈都为空时队列才为空
```

### 图解演示
**操作序列：push(1), push(2), push(3), pop(), push(4), pop(), peek()**

```plain
初始状态：
inStack: []
outStack: []
队列视图: []

操作 1: push(1)
inStack: [1]
outStack: []
队列视图: [1]

操作 2: push(2)  
inStack: [1, 2]
outStack: []
队列视图: [1, 2]

操作 3: push(3)
inStack: [1, 2, 3]
outStack: []
队列视图: [1, 2, 3]

操作 4: pop()
需要出队，outStack为空，转移元素：
转移前：inStack: [1, 2, 3], outStack: []
转移后：inStack: [], outStack: [3, 2, 1]
弹出 outStack 顶部：返回 1
inStack: []
outStack: [3, 2]
队列视图: [2, 3]

操作 5: push(4)
inStack: [4]
outStack: [3, 2]
队列视图: [2, 3, 4]

操作 6: pop()
outStack不为空，直接弹出：返回 2
inStack: [4]
outStack: [3]
队列视图: [3, 4]

操作 7: peek()
outStack不为空，直接查看顶部：返回 3
inStack: [4]
outStack: [3]
队列视图: [3, 4]
```

## 💻 代码实现
### 方法一：双栈实现（推荐）
```java
import java.util.*;

class MyQueue {
    
    private Deque<Integer> inStack;   // 输入栈
    private Deque<Integer> outStack;  // 输出栈
    
    public MyQueue() {
        inStack = new ArrayDeque<>();
        outStack = new ArrayDeque<>();
    }
    
    /**
     * 将元素推入队列末尾
     */
    public void push(int x) {
        inStack.push(x);
    }
    
    /**
     * 从队列开头移除并返回元素
     */
    public int pop() {
        // 确保输出栈有元素
        transferIfNeeded();
        return outStack.pop();
    }
    
    /**
     * 返回队列开头的元素
     */
    public int peek() {
        // 确保输出栈有元素
        transferIfNeeded();
        return outStack.peek();
    }
    
    /**
     * 检查队列是否为空
     */
    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
    
    /**
     * 如果输出栈为空，将输入栈的所有元素转移到输出栈
     */
    private void transferIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}
```

### 方法二：优化版本（延迟转移）
```java
class MyQueueOptimized {
    
    private Deque<Integer> inStack;
    private Deque<Integer> outStack;
    private Integer front; // 缓存队列头元素
    
    public MyQueueOptimized() {
        inStack = new ArrayDeque<>();
        outStack = new ArrayDeque<>();
        front = null;
    }
    
    public void push(int x) {
        // 如果是第一个元素，记录为队列头
        if (inStack.isEmpty()) {
            front = x;
        }
        inStack.push(x);
    }
    
    public int pop() {
        if (outStack.isEmpty()) {
            // 转移所有元素到输出栈
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
        
        int result = outStack.pop();
        
        // 更新front缓存
        if (outStack.isEmpty() && !inStack.isEmpty()) {
            front = inStack.peek();
        }
        
        return result;
    }
    
    public int peek() {
        if (!outStack.isEmpty()) {
            return outStack.peek();
        }
        return front;
    }
    
    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
}
```

### 方法三：单栈递归实现（理论参考）
```java
class MyQueueRecursive {
    
    private Deque<Integer> stack;
    
    public MyQueueRecursive() {
        stack = new ArrayDeque<>();
    }
    
    public void push(int x) {
        stack.push(x);
    }
    
    public int pop() {
        if (stack.size() == 1) {
            return stack.pop();
        }
        
        // 递归取出栈底元素
        int top = stack.pop();
        int result = pop(); // 递归调用
        stack.push(top);    // 恢复栈结构
        return result;
    }
    
    public int peek() {
        if (stack.size() == 1) {
            return stack.peek();
        }
        
        int top = stack.pop();
        int result = peek(); // 递归调用
        stack.push(top);     // 恢复栈结构
        return result;
    }
    
    public boolean empty() {
        return stack.isEmpty();
    }
}
```

### 方法四：使用数组实现
```java
class MyQueueArray {
    
    private int[] inStack;
    private int[] outStack;
    private int inTop;
    private int outTop;
    private static final int CAPACITY = 100;
    
    public MyQueueArray() {
        inStack = new int[CAPACITY];
        outStack = new int[CAPACITY];
        inTop = -1;
        outTop = -1;
    }
    
    public void push(int x) {
        inStack[++inTop] = x;
    }
    
    public int pop() {
        transferIfNeeded();
        return outStack[outTop--];
    }
    
    public int peek() {
        transferIfNeeded();
        return outStack[outTop];
    }
    
    public boolean empty() {
        return inTop == -1 && outTop == -1;
    }
    
    private void transferIfNeeded() {
        if (outTop == -1) {
            while (inTop != -1) {
                outStack[++outTop] = inStack[inTop--];
            }
        }
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**双栈实现：**

+ `push()`：O(1)
+ `pop()`：均摊 O(1)，最坏情况 O(n)
+ `peek()`：均摊 O(1)，最坏情况 O(n)  
+ `empty()`：O(1)

**均摊分析：**

+ 每个元素最多被转移一次（从输入栈到输出栈）
+ n 个操作的总时间复杂度为 O(n)
+ 因此均摊时间复杂度为 O(1)

**单栈递归实现：**

+ `push()`：O(1)
+ `pop()`：O(n)
+ `peek()`：O(n)
+ `empty()`：O(1)

### 空间复杂度
**双栈实现：**

+ O(n)，其中 n 是队列中元素的数量

**单栈递归实现：**

+ O(n)，递归调用栈的深度

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的队列实现
 */
public class VisualMyQueue {
    
    private Deque<Integer> inStack;
    private Deque<Integer> outStack;
    private int operationCount;
    
    public VisualMyQueue() {
        inStack = new ArrayDeque<>();
        outStack = new ArrayDeque<>();
        operationCount = 0;
        
        System.out.println("🚀 创建队列");
        printState();
    }
    
    public void push(int x) {
        operationCount++;
        System.out.printf("\n操作 %d: push(%d)\n", operationCount, x);
        
        inStack.push(x);
        
        System.out.printf("✅ 元素 %d 加入输入栈\n", x);
        printState();
    }
    
    public int pop() {
        operationCount++;
        System.out.printf("\n操作 %d: pop()\n", operationCount);
        
        transferIfNeeded();
        int result = outStack.pop();
        
        System.out.printf("✅ 弹出元素: %d\n", result);
        printState();
        
        return result;
    }
    
    public int peek() {
        operationCount++;
        System.out.printf("\n操作 %d: peek()\n", operationCount);
        
        transferIfNeeded();
        int result = outStack.peek();
        
        System.out.printf("✅ 队列头元素: %d\n", result);
        printState();
        
        return result;
    }
    
    public boolean empty() {
        operationCount++;
        System.out.printf("\n操作 %d: empty()\n", operationCount);
        
        boolean result = inStack.isEmpty() && outStack.isEmpty();
        
        System.out.printf("✅ 队列是否为空: %s\n", result);
        printState();
        
        return result;
    }
    
    private void transferIfNeeded() {
        if (outStack.isEmpty() && !inStack.isEmpty()) {
            System.out.println("🔄 输出栈为空，开始转移元素...");
            
            List<Integer> transferred = new ArrayList<>();
            while (!inStack.isEmpty()) {
                int element = inStack.pop();
                outStack.push(element);
                transferred.add(element);
            }
            
            System.out.printf("   转移了 %d 个元素: %s\n", 
                             transferred.size(), transferred);
            System.out.println("   转移完成！");
        }
    }
    
    private void printState() {
        System.out.println("📊 当前状态:");
        
        // 打印输入栈
        System.out.print("   输入栈: [");
        if (inStack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> inList = new ArrayList<>(inStack);
            Collections.reverse(inList);
            for (int i = 0; i < inList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(inList.get(i));
            }
        }
        System.out.println("] (底 -> 顶)");
        
        // 打印输出栈
        System.out.print("   输出栈: [");
        if (outStack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> outList = new ArrayList<>(outStack);
            Collections.reverse(outList);
            for (int i = 0; i < outList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(outList.get(i));
            }
        }
        System.out.println("] (底 -> 顶)");
        
        // 打印队列视图
        System.out.print("   队列视图: [");
        List<Integer> queueView = getQueueView();
        for (int i = 0; i < queueView.size(); i++) {
            if (i > 0) System.out.print(", ");
            System.out.print(queueView.get(i));
        }
        System.out.println("] (头 -> 尾)");
        
        System.out.println("   " + "-".repeat(40));
    }
    
    private List<Integer> getQueueView() {
        List<Integer> result = new ArrayList<>();
        
        // 输出栈的元素（从底到顶）
        List<Integer> outList = new ArrayList<>(outStack);
        Collections.reverse(outList);
        result.addAll(outList);
        
        // 输入栈的元素（从顶到底）
        result.addAll(inStack);
        
        return result;
    }
    
    public static void main(String[] args) {
        System.out.println("🧪 测试用栈实现队列");
        System.out.println("=" + "=".repeat(50));
        
        VisualMyQueue queue = new VisualMyQueue();
        
        // 执行示例操作
        queue.push(1);
        queue.push(2);
        queue.peek();
        queue.pop();
        queue.empty();
        
        System.out.println("\n🎯 额外测试：");
        queue.push(3);
        queue.push(4);
        queue.pop();
        queue.push(5);
        queue.peek();
        queue.pop();
        queue.pop();
        queue.empty();
    }
}
```

### 运行结果示例
```plain
🧪 测试用栈实现队列
==================================================
🚀 创建队列
📊 当前状态:
   输入栈: [空] (底 -> 顶)
   输出栈: [空] (底 -> 顶)
   队列视图: [] (头 -> 尾)
   ----------------------------------------

操作 1: push(1)
✅ 元素 1 加入输入栈
📊 当前状态:
   输入栈: [1] (底 -> 顶)
   输出栈: [空] (底 -> 顶)
   队列视图: [1] (头 -> 尾)
   ----------------------------------------

操作 2: push(2)
✅ 元素 2 加入输入栈
📊 当前状态:
   输入栈: [1, 2] (底 -> 顶)
   输出栈: [空] (底 -> 顶)
   队列视图: [1, 2] (头 -> 尾)
   ----------------------------------------

操作 3: peek()
🔄 输出栈为空，开始转移元素...
   转移了 2 个元素: [2, 1]
   转移完成！
✅ 队列头元素: 1
📊 当前状态:
   输入栈: [空] (底 -> 顶)
   输出栈: [2, 1] (底 -> 顶)
   队列视图: [1, 2] (头 -> 尾)
   ----------------------------------------

操作 4: pop()
✅ 弹出元素: 1
📊 当前状态:
   输入栈: [空] (底 -> 顶)
   输出栈: [2] (底 -> 顶)
   队列视图: [2] (头 -> 尾)
   ----------------------------------------

操作 5: empty()
✅ 队列是否为空: false
📊 当前状态:
   输入栈: [空] (底 -> 顶)
   输出栈: [2] (底 -> 顶)
   队列视图: [2] (头 -> 尾)
   ----------------------------------------
```

## 🧪 测试用例
### 基础功能测试
```java
public class MyQueueTest {
    
    @Test
    public void testBasicOperations() {
        MyQueue queue = new MyQueue();
        
        // 测试空队列
        assertTrue(queue.empty());
        
        // 测试push和peek
        queue.push(1);
        assertFalse(queue.empty());
        assertEquals(1, queue.peek());
        
        queue.push(2);
        assertEquals(1, queue.peek()); // 队列头仍然是1
        
        // 测试pop
        assertEquals(1, queue.pop());
        assertEquals(2, queue.peek());
        assertEquals(2, queue.pop());
        
        assertTrue(queue.empty());
    }
    
    @Test
    public void testSequentialOperations() {
        MyQueue queue = new MyQueue();
        
        // 连续push
        for (int i = 1; i <= 5; i++) {
            queue.push(i);
        }
        
        // 连续pop，应该按FIFO顺序
        for (int i = 1; i <= 5; i++) {
            assertEquals(i, queue.pop());
        }
        
        assertTrue(queue.empty());
    }
    
    @Test
    public void testMixedOperations() {
        MyQueue queue = new MyQueue();
        
        queue.push(1);
        queue.push(2);
        assertEquals(1, queue.pop());
        
        queue.push(3);
        assertEquals(2, queue.peek());
        assertEquals(2, queue.pop());
        assertEquals(3, queue.pop());
        
        assertTrue(queue.empty());
    }
}
```

### 性能测试
```java
public class PerformanceTest {
    
    @Test
    public void testAmortizedComplexity() {
        MyQueue queue = new MyQueue();
        int n = 10000;
        
        // 测试大量操作的性能
        long startTime = System.nanoTime();
        
        // 先push n个元素
        for (int i = 0; i < n; i++) {
            queue.push(i);
        }
        
        // 再pop n个元素
        for (int i = 0; i < n; i++) {
            assertEquals(i, queue.pop());
        }
        
        long endTime = System.nanoTime();
        double timeMs = (endTime - startTime) / 1_000_000.0;
        
        System.out.printf("执行 %d 次操作耗时: %.2f ms\n", 2 * n, timeMs);
        System.out.printf("平均每次操作: %.4f ms\n", timeMs / (2 * n));
        
        // 验证均摊复杂度接近O(1)
        assertTrue(timeMs / (2 * n) < 0.01); // 每次操作应该小于0.01ms
    }
    
    @Test
    public void compareImplementations() {
        int n = 1000;
        
        // 测试双栈实现
        long startTime = System.nanoTime();
        testImplementation(new MyQueue(), n);
        long time1 = System.nanoTime() - startTime;
        
        // 测试递归实现
        startTime = System.nanoTime();
        testImplementation(new MyQueueRecursive(), n);
        long time2 = System.nanoTime() - startTime;
        
        System.out.printf("双栈实现: %.2f ms\n", time1 / 1_000_000.0);
        System.out.printf("递归实现: %.2f ms\n", time2 / 1_000_000.0);
        System.out.printf("性能提升: %.2fx\n", (double) time2 / time1);
    }
    
    private void testImplementation(Object queue, int n) {
        // 使用反射调用方法进行统一测试
        try {
            Method push = queue.getClass().getMethod("push", int.class);
            Method pop = queue.getClass().getMethod("pop");
            
            for (int i = 0; i < n; i++) {
                push.invoke(queue, i);
            }
            
            for (int i = 0; i < n; i++) {
                pop.invoke(queue);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 225 - 用队列实现栈
```java
/**
 * 用队列实现栈（双栈问题的逆向）
 */
class MyStack {
    
    private Queue<Integer> queue1;
    private Queue<Integer> queue2;
    
    public MyStack() {
        queue1 = new LinkedList<>();
        queue2 = new LinkedList<>();
    }
    
    public void push(int x) {
        queue2.offer(x);
        
        // 将queue1的所有元素转移到queue2
        while (!queue1.isEmpty()) {
            queue2.offer(queue1.poll());
        }
        
        // 交换两个队列
        Queue<Integer> temp = queue1;
        queue1 = queue2;
        queue2 = temp;
    }
    
    public int pop() {
        return queue1.poll();
    }
    
    public int top() {
        return queue1.peek();
    }
    
    public boolean empty() {
        return queue1.isEmpty();
    }
}
```

### 2. 最小队列（扩展应用）
```java
/**
 * 支持获取最小值的队列
 */
class MinQueue {
    
    private Deque<Integer> inStack;
    private Deque<Integer> outStack;
    private Deque<Integer> inMin;    // 输入栈的最小值栈
    private Deque<Integer> outMin;   // 输出栈的最小值栈
    
    public MinQueue() {
        inStack = new ArrayDeque<>();
        outStack = new ArrayDeque<>();
        inMin = new ArrayDeque<>();
        outMin = new ArrayDeque<>();
    }
    
    public void push(int x) {
        inStack.push(x);
        
        // 维护输入栈的最小值
        if (inMin.isEmpty() || x <= inMin.peek()) {
            inMin.push(x);
        }
    }
    
    public int pop() {
        transferIfNeeded();
        
        int result = outStack.pop();
        
        // 维护输出栈的最小值
        if (!outMin.isEmpty() && result == outMin.peek()) {
            outMin.pop();
        }
        
        return result;
    }
    
    public int peek() {
        transferIfNeeded();
        return outStack.peek();
    }
    
    public int getMin() {
        int min = Integer.MAX_VALUE;
        
        if (!inMin.isEmpty()) {
            min = Math.min(min, inMin.peek());
        }
        
        if (!outMin.isEmpty()) {
            min = Math.min(min, outMin.peek());
        }
        
        return min;
    }
    
    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }
    
    private void transferIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                int element = inStack.pop();
                outStack.push(element);
                
                // 维护输出栈的最小值
                if (outMin.isEmpty() || element <= outMin.peek()) {
                    outMin.push(element);
                }
                
                // 维护输入栈的最小值
                if (!inMin.isEmpty() && element == inMin.peek()) {
                    inMin.pop();
                }
            }
        }
    }
}
```

### 3. 循环队列的栈实现
```java
/**
 * 用栈实现固定大小的循环队列
 */
class MyCircularQueue {
    
    private int[] data;
    private int front;
    private int rear;
    private int size;
    private int capacity;
    
    public MyCircularQueue(int k) {
        capacity = k;
        data = new int[k];
        front = 0;
        rear = 0;
        size = 0;
    }
    
    public boolean enQueue(int value) {
        if (isFull()) return false;
        
        data[rear] = value;
        rear = (rear + 1) % capacity;
        size++;
        return true;
    }
    
    public boolean deQueue() {
        if (isEmpty()) return false;
        
        front = (front + 1) % capacity;
        size--;
        return true;
    }
    
    public int Front() {
        return isEmpty() ? -1 : data[front];
    }
    
    public int Rear() {
        return isEmpty() ? -1 : data[(rear - 1 + capacity) % capacity];
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
    
    public boolean isFull() {
        return size == capacity;
    }
}
```

## 💡 解题技巧总结
### 1. 双栈协作的核心思想
+ **分工明确**：一个栈负责入队，一个栈负责出队
+ **延迟转移**：只有在需要时才转移元素
+ **顺序反转**：利用栈的LIFO特性实现FIFO效果

### 2. 均摊复杂度分析
+ **关键观察**：每个元素最多被转移一次
+ **总操作数**：n次push + n次pop = 2n次操作
+ **总转移数**：每个元素最多转移1次 = n次转移
+ **均摊复杂度**：(2n + n) / 2n = O(1)

### 3. 实现技巧
+ **及时转移**：在pop/peek时检查是否需要转移
+ **状态维护**：正确维护两个栈的状态
+ **边界处理**：注意空队列的情况

### 4. 扩展应用
+ **最小队列**：结合最小栈的思想
+ **循环队列**：固定大小的队列实现
+ **双端队列**：支持两端操作的队列

### 5. 性能优化
+ **缓存优化**：缓存队列头元素避免频繁转移
+ **批量转移**：一次性转移所有元素
+ **内存优化**：使用数组代替链表实现栈

这道题展示了如何用栈这种简单的数据结构来实现更复杂的队列功能，是理解数据结构转换和均摊分析的经典例题！

