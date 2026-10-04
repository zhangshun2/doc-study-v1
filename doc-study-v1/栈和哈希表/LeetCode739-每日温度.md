# LeetCode 739 - 每日温度
## 📋 题目描述
**难度：中等**

给定一个整数数组 `temperatures` ，表示每天的温度，返回一个数组 `answer` ，其中 `answer[i]` 是指对于第 `i` 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 `0` 来代替。

### 示例
**示例 1：**

```plain
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
解释:
- 第0天(73°C)，第1天就有更高温度74°C，所以答案是1
- 第1天(74°C)，第2天就有更高温度75°C，所以答案是1  
- 第2天(75°C)，第6天才有更高温度76°C，所以答案是4
- 第3天(71°C)，第5天就有更高温度72°C，所以答案是2
- 第4天(69°C)，第5天就有更高温度72°C，所以答案是1
- 第5天(72°C)，第6天就有更高温度76°C，所以答案是1
- 第6天(76°C)，之后没有更高温度，所以答案是0
- 第7天(73°C)，之后没有更高温度，所以答案是0
```

**示例 2：**

```plain
输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]
```

**示例 3：**

```plain
输入: temperatures = [30,60,90]
输出: [1,1,0]
```

### 约束条件
+ `1 <= temperatures.length <= 10^5`
+ `30 <= temperatures[i] <= 100`

## 🎯 解题思路
### 核心问题分析
这是一个典型的**单调栈+哈希表问题**。关键在于：

1. 使用单调递减栈来维护待匹配的温度索引
2. 使用哈希表来快速存储和查询结果
3. 当遇到更高温度时，弹出栈中所有较小的温度并计算距离

### 单调栈+哈希表解法原理
```plain
核心思想：
- 维护一个单调递减栈，存储温度的索引
- 当遇到更高温度时，弹出栈中所有较小温度的索引
- 计算距离并存储到结果数组中

单调栈的作用：
- 保持栈中元素对应的温度单调递减
- 快速找到每个温度的下一个更高温度

哈希表的作用：
- 在这个问题中，结果数组本身就起到了哈希表的作用
- 直接通过索引访问和存储结果
```

### 算法步骤
```plain
1. 初始化：
   - 创建单调栈（存储索引）
   - 创建结果数组（初始值为0）

2. 遍历温度数组：
   - 当栈不为空且当前温度 > 栈顶索引对应的温度时：
     - 弹出栈顶索引
     - 计算距离：当前索引 - 弹出的索引
     - 将距离存储到结果数组中
   - 将当前索引压入栈

3. 返回结果数组
```

### 图解演示
**示例：temperatures = [73,74,75,71,69,72,76,73]**

```plain
初始状态：
索引: 0  1  2  3  4  5  6  7
温度: 73 74 75 71 69 72 76 73
栈:   []
结果: [0, 0, 0, 0, 0, 0, 0, 0]

步骤 1: 处理索引 0 (温度 73)
栈为空，直接入栈
栈: [0]
结果: [0, 0, 0, 0, 0, 0, 0, 0]

步骤 2: 处理索引 1 (温度 74)
74 > 73 (栈顶索引0对应温度)
弹出索引0，计算距离: 1-0=1
将1存储到result[0]
将索引1入栈
栈: [1]
结果: [1, 0, 0, 0, 0, 0, 0, 0]

步骤 3: 处理索引 2 (温度 75)
75 > 74 (栈顶索引1对应温度)
弹出索引1，计算距离: 2-1=1
将1存储到result[1]
将索引2入栈
栈: [2]
结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 4: 处理索引 3 (温度 71)
71 < 75 (栈顶索引2对应温度)
直接将索引3入栈
栈: [2, 3]
结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 5: 处理索引 4 (温度 69)
69 < 71 (栈顶索引3对应温度)
直接将索引4入栈
栈: [2, 3, 4]
结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 6: 处理索引 5 (温度 72)
72 > 69 (栈顶索引4对应温度)
弹出索引4，计算距离: 5-4=1，result[4]=1
72 > 71 (栈顶索引3对应温度)
弹出索引3，计算距离: 5-3=2，result[3]=2
72 < 75 (栈顶索引2对应温度)
将索引5入栈
栈: [2, 5]
结果: [1, 1, 0, 2, 1, 0, 0, 0]

步骤 7: 处理索引 6 (温度 76)
76 > 72 (栈顶索引5对应温度)
弹出索引5，计算距离: 6-5=1，result[5]=1
76 > 75 (栈顶索引2对应温度)
弹出索引2，计算距离: 6-2=4，result[2]=4
将索引6入栈
栈: [6]
结果: [1, 1, 4, 2, 1, 1, 0, 0]

步骤 8: 处理索引 7 (温度 73)
73 < 76 (栈顶索引6对应温度)
直接将索引7入栈
栈: [6, 7]
结果: [1, 1, 4, 2, 1, 1, 0, 0]

最终结果: [1, 1, 4, 2, 1, 1, 0, 0]
栈中剩余的索引6和7对应的结果保持为0
```

