# LeetCode 84 - 柱状图中最大的矩形
## 📋 题目描述
**难度：困难**

给定 `n` 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。

### 示例
**示例 1：**

![](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)

```plain
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
```

**示例 2：**

```plain
输入：heights = [2,4]
输出：4
```

### 约束条件
+ `1 <= heights.length <= 10^5`
+ `0 <= heights[i] <= 10^4`

## 🎯 解题思路
### 核心问题分析
这是一个经典的**单调栈问题**。关键在于：

1. 对于每个柱子，我们需要找到以它为高度的最大矩形面积
2. 以某个柱子为高度的矩形，其宽度由该柱子能向左右扩展的最大距离决定
3. 扩展的边界是第一个比当前柱子矮的位置

### 单调栈解法原理
```plain
核心思想：
- 使用单调递增栈存储柱子的索引
- 当遇到比栈顶更矮的柱子时，说明栈顶柱子的右边界确定了
- 弹出栈顶，计算以该柱子为高度的最大矩形面积

关键观察：
- 对于柱子 i，如果它被弹出栈，说明：
  - 右边界：当前遍历到的位置（第一个比它矮的位置）
  - 左边界：栈中它下面的元素（左边第一个比它矮的位置）
  - 高度：heights[i]
  - 宽度：右边界 - 左边界 - 1
```

### 算法步骤
```plain
1. 维护一个单调递增栈（存储索引）
2. 遍历每个柱子：
   - 如果当前柱子高度 >= 栈顶柱子高度，入栈
   - 否则，不断弹出栈顶，计算以弹出柱子为高度的矩形面积
3. 遍历结束后，处理栈中剩余元素
4. 返回过程中计算出的最大面积
```

### 图解演示
**示例：heights = [2,1,5,6,2,3]**

```plain
初始状态：
栈: []
最大面积: 0

步骤 1: 处理 heights[0] = 2
栈: [0]
说明: 栈为空，直接入栈

步骤 2: 处理 heights[1] = 1  
当前元素 1 < 栈顶元素 heights[0] = 2
弹出索引 0，计算矩形：
- 高度: heights[0] = 2
- 右边界: 1 (当前位置)
- 左边界: -1 (栈为空)
- 宽度: 1 - (-1) - 1 = 1
- 面积: 2 × 1 = 2
栈: [1]
最大面积: 2

步骤 3: 处理 heights[2] = 5
5 > 1，直接入栈
栈: [1, 2]

步骤 4: 处理 heights[3] = 6
6 > 5，直接入栈  
栈: [1, 2, 3]

步骤 5: 处理 heights[4] = 2
2 < 6，弹出索引 3：
- 高度: 6, 右边界: 4, 左边界: 2
- 宽度: 4 - 2 - 1 = 1, 面积: 6 × 1 = 6

2 < 5，弹出索引 2：
- 高度: 5, 右边界: 4, 左边界: 1  
- 宽度: 4 - 1 - 1 = 2, 面积: 5 × 2 = 10

2 > 1，停止弹出
栈: [1, 4]
最大面积: 10

步骤 6: 处理 heights[5] = 3
3 > 2，直接入栈
栈: [1, 4, 5]

步骤 7: 处理栈中剩余元素
弹出索引 5：面积 = 3 × (6 - 4 - 1) = 3
弹出索引 4：面积 = 2 × (6 - 1 - 1) = 8  
弹出索引 1：面积 = 1 × (6 - (-1) - 1) = 6

最终最大面积: 10
```

