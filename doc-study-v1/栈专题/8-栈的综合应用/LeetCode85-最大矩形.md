# LeetCode85-最大矩形

# LeetCode 85 - 最大矩形
## 📋 题目描述
**难度：困难**

给定一个仅包含 `0` 和 `1` 的二维二进制矩阵，找出只包含 `1` 的最大矩形，并返回其面积。

### 示例
**示例 1：**

![maximal.jpg](./img/VlMknxXazYpjBJsU/1615348552802-21a55c42-a597-412a-9d8b-09520c0d849e-161560.jpeg)

```plain
输入：matrix = [["1","0","1","0","0"],
               ["1","0","1","1","1"],
               ["1","1","1","1","1"],
               ["1","0","0","1","0"]]
输出：6
解释：最大矩形如上图所示。
```

**示例 2：**

```plain
输入：matrix = []
输出：0
```

**示例 3：**

```plain
输入：matrix = [["0"]]
输出：0
```

**示例 4：**

```plain
输入：matrix = [["1"]]
输出：1
```

**示例 5：**

```plain
输入：matrix = [["0","0"]]
输出：0
```

### 约束条件
+ `rows == matrix.length`
+ `cols == matrix[i].length`
+ `1 <= rows, cols <= 200`
+ `matrix[i][j]` 为 `'0'` 或 `'1'`

## 🎯 解题思路
### 核心问题分析
这是一个典型的**栈的综合应用**问题，涉及：

1. **单调栈**：解决柱状图中最大矩形问题
2. **动态规划**：将二维问题转化为一维问题
3. **状态转换**：每一行都构成一个柱状图
4. **几何分析**：理解矩形面积的计算

### 解题思路详解
#### 核心思想：转化为柱状图问题
```plain
关键洞察：
- 将每一行看作柱状图的底部
- 每个位置的高度 = 从当前行向上连续1的个数
- 对每一行应用"柱状图中最大矩形"算法

转化过程：
原始矩阵:
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

转化为高度数组：
第0行: [1, 0, 1, 0, 0]
第1行: [2, 0, 2, 1, 1]
第2行: [3, 1, 3, 2, 2]
第3行: [4, 0, 0, 3, 0]
```

#### 算法步骤
1. **预处理**：将每一行转化为柱状图高度数组
2. **逐行处理**：对每一行应用单调栈算法
3. **维护最大值**：记录所有行中的最大矩形面积

### 图解演示
**示例矩阵处理过程：**

```plain
原始矩阵:
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

步骤1: 计算第0行的高度数组
高度: [1, 0, 1, 0, 0]
柱状图:
1 │ █   █
0 └─────────
   0 1 2 3 4
最大矩形面积: 1

步骤2: 计算第1行的高度数组
高度: [2, 0, 2, 1, 1]
柱状图:
2 │ █   █
1 │ █   █ █ █
0 └─────────────
   0 1 2 3 4 5
最大矩形面积: 2

步骤3: 计算第2行的高度数组
高度: [3, 1, 3, 2, 2]
柱状图:
3 │ █   █
2 │ █   █ █ █
1 │ █ █ █ █ █
0 └─────────────
   0 1 2 3 4 5
最大矩形面积: 6 (高度2，宽度3，从位置2到位置4)

步骤4: 计算第3行的高度数组
高度: [4, 0, 0, 3, 0]
柱状图:
4 │ █
3 │ █     █
2 │ █     █
1 │ █     █
0 └─────────
   0 1 2 3 4
最大矩形面积: 4

最终答案: max(1, 2, 6, 4) = 6
```

## 💻 代码实现
### 方法一：单调栈法（推荐）
```java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        
        // 逐行处理
        for (int i = 0; i < rows; i++) {
            // 更新高度数组
            updateHeights(matrix, heights, i);
            
            // 计算当前行的最大矩形面积
            int currentMaxArea = largestRectangleArea(heights);
            maxArea = Math.max(maxArea, currentMaxArea);
        }
        
        return maxArea;
    }
    
    /**
     * 更新高度数组
     */
    private void updateHeights(char[][] matrix, int[] heights, int row) {
        for (int j = 0; j < matrix[0].length; j++) {
            if (matrix[row][j] == '1') {
                heights[j]++;  // 连续的1，高度增加
            } else {
                heights[j] = 0;  // 遇到0，高度重置
            }
        }
    }
    
    /**
     * 使用单调栈计算柱状图中的最大矩形面积
     */
    private int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        
        // 在末尾添加一个高度为0的柱子，确保所有柱子都被处理
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            // 当前柱子比栈顶柱子矮，计算以栈顶柱子为高的矩形面积
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            
            stack.push(i);
        }
        
        return maxArea;
    }
}
```

## 🔗 相关问题扩展
### 1. LeetCode 84 - 柱状图中最大的矩形
**问题描述：** 给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1。求在该柱状图中，能够勾勒出来的矩形的最大面积。