## 💻 代码实现
### 方法一：单调栈（推荐）
```java
import java.util.*;

public class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < n; i++) {
            // 当栈不为空且当前温度大于栈顶索引对应的温度
            while (!stack.isEmpty() && 
                   temperatures[i] > temperatures[stack.peek()]) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            
            // 将当前索引入栈
            stack.push(i);
        }
        
        return result;
    }
}
```

### 方法二：单调栈+哈希表优化（理论扩展）
```java
public class SolutionWithHashMap {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 使用HashMap记录每个温度最近出现的位置（可选优化）
        Map<Integer, Integer> tempToIndex = new HashMap<>();
        
        for (int i = 0; i < n; i++) {
            int currentTemp = temperatures[i];
            
            // 弹出所有小于当前温度的索引
            while (!stack.isEmpty() && 
                   temperatures[stack.peek()] < currentTemp) {
                int prevIndex = stack.pop();
                result[prevIndex] = i - prevIndex;
            }
            
            stack.push(i);
            tempToIndex.put(currentTemp, i);
        }
        
        return result;
    }
}
```

### 方法三：暴力解法（对比参考）
```java
public class SolutionBruteForce {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (temperatures[j] > temperatures[i]) {
                    result[i] = j - i;
                    break;
                }
            }
        }
        
        return result;
    }
}
```

### 方法四：逆向遍历+跳跃优化
```java
public class SolutionReverse {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        
        // 从右向左遍历
        for (int i = n - 2; i >= 0; i--) {
            int j = i + 1;
            
            // 跳跃查找
            while (j < n && temperatures[j] <= temperatures[i]) {
                if (result[j] == 0) {
                    j = n; // 没有更高温度
                } else {
                    j += result[j]; // 跳跃到下一个可能的位置
                }
            }
            
            if (j < n) {
                result[i] = j - i;
            }
        }
        
        return result;
    }
}
```

