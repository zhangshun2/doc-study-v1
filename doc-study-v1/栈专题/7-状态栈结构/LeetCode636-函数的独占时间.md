# LeetCode636-函数的独占时间

# LeetCode 636 - 函数的独占时间
## 📋 题目描述
**难度：中等**

有一个 **单线程** CPU 正在运行一个含有 `n` 道函数的程序。每道函数都有一个位于 `0` 和 `n-1` 之间的唯一标识符。

函数调用 **存储在一个调用栈上** ：当一个函数调用开始时，它的标识符将会推入栈中。而当一个函数调用结束时，它的标识符将会从栈中弹出。标识符在栈顶的函数是 **当前正在执行的函数** 。每当一个函数开始或者结束时，将会记录一条日志，格式为 `function_id:start_or_end:timestamp`。

给你一个由日志组成的列表 `logs`，其中 `logs[i]` 表示第 `i` 条日志，请你返回每个函数的 **独占时间** 。

函数的 **独占时间** 定义是在这个函数在程序所有函数调用中执行时间的总和，调用其他函数花费的时间不算该函数的独占时间。

### 示例
**示例 1：**

![](https://assets.leetcode.com/uploads/2019/04/05/diag1.png)

```plain
输入：n = 2, logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]
输出：[3,4]
解释：
函数 0 在时间戳 0 的时候开始，在执行了 2 个时间单位结束于时间戳 1。
函数 1 在时间戳 2 的时候开始，在执行了 4 个时间单位结束于时间戳 5。
函数 0 在时间戳 6 的时候结束，在执行了 1 个时间单位。
所以函数 0 总共执行了 2 + 1 = 3 个时间单位，函数 1 总共执行了 4 个时间单位。
```

**示例 2：**

```plain
输入：n = 1, logs = ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]
输出：[8]
解释：
函数 0 在时间戳 0 的时候开始，执行了 2 个时间单位，在时间戳 1 结束。
函数 0 在时间戳 2 的时候开始，执行了 4 个时间单位，在时间戳 5 结束。
函数 0 在时间戳 6 的时候开始，执行了 1 个时间单位，在时间戳 6 结束。
所以函数 0 总共执行了 2 + 4 + 1 = 7 个时间单位。
```

### 约束条件
+ `1 <= n <= 100`
+ `1 <= logs.length <= 500`
+ `0 <= function_id < n`
+ `0 <= timestamp <= 10^9`
+ 两个开始事件不会在同一时间戳发生
+ 两个结束事件不会在同一时间戳发生
+ 每道函数都有一个对应的结束日志

## 🎯 解题思路
### 核心问题分析
这是一个典型的**状态栈结构**问题，需要处理：

1. **函数调用栈**：模拟真实的函数调用过程
2. **时间计算**：准确计算每个函数的独占时间
3. **状态管理**：跟踪当前执行的函数和时间点
4. **嵌套调用**：处理函数之间的相互调用

### 状态栈解法原理
**状态栈的核心思想：**

```plain
状态定义：
- 函数ID：当前执行的函数标识
- 开始时间：函数开始执行的时间戳

栈的作用：
1. 模拟函数调用栈的行为
2. 跟踪函数的嵌套调用关系
3. 计算每个函数的实际执行时间

时间计算规则：
- 函数开始时：暂停当前栈顶函数的计时
- 函数结束时：计算该函数的执行时间，恢复上一个函数的计时
- 独占时间 = 总执行时间 - 被其他函数占用的时间
```

### 算法步骤
```plain
状态栈算法步骤：
1. 初始化：
   - 函数调用栈 stack = []
   - 独占时间数组 result = [0] * n
   - 上一个时间戳 prevTime = 0

2. 遍历每条日志：
   a. 解析日志：提取 functionId, action, timestamp
   
   b. 如果是 "start" 事件：
      - 如果栈不为空：更新栈顶函数的执行时间
      - 将新函数压入栈
      - 更新 prevTime = timestamp
   
   c. 如果是 "end" 事件：
      - 更新当前函数的执行时间
      - 弹出栈顶函数
      - 更新 prevTime = timestamp + 1

3. 返回 result 数组
```

### 图解演示
**示例：logs = ["0:start:0","1:start:2","1:end:5","0:end:6"]**

```plain
时间轴: 0  1  2  3  4  5  6
函数0:  |-----|        |--|
函数1:        |--------|

详细分析:
时间 0-1: 函数0独占执行 (2个时间单位)
时间 2-5: 函数1独占执行 (4个时间单位)
时间 6-6: 函数0独占执行 (1个时间单位)

函数0总独占时间: 2 + 1 = 3
函数1总独占时间: 4
```

#### 详细状态转换过程
```plain
初始状态:
stack = [], result = [0, 0], prevTime = 0

步骤1: 处理 "0:start:0"
操作: 函数0开始执行
- stack为空，直接压栈
- stack = [(0, 0)]
- prevTime = 0

步骤2: 处理 "1:start:2"  
操作: 函数1开始执行
- 更新函数0的执行时间: result[0] += (2 - 0) = 2
- 压栈函数1: stack = [(0, 0), (1, 2)]
- prevTime = 2

步骤3: 处理 "1:end:5"
操作: 函数1结束执行
- 更新函数1的执行时间: result[1] += (5 - 2 + 1) = 4
- 弹栈: stack = [(0, 0)]
- prevTime = 5 + 1 = 6

步骤4: 处理 "0:end:6"
操作: 函数0结束执行
- 更新函数0的执行时间: result[0] += (6 - 6 + 1) = 1
- 弹栈: stack = []
- prevTime = 6 + 1 = 7

最终结果: [3, 4]
```

#### 栈状态可视化
```plain
时间戳 0: "0:start:0"
┌─────────────────┐
│   函数0 (t=0)   │  ← 栈顶
└─────────────────┘

时间戳 2: "1:start:2"
┌─────────────────┐
│   函数1 (t=2)   │  ← 栈顶
├─────────────────┤
│   函数0 (t=0)   │
└─────────────────┘
函数0累计时间: 2-0 = 2

时间戳 5: "1:end:5"
┌─────────────────┐
│   函数0 (t=0)   │  ← 栈顶
└─────────────────┘
函数1累计时间: 5-2+1 = 4

时间戳 6: "0:end:6"
┌─────────────────┐
│      栈空       │
└─────────────────┘
函数0累计时间: 6-6+1 = 1
函数0总时间: 2+1 = 3
```

## 💻 代码实现
### 方法一：状态栈法（推荐）
```java
public class Solution {
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();  // 存储函数ID
        int prevTime = 0;  // 上一个时间戳
        
        for (String log : logs) {
            String[] parts = log.split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            if ("start".equals(action)) {
                // 函数开始执行
                if (!stack.isEmpty()) {
                    // 更新当前栈顶函数的执行时间
                    result[stack.peek()] += timestamp - prevTime;
                }
                
                // 新函数压栈
                stack.push(functionId);
                prevTime = timestamp;
                
            } else {
                // 函数结束执行
                // 更新当前函数的执行时间
                result[stack.pop()] += timestamp - prevTime + 1;
                prevTime = timestamp + 1;
            }
        }
        
        return result;
    }
}
```

### 方法二：带状态记录的栈
```java
public class SolutionWithState {
    
    static class FunctionState {
        int functionId;
        int startTime;
        
        FunctionState(int functionId, int startTime) {
            this.functionId = functionId;
            this.startTime = startTime;
        }
    }
    
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] result = new int[n];
        Deque<FunctionState> stack = new ArrayDeque<>();
        
        for (String log : logs) {
            String[] parts = log.split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            if ("start".equals(action)) {
                // 函数开始执行
                if (!stack.isEmpty()) {
                    // 暂停当前函数的计时
                    FunctionState current = stack.peek();
                    result[current.functionId] += timestamp - current.startTime;
                }
                
                // 新函数开始
                stack.push(new FunctionState(functionId, timestamp));
                
            } else {
                // 函数结束执行
                FunctionState current = stack.pop();
                result[current.functionId] += timestamp - current.startTime + 1;
                
                // 恢复上一个函数的计时
                if (!stack.isEmpty()) {
                    stack.peek().startTime = timestamp + 1;
                }
            }
        }
        
        return result;
    }
}
```

### 方法三：递归模拟法
```java
public class SolutionRecursive {
    
    private int index = 0;
    
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] result = new int[n];
        index = 0;
        parseFunction(logs, result);
        return result;
    }
    
    private int parseFunction(List<String> logs, int[] result) {
        String[] parts = logs.get(index++).split(":");
        int functionId = Integer.parseInt(parts[0]);
        int startTime = Integer.parseInt(parts[2]);
        
        int totalTime = 0;
        
        while (index < logs.size()) {
            String[] nextParts = logs.get(index).split(":");
            int nextFunctionId = Integer.parseInt(nextParts[0]);
            String nextAction = nextParts[1];
            int nextTime = Integer.parseInt(nextParts[2]);
            
            if ("start".equals(nextAction)) {
                // 嵌套函数调用
                totalTime += nextTime - startTime;
                int nestedTime = parseFunction(logs, result);
                startTime = nextTime + nestedTime + 1;
                
            } else if (nextFunctionId == functionId) {
                // 当前函数结束
                totalTime += nextTime - startTime + 1;
                result[functionId] += totalTime;
                index++;
                return nextTime - Integer.parseInt(logs.get(0).split(":")[2]);
            }
        }
        
        return 0;
    }
}
```

### 方法四：事件驱动法
```java
public class SolutionEventDriven {
    
    static class Event {
        int functionId;
        String action;
        int timestamp;
        
        Event(int functionId, String action, int timestamp) {
            this.functionId = functionId;
            this.action = action;
            this.timestamp = timestamp;
        }
    }
    
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] result = new int[n];
        List<Event> events = new ArrayList<>();
        
        // 解析所有事件
        for (String log : logs) {
            String[] parts = log.split(":");
            events.add(new Event(
                Integer.parseInt(parts[0]),
                parts[1],
                Integer.parseInt(parts[2])
            ));
        }
        
        Deque<Event> stack = new ArrayDeque<>();
        
        for (Event event : events) {
            if ("start".equals(event.action)) {
                // 暂停当前函数
                if (!stack.isEmpty()) {
                    Event current = stack.peek();
                    result[current.functionId] += event.timestamp - current.timestamp;
                }
                
                // 开始新函数
                stack.push(new Event(event.functionId, "start", event.timestamp));
                
            } else {
                // 结束当前函数
                Event current = stack.pop();
                result[current.functionId] += event.timestamp - current.timestamp + 1;
                
                // 恢复上一个函数
                if (!stack.isEmpty()) {
                    stack.peek().timestamp = event.timestamp + 1;
                }
            }
        }
        
        return result;
    }
}
```

### 方法五：时间片分析法
```java
public class SolutionTimeSlice {
    
    static class TimeSlice {
        int start;
        int end;
        int functionId;
        
        TimeSlice(int start, int end, int functionId) {
            this.start = start;
            this.end = end;
            this.functionId = functionId;
        }
        
        int duration() {
            return end - start + 1;
        }
    }
    
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] result = new int[n];
        List<TimeSlice> timeSlices = new ArrayList<>();
        Deque<Integer> stack = new ArrayDeque<>();
        Deque<Integer> startTimes = new ArrayDeque<>();
        
        for (String log : logs) {
            String[] parts = log.split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            if ("start".equals(action)) {
                // 记录当前时间片
                if (!stack.isEmpty()) {
                    int currentFunction = stack.peek();
                    int startTime = startTimes.peek();
                    timeSlices.add(new TimeSlice(startTime, timestamp - 1, currentFunction));
                }
                
                stack.push(functionId);
                startTimes.push(timestamp);
                
            } else {
                // 函数结束
                int currentFunction = stack.pop();
                int startTime = startTimes.pop();
                timeSlices.add(new TimeSlice(startTime, timestamp, currentFunction));
                
                // 恢复上一个函数的开始时间
                if (!startTimes.isEmpty()) {
                    startTimes.pop();
                    startTimes.push(timestamp + 1);
                }
            }
        }
        
        // 计算每个函数的总时间
        for (TimeSlice slice : timeSlices) {
            result[slice.functionId] += slice.duration();
        }
        
        return result;
    }
}
```

### 方法六：带详细日志的实现
```java
public class SolutionWithLogging {
    
    public int[] exclusiveTime(int n, List<String> logs) {
        System.out.println("🕐 函数独占时间计算器");
        System.out.println("函数数量: " + n);
        System.out.println("日志数量: " + logs.size());
        System.out.println("=" + "=".repeat(60));
        
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        int prevTime = 0;
        
        for (int i = 0; i < logs.size(); i++) {
            String log = logs.get(i);
            String[] parts = log.split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            System.out.printf("📋 步骤 %d: 处理日志 \"%s\"\n", i + 1, log);
            
            if ("start".equals(action)) {
                System.out.printf("  🚀 函数 %d 开始执行 (时间戳: %d)\n", functionId, timestamp);
                
                if (!stack.isEmpty()) {
                    int currentFunction = stack.peek();
                    int executionTime = timestamp - prevTime;
                    result[currentFunction] += executionTime;
                    
                    System.out.printf("    ⏸️  暂停函数 %d，累计执行时间: %d\n", 
                                    currentFunction, executionTime);
                    System.out.printf("    📊 函数 %d 当前总时间: %d\n", 
                                    currentFunction, result[currentFunction]);
                }
                
                stack.push(functionId);
                prevTime = timestamp;
                
                System.out.printf("    📥 函数 %d 压入栈\n", functionId);
                
            } else {
                System.out.printf("  🏁 函数 %d 结束执行 (时间戳: %d)\n", functionId, timestamp);
                
                int executionTime = timestamp - prevTime + 1;
                result[functionId] += executionTime;
                stack.pop();
                prevTime = timestamp + 1;
                
                System.out.printf("    ⏱️  函数 %d 本次执行时间: %d\n", functionId, executionTime);
                System.out.printf("    📊 函数 %d 当前总时间: %d\n", functionId, result[functionId]);
                System.out.printf("    📤 函数 %d 弹出栈\n", functionId);
            }
            
            printCurrentState(stack, result, prevTime);
            System.out.println();
        }
        
        System.out.println("🏆 计算完成！");
        System.out.print("最终结果: [");
        for (int i = 0; i < result.length; i++) {
            if (i > 0) System.out.print(", ");
            System.out.print(result[i]);
        }
        System.out.println("]");
        
        return result;
    }
    
    private void printCurrentState(Deque<Integer> stack, int[] result, int prevTime) {
        System.out.printf("  📊 当前状态:\n");
        System.out.printf("    调用栈: %s\n", formatStack(stack));
        System.out.printf("    累计时间: %s\n", Arrays.toString(result));
        System.out.printf("    上次时间戳: %d\n", prevTime);
    }
    
    private String formatStack(Deque<Integer> stack) {
        if (stack.isEmpty()) return "[]";
        
        List<Integer> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < stackList.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append("函数").append(stackList.get(i));
        }
        sb.append("] (底→顶)");
        
        return sb.toString();
    }
    
    public static void main(String[] args) {
        SolutionWithLogging solution = new SolutionWithLogging();
        
        // 测试用例1
        System.out.println("🧪 测试用例 1:");
        List<String> logs1 = Arrays.asList("0:start:0", "1:start:2", "1:end:5", "0:end:6");
        solution.exclusiveTime(2, logs1);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试用例2
        System.out.println("🧪 测试用例 2:");
        List<String> logs2 = Arrays.asList("0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7");
        solution.exclusiveTime(1, logs2);
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**状态栈法：**

+ 每条日志被处理一次
+ 栈操作（push/pop）的时间复杂度为 O(1)
+ 时间复杂度：**O(m)**，其中 m 是日志的数量

**递归模拟法：**

+ 每条日志被访问一次
+ 递归深度等于最大函数调用深度
+ 时间复杂度：**O(m)**

**事件驱动法：**

+ 需要解析所有日志
+ 每个事件处理一次
+ 时间复杂度：**O(m)**

### 空间复杂度
**状态栈法：**

+ 栈的大小取决于最大函数调用深度
+ 结果数组大小为 n
+ 空间复杂度：**O(n + d)**，其中 d 是最大调用深度

**递归模拟法：**

+ 递归调用栈的深度等于最大函数调用深度
+ 空间复杂度：**O(n + d)**

**事件驱动法：**

+ 需要存储所有事件
+ 空间复杂度：**O(m + n + d)**

## 🎨 可视化演示
### 详细执行过程演示
```java
/**
 * 可视化函数独占时间计算的详细过程
 */
public class VisualExclusiveTime {
    
    public static int[] calculateWithVisualization(int n, List<String> logs) {
        System.out.println("🕐 函数独占时间可视化计算器");
        System.out.println("=" + "=".repeat(60));
        
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        int prevTime = 0;
        
        // 显示初始状态
        System.out.println("初始状态:");
        printTimelineHeader(logs);
        printCurrentTimeline(logs, -1, stack, result);
        System.out.println();
        
        for (int i = 0; i < logs.size(); i++) {
            String log = logs.get(i);
            String[] parts = log.split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            System.out.printf("📍 步骤 %d: 处理 \"%s\"\n", i + 1, log);
            
            if ("start".equals(action)) {
                if (!stack.isEmpty()) {
                    int currentFunction = stack.peek();
                    int executionTime = timestamp - prevTime;
                    result[currentFunction] += executionTime;
                    
                    System.out.printf("  ⏸️  函数 %d 暂停，执行了 %d 个时间单位\n", 
                                    currentFunction, executionTime);
                }
                
                stack.push(functionId);
                prevTime = timestamp;
                
                System.out.printf("  🚀 函数 %d 开始执行\n", functionId);
                
            } else {
                int executionTime = timestamp - prevTime + 1;
                result[functionId] += executionTime;
                stack.pop();
                prevTime = timestamp + 1;
                
                System.out.printf("  🏁 函数 %d 结束，执行了 %d 个时间单位\n", 
                                functionId, executionTime);
            }
            
            printCurrentTimeline(logs, i, stack, result);
            printStackVisualization(stack);
            printResultSummary(result);
            System.out.println();
        }
        
        System.out.println("🏆 计算完成！");
        printFinalResult(result);
        
        return result;
    }
    
    private static void printTimelineHeader(List<String> logs) {
        System.out.print("时间轴: ");
        Set<Integer> timestamps = new TreeSet<>();
        for (String log : logs) {
            timestamps.add(Integer.parseInt(log.split(":")[2]));
        }
        
        for (int time : timestamps) {
            System.out.printf("%3d", time);
        }
        System.out.println();
    }
    
    private static void printCurrentTimeline(List<String> logs, int currentIndex, 
                                           Deque<Integer> stack, int[] result) {
        // 获取所有时间戳
        Set<Integer> timestamps = new TreeSet<>();
        for (String log : logs) {
            timestamps.add(Integer.parseInt(log.split(":")[2]));
        }
        
        // 构建时间线
        Map<Integer, String> functionAtTime = new HashMap<>();
        Deque<Integer> tempStack = new ArrayDeque<>();
        int tempPrevTime = 0;
        
        for (int i = 0; i <= currentIndex; i++) {
            String[] parts = logs.get(i).split(":");
            int functionId = Integer.parseInt(parts[0]);
            String action = parts[1];
            int timestamp = Integer.parseInt(parts[2]);
            
            if ("start".equals(action)) {
                tempStack.push(functionId);
                for (int t = timestamp; t < (i + 1 < logs.size() ? 
                    Integer.parseInt(logs.get(i + 1).split(":")[2]) : timestamp + 1); t++) {
                    functionAtTime.put(t, "F" + functionId);
                }
            } else {
                tempStack.pop();
                for (int t = tempPrevTime; t <= timestamp; t++) {
                    functionAtTime.put(t, "F" + functionId);
                }
            }
        }
        
        // 显示当前执行状态
        System.out.print("执行状态: ");
        for (int time : timestamps) {
            String func = functionAtTime.getOrDefault(time, "---");
            System.out.printf("%3s", func);
        }
        System.out.println();
    }
    
    private static void printStackVisualization(Deque<Integer> stack) {
        System.out.println("  📚 调用栈状态:");
        
        if (stack.isEmpty()) {
            System.out.println("    ┌─────────────┐");
            System.out.println("    │    栈空     │");
            System.out.println("    └─────────────┘");
            return;
        }
        
        List<Integer> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        for (int i = stackList.size() - 1; i >= 0; i--) {
            System.out.println("    ┌─────────────┐");
            System.out.printf("    │   函数 %-2d   │", stackList.get(i));
            if (i == stackList.size() - 1) {
                System.out.print(" ← 栈顶 (当前执行)");
            }
            System.out.println();
            System.out.println("    └─────────────┘");
        }
    }
    
    private static void printResultSummary(int[] result) {
        System.out.println("  📊 当前累计时间:");
        for (int i = 0; i < result.length; i++) {
            System.out.printf("    函数 %d: %d 个时间单位\n", i, result[i]);
        }
    }
    
    private static void printFinalResult(int[] result) {
        System.out.println("📈 最终独占时间统计:");
        System.out.println("┌─────────┬─────────────┐");
        System.out.println("│  函数ID │  独占时间   │");
        System.out.println("├─────────┼─────────────┤");
        
        for (int i = 0; i < result.length; i++) {
            System.out.printf("│   %-2d    │     %-2d      │\n", i, result[i]);
        }
        
        System.out.println("└─────────┴─────────────┘");
        
        int totalTime = Arrays.stream(result).sum();
        System.out.printf("总执行时间: %d 个时间单位\n", totalTime);
    }
    
    public static void main(String[] args) {
        // 测试用例1
        System.out.println("🧪 测试用例 1: 基本嵌套调用");
        List<String> logs1 = Arrays.asList("0:start:0", "1:start:2", "1:end:5", "0:end:6");
        calculateWithVisualization(2, logs1);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试用例2
        System.out.println("🧪 测试用例 2: 递归调用");
        List<String> logs2 = Arrays.asList("0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7");
        calculateWithVisualization(1, logs2);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试用例3
        System.out.println("🧪 测试用例 3: 复杂嵌套");
        List<String> logs3 = Arrays.asList("0:start:0", "1:start:1", "2:start:2", "2:end:3", "1:end:4", "0:end:5");
        calculateWithVisualization(3, logs3);
    }
}
```

### 运行结果示例
```plain
🧪 测试用例 1: 基本嵌套调用
🕐 函数独占时间可视化计算器
============================================================

初始状态:
时间轴:   0  2  5  6
执行状态: ---  ---  ---  ---

📍 步骤 1: 处理 "0:start:0"
  🚀 函数 0 开始执行
执行状态: F0  ---  ---  ---
  📚 调用栈状态:
    ┌─────────────┐
    │   函数 0    │ ← 栈顶 (当前执行)
    └─────────────┘
  📊 当前累计时间:
    函数 0: 0 个时间单位
    函数 1: 0 个时间单位

📍 步骤 2: 处理 "1:start:2"
  ⏸️  函数 0 暂停，执行了 2 个时间单位
  🚀 函数 1 开始执行
执行状态: F0  F1  ---  ---
  📚 调用栈状态:
    ┌─────────────┐
    │   函数 1    │ ← 栈顶 (当前执行)
    └─────────────┘
    ┌─────────────┐
    │   函数 0    │
    └─────────────┘
  📊 当前累计时间:
    函数 0: 2 个时间单位
    函数 1: 0 个时间单位

📍 步骤 3: 处理 "1:end:5"
  🏁 函数 1 结束，执行了 4 个时间单位
执行状态: F0  F1  F1  ---
  📚 调用栈状态:
    ┌─────────────┐
    │   函数 0    │ ← 栈顶 (当前执行)
    └─────────────┘
  📊 当前累计时间:
    函数 0: 2 个时间单位
    函数 1: 4 个时间单位

📍 步骤 4: 处理 "0:end:6"
  🏁 函数 0 结束，执行了 1 个时间单位
执行状态: F0  F1  F1  F0
  📚 调用栈状态:
    ┌─────────────┐
    │    栈空     │
    └─────────────┘
  📊 当前累计时间:
    函数 0: 3 个时间单位
    函数 1: 4 个时间单位

🏆 计算完成！
📈 最终独占时间统计:
┌─────────┬─────────────┐
│  函数ID │  独占时间   │
├─────────┼─────────────┤
│   0     │     3       │
│   1     │     4       │
└─────────┴─────────────┘
总执行时间: 7 个时间单位
```

## 🧪 测试用例
### 基础功能测试
```java
public class ExclusiveTimeTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 简单嵌套
        List<String> logs1 = Arrays.asList("0:start:0", "1:start:2", "1:end:5", "0:end:6");
        int[] expected1 = {3, 4};
        assertArrayEquals(expected1, solution.exclusiveTime(2, logs1));
        
        // 递归调用
        List<String> logs2 = Arrays.asList("0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7");
        int[] expected2 = {8};
        assertArrayEquals(expected2, solution.exclusiveTime(1, logs2));
        
        // 单个函数
        List<String> logs3 = Arrays.asList("0:start:0", "0:end:5");
        int[] expected3 = {6};
        assertArrayEquals(expected3, solution.exclusiveTime(1, logs3));
    }
    
    @Test
    public void testComplexNesting() {
        // 三层嵌套
        List<String> logs = Arrays.asList(
            "0:start:0", "1:start:1", "2:start:2", "2:end:3", "1:end:4", "0:end:5"
        );
        int[] expected = {3, 2, 2};
        assertArrayEquals(expected, solution.exclusiveTime(3, logs));
        
        // 深度嵌套
        List<String> logs2 = Arrays.asList(
            "0:start:0", "1:start:1", "2:start:2", "3:start:3", "3:end:3", "2:end:4", "1:end:5", "0:end:6"
        );
        int[] expected2 = {3, 2, 2, 1};
        assertArrayEquals(expected2, solution.exclusiveTime(4, logs2));
    }
    
    @Test
    public void testSequentialCalls() {
        // 顺序调用
        List<String> logs = Arrays.asList(
            "0:start:0", "0:end:2", "1:start:3", "1:end:5", "2:start:6", "2:end:8"
        );
        int[] expected = {3, 3, 3};
        assertArrayEquals(expected, solution.exclusiveTime(3, logs));
        
        // 交替调用
        List<String> logs2 = Arrays.asList(
            "0:start:0", "0:end:1", "1:start:2", "1:end:3", "0:start:4", "0:end:5"
        );
        int[] expected2 = {4, 2};
        assertArrayEquals(expected2, solution.exclusiveTime(2, logs2));
    }
}
```

### 边界条件测试
```java
public class ExclusiveTimeBoundaryTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testMinimalCases() {
        // 最小输入
        List<String> logs = Arrays.asList("0:start:0", "0:end:0");
        int[] expected = {1};
        assertArrayEquals(expected, solution.exclusiveTime(1, logs));
        