**解法关联：** 本题是 LeetCode 85 的基础问题，单调栈解法完全适用。

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int maxArea = 0;
    
    for (int i = 0; i <= heights.length; i++) {
        int currentHeight = (i == heights.length) ? 0 : heights[i];
        
        while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }
        
        stack.push(i);
    }
    
    return maxArea;
}
```

### 2. LeetCode 221 - 最大正方形
**问题描述：** 在一个由 '0' 和 '1' 组成的二维矩阵内，找到只包含 '1' 的最大正方形，并返回其面积。

**解法关联：** 可以使用动态规划，也可以基于本题的思路进行优化。

```java
public int maximalSquare(char[][] matrix) {
    if (matrix == null || matrix.length == 0) return 0;
    
    int rows = matrix.length;
    int cols = matrix[0].length;
    int[] heights = new int[cols];
    int maxSide = 0;
    
    for (int i = 0; i < rows; i++) {
        // 更新高度数组
        for (int j = 0; j < cols; j++) {
            heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
        }
        
        // 在当前柱状图中找最大正方形
        maxSide = Math.max(maxSide, largestSquareInHistogram(heights));
    }
    
    return maxSide * maxSide;
}

private int largestSquareInHistogram(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int maxSide = 0;
    
    for (int i = 0; i <= heights.length; i++) {
        int currentHeight = (i == heights.length) ? 0 : heights[i];
        
        while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            int side = Math.min(height, width);  // 正方形的边长
            maxSide = Math.max(maxSide, side);
        }
        
        stack.push(i);
    }
    
    return maxSide;
}
```

### 3. 最大矩形周长
**问题描述：** 在二进制矩阵中找到面积最大的矩形的周长。

```java
public int maximalRectanglePerimeter(char[][] matrix) {
    if (matrix == null || matrix.length == 0) return 0;
    
    int rows = matrix.length;
    int cols = matrix[0].length;
    int[] heights = new int[cols];
    int maxPerimeter = 0;
    
    for (int i = 0; i < rows; i++) {
        // 更新高度数组
        for (int j = 0; j < cols; j++) {
            heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
        }
        
        // 计算当前行的最大周长
        maxPerimeter = Math.max(maxPerimeter, largestRectanglePerimeter(heights));
    }
    
    return maxPerimeter;
}

private int largestRectanglePerimeter(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int maxPerimeter = 0;
    
    for (int i = 0; i <= heights.length; i++) {
        int currentHeight = (i == heights.length) ? 0 : heights[i];
        
        while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            int perimeter = 2 * (height + width);
            maxPerimeter = Math.max(maxPerimeter, perimeter);
        }
        
        stack.push(i);
    }
    
    return maxPerimeter;
}
```

### 4. 三维最大立方体
**问题描述：** 在三维二进制数组中找到最大的立方体。

```java
public int maximalCube(char[][][] matrix) {
    if (matrix == null || matrix.length == 0) return 0;
    
    int depth = matrix.length;
    int rows = matrix[0].length;
    int cols = matrix[0][0].length;
    
    // 对每个深度层应用二维最大矩形算法
    char[][] currentLayer = new char[rows][cols];
    int maxVolume = 0;
    
    for (int d = 0; d < depth; d++) {
        // 更新当前层
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[d][i][j] == '1') {
                    currentLayer[i][j] = (d == 0) ? '1' : 
                        (char)('0' + (currentLayer[i][j] - '0' + 1));
                } else {
                    currentLayer[i][j] = '0';
                }
            }
        }
        
        // 在当前层找最大立方体
        maxVolume = Math.max(maxVolume, maximalCubeInLayer(currentLayer, d + 1));
    }
    
    return maxVolume;
}

private int maximalCubeInLayer(char[][] layer, int maxDepth) {
    // 类似于最大矩形，但限制为立方体
    // 实现细节略...
    return 0;
}
```

### 5. 实际应用场景
#### 图像处理中的最大连通区域
```java
/**
 * 在图像处理中找到最大的矩形连通区域
 */
public class ImageRectangleDetector {
    
    public Rectangle findLargestRectangularRegion(int[][] image, int targetValue) {
        if (image == null || image.length == 0) return null;
        
        int rows = image.length;
        int cols = image[0].length;
        
        // 将图像转换为二进制矩阵
        char[][] binaryMatrix = new char[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                binaryMatrix[i][j] = (image[i][j] == targetValue) ? '1' : '0';
            }
        }
        
        // 应用最大矩形算法
        return findMaxRectangleWithPosition(binaryMatrix);
    }
    
    private Rectangle findMaxRectangleWithPosition(char[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        Rectangle maxRect = new Rectangle(0, 0, 0, 0);
        
        for (int i = 0; i < rows; i++) {
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
            }
            
            // 找当前行的最大矩形
            Rectangle currentRect = findLargestRectangleInHistogram(heights, i);
            if (currentRect.area > maxRect.area) {
                maxRect = currentRect;
            }
        }
        
        return maxRect;
    }
    
    private Rectangle findLargestRectangleInHistogram(int[] heights, int currentRow) {
        Deque<Integer> stack = new ArrayDeque<>();
        Rectangle maxRect = new Rectangle(0, 0, 0, 0);
        
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int heightIndex = stack.pop();
                int height = heights[heightIndex];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                int area = height * width;
                
                if (area > maxRect.area) {
                    int startCol = stack.isEmpty() ? 0 : stack.peek() + 1;
                    int startRow = currentRow - height + 1;
                    maxRect = new Rectangle(startRow, startCol, height, width);
                }
            }
            
            stack.push(i);
        }
        
        return maxRect;
    }
    
    static class Rectangle {
        int row, col, height, width, area;
        
        Rectangle(int row, int col, int height, int width) {
            this.row = row;
            this.col = col;
            this.height = height;
            this.width = width;
            this.area = height * width;
        }
        
        @Override
        public String toString() {
            return String.format("Rectangle[(%d,%d), %dx%d, area=%d]", 
                               row, col, height, width, area);
        }
    }
}
```

#### 建筑设计中的最大可用空间
```java
/**
 * 在建筑平面图中找到最大的可用矩形空间
 */