### 方法五：基于温度范围的桶排序优化
```java
public class SolutionBucket {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] result = new int[n];
        
        // 温度范围是30-100，创建对应的桶
        int[] next = new int[101]; // next[temp] 表示温度temp下次出现的位置
        Arrays.fill(next, Integer.MAX_VALUE);
        
        // 从右向左遍历
        for (int i = n - 1; i >= 0; i--) {
            int currentTemp = temperatures[i];
            int nextWarmerDay = Integer.MAX_VALUE;
            
            // 查找所有比当前温度高的温度的最近出现位置
            for (int temp = currentTemp + 1; temp <= 100; temp++) {
                if (next[temp] < nextWarmerDay) {
                    nextWarmerDay = next[temp];
                }
            }
            
            if (nextWarmerDay != Integer.MAX_VALUE) {
                result[i] = nextWarmerDay - i;
            }
            
            next[currentTemp] = i;
        }
        
        return result;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**单调栈解法：**

+ 每个元素最多入栈一次，出栈一次
+ 总时间复杂度：O(n)

**暴力解法：**

+ 双重循环遍历
+ 总时间复杂度：O(n²)

**逆向遍历+跳跃优化：**

+ 最坏情况下仍是O(n²)，但平均情况下更优
+ 总时间复杂度：O(n²) 最坏，O(n) 平均

**桶排序优化：**

+ 外层循环O(n)，内层循环O(70)（温度范围）
+ 总时间复杂度：O(n × 70) = O(n)

### 空间复杂度
**单调栈解法：**

+ 栈空间：O(n) 最坏情况下所有元素都在栈中
+ 总空间复杂度：O(n)

**暴力解法：**

+ 只使用常数额外空间
+ 总空间复杂度：O(1)

**逆向遍历+跳跃优化：**

+ 只使用常数额外空间
+ 总空间复杂度：O(1)

**桶排序优化：**

+ 需要额外的桶数组
+ 总空间复杂度：O(1)（桶大小固定为101）

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的每日温度计算
 */
public class VisualDailyTemperatures {
    
    public static int[] dailyTemperaturesWithVisualization(int[] temperatures) {
        System.out.println("🌡️ 每日温度问题");
        System.out.println("输入温度数组: " + Arrays.toString(temperatures));
        printArrayWithIndices(temperatures);
        System.out.println("=" + "=".repeat(80));
        
        int n = temperatures.length;
        int[] result = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        
        System.out.println("📊 使用单调栈处理:");
        
        for (int i = 0; i < n; i++) {
            int currentTemp = temperatures[i];
            System.out.printf("\n步骤 %d: 处理索引 %d (温度 %d°C)\n", 
                            i + 1, i, currentTemp);
            
            // 处理栈中小于当前温度的元素
            List<String> poppedElements = new ArrayList<>();
            while (!stack.isEmpty() && 
                   temperatures[stack.peek()] < currentTemp) {
                int prevIndex = stack.pop();
                int distance = i - prevIndex;
                result[prevIndex] = distance;
                
                poppedElements.add(String.format(
                    "索引%d(温度%d°C) -> 距离%d", 
                    prevIndex, temperatures[prevIndex], distance));
            }
            
            if (!poppedElements.isEmpty()) {
                System.out.println("  🔥 找到更高温度，弹出栈中元素:");
                for (String element : poppedElements) {
                    System.out.println("    " + element);
                }
            } else {
                System.out.println("  ❄️ 当前温度不高于栈顶，无需弹出");
            }
            
            stack.push(i);
            System.out.printf("  📥 将索引 %d 入栈\n", i);
            
            printStackState(stack, temperatures);
            printCurrentResult(result);
        }
        
        System.out.println("\n🔚 处理完成，栈中剩余元素对应的结果保持为0");
        printFinalStackState(stack, temperatures);
        
        System.out.println("\n🏆 最终结果: " + Arrays.toString(result));
        
        // 验证结果
        System.out.println("\n🧪 验证结果:");
        verifyResult(temperatures, result);
        
        return result;
    }
    
    private static void printArrayWithIndices(int[] arr) {
        System.out.print("索引: ");
        for (int i = 0; i < arr.length; i++) {
            System.out.printf("%3d ", i);
        }
        System.out.println();
        
        System.out.print("温度: ");
        for (int temp : arr) {
            System.out.printf("%3d ", temp);
        }
        System.out.println();
    }
    
    private static void printStackState(Deque<Integer> stack, int[] temperatures) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                int index = stackList.get(i);
                System.out.printf("%d(%d°C)", index, temperatures[index]);
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    private static void printCurrentResult(int[] result) {
        System.out.print("  当前结果: [");
        for (int i = 0; i < result.length; i++) {
            if (i > 0) System.out.print(", ");
            System.out.print(result[i]);
        }
        System.out.println("]");
    }
    
    private static void printFinalStackState(Deque<Integer> stack, int[] temperatures) {
        if (!stack.isEmpty()) {
            System.out.print("栈中剩余元素: ");
            List<Integer> remaining = new ArrayList<>(stack);
            Collections.reverse(remaining);
            for (int i = 0; i < remaining.size(); i++) {
                if (i > 0) System.out.print(", ");
                int index = remaining.get(i);
                System.out.printf("索引%d(温度%d°C)", index, temperatures[index]);
            }
            System.out.println(" - 这些位置之后没有更高温度");
        }
    }
    
    private static void verifyResult(int[] temperatures, int[] result) {
        boolean isValid = true;
        
        for (int i = 0; i < temperatures.length; i++) {
            if (result[i] == 0) {
                // 验证后面确实没有更高温度
                boolean hasHigher = false;
                for (int j = i + 1; j < temperatures.length; j++) {
                    if (temperatures[j] > temperatures[i]) {
                        hasHigher = true;
                        break;
                    }
                }
                if (hasHigher) {
                    System.out.printf("  ❌ 索引 %d 的结果错误\n", i);
                    isValid = false;
                }
            } else {
                // 验证指定位置确实有更高温度
                int targetIndex = i + result[i];
                if (targetIndex >= temperatures.length || 
                    temperatures[targetIndex] <= temperatures[i]) {
                    System.out.printf("  ❌ 索引 %d 的结果错误\n", i);
                    isValid = false;
                }
            }
        }
        
        if (isValid) {
            System.out.println("  ✅ 结果验证通过");
        }
    }
    
    public static void main(String[] args) {
        // 测试示例
        int[][] testCases = {
            {73, 74, 75, 71, 69, 72, 76, 73},
            {30, 40, 50, 60},
            {30, 60, 90},
            {89, 62, 70, 58, 47, 47, 46, 76, 100, 70}
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("测试用例 %d:\n", i + 1);
            dailyTemperaturesWithVisualization(testCases[i]);
            System.out.println("\n" + "=".repeat(90) + "\n");
        }
    }
}
```