        // 零时间执行
        List<String> logs2 = Arrays.asList("0:start:5", "0:end:5");
        int[] expected2 = {1};
        assertArrayEquals(expected2, solution.exclusiveTime(1, logs2));
    }
    
    @Test
    public void testLargeTimestamps() {
        // 大时间戳
        List<String> logs = Arrays.asList("0:start:1000000000", "0:end:1000000000");
        int[] expected = {1};
        assertArrayEquals(expected, solution.exclusiveTime(1, logs));
        
        // 时间戳跨度大
        List<String> logs2 = Arrays.asList("0:start:0", "0:end:1000000000");
        int[] expected2 = {1000000001};
        assertArrayEquals(expected2, solution.exclusiveTime(1, logs2));
    }
    
    @Test
    public void testMaxFunctions() {
        // 最大函数数量
        List<String> logs = new ArrayList<>();
        int n = 100;
        
        // 所有函数顺序执行
        for (int i = 0; i < n; i++) {
            logs.add(i + ":start:" + (i * 2));
            logs.add(i + ":end:" + (i * 2 + 1));
        }
        
        int[] result = solution.exclusiveTime(n, logs);
        
        // 每个函数执行2个时间单位
        for (int i = 0; i < n; i++) {
            assertEquals(2, result[i]);
        }
    }
    
    @Test
    public void testDeepNesting() {
        // 深度嵌套
        List<String> logs = new ArrayList<>();
        int depth = 50;
        
        // 开始所有函数
        for (int i = 0; i < depth; i++) {
            logs.add(i + ":start:" + i);
        }
        
        // 结束所有函数
        for (int i = depth - 1; i >= 0; i--) {
            logs.add(i + ":end:" + (depth + (depth - 1 - i)));
        }
        
        int[] result = solution.exclusiveTime(depth, logs);
        
        // 验证结果
        assertEquals(1, result[0]); // 最外层函数
        assertEquals(1, result[depth - 1]); // 最内层函数
    }
}
```

### 性能测试
```java
public class ExclusiveTimePerformanceTest {
    
