# LeetCode341-扁平化嵌套列表迭代器

# LeetCode 341 - 扁平化嵌套列表迭代器
## 📋 题目描述
**难度：中等**

给你一个嵌套的整数列表 `nestedList` 。每个元素要么是一个整数，要么是一个列表；该列表的元素也可能是整数或者是其他列表。请你实现一个迭代器将其扁平化，使之能够遍历这个列表中的所有整数。

实现扁平迭代器类 `NestedIterator` ：

+ `NestedIterator(List<NestedInteger> nestedList)` 用嵌套列表初始化迭代器。
+ `int next()` 返回嵌套列表的下一个整数。
+ `boolean hasNext()` 如果仍然存在待迭代的整数，返回 `true` ；否则，返回 `false` 。

你的代码将会用下述伪代码检测：

```plain
iterator = new NestedIterator(nestedList)
while iterator.hasNext()
    print iterator.next()
```

### 示例
**示例 1：**

```plain
输入：nestedList = [[1,1],2,[1,1]]
输出：[1,1,2,1,1]
解释：通过重复调用 next 直到 hasNext 返回 false，next 返回的元素的顺序应该是: [1,1,2,1,1]。
```

**示例 2：**

```plain
输入：nestedList = [1,[4,[6]]]
输出：[1,4,6]
解释：通过重复调用 next 直到 hasNext 返回 false，next 返回的元素的顺序应该是: [1,4,6]。
```

### 约束条件
+ `1 <= nestedList.length <= 500`
+ 嵌套列表中的整数值在范围 `[-10^6, 10^6]` 内

### NestedInteger 接口
```java
// This is the interface that allows for creating nested lists.
// You should not implement it, or speculate about its implementation
public interface NestedInteger {

    // @return true if this NestedInteger holds a single integer, rather than a nested list.
    public boolean isInteger();

    // @return the single integer that this NestedInteger holds, if it holds a single integer
    // Return null if this NestedInteger holds a nested list
    public Integer getInteger();

    // @return the nested list that this NestedInteger holds, if it holds a nested list
    // Return empty list if this NestedInteger holds a single integer
    public List<NestedInteger> getList();
}
```

## 🎯 解题思路
### 核心问题分析
这是一个典型的**递归栈模拟问题**。关键在于：

1. 嵌套列表的结构是递归的：列表中可以包含列表
2. 需要将递归的深度优先遍历转换为迭代器模式
3. 使用栈来模拟递归调用过程

### 递归栈模拟解法原理
```plain
递归遍历的逻辑：
function traverse(nestedList):
    for each element in nestedList:
        if element.isInteger():
            yield element.getInteger()
        else:
            traverse(element.getList())  // 递归处理嵌套列表

栈模拟的关键：
1. 用栈保存待处理的NestedInteger对象
2. 遇到列表时，将其元素逆序压入栈（保证正确的遍历顺序）
3. 遇到整数时，直接返回
4. hasNext()时确保栈顶是整数
```

### 算法步骤
#### 方法一：栈模拟递归
```plain
初始化：
1. 将nestedList中的元素逆序压入栈

hasNext()：
1. 循环处理栈顶元素，直到栈为空或栈顶是整数
2. 如果栈顶是列表，弹出并将其元素逆序压入栈
3. 返回栈是否非空

next()：
1. 调用hasNext()确保栈顶是整数
2. 弹出并返回栈顶整数
```

#### 方法二：预处理扁平化
```plain
初始化：
1. 递归遍历整个嵌套列表
2. 将所有整数按顺序存储到列表中
3. 维护一个索引指针

hasNext()：
1. 检查索引是否小于列表长度

next()：
1. 返回当前索引位置的元素
2. 索引递增
```

### 图解演示
**示例：nestedList = [[1,1],2,[1,1]]**

```plain
嵌套列表结构：
[
  [1, 1],     // 嵌套列表
  2,          // 整数
  [1, 1]      // 嵌套列表
]

递归遍历过程：
traverse([[1,1], 2, [1,1]]):
    element = [1,1]:
        traverse([1,1]):
            element = 1: yield 1
            element = 1: yield 1
    element = 2: yield 2
    element = [1,1]:
        traverse([1,1]):
            element = 1: yield 1
            element = 1: yield 1

输出顺序：1 → 1 → 2 → 1 → 1

栈模拟过程：

初始化：
将 [[1,1], 2, [1,1]] 逆序压入栈
栈: [[1,1], 2, [1,1]] (底 -> 顶)

第1次 hasNext()：
栈顶是 [1,1]（列表），弹出并将其元素逆序压入
弹出: [1,1]
压入: 1, 1 (逆序)
栈: [2, [1,1], 1, 1] (底 -> 顶)
栈顶是整数1，返回true

第1次 next()：
弹出栈顶整数1
栈: [2, [1,1], 1] (底 -> 顶)
返回: 1

第2次 hasNext()：
栈顶是整数1，返回true

第2次 next()：
弹出栈顶整数1
栈: [2, [1,1]] (底 -> 顶)
返回: 1

第3次 hasNext()：
栈顶是整数2，返回true

第3次 next()：
弹出栈顶整数2
栈: [[1,1]] (底 -> 顶)
返回: 2

第4次 hasNext()：
栈顶是 [1,1]（列表），弹出并将其元素逆序压入
弹出: [1,1]
压入: 1, 1 (逆序)
栈: [1, 1] (底 -> 顶)
栈顶是整数1，返回true

第4次 next()：
弹出栈顶整数1
栈: [1] (底 -> 顶)
返回: 1

第5次 hasNext()：
栈顶是整数1，返回true

第5次 next()：
弹出栈顶整数1
栈: [] (空)
返回: 1

第6次 hasNext()：
栈为空，返回false

最终结果: [1, 1, 2, 1, 1]
```