### 运行结果示例
```plain
🌡️ 每日温度问题
输入温度数组: [73, 74, 75, 71, 69, 72, 76, 73]
索引:   0   1   2   3   4   5   6   7 
温度:  73  74  75  71  69  72  76  73 
================================================================================

📊 使用单调栈处理:

步骤 1: 处理索引 0 (温度 73°C)
  ❄️ 当前温度不高于栈顶，无需弹出
  📥 将索引 0 入栈
  栈状态: [0(73°C)] (底 -> 顶)
  当前结果: [0, 0, 0, 0, 0, 0, 0, 0]

步骤 2: 处理索引 1 (温度 74°C)
  🔥 找到更高温度，弹出栈中元素:
    索引0(温度73°C) -> 距离1
  📥 将索引 1 入栈
  栈状态: [1(74°C)] (底 -> 顶)
  当前结果: [1, 0, 0, 0, 0, 0, 0, 0]

步骤 3: 处理索引 2 (温度 75°C)
  🔥 找到更高温度，弹出栈中元素:
    索引1(温度74°C) -> 距离1
  📥 将索引 2 入栈
  栈状态: [2(75°C)] (底 -> 顶)
  当前结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 4: 处理索引 3 (温度 71°C)
  ❄️ 当前温度不高于栈顶，无需弹出
  📥 将索引 3 入栈
  栈状态: [2(75°C), 3(71°C)] (底 -> 顶)
  当前结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 5: 处理索引 4 (温度 69°C)
  ❄️ 当前温度不高于栈顶，无需弹出
  📥 将索引 4 入栈
  栈状态: [2(75°C), 3(71°C), 4(69°C)] (底 -> 顶)
  当前结果: [1, 1, 0, 0, 0, 0, 0, 0]

步骤 6: 处理索引 5 (温度 72°C)
  🔥 找到更高温度，弹出栈中元素:
    索引4(温度69°C) -> 距离1
    索引3(温度71°C) -> 距离2
  📥 将索引 5 入栈
  栈状态: [2(75°C), 5(72°C)] (底 -> 顶)
  当前结果: [1, 1, 0, 2, 1, 0, 0, 0]

步骤 7: 处理索引 6 (温度 76°C)
  🔥 找到更高温度，弹出栈中元素:
    索引5(温度72°C) -> 距离1
    索引2(温度75°C) -> 距离4
  📥 将索引 6 入栈
  栈状态: [6(76°C)] (底 -> 顶)
  当前结果: [1, 1, 4, 2, 1, 1, 0, 0]

步骤 8: 处理索引 7 (温度 73°C)
  ❄️ 当前温度不高于栈顶，无需弹出
  📥 将索引 7 入栈
  栈状态: [6(76°C), 7(73°C)] (底 -> 顶)
  当前结果: [1, 1, 4, 2, 1, 1, 0, 0]

🔚 处理完成，栈中剩余元素对应的结果保持为0
栈中剩余元素: 索引6(温度76°C), 索引7(温度73°C) - 这些位置之后没有更高温度

🏆 最终结果: [1, 1, 4, 2, 1, 1, 0, 0]

🧪 验证结果:
  ✅ 结果验证通过
```

