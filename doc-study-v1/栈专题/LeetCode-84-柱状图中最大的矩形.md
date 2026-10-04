# LeetCode-84-柱状图中最大的矩形

# LeetCode 84 - 柱状图中最大的矩形
## 题目描述
**难度：困难**

给定 `n` 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。

求在该柱状图中，能够勾勒出来的矩形的最大面积。

### 示例
**示例 1：**

![histogram.jpg](./img/T3WJibJppOe66VLG/1632901401287-8081dd4c-770f-442c-bc08-8fd327cd137f-743967.jpeg)

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

## 解题思路
这道题是**单调栈**的经典应用，与接雨水问题有相似之处，但思路略有不同。

### 核心思想：单调栈
对于每个柱子，我们要找到：

+ **左边界**：左边第一个比它矮的柱子
+ **右边界**：右边第一个比它矮的柱子
+ 以当前柱子的高度为矩形高度，左右边界之间的宽度为矩形宽度

单调栈的思路：

+ 维护一个**单调递增栈**（栈底到栈顶高度递增）
+ 当遇到比栈顶更矮的柱子时，说明栈顶柱子的右边界确定了
+ 计算以栈顶柱子为高度的最大矩形面积

### 算法步骤
1. **预处理**：在数组首尾添加高度为0的哨兵，简化边界处理
2. **初始化栈**：存储柱子的索引
3. **遍历数组**：
    - 如果当前柱子高度 ≥ 栈顶柱子高度：直接入栈
    - 如果当前柱子高度 < 栈顶柱子高度：
        * 弹出栈顶（以此柱子为高度计算矩形）
        * 计算矩形面积：高度 × 宽度
        * 重复此过程直到栈为空或当前高度 ≥ 栈顶高度

### 图解分析
以数组 `[2,1,5,6,2,3]` 为例：

```plain
原数组: [2,1,5,6,2,3]
添加哨兵后: [0,2,1,5,6,2,3,0]
索引:      [0,1,2,3,4,5,6,7]

可视化：
6 |     ■
5 |     ■ ■
4 |     ■ ■
3 |     ■ ■   ■
2 | ■   ■ ■ ■ ■
1 | ■ ■ ■ ■ ■ ■
0 |■■■■■■■■
  0 1 2 3 4 5 6 7
```

**详细步骤分析：**

```plain
步骤1: i=0, height=0
栈: [0]

步骤2: i=1, height=2 > height[0]=0
栈: [0,1]

步骤3: i=2, height=1 < height[1]=2
- 弹出1，栈顶为0
- 以height[1]=2为高度的矩形
- 左边界：0，右边界：2，宽度：2-0-1=1
- 面积：2×1=2
- height[2]=1 > height[0]=0，停止弹出
栈: [0,2]
最大面积: 2

步骤4: i=3, height=5 > height[2]=1
栈: [0,2,3]

步骤5: i=4, height=6 > height[3]=5
栈: [0,2,3,4]

步骤6: i=5, height=2 < height[4]=6
- 弹出4，栈顶为3
- 以height[4]=6为高度的矩形
- 左边界：3，右边界：5，宽度：5-3-1=1
- 面积：6×1=6
- height[5]=2 < height[3]=5，继续弹出3
- 弹出3，栈顶为2
- 以height[3]=5为高度的矩形
- 左边界：2，右边界：5，宽度：5-2-1=2
- 面积：5×2=10
- height[5]=2 > height[2]=1，停止弹出
栈: [0,2,5]
最大面积: 10

步骤7: i=6, height=3 > height[5]=2
栈: [0,2,5,6]

步骤8: i=7, height=0 < height[6]=3
- 依次弹出所有元素，计算各自的最大矩形
- 最终得到最大面积：10
```

## 代码实现
### 方法一：单调栈解法（推荐）
```java
public class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int[] newHeights = new int[n + 2];
        
        // 添加哨兵，简化边界处理
        newHeights[0] = 0;
        newHeights[n + 1] = 0;
        for (int i = 0; i < n; i++) {
            newHeights[i + 1] = heights[i];
        }
        
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        
        for (int i = 0; i < newHeights.length; i++) {
            // 当前高度小于栈顶高度时，计算矩形面积
            while (!stack.isEmpty() && newHeights[i] < newHeights[stack.peek()]) {
                int height = newHeights[stack.pop()]; // 矩形高度
                int width = i - stack.peek() - 1;     // 矩形宽度
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        
        return maxArea;
    }
}
```

### 方法二：优化的单调栈（无哨兵）
```java
public class Solution {
    public int largestRectangleArea(int[] heights) {
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

### 方法三：分治法
```java
public class Solution {
    public int largestRectangleArea(int[] heights) {
        return calculateArea(heights, 0, heights.length - 1);
    }
    