## 💻 代码实现
### 方法一：单调栈（推荐）
```java
import java.util.*;

public class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int maxArea = 0;
        
        // 单调递增栈，存储索引
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < n; i++) {
            // 当前柱子比栈顶柱子矮，需要计算以栈顶为高度的矩形
            while (!stack.isEmpty() && heights[i] < heights[stack.peek()]) {
                int height = heights[stack.pop()]; // 弹出的柱子高度
                
                // 计算宽度
                int width;
                if (stack.isEmpty()) {
                    // 栈为空，说明左边没有更矮的柱子
                    width = i;
                } else {
                    // 宽度 = 右边界 - 左边界 - 1
                    width = i - stack.peek() - 1;
                }
                
                // 更新最大面积
                maxArea = Math.max(maxArea, height * width);
            }
            
            // 当前索引入栈
            stack.push(i);
        }
        
        // 处理栈中剩余元素
        while (!stack.isEmpty()) {
            int height = heights[stack.pop()];
            
            int width;
            if (stack.isEmpty()) {
                width = n;
            } else {
                width = n - stack.peek() - 1;
            }
            
            maxArea = Math.max(maxArea, height * width);
        }
        
        return maxArea;
    }
}
```

### 方法二：单调栈优化版（哨兵技巧）
```java
public class SolutionOptimized {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        
        // 在数组两端添加哨兵，简化边界处理
        int[] newHeights = new int[n + 2];
        newHeights[0] = 0; // 左哨兵
        newHeights[n + 1] = 0; // 右哨兵
        System.arraycopy(heights, 0, newHeights, 1, n);
        
        int maxArea = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < newHeights.length; i++) {
            while (!stack.isEmpty() && newHeights[i] < newHeights[stack.peek()]) {
                int height = newHeights[stack.pop()];
                int width = i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        
        return maxArea;
    }
}
```

### 方法三：分治法（对比参考）
```java
public class SolutionDivideConquer {
    public int largestRectangleArea(int[] heights) {
        return calculateArea(heights, 0, heights.length - 1);
    }
    
    private int calculateArea(int[] heights, int start, int end) {
        if (start > end) return 0;
        
        // 找到最小高度的索引
        int minIndex = start;
        for (int i = start; i <= end; i++) {
            if (heights[i] < heights[minIndex]) {
                minIndex = i;
            }
        }
        
        // 计算三种情况的最大面积
        int area1 = heights[minIndex] * (end - start + 1); // 跨越最小高度
        int area2 = calculateArea(heights, start, minIndex - 1); // 左半部分
        int area3 = calculateArea(heights, minIndex + 1, end); // 右半部分
        
        return Math.max(area1, Math.max(area2, area3));
    }
}
```