## 🧪 测试用例
### 基础功能测试
```java
public class DailyTemperaturesTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 示例 1
        int[] temperatures1 = {73, 74, 75, 71, 69, 72, 76, 73};
        int[] expected1 = {1, 1, 4, 2, 1, 1, 0, 0};
        assertArrayEquals(expected1, solution.dailyTemperatures(temperatures1));
        
        // 示例 2
        int[] temperatures2 = {30, 40, 50, 60};
        int[] expected2 = {1, 1, 1, 0};
        assertArrayEquals(expected2, solution.dailyTemperatures(temperatures2));
        
        // 示例 3
        int[] temperatures3 = {30, 60, 90};
        int[] expected3 = {1, 1, 0};
        assertArrayEquals(expected3, solution.dailyTemperatures(temperatures3));
    }
    
    @Test
    public void testEdgeCases() {
        // 单个元素
        int[] temperatures1 = {30};
        int[] expected1 = {0};
        assertArrayEquals(expected1, solution.dailyTemperatures(temperatures1));
        
        // 递增序列
        int[] temperatures2 = {30, 40, 50, 60, 70};
        int[] expected2 = {1, 1, 1, 1, 0};
        assertArrayEquals(expected2, solution.dailyTemperatures(temperatures2));
        
        // 递减序列
        int[] temperatures3 = {70, 60, 50, 40, 30};
        int[] expected3 = {0, 0, 0, 0, 0};
        assertArrayEquals(expected3, solution.dailyTemperatures(temperatures3));
        
        // 相同温度
        int[] temperatures4 = {50, 50, 50, 50};
        int[] expected4 = {0, 0, 0, 0};
        assertArrayEquals(expected4, solution.dailyTemperatures(temperatures4));
    }
    
    @Test
    public void testComplexCases() {
        // 复杂情况1：山峰型
        int[] temperatures1 = {30, 40, 50, 60, 70, 60, 50, 40, 30};
        int[] expected1 = {1, 1, 1, 1, 0, 0, 0, 0, 0};
        assertArrayEquals(expected1, solution.dailyTemperatures(temperatures1));
        
        // 复杂情况2：波浪型
        int[] temperatures2 = {30, 60, 40, 70, 50, 80};
        int[] expected2 = {1, 2, 1, 2, 1, 0};
        assertArrayEquals(expected2, solution.dailyTemperatures(temperatures2));
        
        // 复杂情况3：最后一天最高
        int[] temperatures3 = {30, 40, 35, 45, 38, 100};
        int[] expected3 = {1, 3, 1, 2, 1, 0};
        assertArrayEquals(expected3, solution.dailyTemperatures(temperatures3));
    }
    
    @Test
    public void testLargeInput() {
        // 大输入测试
        int[] temperatures = new int[10000];
        for (int i = 0; i < 10000; i++) {
            temperatures[i] = 30 + (i % 71); // 温度在30-100之间循环
        }
        
        long startTime = System.nanoTime();
        int[] result = solution.dailyTemperatures(temperatures);
        long endTime = System.nanoTime();
        
        // 验证结果长度
        assertEquals(10000, result.length);
        
        // 验证性能（应该在合理时间内完成）
        long duration = endTime - startTime;
        assertTrue("算法应该在1秒内完成", duration < 1_000_000_000L);
        
        System.out.printf("大输入测试完成，耗时: %.2f ms\n", duration / 1_000_000.0);
    }
}
```