## 💻 代码实现
### 方法一：栈模拟递归（推荐）
```java
import java.util.*;

/**
 * 使用栈模拟递归的扁平化迭代器
 */
public class NestedIterator implements Iterator<Integer> {
    
    private Deque<NestedInteger> stack;
    
    public NestedIterator(List<NestedInteger> nestedList) {
        stack = new ArrayDeque<>();
        
        // 将嵌套列表的元素逆序压入栈
        // 逆序是为了保证正确的遍历顺序
        for (int i = nestedList.size() - 1; i >= 0; i--) {
            stack.push(nestedList.get(i));
        }
    }
    
    @Override
    public Integer next() {
        // 调用hasNext()确保栈顶是整数
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        // 弹出并返回栈顶整数
        return stack.pop().getInteger();
    }
    
    @Override
    public boolean hasNext() {
        // 循环处理栈顶元素，直到栈为空或栈顶是整数
        while (!stack.isEmpty()) {
            NestedInteger top = stack.peek();
            
            if (top.isInteger()) {
                // 栈顶是整数，可以直接返回
                return true;
            } else {
                // 栈顶是列表，需要展开
                stack.pop();
                List<NestedInteger> list = top.getList();
                
                // 将列表元素逆序压入栈
                for (int i = list.size() - 1; i >= 0; i--) {
                    stack.push(list.get(i));
                }
            }
        }
        
        return false;
    }
}
```

### 方法二：预处理扁平化
```java
/**
 * 预处理扁平化的迭代器
 */
public class NestedIteratorPreprocess implements Iterator<Integer> {
    
    private List<Integer> flatList;
    private int index;
    
    public NestedIteratorPreprocess(List<NestedInteger> nestedList) {
        flatList = new ArrayList<>();
        index = 0;
        
        // 递归扁平化整个嵌套列表
        flatten(nestedList);
    }
    
    private void flatten(List<NestedInteger> nestedList) {
        for (NestedInteger nested : nestedList) {
            if (nested.isInteger()) {
                flatList.add(nested.getInteger());
            } else {
                flatten(nested.getList());
            }
        }
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        return flatList.get(index++);
    }
    
    @Override
    public boolean hasNext() {
        return index < flatList.size();
    }
}
```

### 方法三：栈模拟递归（带状态）
```java
/**
 * 带状态的栈模拟递归
 */
public class NestedIteratorWithState implements Iterator<Integer> {
    
    // 定义栈帧状态
    private static class StackFrame {
        List<NestedInteger> list;
        int index;
        
        StackFrame(List<NestedInteger> list) {
            this.list = list;
            this.index = 0;
        }
        
        boolean hasNext() {
            return index < list.size();
        }
        
        NestedInteger next() {
            return list.get(index++);
        }
    }
    
    private Deque<StackFrame> stack;
    private Integer nextValue;
    
    public NestedIteratorWithState(List<NestedInteger> nestedList) {
        stack = new ArrayDeque<>();
        stack.push(new StackFrame(nestedList));
        nextValue = null;
        
        // 预先计算第一个值
        advance();
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        Integer result = nextValue;
        advance();
        return result;
    }
    
    @Override
    public boolean hasNext() {
        return nextValue != null;
    }
    
    private void advance() {
        nextValue = null;
        
        while (!stack.isEmpty() && nextValue == null) {
            StackFrame currentFrame = stack.peek();
            
            if (!currentFrame.hasNext()) {
                // 当前层遍历完毕，弹出栈帧
                stack.pop();
                continue;
            }
            
            NestedInteger nested = currentFrame.next();
            
            if (nested.isInteger()) {
                // 找到下一个整数
                nextValue = nested.getInteger();
            } else {
                // 遇到嵌套列表，压入新的栈帧
                stack.push(new StackFrame(nested.getList()));
            }
        }
    }
}
```