    private int calculateArea(int[] heights, int start, int end) {
        if (start > end) {
            return 0;
        }
        
        // 找到最小高度的索引
        int minIndex = start;
        for (int i = start; i <= end; i++) {
            if (heights[i] < heights[minIndex]) {
                minIndex = i;
            }
        }
        
        // 计算三种情况的最大面积
        int areaWithMin = heights[minIndex] * (end - start + 1);
        int leftArea = calculateArea(heights, start, minIndex - 1);
        int rightArea = calculateArea(heights, minIndex + 1, end);
        
        return Math.max(areaWithMin, Math.max(leftArea, rightArea));
    }
}
```

### 方法四：动态规划（预计算左右边界）
```java
public class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int[] left = new int[n];   // 左边第一个小于当前高度的位置
        int[] right = new int[n];  // 右边第一个小于当前高度的位置
        
        // 计算左边界
        left[0] = -1;
        for (int i = 1; i < n; i++) {
            int p = i - 1;
            while (p >= 0 && heights[p] >= heights[i]) {
                p = left[p];
            }
            left[i] = p;
        }
        
        // 计算右边界
        right[n - 1] = n;
        for (int i = n - 2; i >= 0; i--) {
            int p = i + 1;
            while (p < n && heights[p] >= heights[i]) {
                p = right[p];
            }
            right[i] = p;
        }
        
        // 计算最大面积
        int maxArea = 0;
        for (int i = 0; i < n; i++) {
            maxArea = Math.max(maxArea, heights[i] * (right[i] - left[i] - 1));
        }
        
        return maxArea;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **单调栈解法**：O(n)，每个元素最多入栈和出栈一次
+ **分治法**：O(n log n) 平均情况，O(n²) 最坏情况
+ **动态规划**：O(n)，需要两次遍历计算边界

### 空间复杂度
+ **单调栈解法**：O(n)，栈的空间复杂度
+ **分治法**：O(log n)，递归调用栈的深度
+ **动态规划**：O(n)，需要两个辅助数组

## 关键点总结
### 1. 单调栈的应用精髓
+ **单调性维护**：栈中元素保持单调递增
+ **边界确定**：当遇到更矮的柱子时，确定右边界
+ **面积计算**：高度 × 宽度 = 矩形面积

### 2. 矩形面积的计算要素
+ **高度**：被弹出的栈顶元素对应的柱子高度
+ **左边界**：弹出后的新栈顶元素的下一个位置
+ **右边界**：当前遍历到的位置
+ **宽度**：右边界 - 左边界 - 1

### 3. 哨兵的作用
+ **简化边界处理**：避免栈为空的特殊情况
+ **确保所有元素被处理**：最后的0确保栈中所有元素都被弹出

### 4. 常见错误
+ **宽度计算错误**：忘记减去边界本身的位置
+ **边界处理**：没有正确处理数组首尾的特殊情况
+ **栈为空判断**：在计算宽度时没有考虑栈为空的情况

## 扩展思考
### 1. 变种问题
+ **接雨水**：LeetCode 42（单调栈的另一个经典应用）
+ **最大矩形**：LeetCode 85（二维版本）
+ **最大正方形**：LeetCode 221

### 2. 单调栈的其他应用
+ **下一个更大元素**：LeetCode 496, 503
+ **每日温度**：LeetCode 739
+ **去除重复字母**：LeetCode 316

### 3. 优化思路
+ **提前终止**：如果当前最大面积已经超过剩余可能的最大面积
+ **并行处理**：对于超大数组，可以考虑分段并行处理
+ **缓存优化**：对于重复查询，可以缓存结果

### 4. 实际应用
+ **建筑设计**：最大可用空间计算
+ **图像处理**：矩形区域检测
+ **数据可视化**：柱状图分析

### 5. 解法选择建议
+ **面试推荐**：单调栈解法，思路清晰，代码简洁
+ **理解算法思想**：分治法，体现分而治之的思想
+ **空间优化**：如果需要多次查询，动态规划预处理更高效

### 6. 与接雨水问题的对比
+ **相同点**：都使用单调栈，都需要找左右边界
+ **不同点**：
    - 接雨水：单调递减栈，计算凹槽面积
    - 最大矩形：单调递增栈，计算矩形面积

这道题是单调栈应用的另一个经典题目，通过它可以深入理解单调栈在解决"寻找边界"类问题中的通用模式！



> 更新: 2025-09-19 00:54:40  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/8b93c4e9433abc415de37dddad35e921>