### 性能对比测试
```java
public class PerformanceComparisonTest {
    
    @Test
    public void compareAlgorithms() {
        // 生成测试数据
        int[] temperatures = generateTestData(5000);
        
        // 测试单调栈解法
        long startTime = System.nanoTime();
        Solution solution1 = new Solution();
        int[] result1 = solution1.dailyTemperatures(temperatures);
        long time1 = System.nanoTime() - startTime;
        
        // 测试暴力解法
        startTime = System.nanoTime();
        SolutionBruteForce solution2 = new SolutionBruteForce();
        int[] result2 = solution2.dailyTemperatures(temperatures);
        long time2 = System.nanoTime() - startTime;
        
        // 测试逆向遍历解法
        startTime = System.nanoTime();
        SolutionReverse solution3 = new SolutionReverse();
        int[] result3 = solution3.dailyTemperatures(temperatures);
        long time3 = System.nanoTime() - startTime;
        
        // 测试桶排序解法
        startTime = System.nanoTime();
        SolutionBucket solution4 = new SolutionBucket();
        int[] result4 = solution4.dailyTemperatures(temperatures);
        long time4 = System.nanoTime() - startTime;
        
        // 验证结果一致性
        assertArrayEquals(result1, result2);
        assertArrayEquals(result1, result3);
        assertArrayEquals(result1, result4);
        
        System.out.printf("单调栈解法: %.2f ms\n", time1 / 1_000_000.0);
        System.out.printf("暴力解法: %.2f ms\n", time2 / 1_000_000.0);
        System.out.printf("逆向遍历解法: %.2f ms\n", time3 / 1_000_000.0);
        System.out.printf("桶排序解法: %.2f ms\n", time4 / 1_000_000.0);
    }
    
    private int[] generateTestData(int size) {
        Random random = new Random(42);
        int[] temperatures = new int[size];
        
        for (int i = 0; i < size; i++) {
            temperatures[i] = 30 + random.nextInt(71); // 30-100
        }
        
        return temperatures;
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 496 - 下一个更大元素 I
```java
/**
 * 在nums1中找到nums2中对应元素的下一个更大元素
 */
public class NextGreaterElementI {
    
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 构建nums2中每个元素的下一个更大元素映射
        for (int num : nums2) {
            while (!stack.isEmpty() && stack.peek() < num) {
                nextGreaterMap.put(stack.pop(), num);
            }
            stack.push(num);
        }
        
        // 构建结果
        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            result[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
        }
        
        return result;
    }
}
```

### 2. LeetCode 503 - 下一个更大元素 II（循环数组）
```java
/**
 * 循环数组中的下一个更大元素
 */
public class NextGreaterElementII {
    
    public int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 遍历两遍数组来模拟循环
        for (int i = 0; i < 2 * n; i++) {
            int num = nums[i % n];
            
            while (!stack.isEmpty() && nums[stack.peek()] < num) {
                result[stack.pop()] = num;
            }
            
            if (i < n) {
                stack.push(i);
            }
        }
        
        return result;
    }
}
```

### 3. 下一个更小元素
```java
/**
 * 找到每个元素的下一个更小元素
 */
public class NextSmallerElement {
    
