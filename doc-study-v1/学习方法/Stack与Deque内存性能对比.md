# Stack与Deque内存性能对比

# Stack与Deque内存性能对比
## 概述
在Java中，实现栈功能有多种选择，最常见的是直接使用`Stack`类和使用`Deque`接口的实现类（如`LinkedList`、`ArrayDeque`）。本文档详细分析这两种方式在内存使用上的优劣。

## 数据结构对比
### 1. Stack类的内存结构
```java
// 传统Stack写法
Stack<Integer> stack = new Stack<>();
```

**内存特点：**

+ **继承关系**：`Stack extends Vector extends AbstractList`
+ **底层实现**：基于动态数组（Object[]）
+ **同步机制**：所有方法都是synchronized的
+ **内存开销**：
    - 对象头：12-16字节（取决于JVM）
    - Vector的字段：elementData数组引用、elementCount、capacityIncrement等
    - 数组本身：初始容量10个Object引用 = 40字节（64位JVM）
    - **总计**：约60-80字节的基础开销

### 2. Deque接口实现的内存结构
#### 2.1 LinkedList实现
```java
// LinkedList作为栈
Deque<Integer> stack = new LinkedList<>();
```

**内存特点：**

+ **数据结构**：双向链表
+ **节点开销**：每个节点包含
    - 对象头：12-16字节
    - item引用：8字节
    - next引用：8字节  
    - prev引用：8字节
    - **每节点总计**：36-40字节
+ **LinkedList对象**：
    - 对象头：12-16字节
    - first/last引用：16字节
    - size字段：4字节
    - **总计**：约32-36字节基础开销

#### 2.2 ArrayDeque实现
```java
// ArrayDeque作为栈（推荐）
Deque<Integer> stack = new ArrayDeque<>();
```

**内存特点：**

+ **数据结构**：循环数组
+ **内存开销**：
    - 对象头：12-16字节
    - elements数组引用：8字节
    - head/tail索引：8字节
    - 数组本身：初始容量16个Object引用 = 64字节
    - **总计**：约92-96字节基础开销

## 详细性能分析
### 1. 内存使用效率
| 实现方式 | 基础开销 | 每元素开销 | 空间局部性 | 缓存友好性 |
| --- | --- | --- | --- | --- |
| Stack | 60-80字节 | 8字节 | 好 | 好 |
| LinkedList | 32-36字节 | 36-40字节 | 差 | 差 |
| ArrayDeque | 92-96字节 | 8字节 | 好 | 好 |


### 2. 内存分配模式
#### Stack/ArrayDeque（数组实现）
```java
// 连续内存分配示例
Object[] elements = new Object[capacity];
// 内存布局：[obj1][obj2][obj3][obj4]...
// 优点：缓存命中率高，内存访问效率好
```

#### LinkedList（链表实现）
```java
// 分散内存分配示例
class Node {
    Object item;
    Node next, prev;
}
// 内存布局：分散在堆的不同位置
// 缺点：缓存命中率低，内存碎片多
```

### 3. 扩容机制对比
#### Stack扩容
```java
// Vector的扩容机制
private void grow(int minCapacity) {
    int oldCapacity = elementData.length;
    // 默认扩容为原来的2倍
    int newCapacity = oldCapacity + ((capacityIncrement > 0) ? 
                     capacityIncrement : oldCapacity);
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

#### ArrayDeque扩容
```java
// ArrayDeque的扩容机制
private void doubleCapacity() {
    // 扩容为原来的2倍，但使用更高效的复制策略
    int oldCapacity = elements.length;
    int newCapacity = oldCapacity << 1;
    // 优化的数组复制
}
```

#### LinkedList扩容
```java
// LinkedList无需扩容，动态分配
private void linkLast(E e) {
    // 每次添加元素都会new一个Node对象
    Node<E> newNode = new Node<>(l, e, null);
}
```

## 实际测试代码
### 内存使用测试
```java
import java.util.*;

public class StackMemoryTest {
    
    public static void main(String[] args) {
        testMemoryUsage();
        testPerformance();
    }
    
