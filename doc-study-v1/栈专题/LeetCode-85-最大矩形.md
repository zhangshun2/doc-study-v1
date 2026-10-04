# LeetCode-85-最大矩形

# LeetCode 85 - 最大矩形
## 题目描述
**难度：困难**

给定一个仅包含 `0` 和 `1` 、大小为 `rows x cols` 的二维二进制矩阵，找出只包含 `1` 的最大矩形，并返回其面积。

### 示例
**示例 1：**

![maximal.jpg](./img/MWJqIcG_tS5MP7B7/1615348552802-21a55c42-a597-412a-9d8b-09520c0d849e-116236.jpeg)

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
输入：matrix = [["0"]]
输出：0
```

**示例 3：**

```plain
输入：matrix = [["1"]]
输出：1
```

### 约束条件
+ `rows == matrix.length`
+ `cols == matrix[i].length`
+ `1 <= row, cols <= 200`
+ `matrix[i][j]` 为 `'0'` 或 `'1'`

## 解题思路
这道题是**LeetCode 84 柱状图中最大的矩形**的二维扩展版本。核心思想是将二维问题转化为多个一维问题。

### 核心思想：转化为柱状图问题
对于矩阵的每一行，我们可以将其看作柱状图的底部：

+ 如果当前位置是 `'1'`，则柱子高度为从当前行向上连续 `'1'` 的个数
+ 如果当前位置是 `'0'`，则柱子高度为 0

然后对每一行形成的柱状图，使用 LeetCode 84 的解法求最大矩形面积。

### 算法步骤
1. **预处理**：对于每一行，计算以该行为底的柱状图高度
2. **逐行处理**：对每一行的柱状图，使用单调栈求最大矩形面积
3. **更新答案**：取所有行中的最大值

### 图解分析
以示例矩阵为例：

```plain
原始矩阵:
[["1","0","1","0","0"],
 ["1","0","1","1","1"],
 ["1","1","1","1","1"],
 ["1","0","0","1","0"]]

转化为柱状图高度:

第0行: [1,0,1,0,0]
柱状图: 1 0 1 0 0
        ■   ■
        ■   ■
最大矩形面积: 1

第1行: [2,0,2,1,1]  
柱状图: 2 0 2 1 1
        ■   ■ ■ ■
        ■   ■ ■ ■
最大矩形面积: 3 (右边三个柱子，高度1，宽度3)

第2行: [3,1,3,2,2]
柱状图: 3 1 3 2 2
        ■ ■ ■ ■ ■
        ■ ■ ■ ■ ■
        ■   ■ ■ ■
最大矩形面积: 6 (右边三个柱子，高度2，宽度3)

第3行: [4,0,0,3,0]
柱状图: 4 0 0 3 0
        ■     ■
        ■     ■
        ■     ■
        ■     ■
最大矩形面积: 4

最终答案: 6
```

**高度计算详解：**

```plain
对于位置 (i,j)：
- 如果 matrix[i][j] == '0'，则 heights[j] = 0
- 如果 matrix[i][j] == '1'，则 heights[j] = heights[j] + 1

示例计算过程：
第0行: matrix[0] = ["1","0","1","0","0"]
       heights = [1,0,1,0,0]

第1行: matrix[1] = ["1","0","1","1","1"]
       heights[0] = 1+1 = 2 (连续的1)
       heights[1] = 0     (遇到0重置)
       heights[2] = 1+1 = 2 (连续的1)
       heights[3] = 0+1 = 1 (新的1)
       heights[4] = 0+1 = 1 (新的1)
       结果: [2,0,2,1,1]