    public int[] nextSmallerElement(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) {
                result[stack.pop()] = nums[i];
            }
            stack.push(i);
        }
        
        return result;
    }
}
```

### 4. 前一个更大元素
```java
/**
 * 找到每个元素的前一个更大元素
 */
public class PreviousGreaterElement {
    
    public int[] previousGreaterElement(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < n; i++) {
            // 维护单调递减栈
            while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
                stack.pop();
            }
            
            if (!stack.isEmpty()) {
                result[i] = nums[stack.peek()];
            }
            
            stack.push(i);
        }
        
        return result;
    }
}
```

### 5. 温度变化趋势分析
```java
/**
 * 分析温度变化趋势
 */
public class TemperatureTrendAnalysis {
    
    public static class TrendInfo {
        public int[] nextWarmerDays;
        public int[] nextCoolerDays;
        public int[] longestWarmStreak;
        public int[] longestCoolStreak;
        
        public TrendInfo(int size) {
            nextWarmerDays = new int[size];
            nextCoolerDays = new int[size];
            longestWarmStreak = new int[size];
            longestCoolStreak = new int[size];
        }
    }
    
    public TrendInfo analyzeTrends(int[] temperatures) {
        int n = temperatures.length;
        TrendInfo info = new TrendInfo(n);
        
        // 计算下一个更暖的日子
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && 
                   temperatures[stack.peek()] < temperatures[i]) {
                int prevIndex = stack.pop();
                info.nextWarmerDays[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        
        // 计算下一个更冷的日子
        stack.clear();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && 
                   temperatures[stack.peek()] > temperatures[i]) {
                int prevIndex = stack.pop();
                info.nextCoolerDays[prevIndex] = i - prevIndex;
            }
            stack.push(i);
        }
        
        // 计算最长升温连续天数
        for (int i = 0; i < n; i++) {
            int streak = 1;
            for (int j = i + 1; j < n && temperatures[j] > temperatures[j-1]; j++) {
                streak++;
            }
            info.longestWarmStreak[i] = streak;
        }
        
        // 计算最长降温连续天数
        for (int i = 0; i < n; i++) {
            int streak = 1;
            for (int j = i + 1; j < n && temperatures[j] < temperatures[j-1]; j++) {
                streak++;
            }
            info.longestCoolStreak[i] = streak;
        }
        
        return info;
    }
}
```

## 💡 解题技巧总结
### 1. 单调栈的核心思想
+ **维护单调性**：栈中元素保持单调递减（或递增）
+ **及时弹出**：当遇到破坏单调性的元素时，弹出并处理
+ **存储索引**：通常存储索引而不是值，便于计算距离

### 2. 单调栈的通用模板
```java
// 寻找下一个更大元素的模板
Deque<Integer> stack = new ArrayDeque<>();
for (int i = 0; i < n; i++) {
    while (!stack.isEmpty() && 
           condition(stack.peek(), i)) {
        int index = stack.pop();
        // 处理找到的配对
        result[index] = process(index, i);
    }
    stack.push(i);
}
```

### 3. 问题变形的处理技巧
+ **循环数组**：遍历两遍数组，第二遍只处理不入栈
+ **前一个元素**：从左到右遍历，栈顶就是前一个更大/小元素
+ **多种条件**：可以同时维护多个栈处理不同条件

### 4. 优化技巧
+ **跳跃查找**：利用已计算的结果进行跳跃
+ **桶排序**：当数据范围有限时，可以用桶来优化
+ **双向处理**：同时从两个方向处理可以减少时间复杂度

### 5. 复杂度分析要点
+ **均摊分析**：每个元素最多入栈出栈一次，所以是O(n)
+ **空间优化**：考虑是否可以用常数空间代替栈
+ **实际性能**：考虑缓存友好性和常数因子

这道题完美展示了单调栈在解决"下一个更大/小元素"类问题中的威力，是掌握单调栈技巧的经典例题！