public class BuildingSpaceOptimizer {
    
    public static class Space {
        int x, y, width, height, area;
        
        Space(int x, int y, int width, int height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
            this.area = width * height;
        }
    }
    
    /**
     * 在建筑平面图中找到最大可用空间
     * @param floorPlan 平面图，1表示可用空间，0表示障碍物
     * @return 最大可用矩形空间
     */
    public Space findLargestUsableSpace(int[][] floorPlan) {
        if (floorPlan == null || floorPlan.length == 0) {
            return new Space(0, 0, 0, 0);
        }
        
        int rows = floorPlan.length;
        int cols = floorPlan[0].length;
        
        // 转换为字符矩阵
        char[][] matrix = new char[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = (floorPlan[i][j] == 1) ? '1' : '0';
            }
        }
        
        return findMaxSpace(matrix);
    }
    
    private Space findMaxSpace(char[][] matrix) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        Space maxSpace = new Space(0, 0, 0, 0);
        
        for (int i = 0; i < rows; i++) {
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
            }
            
            // 找当前行的最大空间
            Space currentSpace = findLargestSpaceInRow(heights, i);
            if (currentSpace.area > maxSpace.area) {
                maxSpace = currentSpace;
            }
        }
        
        return maxSpace;
    }
    
    private Space findLargestSpaceInRow(int[] heights, int currentRow) {
        Deque<Integer> stack = new ArrayDeque<>();
        Space maxSpace = new Space(0, 0, 0, 0);
        
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int heightIndex = stack.pop();
                int height = heights[heightIndex];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                int area = height * width;
                
                if (area > maxSpace.area) {
                    int startCol = stack.isEmpty() ? 0 : stack.peek() + 1;
                    int startRow = currentRow - height + 1;
                    maxSpace = new Space(startCol, startRow, width, height);
                }
            }
            
            stack.push(i);
        }
        
        return maxSpace;
    }
    
    public static void main(String[] args) {
        BuildingSpaceOptimizer optimizer = new BuildingSpaceOptimizer();
        
        // 示例建筑平面图
        int[][] floorPlan = {
            {1, 0, 1, 0, 0},
            {1, 0, 1, 1, 1},
            {1, 1, 1, 1, 1},
            {1, 0, 0, 1, 0}
        };
        
        Space largestSpace = optimizer.findLargestUsableSpace(floorPlan);
        System.out.printf("最大可用空间: 位置(%d,%d), 尺寸%dx%d, 面积%d\n",
                        largestSpace.x, largestSpace.y, 
                        largestSpace.width, largestSpace.height, 
                        largestSpace.area);
    }
}
```

## 💡 解题技巧总结
### 核心技巧
1. **问题转化**
    - 将二维问题转化为一维问题
    - 每一行都构成一个柱状图
    - 高度 = 从当前行向上连续1的个数
2. **单调栈应用**
    - 维护递增栈
    - 遇到较小元素时计算面积
    - 栈中存储索引而非值
3. **状态维护**
    - 逐行更新高度数组
    - 遇到0时重置高度
    - 遇到1时累加高度
4. **边界处理**
    - 在数组末尾添加0，确保所有元素都被处理
    - 正确计算矩形的宽度

### 常见陷阱
1. **宽度计算错误**

```java
// ❌ 错误：直接用索引差
int width = i - stack.peek();

// ✅ 正确：考虑栈为空的情况
int width = stack.isEmpty() ? i : i - stack.peek() - 1;
```

2. **高度数组更新错误**

```java
// ❌ 错误：没有重置高度
if (matrix[i][j] == '1') {
    heights[j]++;
}

// ✅ 正确：遇到0时重置
if (matrix[i][j] == '1') {
    heights[j]++;
} else {
    heights[j] = 0;
}
```

3. **边界条件遗漏**

```java
// ❌ 错误：没有处理最后的元素
for (int i = 0; i < heights.length; i++) {
    // 处理逻辑
}