### 方法四：暴力解法（超时，仅供理解）
```java
public class SolutionBruteForce {
    public int largestRectangleArea(int[] heights) {
        int maxArea = 0;
        int n = heights.length;
        
        // 枚举所有可能的矩形
        for (int i = 0; i < n; i++) {
            int minHeight = heights[i];
            for (int j = i; j < n; j++) {
                minHeight = Math.min(minHeight, heights[j]);
                int width = j - i + 1;
                maxArea = Math.max(maxArea, minHeight * width);
            }
        }
        
        return maxArea;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
+ **单调栈解法**：O(n)
    - 每个元素最多入栈和出栈一次
    - 总的操作次数是 O(n)
+ **分治法**：O(n log n) 平均情况，O(n²) 最坏情况
    - 每次分治需要 O(n) 时间找最小值
    - 递归深度平均为 log n
+ **暴力解法**：O(n²)
    - 双重循环枚举所有子数组

### 空间复杂度
+ **单调栈解法**：O(n)
    - 栈的空间复杂度
+ **分治法**：O(log n)
    - 递归调用栈的深度
+ **暴力解法**：O(1)
    - 只使用常数额外空间

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的柱状图最大矩形求解
 */
public class VisualLargestRectangle {
    
    public static int largestRectangleAreaWithVisualization(int[] heights) {
        System.out.println("🏗️ 柱状图中最大的矩形");
        System.out.println("柱子高度: " + Arrays.toString(heights));
        printHistogram(heights);
        System.out.println("=" + "=".repeat(60));
        
        int n = heights.length;
        int maxArea = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        
        System.out.println("📊 使用单调栈求解:");
        
        for (int i = 0; i < n; i++) {
            System.out.printf("\n步骤 %d: 处理柱子 %d (高度 %d)\n", 
                             i + 1, i, heights[i]);
            
            // 处理需要弹出的元素
            while (!stack.isEmpty() && heights[i] < heights[stack.peek()]) {
                int heightIndex = stack.pop();
                int height = heights[heightIndex];
                
                int width;
                if (stack.isEmpty()) {
                    width = i;
                } else {
                    width = i - stack.peek() - 1;
                }
                
                int area = height * width;
                maxArea = Math.max(maxArea, area);
                
                System.out.printf("  ✅ 弹出柱子 %d (高度 %d)\n", heightIndex, height);
                System.out.printf("     左边界: %s, 右边界: %d\n", 
                                 stack.isEmpty() ? "起始" : String.valueOf(stack.peek()), i);
                System.out.printf("     宽度: %d, 面积: %d × %d = %d\n", 
                                 width, height, width, area);
                System.out.printf("     当前最大面积: %d\n", maxArea);
            }
            
            stack.push(i);
            System.out.printf("  📥 柱子 %d 入栈\n", i);
            printStackState(stack, heights);
        }
        
        // 处理栈中剩余元素
        System.out.println("\n🔚 处理栈中剩余柱子:");
        while (!stack.isEmpty()) {
            int heightIndex = stack.pop();
            int height = heights[heightIndex];
            
            int width;
            if (stack.isEmpty()) {
                width = n;
            } else {
                width = n - stack.peek() - 1;
            }
            
            int area = height * width;
            maxArea = Math.max(maxArea, area);
            
            System.out.printf("  ✅ 弹出柱子 %d (高度 %d)\n", heightIndex, height);
            System.out.printf("     左边界: %s, 右边界: 末尾\n", 
                             stack.isEmpty() ? "起始" : String.valueOf(stack.peek()));
            System.out.printf("     宽度: %d, 面积: %d × %d = %d\n", 
                             width, height, width, area);
            System.out.printf("     当前最大面积: %d\n", maxArea);
        }
        
        System.out.println("\n🏆 最大矩形面积: " + maxArea);
        return maxArea;
    }
    
    private static void printStackState(Deque<Integer> stack, int[] heights) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                int index = stackList.get(i);
                System.out.printf("%d(h=%d)", index, heights[index]);
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    private static void printHistogram(int[] heights) {
        int maxHeight = Arrays.stream(heights).max().orElse(0);
        
        System.out.println("\n柱状图可视化:");
        for (int level = maxHeight; level > 0; level--) {
            System.out.printf("%2d |", level);
            for (int height : heights) {
                if (height >= level) {
                    System.out.print(" ██");
                } else {
                    System.out.print("   ");
                }
            }
            System.out.println();
        }
        
        System.out.print("   +");
        for (int i = 0; i < heights.length; i++) {
            System.out.print("---");
        }
        System.out.println();
        
        System.out.print("    ");
        for (int i = 0; i < heights.length; i++) {
            System.out.printf("%2d ", i);
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        // 测试示例
        int[] heights1 = {2, 1, 5, 6, 2, 3};
        largestRectangleAreaWithVisualization(heights1);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        int[] heights2 = {2, 4};
        largestRectangleAreaWithVisualization(heights2);
    }
}
```