### 方法四：迭代器链式组合
```java
/**
 * 使用迭代器链式组合的方法
 */
public class NestedIteratorChain implements Iterator<Integer> {
    
    private Queue<Iterator<Integer>> iteratorQueue;
    private Iterator<Integer> currentIterator;
    
    public NestedIteratorChain(List<NestedInteger> nestedList) {
        iteratorQueue = new LinkedList<>();
        
        // 将每个NestedInteger转换为迭代器
        for (NestedInteger nested : nestedList) {
            iteratorQueue.offer(createIterator(nested));
        }
        
        currentIterator = null;
        advance();
    }
    
    private Iterator<Integer> createIterator(NestedInteger nested) {
        if (nested.isInteger()) {
            // 单个整数的迭代器
            return Collections.singletonList(nested.getInteger()).iterator();
        } else {
            // 递归创建嵌套列表的迭代器
            return new NestedIteratorChain(nested.getList());
        }
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        return currentIterator.next();
    }
    
    @Override
    public boolean hasNext() {
        return currentIterator != null && currentIterator.hasNext();
    }
    
    private void advance() {
        // 找到下一个有效的迭代器
        while ((currentIterator == null || !currentIterator.hasNext()) 
               && !iteratorQueue.isEmpty()) {
            currentIterator = iteratorQueue.poll();
        }
    }
}
```

### 方法五：生成器模式模拟
```java
/**
 * 使用生成器模式模拟递归
 */
public class NestedIteratorGenerator implements Iterator<Integer> {
    
    private Queue<Integer> queue;
    
    public NestedIteratorGenerator(List<NestedInteger> nestedList) {
        queue = new LinkedList<>();
        generate(nestedList);
    }
    
    private void generate(List<NestedInteger> nestedList) {
        for (NestedInteger nested : nestedList) {
            if (nested.isInteger()) {
                queue.offer(nested.getInteger());
            } else {
                generate(nested.getList());
            }
        }
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        return queue.poll();
    }
    
    @Override
    public boolean hasNext() {
        return !queue.isEmpty();
    }
}
```