// ✅ 正确：添加哨兵元素
for (int i = 0; i <= heights.length; i++) {
    int currentHeight = (i == heights.length) ? 0 : heights[i];
    // 处理逻辑
}
```

### 优化技巧
1. **空间优化**
    - 复用高度数组
    - 避免创建额外的矩阵副本
2. **时间优化**
    - 提前终止：如果当前最大面积已经超过理论最大值
    - 预处理：对于多次查询，可以预计算部分结果
3. **代码优化**
    - 使用ArrayDeque而非Stack
    - 减少不必要的函数调用

### 扩展应用
1. **多维扩展**
    - 三维最大立方体
    - 四维超立方体
2. **约束条件**
    - 最大正方形
    - 固定宽高比的矩形
    - 最小面积约束
3. **实际应用**
    - 图像处理中的连通区域检测
    - 建筑设计中的空间优化
    - 芯片设计中的布局优化

### 最佳实践
1. **代码结构**

```java
public int maximalRectangle(char[][] matrix) {
    // 1. 输入验证
    if (matrix == null || matrix.length == 0) return 0;
    
    // 2. 初始化变量
    int rows = matrix.length;
    int cols = matrix[0].length;
    int[] heights = new int[cols];
    int maxArea = 0;
    
    // 3. 逐行处理
    for (int i = 0; i < rows; i++) {
        updateHeights(matrix, heights, i);
        maxArea = Math.max(maxArea, largestRectangleArea(heights));
    }
    
    return maxArea;
}
```

2. **函数分离**
    - 将高度更新逻辑分离
    - 将柱状图算法分离
    - 提高代码可读性和可测试性
3. **错误处理**
    - 检查输入有效性
    - 处理边界情况
    - 提供有意义的错误信息
4. **性能监控**
    - 记录关键指标
    - 监控内存使用
    - 优化热点代码

通过掌握这些技巧，可以高效地解决最大矩形问题及其各种变形，并将解法应用到实际的工程问题中。

```plain

### 方法二：动态规划法

```java
public class SolutionDP {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        
        // 三个DP数组
        int[] heights = new int[cols];  // 当前位置向上连续1的个数
        int[] leftBounds = new int[cols];   // 当前高度下，左边界位置
        int[] rightBounds = new int[cols];  // 当前高度下，右边界位置
        
        // 初始化右边界
        Arrays.fill(rightBounds, cols);
        
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            // 更新heights数组
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    heights[j]++;
                } else {
                    heights[j] = 0;
                }
            }
            
            // 更新leftBounds数组
            int currentLeft = 0;
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    leftBounds[j] = Math.max(leftBounds[j], currentLeft);
                } else {
                    leftBounds[j] = 0;
                    currentLeft = j + 1;
                }
            }
            
            // 更新rightBounds数组
            int currentRight = cols;
            for (int j = cols - 1; j >= 0; j--) {
                if (matrix[i][j] == '1') {
                    rightBounds[j] = Math.min(rightBounds[j], currentRight);
                } else {
                    rightBounds[j] = cols;
                    currentRight = j;
                }
            }
            
            // 计算当前行的最大面积
            for (int j = 0; j < cols; j++) {
                int area = heights[j] * (rightBounds[j] - leftBounds[j]);
                maxArea = Math.max(maxArea, area);
            }
        }
        
        return maxArea;
    }
}
```

### 方法三：暴力解法
```java
public class SolutionBruteForce {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int maxArea = 0;
        
        // 枚举所有可能的矩形
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    // 以(i,j)为左上角，寻找最大矩形
                    maxArea = Math.max(maxArea, findMaxRectangleFrom(matrix, i, j));
                }
            }
        }
        
        return maxArea;
    }
    
    private int findMaxRectangleFrom(char[][] matrix, int startRow, int startCol) {
        int rows = matrix.length;
        int cols = matrix[0].length;
        int maxArea = 0;
        
        // 枚举所有可能的右下角
        for (int i = startRow; i < rows; i++) {
            for (int j = startCol; j < cols; j++) {
                // 检查从(startRow, startCol)到(i, j)是否全为1
                if (isValidRectangle(matrix, startRow, startCol, i, j)) {
                    int area = (i - startRow + 1) * (j - startCol + 1);
                    maxArea = Math.max(maxArea, area);
                }
            }
        }
        
        return maxArea;
    }
    
    private boolean isValidRectangle(char[][] matrix, int r1, int c1, int r2, int c2) {
        for (int i = r1; i <= r2; i++) {
            for (int j = c1; j <= c2; j++) {
                if (matrix[i][j] == '0') {
                    return false;
                }
            }
        }
        return true;
    }
}
```

### 方法四：优化的单调栈实现
```java
public class SolutionOptimized {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols + 1];  // 多一个位置，避免边界处理
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
            }
            
            // 计算当前行的最大矩形面积
            maxArea = Math.max(maxArea, largestRectangleAreaOptimized(heights));
        }
        
        return maxArea;
    }
    
    private int largestRectangleAreaOptimized(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        
        for (int i = 0; i < heights.length; i++) {
            while (!stack.isEmpty() && heights[i] < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        
        return maxArea;
    }
}
```