### 运行结果示例
```plain
🏗️ 柱状图中最大的矩形
柱子高度: [2, 1, 5, 6, 2, 3]

柱状图可视化:
 6 |      ██      
 5 |      ██      
 4 |      ██      
 3 |      ██      ██
 2 | ██   ██   ██ ██
 1 | ██ ██ ██ ██ ██ ██
   +------------------
     0  1  2  3  4  5 
============================================================

📊 使用单调栈求解:

步骤 1: 处理柱子 0 (高度 2)
  📥 柱子 0 入栈
  栈状态: [0(h=2)] (底 -> 顶)

步骤 2: 处理柱子 1 (高度 1)
  ✅ 弹出柱子 0 (高度 2)
     左边界: 起始, 右边界: 1
     宽度: 1, 面积: 2 × 1 = 2
     当前最大面积: 2
  📥 柱子 1 入栈
  栈状态: [1(h=1)] (底 -> 顶)

步骤 3: 处理柱子 2 (高度 5)
  📥 柱子 2 入栈
  栈状态: [1(h=1), 2(h=5)] (底 -> 顶)

步骤 4: 处理柱子 3 (高度 6)
  📥 柱子 3 入栈
  栈状态: [1(h=1), 2(h=5), 3(h=6)] (底 -> 顶)

步骤 5: 处理柱子 4 (高度 2)
  ✅ 弹出柱子 3 (高度 6)
     左边界: 2, 右边界: 4
     宽度: 1, 面积: 6 × 1 = 6
     当前最大面积: 6
  ✅ 弹出柱子 2 (高度 5)
     左边界: 1, 右边界: 4
     宽度: 2, 面积: 5 × 2 = 10
     当前最大面积: 10
  📥 柱子 4 入栈
  栈状态: [1(h=1), 4(h=2)] (底 -> 顶)

步骤 6: 处理柱子 5 (高度 3)
  📥 柱子 5 入栈
  栈状态: [1(h=1), 4(h=2), 5(h=3)] (底 -> 顶)

🔚 处理栈中剩余柱子:
  ✅ 弹出柱子 5 (高度 3)
     左边界: 4, 右边界: 末尾
     宽度: 1, 面积: 3 × 1 = 3
     当前最大面积: 10
  ✅ 弹出柱子 4 (高度 2)
     左边界: 1, 右边界: 末尾
     宽度: 4, 面积: 2 × 4 = 8
     当前最大面积: 10
  ✅ 弹出柱子 1 (高度 1)
     左边界: 起始, 右边界: 末尾
     宽度: 6, 面积: 1 × 6 = 6
     当前最大面积: 10

🏆 最大矩形面积: 10
```

## 🧪 测试用例
### 基础功能测试
```java
public class LargestRectangleTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 示例 1
        int[] heights = {2, 1, 5, 6, 2, 3};
        assertEquals(10, solution.largestRectangleArea(heights));
        
        // 示例 2
        heights = new int[]{2, 4};
        assertEquals(4, solution.largestRectangleArea(heights));
    }
    
    @Test
    public void testEdgeCases() {
        // 单个柱子
        int[] heights = {5};
        assertEquals(5, solution.largestRectangleArea(heights));
        
        // 递增序列
        heights = new int[]{1, 2, 3, 4, 5};
        assertEquals(9, solution.largestRectangleArea(heights)); // 3×3
        
        // 递减序列
        heights = new int[]{5, 4, 3, 2, 1};
        assertEquals(9, solution.largestRectangleArea(heights)); // 3×3
        
        // 相同高度
        heights = new int[]{3, 3, 3, 3};
        assertEquals(12, solution.largestRectangleArea(heights)); // 3×4
        
        // 包含0
        heights = new int[]{2, 0, 2};
        assertEquals(2, solution.largestRectangleArea(heights));
    }
    
    @Test
    public void testComplexCases() {
        // 复杂情况1
        int[] heights = {6, 7, 5, 2, 4, 5, 9, 3};
        assertEquals(16, solution.largestRectangleArea(heights));
        
        // 复杂情况2
        heights = new int[]{1, 1, 1, 1, 1};
        assertEquals(5, solution.largestRectangleArea(heights));
        
        // 山峰形状
        heights = new int[]{1, 2, 3, 4, 3, 2, 1};
        assertEquals(10, solution.largestRectangleArea(heights));
    }
}
```