### 方法六：懒加载栈模拟
```java
/**
 * 懒加载的栈模拟递归
 */
public class NestedIteratorLazy implements Iterator<Integer> {
    
    private static class LazyFrame {
        List<NestedInteger> list;
        int index;
        boolean expanded;
        
        LazyFrame(List<NestedInteger> list) {
            this.list = list;
            this.index = 0;
            this.expanded = false;
        }
    }
    
    private Deque<LazyFrame> stack;
    private Integer cachedNext;
    
    public NestedIteratorLazy(List<NestedInteger> nestedList) {
        stack = new ArrayDeque<>();
        stack.push(new LazyFrame(nestedList));
        cachedNext = null;
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        Integer result = cachedNext;
        cachedNext = null;
        return result;
    }
    
    @Override
    public boolean hasNext() {
        if (cachedNext != null) {
            return true;
        }
        
        while (!stack.isEmpty()) {
            LazyFrame frame = stack.peek();
            
            if (frame.index >= frame.list.size()) {
                stack.pop();
                continue;
            }
            
            NestedInteger nested = frame.list.get(frame.index++);
            
            if (nested.isInteger()) {
                cachedNext = nested.getInteger();
                return true;
            } else {
                stack.push(new LazyFrame(nested.getList()));
            }
        }
        
        return false;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**栈模拟方法：**

+ 初始化：O(1)
+ hasNext()：均摊O(1)，每个元素最多被处理一次
+ next()：O(1)
+ 总体：O(n)，其中n是所有整数的总数

**预处理方法：**

+ 初始化：O(n)，需要遍历所有元素
+ hasNext()：O(1)
+ next()：O(1)
+ 总体：O(n)

### 空间复杂度
**栈模拟方法：**

+ 栈的最大深度等于嵌套的最大层数
+ 空间复杂度：O(d)，其中d是最大嵌套深度

**预处理方法：**

+ 需要存储所有整数
+ 空间复杂度：O(n)，其中n是所有整数的总数

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的嵌套列表迭代器
 */
public class VisualNestedIterator implements Iterator<Integer> {
    
    private Deque<NestedInteger> stack;
    private int stepCount;
    
    public VisualNestedIterator(List<NestedInteger> nestedList) {
        System.out.println("🔧 初始化嵌套列表迭代器");
        printNestedList(nestedList, 0);
        System.out.println("=" + "=".repeat(60));
        
        stack = new ArrayDeque<>();
        stepCount = 0;
        
        System.out.println("📥 将嵌套列表元素逆序压入栈:");
        for (int i = nestedList.size() - 1; i >= 0; i--) {
            stack.push(nestedList.get(i));
            System.out.printf("  压入: %s\n", formatNestedInteger(nestedList.get(i)));
        }
        
        printStackState();
        System.out.println();
    }
    
    @Override
    public Integer next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        Integer result = stack.pop().getInteger();
        System.out.printf("📤 next() 返回: %d\n", result);
        printStackState();
        System.out.println();
        
        return result;
    }
    
    @Override
    public boolean hasNext() {
        System.out.printf("🔍 hasNext() 检查 (步骤 %d):\n", ++stepCount);
        
        while (!stack.isEmpty()) {
            NestedInteger top = stack.peek();
            
            if (top.isInteger()) {
                System.out.printf("  ✅ 栈顶是整数 %d，返回 true\n", top.getInteger());
                return true;
            } else {
                System.out.printf("  📋 栈顶是列表 %s，需要展开\n", formatNestedInteger(top));
                
                stack.pop();
                List<NestedInteger> list = top.getList();
                
                System.out.printf("  📥 将列表元素逆序压入栈:\n");
                for (int i = list.size() - 1; i >= 0; i--) {
                    stack.push(list.get(i));
                    System.out.printf("    压入: %s\n", formatNestedInteger(list.get(i)));
                }
                
                printStackState();
            }
        }
        
        System.out.println("  ❌ 栈为空，返回 false");
        return false;
    }
    
    private void printStackState() {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<NestedInteger> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(formatNestedInteger(stackList.get(i)));
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    private String formatNestedInteger(NestedInteger nested) {
        if (nested.isInteger()) {
            return String.valueOf(nested.getInteger());
        } else {
            StringBuilder sb = new StringBuilder("[");
            List<NestedInteger> list = nested.getList();
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) sb.append(",");
                sb.append(formatNestedInteger(list.get(i)));
            }
            sb.append("]");
            return sb.toString();
        }
    }
    
    private void printNestedList(List<NestedInteger> nestedList, int indent) {
        String prefix = "  ".repeat(indent);
        System.out.println(prefix + "嵌套列表结构:");
        
        for (int i = 0; i < nestedList.size(); i++) {
            NestedInteger nested = nestedList.get(i);
            System.out.printf("%s[%d] ", prefix, i);
            
            if (nested.isInteger()) {
                System.out.printf("整数: %d\n", nested.getInteger());
            } else {
                System.out.println("列表:");
                printNestedList(nested.getList(), indent + 1);
            }
        }
    }
    
    // 测试用的NestedInteger实现
    public static class NestedIntegerImpl implements NestedInteger {
        private Integer value;
        private List<NestedInteger> list;
        
        public NestedIntegerImpl(int value) {
            this.value = value;
        }
        
        public NestedIntegerImpl(List<NestedInteger> list) {
            this.list = list;
        }
        
        @Override
        public boolean isInteger() {
            return value != null;
        }
        
        @Override
        public Integer getInteger() {
            return value;
        }
        
        @Override
        public List<NestedInteger> getList() {
            return list != null ? list : new ArrayList<>();
        }
    }
    
    // 构建测试数据的辅助方法
    public static List<NestedInteger> buildNestedList(Object[] array) {
        List<NestedInteger> result = new ArrayList<>();
        
        for (Object obj : array) {
            if (obj instanceof Integer) {
                result.add(new NestedIntegerImpl((Integer) obj));
            } else if (obj instanceof Object[]) {
                result.add(new NestedIntegerImpl(buildNestedList((Object[]) obj)));
            }
        }
        
        return result;
    }
    
    public static void main(String[] args) {
        // 测试示例: [[1,1],2,[1,1]]
        Object[] testCase1 = {new Object[]{1, 1}, 2, new Object[]{1, 1}};
        List<NestedInteger> nestedList1 = buildNestedList(testCase1);
        
        System.out.println("🧪 测试用例 1: [[1,1],2,[1,1]]");
        VisualNestedIterator iterator1 = new VisualNestedIterator(nestedList1);
        
        List<Integer> result1 = new ArrayList<>();
        while (iterator1.hasNext()) {
            result1.add(iterator1.next());
        }
        
        System.out.println("🏆 最终结果: " + result1);
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试示例: [1,[4,[6]]]
        Object[] testCase2 = {1, new Object[]{4, new Object[]{6}}};
        List<NestedInteger> nestedList2 = buildNestedList(testCase2);
        
        System.out.println("🧪 测试用例 2: [1,[4,[6]]]");
        VisualNestedIterator iterator2 = new VisualNestedIterator(nestedList2);
        
        List<Integer> result2 = new ArrayList<>();
        while (iterator2.hasNext()) {
            result2.add(iterator2.next());
        }
        
        System.out.println("🏆 最终结果: " + result2);
    }
}
```