```

## 代码实现
### 方法一：单调栈解法（推荐）
```java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            // 更新当前行的柱状图高度
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    heights[j] += 1;
                } else {
                    heights[j] = 0;
                }
            }
            
            // 计算当前柱状图的最大矩形面积
            maxArea = Math.max(maxArea, largestRectangleArea(heights));
        }
        
        return maxArea;
    }
    
    // LeetCode 84 的解法：柱状图中最大的矩形
    private int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        int n = heights.length;
        
        for (int i = 0; i <= n; i++) {
            int currentHeight = (i == n) ? 0 : heights[i];
            
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

### 方法二：动态规划解法
```java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int[] left = new int[cols];    // 左边界
        int[] right = new int[cols];   // 右边界
        
        // 初始化右边界
        Arrays.fill(right, cols);
        
        int maxArea = 0;
        
        for (int i = 0; i < rows; i++) {
            int currentLeft = 0, currentRight = cols;
            
            // 更新高度数组
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    heights[j]++;
                } else {
                    heights[j] = 0;
                }
            }
            
            // 更新左边界
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    left[j] = Math.max(left[j], currentLeft);
                } else {
                    left[j] = 0;
                    currentLeft = j + 1;
                }
            }
            
            // 更新右边界
            for (int j = cols - 1; j >= 0; j--) {
                if (matrix[i][j] == '1') {
                    right[j] = Math.min(right[j], currentRight);
                } else {
                    right[j] = cols;
                    currentRight = j;
                }
            }
            
            // 计算当前行的最大面积
            for (int j = 0; j < cols; j++) {
                maxArea = Math.max(maxArea, (right[j] - left[j]) * heights[j]);
            }
        }
        
        return maxArea;
    }
}
```

### 方法三：暴力优化解法
```java
public class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        
        int rows = matrix.length;
        int cols = matrix[0].length;
        int maxArea = 0;
        
        // 预处理：计算每个位置向左连续1的个数
        int[][] left = new int[rows][cols];
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '1') {
                    left[i][j] = (j == 0) ? 1 : left[i][j - 1] + 1;
                }
            }
        }
        
        // 对每个位置，向上扩展计算矩形面积
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if (matrix[i][j] == '0') continue;
                
                int width = left[i][j];
                for (int k = i; k >= 0; k--) {
                    width = Math.min(width, left[k][j]);
                    maxArea = Math.max(maxArea, width * (i - k + 1));
                }
            }
        }
        
        return maxArea;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **单调栈解法**：O(rows × cols)，每行需要 O(cols) 时间处理柱状图
+ **动态规划解法**：O(rows × cols)，需要三次遍历每行
+ **暴力优化解法**：O(rows² × cols)，对每个位置向上扩展

### 空间复杂度
+ **单调栈解法**：O(cols)，需要高度数组和栈
+ **动态规划解法**：O(cols)，需要三个辅助数组
+ **暴力优化解法**：O(rows × cols)，需要预处理数组

## 关键点总结
### 1. 问题转化的精髓
+ **降维思想**：将二维问题转化为多个一维问题
+ **状态累积**：每行的柱状图高度基于前面行的累积
+ **重置机制**：遇到 `'0'` 时重置高度为 0

### 2. 柱状图高度的计算
+ **连续性**：只有连续的 `'1'` 才能形成柱子
+ **累积性**：当前行的高度 = 前一行高度 + 1（如果当前位置是 `'1'`）
+ **重置性**：遇到 `'0'` 时高度重置为 0

### 3. 单调栈的应用
+ **复用算法**：直接使用 LeetCode 84 的解法
+ **效率优势**：每行只需 O(cols) 时间
+ **代码简洁**：逻辑清晰，易于理解和实现

### 4. 常见错误
+ **高度计算错误**：没有正确处理连续性和重置
+ **边界处理**：矩阵为空或单行单列的特殊情况
+ **数据类型**：字符 `'0'` 和 `'1'` 与数字 0 和 1 的区别

## 扩展思考
### 1. 变种问题
+ **柱状图中最大的矩形**：LeetCode 84（一维版本）
+ **最大正方形**：LeetCode 221（限制为正方形）
+ **最大加号标志**：LeetCode 764

### 2. 优化方向
+ **空间优化**：可以只使用一个高度数组，不需要存储整个矩阵的高度
+ **早期终止**：如果当前最大面积已经超过剩余可能的最大面积
+ **并行处理**：不同行的处理可以并行进行

### 3. 实际应用
+ **图像处理**：最大矩形区域检测
+ **建筑设计**：最大可用矩形空间计算
+ **数据分析**：二维数据中的最大连续区域

### 4. 解法选择建议
+ **面试推荐**：单调栈解法，思路清晰，复用经典算法
+ **理解DP思想**：动态规划解法，体现状态转移思想
+ **简单实现**：暴力优化解法，逻辑直观但效率较低

### 5. 与相关问题的联系
+ **LeetCode 84**：一维版本，是本题的基础
+ **LeetCode 221**：最大正方形，限制了矩形的形状
+ **LeetCode 42**：接雨水，同样使用单调栈但计算不同

### 6. 算法思想总结
+ **分治思想**：将复杂问题分解为简单问题
+ **状态转移**：当前状态基于历史状态计算
+ **单调栈应用**：在寻找边界问题中的通用解法

这道题完美展示了如何将复杂的二维问题转化为熟悉的一维问题，体现了算法设计中"化繁为简"的重要思想！



> 更新: 2025-09-19 00:54:42  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/0256c894d3f670f5b906a08832fa2360>