    // 内存使用测试
    public static void testMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // 测试Stack
        runtime.gc();
        long beforeStack = runtime.totalMemory() - runtime.freeMemory();
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < 10000; i++) {
            stack.push(i);
        }
        long afterStack = runtime.totalMemory() - runtime.freeMemory();
        
        // 测试LinkedList
        runtime.gc();
        long beforeLinked = runtime.totalMemory() - runtime.freeMemory();
        Deque<Integer> linkedStack = new LinkedList<>();
        for (int i = 0; i < 10000; i++) {
            linkedStack.push(i);
        }
        long afterLinked = runtime.totalMemory() - runtime.freeMemory();
        
        // 测试ArrayDeque
        runtime.gc();
        long beforeArray = runtime.totalMemory() - runtime.freeMemory();
        Deque<Integer> arrayStack = new ArrayDeque<>();
        for (int i = 0; i < 10000; i++) {
            arrayStack.push(i);
        }
        long afterArray = runtime.totalMemory() - runtime.freeMemory();
        
        System.out.println("Stack内存使用: " + (afterStack - beforeStack) + " bytes");
        System.out.println("LinkedList内存使用: " + (afterLinked - beforeLinked) + " bytes");
        System.out.println("ArrayDeque内存使用: " + (afterArray - beforeArray) + " bytes");
    }
    
    // 性能测试
    public static void testPerformance() {
        int iterations = 1000000;
        
        // Stack性能测试
        long start = System.nanoTime();
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < iterations; i++) {
            stack.push(i);
        }
        for (int i = 0; i < iterations; i++) {
            stack.pop();
        }
        long stackTime = System.nanoTime() - start;
        
        // LinkedList性能测试
        start = System.nanoTime();
        Deque<Integer> linkedStack = new LinkedList<>();
        for (int i = 0; i < iterations; i++) {
            linkedStack.push(i);
        }
        for (int i = 0; i < iterations; i++) {
            linkedStack.pop();
        }
        long linkedTime = System.nanoTime() - start;
        
        // ArrayDeque性能测试
        start = System.nanoTime();
        Deque<Integer> arrayStack = new ArrayDeque<>();
        for (int i = 0; i < iterations; i++) {
            arrayStack.push(i);
        }
        for (int i = 0; i < iterations; i++) {
            arrayStack.pop();
        }
        long arrayTime = System.nanoTime() - start;
        
        System.out.println("Stack耗时: " + stackTime / 1000000 + " ms");
        System.out.println("LinkedList耗时: " + linkedTime / 1000000 + " ms");
        System.out.println("ArrayDeque耗时: " + arrayTime / 1000000 + " ms");
    }
}
```

## 内存优劣总结
### Stack的优劣
**优点：**

+ 数组实现，内存连续，缓存友好
+ 随机访问能力（虽然栈不需要）
+ 相对较小的基础内存开销

**缺点：**

+ 继承自Vector，携带历史包袱
+ 所有方法都同步，单线程环境下性能损失
+ 扩容时需要复制整个数组

### LinkedList的优劣
**优点：**

+ 动态大小，无需预分配内存
+ 插入删除操作O(1)时间复杂度
+ 无扩容开销

**缺点：**

+ **内存开销最大**：每个元素需要额外36-40字节
+ 内存分散，缓存命中率低
+ 指针追踪开销，影响性能

### ArrayDeque的优劣
**优点：**

+ **最佳选择**：无同步开销，性能最好
+ 数组实现，内存效率高
+ 双端队列，功能更丰富
+ 扩容策略优化

**缺点：**

+ 基础内存开销略高于Stack
+ 循环数组实现相对复杂

## 推荐使用方案
### 1. 性能优先场景
```java
// 推荐：ArrayDeque
Deque<Integer> stack = new ArrayDeque<>();
```

### 2. 内存敏感场景
```java
// 如果元素数量少且固定，考虑ArrayList
List<Integer> stack = new ArrayList<>(expectedSize);
// 手动实现push/pop操作
```

### 3. 线程安全场景
```java
// 使用ConcurrentLinkedDeque或加锁的ArrayDeque
Deque<Integer> stack = new ConcurrentLinkedDeque<>();
```

## 最佳实践建议
1. **默认选择**：`ArrayDeque` - 性能最佳，内存效率高
2. **避免使用**：`Stack` - 过时的设计，性能较差
3. **特殊情况**：`LinkedList` - 仅在需要频繁中间插入时考虑
4. **内存优化**：预估容量，使用带初始容量的构造函数

```java
// 最佳实践示例
Deque<Integer> stack = new ArrayDeque<>(expectedSize);
```

这样可以避免多次扩容，减少内存分配和复制开销。



> 更新: 2025-09-19 00:54:43  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/87bb93ee88d4408ee845604f53ce6b03>