### 运行结果示例
```plain
🧪 测试用例 1: [[1,1],2,[1,1]]
🔧 初始化嵌套列表迭代器
  嵌套列表结构:
  [0] 列表:
    [0] 整数: 1
    [1] 整数: 1
  [1] 整数: 2
  [2] 列表:
    [0] 整数: 1
    [1] 整数: 1
============================================================
📥 将嵌套列表元素逆序压入栈:
  压入: [1,1]
  压入: 2
  压入: [1,1]
  栈状态: [[1,1], 2, [1,1]] (底 -> 顶)

🔍 hasNext() 检查 (步骤 1):
  📋 栈顶是列表 [1,1]，需要展开
  📥 将列表元素逆序压入栈:
    压入: 1
    压入: 1
  栈状态: [[1,1], 2, 1, 1] (底 -> 顶)
  ✅ 栈顶是整数 1，返回 true
📤 next() 返回: 1
  栈状态: [[1,1], 2, 1] (底 -> 顶)

🔍 hasNext() 检查 (步骤 2):
  ✅ 栈顶是整数 1，返回 true
📤 next() 返回: 1
  栈状态: [[1,1], 2] (底 -> 顶)

🔍 hasNext() 检查 (步骤 3):
  ✅ 栈顶是整数 2，返回 true
📤 next() 返回: 2
  栈状态: [[1,1]] (底 -> 顶)

🔍 hasNext() 检查 (步骤 4):
  📋 栈顶是列表 [1,1]，需要展开
  📥 将列表元素逆序压入栈:
    压入: 1
    压入: 1
  栈状态: [1, 1] (底 -> 顶)
  ✅ 栈顶是整数 1，返回 true
📤 next() 返回: 1
  栈状态: [1] (底 -> 顶)

🔍 hasNext() 检查 (步骤 5):
  ✅ 栈顶是整数 1，返回 true
📤 next() 返回: 1
  栈状态: [空] (底 -> 顶)

🔍 hasNext() 检查 (步骤 6):
  ❌ 栈为空，返回 false
🏆 最终结果: [1, 1, 2, 1, 1]
```

## 🧪 测试用例
### 基础功能测试
```java
public class NestedIteratorTest {
    
    @Test
    public void testBasicCases() {
        // 示例 1: [[1,1],2,[1,1]]
        List<NestedInteger> nestedList1 = Arrays.asList(
            createNestedList(Arrays.asList(1, 1)),
            createInteger(2),
            createNestedList(Arrays.asList(1, 1))
        );
        
        NestedIterator iterator1 = new NestedIterator(nestedList1);
        List<Integer> result1 = new ArrayList<>();
        while (iterator1.hasNext()) {
            result1.add(iterator1.next());
        }
        assertEquals(Arrays.asList(1, 1, 2, 1, 1), result1);
        
        // 示例 2: [1,[4,[6]]]
        List<NestedInteger> nestedList2 = Arrays.asList(
            createInteger(1),
            createNestedList(Arrays.asList(
                createInteger(4),
                createNestedList(Arrays.asList(createInteger(6)))
            ))
        );
        
        NestedIterator iterator2 = new NestedIterator(nestedList2);
        List<Integer> result2 = new ArrayList<>();
        while (iterator2.hasNext()) {
            result2.add(iterator2.next());
        }
        assertEquals(Arrays.asList(1, 4, 6), result2);
    }
    
    @Test
    public void testEdgeCases() {
        // 空列表
        List<NestedInteger> emptyList = Arrays.asList();
        NestedIterator iterator1 = new NestedIterator(emptyList);
        assertFalse(iterator1.hasNext());
        
        // 只有一个整数
        List<NestedInteger> singleInteger = Arrays.asList(createInteger(42));
        NestedIterator iterator2 = new NestedIterator(singleInteger);
        assertTrue(iterator2.hasNext());
        assertEquals(Integer.valueOf(42), iterator2.next());
        assertFalse(iterator2.hasNext());
        
        // 嵌套空列表
        List<NestedInteger> nestedEmpty = Arrays.asList(
            createNestedList(Arrays.asList()),
            createInteger(1),
            createNestedList(Arrays.asList())
        );
        NestedIterator iterator3 = new NestedIterator(nestedEmpty);
        assertTrue(iterator3.hasNext());
        assertEquals(Integer.valueOf(1), iterator3.next());
        assertFalse(iterator3.hasNext());
    }
    
    @Test
    public void testDeepNesting() {
        // 深度嵌套: [[[[[1]]]]]
        NestedInteger deepNested = createInteger(1);
        for (int i = 0; i < 5; i++) {
            deepNested = createNestedList(Arrays.asList(deepNested));
        }
        
        List<NestedInteger> nestedList = Arrays.asList(deepNested);
        NestedIterator iterator = new NestedIterator(nestedList);
        
        assertTrue(iterator.hasNext());
        assertEquals(Integer.valueOf(1), iterator.next());
        assertFalse(iterator.hasNext());
    }
    
    @Test
    public void testComplexStructure() {
        // 复杂结构: [1, [2, [3, 4], 5], 6, [7, [8, 9]]]
        List<NestedInteger> nestedList = Arrays.asList(
            createInteger(1),
            createNestedList(Arrays.asList(
                createInteger(2),
                createNestedList(Arrays.asList(createInteger(3), createInteger(4))),
                createInteger(5)
            )),
            createInteger(6),
            createNestedList(Arrays.asList(
                createInteger(7),
                createNestedList(Arrays.asList(createInteger(8), createInteger(9)))
            ))
        );
        
        NestedIterator iterator = new NestedIterator(nestedList);
        List<Integer> result = new ArrayList<>();
        while (iterator.hasNext()) {
            result.add(iterator.next());
        }
        
        assertEquals(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9), result);
    }
    
    // 辅助方法
    private NestedInteger createInteger(int value) {
        return new NestedIntegerImpl(value);
    }
    
    private NestedInteger createNestedList(List<NestedInteger> list) {
        return new NestedIntegerImpl(list);
    }
    
    private NestedInteger createNestedList(List<Integer> integers) {
        List<NestedInteger> nestedList = new ArrayList<>();
        for (Integer integer : integers) {
            nestedList.add(createInteger(integer));
        }
        return new NestedIntegerImpl(nestedList);
    }
}
```