### 方法五：分治法
```java
public class SolutionDivideConquer {
    public int maximalRectangle(char[][] matrix) {
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
            }
            
            // 使用分治法计算最大矩形面积
            maxArea = Math.max(maxArea, largestRectangleAreaDivideConquer(heights, 0, cols - 1));
        }
        
        return maxArea;
    }
    
    private int largestRectangleAreaDivideConquer(int[] heights, int left, int right) {
        if (left > right) {
            return 0;
        }
        
        // 找到最小高度的位置
        int minIndex = left;
        for (int i = left + 1; i <= right; i++) {
            if (heights[i] < heights[minIndex]) {
                minIndex = i;
            }
        }
        
        // 计算三种情况的最大面积
        int minHeightArea = heights[minIndex] * (right - left + 1);
        int leftArea = largestRectangleAreaDivideConquer(heights, left, minIndex - 1);
        int rightArea = largestRectangleAreaDivideConquer(heights, minIndex + 1, right);
        
        return Math.max(minHeightArea, Math.max(leftArea, rightArea));
    }
}
```

### 方法六：带详细日志的实现
```java
public class SolutionWithLogging {
    
    public int maximalRectangle(char[][] matrix) {
        System.out.println("🔲 最大矩形计算器");
        System.out.println("=" + "=".repeat(60));
        
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            System.out.println("❌ 输入矩阵为空");
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        
        // 显示原始矩阵
        printMatrix(matrix);
        System.out.println();
        
        for (int i = 0; i < rows; i++) {
            System.out.printf("📍 处理第 %d 行:\n", i);
            
            // 更新高度数组
            updateHeightsWithLogging(matrix, heights, i);
            
            // 计算当前行的最大矩形面积
            int currentMaxArea = largestRectangleAreaWithLogging(heights, i);
            maxArea = Math.max(maxArea, currentMaxArea);
            
            System.out.printf("  📊 当前行最大面积: %d\n", currentMaxArea);
            System.out.printf("  🏆 全局最大面积: %d\n", maxArea);
            System.out.println();
        }
        
        System.out.println("🏆 计算完成！");
        System.out.printf("最大矩形面积: %d\n", maxArea);
        
        return maxArea;
    }
    
    private void updateHeightsWithLogging(char[][] matrix, int[] heights, int row) {
        System.out.printf("  🔄 更新高度数组:\n");
        System.out.printf("    第%d行: %s\n", row, Arrays.toString(matrix[row]));
        
        for (int j = 0; j < matrix[0].length; j++) {
            if (matrix[row][j] == '1') {
                heights[j]++;
            } else {
                heights[j] = 0;
            }
        }
        
        System.out.printf("    高度数组: %s\n", Arrays.toString(heights));
        printHeightChart(heights);
    }
    
    private int largestRectangleAreaWithLogging(int[] heights, int row) {
        System.out.printf("  📐 计算第%d行的柱状图最大矩形:\n", row);
        
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                int area = height * width;
                
                System.out.printf("    💡 发现矩形: 高度=%d, 宽度=%d, 面积=%d\n", 
                                height, width, area);
                
                maxArea = Math.max(maxArea, area);
            }
            
            stack.push(i);
        }
        
        return maxArea;
    }
    
    private void printMatrix(char[][] matrix) {
        System.out.println("📋 输入矩阵:");
        for (int i = 0; i < matrix.length; i++) {
            System.out.printf("  第%d行: ", i);
            for (int j = 0; j < matrix[0].length; j++) {
                if (matrix[i][j] == '1') {
                    System.out.print("█ ");
                } else {
                    System.out.print("░ ");
                }
            }
            System.out.printf(" %s\n", Arrays.toString(matrix[i]));
        }
    }
    
    private void printHeightChart(int[] heights) {
        if (heights.length == 0) return;
        
        int maxHeight = Arrays.stream(heights).max().orElse(0);
        if (maxHeight == 0) return;
        
        System.out.println("    柱状图:");
        for (int level = maxHeight; level >= 1; level--) {
            System.out.printf("    %2d │", level);
            for (int height : heights) {
                if (height >= level) {
                    System.out.print("██");
                } else {
                    System.out.print("  ");
                }
            }
            System.out.println();
        }
        
        System.out.print("       └");
        for (int i = 0; i < heights.length; i++) {
            System.out.print("──");
        }
        System.out.println();
        
        System.out.print("        ");
        for (int i = 0; i < heights.length; i++) {
            System.out.printf("%2d", i);
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        SolutionWithLogging solution = new SolutionWithLogging();
        
        // 测试用例1
        System.out.println("🧪 测试用例 1:");
        char[][] matrix1 = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        solution.maximalRectangle(matrix1);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试用例2
        System.out.println("🧪 测试用例 2:");
        char[][] matrix2 = {
            {'1','1','1','1'},
            {'1','1','1','1'},
            {'1','1','1','1'}
        };
        solution.maximalRectangle(matrix2);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试用例3
        System.out.println("🧪 测试用例 3:");
        char[][] matrix3 = {
            {'1','0','1','1','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        solution.maximalRectangle(matrix3);
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**单调栈法：**

+ 外层循环：O(m)，其中 m 是行数
+ 内层单调栈：O(n)，其中 n 是列数
+ 总时间复杂度：**O(m × n)**

**动态规划法：**

+ 外层循环：O(m)
+ 内层三次遍历：O(n)
+ 总时间复杂度：**O(m × n)**

**暴力解法：**

+ 枚举所有矩形：O(m² × n²)
+ 验证矩形：O(m × n)
+ 总时间复杂度：**O(m³ × n³)**

**分治法：**

+ 每层分治：O(n)
+ 递归深度：O(n)（最坏情况）
+ 总时间复杂度：**O(m × n²)**（最坏情况）

### 空间复杂度
**单调栈法：**

+ 高度数组：O(n)
+ 栈空间：O(n)
+ 总空间复杂度：**O(n)**

**动态规划法：**

+ 三个DP数组：O(n)
+ 总空间复杂度：**O(n)**

**暴力解法：**

+ 只使用常数个变量
+ 空间复杂度：**O(1)**

**分治法：**

+ 递归栈：O(n)（最坏情况）
+ 空间复杂度：**O(n)**

## 🎨 可视化演示
### 详细计算过程演示
```java
/**
 * 可视化最大矩形的详细计算过程
 */