### 性能对比测试
```java
public class PerformanceTest {
    
    @Test
    public void compareAlgorithms() {
        // 生成测试数据
        Random random = new Random(42);
        int[] heights = new int[10000];
        for (int i = 0; i < heights.length; i++) {
            heights[i] = random.nextInt(1000) + 1;
        }
        
        // 测试单调栈解法
        long startTime = System.nanoTime();
        Solution solution = new Solution();
        int result1 = solution.largestRectangleArea(heights);
        long time1 = System.nanoTime() - startTime;
        
        // 测试分治法
        startTime = System.nanoTime();
        SolutionDivideConquer dcSolution = new SolutionDivideConquer();
        int result2 = dcSolution.largestRectangleArea(heights);
        long time2 = System.nanoTime() - startTime;
        
        // 验证结果一致性
        assertEquals(result1, result2);
        
        System.out.printf("单调栈解法: %.2f ms, 结果: %d\n", 
                         time1 / 1_000_000.0, result1);
        System.out.printf("分治法: %.2f ms, 结果: %d\n", 
                         time2 / 1_000_000.0, result2);
        System.out.printf("性能提升: %.2fx\n", (double) time2 / time1);
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 85 - 最大矩形（二维扩展）
```java
/**
 * 在二进制矩阵中找最大矩形
 */
public class MaximalRectangle {
    
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0) return 0;
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            // 更新每列的高度
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    heights[j]++;
                } else {
                    heights[j] = 0;
                }
            }
            
            // 计算当前行的最大矩形面积
            maxArea = Math.max(maxArea, largestRectangleArea(heights));
        }
        
        return maxArea;
    }
    
    private int largestRectangleArea(int[] heights) {
        // 使用前面实现的单调栈算法
        int n = heights.length;
        int maxArea = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && heights[i] < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        
        while (!stack.isEmpty()) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? n : n - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        
        return maxArea;
    }
}
```

### 2. 接雨水问题的关联
```java
/**
 * LeetCode 42 - 接雨水
 * 与柱状图最大矩形有相似的单调栈思路
 */
public class TrappingRainWater {
    
    public int trap(int[] height) {
        int water = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < height.length; i++) {
            while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
                int bottom = stack.pop();
                
                if (stack.isEmpty()) break;
                
                int left = stack.peek();
                int width = i - left - 1;
                int h = Math.min(height[left], height[i]) - height[bottom];
                
                water += width * h;
            }
            
            stack.push(i);
        }
        
        return water;
    }
}
```

### 3. 最大正方形
```java
/**
 * LeetCode 221 - 最大正方形
 * 动态规划解法，与矩形问题相关
 */
public class MaximalSquare {
    
    public int maximalSquare(char[][] matrix) {
        if (matrix.length == 0) return 0;
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[][] dp = new int[rows + 1][cols + 1];
        int maxSide = 0;
        
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= cols; j++) {
                if (matrix[i-1][j-1] == '1') {
                    dp[i][j] = Math.min(Math.min(dp[i-1][j], dp[i][j-1]), 
                                       dp[i-1][j-1]) + 1;
                    maxSide = Math.max(maxSide, dp[i][j]);
                }
            }
        }
        
        return maxSide * maxSide;
    }
}
```

## 💡 解题技巧总结
### 1. 单调栈的核心思想
+ **维护单调性**：栈中索引对应的高度单调递增
+ **及时计算**：当单调性被破坏时，计算矩形面积
+ **边界处理**：左边界是栈中下一个元素，右边界是当前位置

### 2. 面积计算公式
```plain
对于被弹出的柱子 i：
- 高度：heights[i]
- 右边界：当前遍历位置 j
- 左边界：栈中 i 下面的元素位置 k（如果栈为空则为 -1）
- 宽度：j - k - 1
- 面积：heights[i] × (j - k - 1)
```

### 3. 优化技巧
+ **哨兵技巧**：在数组两端添加高度为0的哨兵，简化边界处理
+ **索引存储**：栈中存储索引而不是值，便于计算宽度
+ **及时更新**：每次计算后立即更新最大面积

### 4. 时间复杂度分析
+ **均摊 O(n)**：每个元素最多入栈出栈一次
+ **空间复杂度 O(n)**：栈的空间

### 5. 问题扩展思路
+ **二维扩展**：将二维问题转化为多个一维问题
+ **相关问题**：接雨水、最大正方形等都有类似的思路
+ **状态转移**：理解单调栈如何维护有用信息

这道题是单调栈应用的经典例题，掌握了这个模板，就能解决很多类似的几何优化问题！