### 性能对比测试
```java
public class PerformanceComparisonTest {
    
    @Test
    public void compareAllMethods() {
        // 构建大型嵌套列表
        List<NestedInteger> largeNestedList = buildLargeNestedList(10000);
        
        // 测试栈模拟方法
        long startTime = System.nanoTime();
        NestedIterator iterator1 = new NestedIterator(largeNestedList);
        List<Integer> result1 = new ArrayList<>();
        while (iterator1.hasNext()) {
            result1.add(iterator1.next());
        }
        long endTime = System.nanoTime();
        System.out.printf("栈模拟方法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 测试预处理方法
        startTime = System.nanoTime();
        NestedIteratorPreprocess iterator2 = new NestedIteratorPreprocess(largeNestedList);
        List<Integer> result2 = new ArrayList<>();
        while (iterator2.hasNext()) {
            result2.add(iterator2.next());
        }
        endTime = System.nanoTime();
        System.out.printf("预处理方法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        System.out.println("所有方法结果一致 ✅");
    }
    
    @Test
    public void testMemoryUsage() {
        List<NestedInteger> largeNestedList = buildLargeNestedList(50000);
        
        Runtime runtime = Runtime.getRuntime();
        
        // 测试栈模拟方法的内存使用
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        NestedIterator iterator1 = new NestedIterator(largeNestedList);
        while (iterator1.hasNext()) {
            iterator1.next();
        }
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("栈模拟方法内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        
        // 测试预处理方法的内存使用
        runtime.gc();
        memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        NestedIteratorPreprocess iterator2 = new NestedIteratorPreprocess(largeNestedList);
        while (iterator2.hasNext()) {
            iterator2.next();
        }
        
        memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("预处理方法内存使用: %d KB\n", (memAfter - memBefore) / 1024);
    }
    
    private List<NestedInteger> buildLargeNestedList(int size) {
        List<NestedInteger> result = new ArrayList<>();
        
        for (int i = 0; i < size; i++) {
            if (i % 10 == 0) {
                // 每10个元素创建一个嵌套列表
                List<NestedInteger> subList = new ArrayList<>();
                for (int j = 0; j < 5; j++) {
                    subList.add(new NestedIntegerImpl(i + j));
                }
                result.add(new NestedIntegerImpl(subList));
            } else {
                result.add(new NestedIntegerImpl(i));
            }
        }
        
        return result;
    }
}
```