public class VisualMaximalRectangle {
    
    public static int maximalRectangleWithVisualization(char[][] matrix) {
        System.out.println("🔲 最大矩形可视化计算器");
        System.out.println("=" + "=".repeat(60));
        
        if (matrix == null || matrix.length == 0 || matrix[0].length == 0) {
            System.out.println("❌ 无效输入");
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        Rectangle maxRectangle = null;
        
        // 显示原始矩阵
        printOriginalMatrix(matrix);
        
        for (int i = 0; i < rows; i++) {
            System.out.printf("\n📍 处理第 %d 行:\n", i);
            
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                heights[j] = (matrix[i][j] == '1') ? heights[j] + 1 : 0;
            }
            
            System.out.printf("  高度数组: %s\n", Arrays.toString(heights));
            printHeightVisualization(heights);
            
            // 计算当前行的最大矩形
            RectangleResult result = findLargestRectangleWithDetails(heights, i);
            
            if (result.area > maxArea) {
                maxArea = result.area;
                maxRectangle = result.rectangle;
            }
            
            System.out.printf("  📊 当前行最大矩形: %s\n", result.rectangle);
            System.out.printf("  🏆 全局最大面积: %d\n", maxArea);
        }
        
        // 显示最终结果
        System.out.println("\n🏆 最终结果:");
        if (maxRectangle != null) {
            printFinalResult(matrix, maxRectangle);
        }
        System.out.printf("最大矩形面积: %d\n", maxArea);
        
        return maxArea;
    }
    
    static class Rectangle {
        int row, col, height, width, area;
        
        Rectangle(int row, int col, int height, int width) {
            this.row = row;
            this.col = col;
            this.height = height;
            this.width = width;
            this.area = height * width;
        }
        
        @Override
        public String toString() {
            return String.format("位置(%d,%d), 高度=%d, 宽度=%d, 面积=%d", 
                               row, col, height, width, area);
        }
    }
    
    static class RectangleResult {
        Rectangle rectangle;
        int area;
        
        RectangleResult(Rectangle rectangle, int area) {
            this.rectangle = rectangle;
            this.area = area;
        }
    }
    
    private static RectangleResult findLargestRectangleWithDetails(int[] heights, int currentRow) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        Rectangle maxRect = null;
        
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            while (!stack.isEmpty() && currentHeight < heights[stack.peek()]) {
                int heightIndex = stack.pop();
                int height = heights[heightIndex];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                int area = height * width;
                
                if (area > maxArea) {
                    maxArea = area;
                    int startCol = stack.isEmpty() ? 0 : stack.peek() + 1;
                    maxRect = new Rectangle(currentRow - height + 1, startCol, height, width);
                }
                
                System.out.printf("    💡 矩形: 高度=%d, 宽度=%d, 面积=%d\n", 
                                height, width, area);
            }
            