    @Test
    public void testPerformanceComparison() {
        // 构造大型测试数据
        List<String> logs = generateLargeLogs(1000);
        
        Solution solution1 = new Solution();
        SolutionWithState solution2 = new SolutionWithState();
        SolutionEventDriven solution3 = new SolutionEventDriven();
        
        long startTime, endTime;
        
        // 状态栈法
        startTime = System.nanoTime();
        int[] result1 = solution1.exclusiveTime(100, logs);
        endTime = System.nanoTime();
        System.out.printf("状态栈法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 带状态记录的栈
        startTime = System.nanoTime();
        int[] result2 = solution2.exclusiveTime(100, logs);
        endTime = System.nanoTime();
        System.out.printf("状态记录栈: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 事件驱动法
        startTime = System.nanoTime();
        int[] result3 = solution3.exclusiveTime(100, logs);
        endTime = System.nanoTime();
        System.out.printf("事件驱动法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertArrayEquals(result1, result2);
        assertArrayEquals(result1, result3);
        
        System.out.println("性能测试通过 ✅");
    }
    
    private List<String> generateLargeLogs(int logCount) {
        List<String> logs = new ArrayList<>();
        Random random = new Random(42); // 固定种子保证可重现
        
        int functionCount = 100;
        int currentTime = 0;
        
        for (int i = 0; i < logCount / 2; i++) {
            int functionId = random.nextInt(functionCount);
            
            logs.add(functionId + ":start:" + currentTime);
            currentTime += random.nextInt(10) + 1;
            
            logs.add(functionId + ":end:" + currentTime);
            currentTime += random.nextInt(5) + 1;
        }
        
        return logs;
    }
    
    @Test
    public void testMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // 构造大型嵌套调用
        List<String> logs = generateNestedLogs(1000);
        
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        Solution solution = new Solution();
        int[] result = solution.exclusiveTime(100, logs);
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        System.out.printf("日志数量: %d\n", logs.size());
        System.out.printf("函数数量: %d\n", result.length);
    }
    
    private List<String> generateNestedLogs(int depth) {
        List<String> logs = new ArrayList<>();
        
        // 创建深度嵌套的函数调用
        for (int i = 0; i < depth; i++) {
            logs.add((i % 100) + ":start:" + i);
        }
        
        for (int i = depth - 1; i >= 0; i--) {
            logs.add((i % 100) + ":end:" + (depth + (depth - 1 - i)));
        }
        
        return logs;
    }
}
```



> 更新: 2025-09-19 00:54:23  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/4cf93230e4336eb7fb25473bfd0e7132>