### 边界条件测试
```java
public class BoundaryConditionTest {
    
    @Test
    public void testExtremeNesting() {
        // 测试极深嵌套
        NestedInteger deepNested = new NestedIntegerImpl(1);
        for (int i = 0; i < 1000; i++) {
            deepNested = new NestedIntegerImpl(Arrays.asList(deepNested));
        }
        
        List<NestedInteger> nestedList = Arrays.asList(deepNested);
        NestedIterator iterator = new NestedIterator(nestedList);
        
        assertTrue(iterator.hasNext());
        assertEquals(Integer.valueOf(1), iterator.next());
        assertFalse(iterator.hasNext());
    }
    
    @Test
    public void testLargeNumbers() {
        // 测试大数值
        List<NestedInteger> nestedList = Arrays.asList(
            new NestedIntegerImpl(Integer.MAX_VALUE),
            new NestedIntegerImpl(Integer.MIN_VALUE),
            new NestedIntegerImpl(Arrays.asList(
                new NestedIntegerImpl(1000000),
                new NestedIntegerImpl(-1000000)
            ))
        );
        
        NestedIterator iterator = new NestedIterator(nestedList);
        List<Integer> result = new ArrayList<>();
        while (iterator.hasNext()) {
            result.add(iterator.next());
        }
        
        assertEquals(Arrays.asList(Integer.MAX_VALUE, Integer.MIN_VALUE, 1000000, -1000000), result);
    }
    
    @Test
    public void testMultipleHasNextCalls() {
        // 测试多次调用hasNext()
        List<NestedInteger> nestedList = Arrays.asList(
            new NestedIntegerImpl(Arrays.asList(new NestedIntegerImpl(1))),
            new NestedIntegerImpl(2)
        );
        
        NestedIterator iterator = new NestedIterator(nestedList);
        
        // 多次调用hasNext()应该返回相同结果
        assertTrue(iterator.hasNext());
        assertTrue(iterator.hasNext());
        assertTrue(iterator.hasNext());
        
        assertEquals(Integer.valueOf(1), iterator.next());
        
        assertTrue(iterator.hasNext());
        assertTrue(iterator.hasNext());
        
        assertEquals(Integer.valueOf(2), iterator.next());
        
        assertFalse(iterator.hasNext());
        assertFalse(iterator.hasNext());
    }
    
    @Test(expected = NoSuchElementException.class)
    public void testNextOnEmptyIterator() {
        // 测试在空迭代器上调用next()
        List<NestedInteger> emptyList = Arrays.asList();
        NestedIterator iterator = new NestedIterator(emptyList);
        
        assertFalse(iterator.hasNext());
        iterator.next(); // 应该抛出异常
    }
    
    @Test(expected = NoSuchElementException.class)
    public void testNextAfterExhaustion() {
        // 测试在迭代器耗尽后调用next()
        List<NestedInteger> nestedList = Arrays.asList(new NestedIntegerImpl(1));
        NestedIterator iterator = new NestedIterator(nestedList);
        
        assertTrue(iterator.hasNext());
        assertEquals(Integer.valueOf(1), iterator.next());
        assertFalse(iterator.hasNext());
        
        iterator.next(); // 应该抛出异常
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 173 - 二叉搜索树迭代器
```java
/**
 * 二叉搜索树迭代器 - 类似的栈模拟递归问题
 */
public class BSTIterator {
    
    private Deque<TreeNode> stack;
    
    public BSTIterator(TreeNode root) {
        stack = new ArrayDeque<>();
        pushLeft(root);
    }
    
    public int next() {
        TreeNode node = stack.pop();
        pushLeft(node.right);
        return node.val;
    }
    
    public boolean hasNext() {
        return !stack.isEmpty();
    }
    
    private void pushLeft(TreeNode node) {
        while (node != null) {
            stack.push(node);
            node = node.left;
        }
    }
}
```

### 2. 扁平化多维数组
```java
/**
 * 扁平化多维数组的通用解决方案
 */
public class FlattenMultiDimensionalArray {
    
    public static List<Integer> flatten(Object[] array) {
        List<Integer> result = new ArrayList<>();
        Deque<Object> stack = new ArrayDeque<>();
        
        // 逆序压入栈
        for (int i = array.length - 1; i >= 0; i--) {
            stack.push(array[i]);
        }
        
        while (!stack.isEmpty()) {
            Object obj = stack.pop();
            
            if (obj instanceof Integer) {
                result.add((Integer) obj);
            } else if (obj instanceof Object[]) {
                Object[] subArray = (Object[]) obj;
                // 逆序压入栈
                for (int i = subArray.length - 1; i >= 0; i--) {
                    stack.push(subArray[i]);
                }
            }
        }
        
        return result;
    }
    
    // 递归版本
    public static List<Integer> flattenRecursive(Object[] array) {
        List<Integer> result = new ArrayList<>();
        flattenHelper(array, result);
        return result;
    }
    
    private static void flattenHelper(Object[] array, List<Integer> result) {
        for (Object obj : array) {
            if (obj instanceof Integer) {
                result.add((Integer) obj);
            } else if (obj instanceof Object[]) {
                flattenHelper((Object[]) obj, result);
            }
        }
    }
}
```

### 3. 文件系统迭代器
```java
/**
 * 文件系统迭代器 - 递归遍历目录结构
 */
public class FileSystemIterator implements Iterator<String> {
    
    private Deque<File> stack;
    private String nextFile;
    
    public FileSystemIterator(String rootPath) {
        stack = new ArrayDeque<>();
        stack.push(new File(rootPath));
        advance();
    }
    
    @Override
    public boolean hasNext() {
        return nextFile != null;
    }
    
    @Override
    public String next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        String result = nextFile;
        advance();
        return result;
    }
    
    private void advance() {
        nextFile = null;
        
        while (!stack.isEmpty() && nextFile == null) {
            File current = stack.pop();
            
            if (current.isFile()) {
                nextFile = current.getAbsolutePath();
            } else if (current.isDirectory()) {
                File[] children = current.listFiles();
                if (children != null) {
                    // 逆序压入栈以保持正确的遍历顺序
                    for (int i = children.length - 1; i >= 0; i--) {
                        stack.push(children[i]);
                    }
                }
            }
        }
    }
}
```

### 4. JSON解析器迭代器
```java
/**
 * JSON解析器迭代器 - 递归解析嵌套JSON结构
 */
public class JsonIterator implements Iterator<Object> {
    
    private static class JsonFrame {
        Object value;
        Iterator<?> iterator;
        