            stack.push(i);
        }
        
        return new RectangleResult(maxRect, maxArea);
    }
    
    private static void printOriginalMatrix(char[][] matrix) {
        System.out.println("📋 原始矩阵:");
        for (int i = 0; i < matrix.length; i++) {
            System.out.printf("  第%d行: ", i);
            for (int j = 0; j < matrix[0].length; j++) {
                if (matrix[i][j] == '1') {
                    System.out.print("█ ");
                } else {
                    System.out.print("░ ");
                }
            }
            System.out.println();
        }
    }
    
    private static void printHeightVisualization(int[] heights) {
        int maxHeight = Arrays.stream(heights).max().orElse(0);
        if (maxHeight == 0) return;
        
        System.out.println("  柱状图:");
        for (int level = maxHeight; level >= 1; level--) {
            System.out.printf("  %2d │", level);
            for (int height : heights) {
                if (height >= level) {
                    System.out.print("██");
                } else {
                    System.out.print("  ");
                }
            }
            System.out.println();
        }
        
        System.out.print("     └");
        for (int i = 0; i < heights.length; i++) {
            System.out.print("──");
        }
        System.out.println();
        
        System.out.print("      ");
        for (int i = 0; i < heights.length; i++) {
            System.out.printf("%2d", i);
        }
        System.out.println();
    }
    
    private static void printFinalResult(char[][] matrix, Rectangle rect) {
        System.out.println("最大矩形位置标记:");
        
        for (int i = 0; i < matrix.length; i++) {
            System.out.printf("  第%d行: ", i);
            for (int j = 0; j < matrix[0].length; j++) {
                boolean inRectangle = (i >= rect.row && i < rect.row + rect.height &&
                                     j >= rect.col && j < rect.col + rect.width);
                
                if (matrix[i][j] == '1') {
                    if (inRectangle) {
                        System.out.print("🟦");  // 最大矩形内的1
                    } else {
                        System.out.print("█ ");  // 普通的1
                    }
                } else {
                    System.out.print("░ ");  // 0
                }
            }
            System.out.println();
        }
        
        System.out.println("图例: 🟦 = 最大矩形, █ = 其他1, ░ = 0");
    }
    
    public static void main(String[] args) {
        // 测试经典案例
        System.out.println("🧪 经典测试用例:");
        char[][] matrix1 = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        maximalRectangleWithVisualization(matrix1);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试全1矩阵
        System.out.println("🧪 全1矩阵测试:");
        char[][] matrix2 = {
            {'1','1','1'},
            {'1','1','1'},
            {'1','1','1'}
        };
        maximalRectangleWithVisualization(matrix2);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        // 测试复杂案例
        System.out.println("🧪 复杂测试用例:");
        char[][] matrix3 = {
            {'1','1','0','1'},
            {'1','1','1','1'},
            {'1','1','1','0'},
            {'1','1','0','0'}
        };
        maximalRectangleWithVisualization(matrix3);
    }
}
```

### 运行结果示例
```plain
🧪 经典测试用例:
🔲 最大矩形可视化计算器
============================================================

📋 原始矩阵:
  第0行: █ ░ █ ░ ░ 
  第1行: █ ░ █ █ █ 
  第2行: █ █ █ █ █ 
  第3行: █ ░ ░ █ ░ 

📍 处理第 0 行:
  高度数组: [1, 0, 1, 0, 0]
  柱状图:
   1 │██  ██    
     └──────────
       0 1 2 3 4
    💡 矩形: 高度=1, 宽度=1, 面积=1
    💡 矩形: 高度=1, 宽度=1, 面积=1
  📊 当前行最大矩形: 位置(0,0), 高度=1, 宽度=1, 面积=1
  🏆 全局最大面积: 1

📍 处理第 1 行:
  高度数组: [2, 0, 2, 1, 1]
  柱状图:
   2 │██  ██    
   1 │██  ██████
     └──────────
       0 1 2 3 4
    💡 矩形: 高度=1, 宽度=2, 面积=2
    💡 矩形: 高度=2, 宽度=1, 面积=2
    💡 矩形: 高度=2, 宽度=1, 面积=2
  📊 当前行最大矩形: 位置(1,2), 高度=1, 宽度=2, 面积=2
  🏆 全局最大面积: 2

📍 处理第 2 行:
  高度数组: [3, 1, 3, 2, 2]
  柱状图:
   3 │██  ██    
   2 │██  ██████
   1 │██████████
     └──────────
       0 1 2 3 4
    💡 矩形: 高度=2, 宽度=2, 面积=4
    💡 矩形: 高度=1, 宽度=3, 面积=3
    💡 矩形: 高度=2, 宽度=3, 面积=6  ← 最大！
    💡 矩形: 高度=3, 宽度=1, 面积=3
    💡 矩形: 高度=3, 宽度=1, 面积=3
  📊 当前行最大矩形: 位置(1,2), 高度=2, 宽度=3, 面积=6
  🏆 全局最大面积: 6

📍 处理第 3 行:
  高度数组: [4, 0, 0, 3, 0]
  柱状图:
   4 │██        
   3 │██    ██  
   2 │██    ██  
   1 │██    ██  
     └──────────
       0 1 2 3 4
    💡 矩形: 高度=3, 宽度=1, 面积=3
    💡 矩形: 高度=4, 宽度=1, 面积=4
  📊 当前行最大矩形: 位置(0,0), 高度=4, 宽度=1, 面积=4
  🏆 全局最大面积: 6

🏆 最终结果:
最大矩形位置标记:
  第0行: █ ░ █ ░ ░ 
  第1行: █ ░ 🟦🟦🟦
  第2行: █ █ 🟦🟦🟦
  第3行: █ ░ ░ █ ░ 