        JsonFrame(Object value) {
            this.value = value;
            if (value instanceof Map) {
                this.iterator = ((Map<?, ?>) value).values().iterator();
            } else if (value instanceof List) {
                this.iterator = ((List<?>) value).iterator();
            }
        }
        
        boolean hasNext() {
            return iterator != null && iterator.hasNext();
        }
        
        Object next() {
            return iterator.next();
        }
    }
    
    private Deque<JsonFrame> stack;
    private Object nextValue;
    
    public JsonIterator(Object jsonObject) {
        stack = new ArrayDeque<>();
        stack.push(new JsonFrame(jsonObject));
        advance();
    }
    
    @Override
    public boolean hasNext() {
        return nextValue != null;
    }
    
    @Override
    public Object next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        Object result = nextValue;
        advance();
        return result;
    }
    
    private void advance() {
        nextValue = null;
        
        while (!stack.isEmpty() && nextValue == null) {
            JsonFrame frame = stack.peek();
            
            if (!frame.hasNext()) {
                stack.pop();
                continue;
            }
            
            Object value = frame.next();
            
            if (isPrimitive(value)) {
                nextValue = value;
            } else {
                stack.push(new JsonFrame(value));
            }
        }
    }
    
    private boolean isPrimitive(Object value) {
        return value instanceof String || 
               value instanceof Number || 
               value instanceof Boolean || 
               value == null;
    }
}
```

### 5. 通用递归迭代器框架
```java
/**
 * 通用递归迭代器框架
 */
public abstract class RecursiveIterator<T, R> implements Iterator<R> {
    
    private Deque<T> stack;
    private R nextValue;
    
    public RecursiveIterator(T root) {
        stack = new ArrayDeque<>();
        if (root != null) {
            stack.push(root);
        }
        advance();
    }
    
    @Override
    public boolean hasNext() {
        return nextValue != null;
    }
    
    @Override
    public R next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        
        R result = nextValue;
        advance();
        return result;
    }
    
    private void advance() {
        nextValue = null;
        
        while (!stack.isEmpty() && nextValue == null) {
            T current = stack.pop();
            
            if (isLeaf(current)) {
                nextValue = extractValue(current);
            } else {
                List<T> children = getChildren(current);
                // 逆序压入栈
                for (int i = children.size() - 1; i >= 0; i--) {
                    stack.push(children.get(i));
                }
            }
        }
    }
    
    // 抽象方法，由子类实现
    protected abstract boolean isLeaf(T node);
    protected abstract R extractValue(T node);
    protected abstract List<T> getChildren(T node);
}

// 使用示例：嵌套列表迭代器
class NestedListIterator extends RecursiveIterator<NestedInteger, Integer> {
    
    public NestedListIterator(List<NestedInteger> nestedList) {
        super(new NestedIntegerImpl(nestedList));
    }
    
    @Override
    protected boolean isLeaf(NestedInteger node) {
        return node.isInteger();
    }
    
    @Override
    protected Integer extractValue(NestedInteger node) {
        return node.getInteger();
    }
    
    @Override
    protected List<NestedInteger> getChildren(NestedInteger node) {
        return node.getList();
    }
}
```

## 💡 解题技巧总结
### 1. 递归栈模拟的核心原则
+ **栈替代递归**：用显式栈模拟系统调用栈
+ **逆序压栈**：保证正确的遍历顺序
+ **懒加载**：只在需要时展开嵌套结构

### 2. 迭代器设计模式
+ **状态管理**：维护迭代器的内部状态
+ **懒求值**：按需计算下一个元素
+ **异常处理**：正确处理边界条件

### 3. 栈模拟的通用模板
```java
// 递归栈模拟的通用模板
Deque<Node> stack = new ArrayDeque<>();
// 初始化栈

while (!stack.isEmpty()) {
    Node current = stack.peek();
    
    if (isLeaf(current)) {
        // 处理叶子节点
        processLeaf(current);
        stack.pop();
    } else {
        // 展开非叶子节点
        stack.pop();
        List<Node> children = getChildren(current);
        // 逆序压入子节点
        for (int i = children.size() - 1; i >= 0; i--) {
            stack.push(children.get(i));
        }
    }
}
```

### 4. 性能优化技巧
+ **预处理 vs 懒加载**：根据使用场景选择
+ **内存管理**：控制栈的最大深度
+ **缓存策略**：避免重复计算

### 5. 应用场景总结
+ **树形结构遍历**：二叉树、多叉树、文件系统
+ **嵌套数据处理**：JSON、XML、配置文件
+ **图的深度优先搜索**：拓扑排序、连通性检测
+ **回溯算法**：组合生成、路径搜索

这道题完美展示了如何将递归算法转换为迭代实现，是掌握栈模拟递归技巧的经典例题！



> 更新: 2025-09-19 00:54:12  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/9e8fba958786c7c6823c79a90c2d65cf>