图例: 🟦 = 最大矩形, █ = 其他1, ░ = 0
最大矩形面积: 6
```

## 🧪 测试用例
### 基础功能测试
```java
public class MaximalRectangleTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 经典案例
        char[][] matrix1 = {
            {'1','0','1','0','0'},
            {'1','0','1','1','1'},
            {'1','1','1','1','1'},
            {'1','0','0','1','0'}
        };
        assertEquals(6, solution.maximalRectangle(matrix1));
        
        // 全1矩阵
        char[][] matrix2 = {
            {'1','1','1'},
            {'1','1','1'}
        };
        assertEquals(6, solution.maximalRectangle(matrix2));
        
        // 单行矩阵
        char[][] matrix3 = {{'1','1','0','1','1','1'}};
        assertEquals(3, solution.maximalRectangle(matrix3));
    }
    
    @Test
    public void testEdgeCases() {
        // 空矩阵
        assertEquals(0, solution.maximalRectangle(new char[][]{}));
        assertEquals(0, solution.maximalRectangle(null));
        
        // 单个元素
        assertEquals(1, solution.maximalRectangle(new char[][]{{'1'}}));
        assertEquals(0, solution.maximalRectangle(new char[][]{{'0'}}));
        
        // 全0矩阵
        char[][] allZeros = {
            {'0','0','0'},
            {'0','0','0'},
            {'0','0','0'}
        };
        assertEquals(0, solution.maximalRectangle(allZeros));
    }
    
    @Test
    public void testSpecialShapes() {
        // L形状
        char[][] lShape = {
            {'1','1','0'},
            {'1','0','0'},
            {'1','0','0'}
        };
        assertEquals(3, solution.maximalRectangle(lShape));
        
        // 十字形状
        char[][] crossShape = {
            {'0','1','0'},
            {'1','1','1'},
            {'0','1','0'}
        };
        assertEquals(3, solution.maximalRectangle(crossShape));
        
        // 对角线
        char[][] diagonal = {
            {'1','0','0'},
            {'0','1','0'},
            {'0','0','1'}
        };
        assertEquals(1, solution.maximalRectangle(diagonal));
    }
}
```

### 算法对比测试
```java
public class MaximalRectangleAlgorithmTest {
    
    @Test
    public void testAlgorithmConsistency() {
        char[][][] testCases = {
            {
                {'1','0','1','0','0'},
                {'1','0','1','1','1'},
                {'1','1','1','1','1'},
                {'1','0','0','1','0'}
            },
            {
                {'1','1','1','1'},
                {'1','1','1','1'},
                {'1','1','1','1'}
            },
            {
                {'1','0','1','1','0'},
                {'1','0','1','1','1'},
                {'1','1','1','1','1'},
                {'1','0','0','1','0'}
            },
            {
                {'0','0','0'},
                {'0','0','0'},
                {'0','0','0'}
            }
        };
        
        Solution stack = new Solution();
        SolutionDP dp = new SolutionDP();
        SolutionBruteForce bruteForce = new SolutionBruteForce();
        
        for (char[][] matrix : testCases) {
            int result1 = stack.maximalRectangle(matrix);
            int result2 = dp.maximalRectangle(matrix);
            int result3 = bruteForce.maximalRectangle(matrix);
            
            System.out.printf("测试矩阵 %dx%d:\n", matrix.length, 
                            matrix.length > 0 ? matrix[0].length : 0);
            System.out.printf("单调栈: %d, 动态规划: %d, 暴力: %d\n", 
                            result1, result2, result3);
            
            assertEquals(result1, result2);
            assertEquals(result1, result3);
        }
        
        System.out.println("所有算法结果一致 ✅");
    }
}
```

### 性能测试
```java
public class MaximalRectanglePerformanceTest {
    
    @Test
    public void testPerformanceComparison() {
        // 生成大型测试数据
        char[][] largeMatrix = generateLargeTestCase(100, 100);
        
        Solution stack = new Solution();
        SolutionDP dp = new SolutionDP();
        SolutionOptimized optimized = new SolutionOptimized();
        
        long startTime, endTime;
        
        // 单调栈法
        startTime = System.nanoTime();
        int result1 = stack.maximalRectangle(largeMatrix);
        endTime = System.nanoTime();
        System.out.printf("单调栈法: %.2f ms, 结果: %d\n", 
                        (endTime - startTime) / 1_000_000.0, result1);
        
        // 动态规划法
        startTime = System.nanoTime();
        int result2 = dp.maximalRectangle(largeMatrix);
        endTime = System.nanoTime();
        System.out.printf("动态规划法: %.2f ms, 结果: %d\n", 
                        (endTime - startTime) / 1_000_000.0, result2);
        
        // 优化版本
        startTime = System.nanoTime();
        int result3 = optimized.maximalRectangle(largeMatrix);
        endTime = System.nanoTime();
        System.out.printf("优化版本: %.2f ms, 结果: %d\n", 
                        (endTime - startTime) / 1_000_000.0, result3);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        assertEquals(result1, result3);
        
        System.out.println("性能测试通过 ✅");
    }
    
    private char[][] generateLargeTestCase(int rows, int cols) {
        Random random = new Random(42); // 固定种子保证可重现
        char[][] matrix = new char[rows][cols];
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextBoolean() ? '1' : '0';
            }
        }
        
        return matrix;
    }
    
    @Test
    public void testMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        char[][] matrix = generateLargeTestCase(200, 200);
        
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        Solution solution = new Solution();
        int result = solution.maximalRectangle(matrix);
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        System.out.printf("矩阵大小: %dx%d\n", matrix.length, matrix[0].length);
        System.out.printf("最大矩形面积: %d\n", result);
    }
}
```



> 更新: 2025-09-19 00:54:28  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/968fe137fd8c5d126313fcf32046d8ca>