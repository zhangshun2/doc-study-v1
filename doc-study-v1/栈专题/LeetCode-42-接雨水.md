# LeetCode-42-接雨水

# LeetCode 42 - 接雨水
## 题目描述
**难度：困难**

给定 `n` 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能够接多少雨水。

### 示例
**示例 1：**

![rainwatertrap.png](./img/HoLP819NWo4RvDvD/1587652825913-22489202-afed-48b4-a0b5-90243ab23899-182330.png)

```plain
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。
```

**示例 2：**

```plain
输入：height = [4,2,0,3,2,5]
输出：9
```

### 约束条件
+ `n == height.length`
+ `1 <= n <= 2 * 10^4`
+ `0 <= height[i] <= 3 * 10^4`

## 解题思路
这道题有多种解法，我们重点介绍**单调栈解法**，因为它最能体现栈在解决此类问题中的应用。

### 核心思想：单调栈
接雨水的关键在于：**对于每个位置，能接到的雨水量取决于它左右两边的最高柱子中较矮的那个**。

单调栈的思路：

+ 维护一个**单调递减栈**（栈底到栈顶高度递减）
+ 当遇到比栈顶更高的柱子时，说明可以形成"凹槽"接雨水
+ 计算这个凹槽能接多少雨水

### 算法步骤
1. **初始化栈**：存储柱子的索引
2. **遍历数组**：
    - 如果当前柱子高度 ≤ 栈顶柱子高度：直接入栈
    - 如果当前柱子高度 > 栈顶柱子高度：
        * 弹出栈顶（这是凹槽的底部）
        * 如果栈不为空，计算能接的雨水
        * 重复此过程直到栈为空或当前高度 ≤ 栈顶高度

### 图解分析
以数组 `[0,1,0,2,1,0,1,3,2,1,2,1]` 为例：

```plain
柱子高度: [0,1,0,2,1,0,1,3,2,1,2,1]
索引:     [0,1,2,3,4,5,6,7,8,9,10,11]

可视化：
    3 |       ■
    2 |   ■   ■ ■   ■
    1 | ■ ■ ■ ■ ■ ■ ■ ■
    0 |■■■■■■■■■■■■
      0 1 2 3 4 5 6 7 8 9 10 11

接雨水后：
    3 |       ■
    2 |   ■~~~■~■~~~■
    1 | ■~■~■~■~■~■~■~■
    0 |■■■■■■■■■■■■
      0 1 2 3 4 5 6 7 8 9 10 11
```

**详细步骤分析：**

```plain
步骤1: i=0, height=0
栈: [0]

步骤2: i=1, height=1 > height[0]=0
- 弹出0，栈为空，无法形成凹槽
- 压入1
栈: [1]

步骤3: i=2, height=0 < height[1]=1
栈: [1,2]

步骤4: i=3, height=2 > height[2]=0
- 弹出2（凹槽底部），栈顶为1
- 左边界：height[1]=1，右边界：height[3]=2
- 凹槽高度：min(1,2)-0=1，宽度：3-1-1=1
- 接雨水：1×1=1
- height[3]=2 > height[1]=1，继续弹出1
- 弹出1，栈为空，无法形成凹槽
- 压入3
栈: [3]
累计雨水: 1

步骤5: i=4, height=1 < height[3]=2
栈: [3,4]

步骤6: i=5, height=0 < height[4]=1
栈: [3,4,5]

步骤7: i=6, height=1 > height[5]=0
- 弹出5，栈顶为4
- 左边界：height[4]=1，右边界：height[6]=1
- 凹槽高度：min(1,1)-0=1，宽度：6-4-1=1
- 接雨水：1×1=1
- height[6]=1 = height[4]=1，停止弹出
- 压入6
栈: [3,4,6]
累计雨水: 2

... 继续类似过程
```

## 代码实现
### 方法一：单调栈解法（推荐）
```java
public class Solution {
    public int trap(int[] height) {
        int ans = 0;
        Deque<Integer> stack = new LinkedList<Integer>();
        int n = height.length;
        
        for (int i = 0; i < n; ++i) {
            // 当前柱子高度大于栈顶柱子高度时，可以接雨水
            while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
                int top = stack.pop(); // 凹槽底部
                
                if (stack.isEmpty()) {
                    break; // 没有左边界，无法形成凹槽
                }
                
                int left = stack.peek();  // 左边界
                int currWidth = i - left - 1;  // 凹槽宽度
                int currHeight = Math.min(height[left], height[i]) - height[top]; // 凹槽高度
                ans += currWidth * currHeight;
            }
            stack.push(i);
        }
        
        return ans;
    }
}
```

### 方法二：双指针解法
```java
public class Solution {
    public int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int ans = 0;
        
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) {
                    leftMax = height[left];
                } else {
                    ans += leftMax - height[left];
                }
                ++left;
            } else {
                if (height[right] >= rightMax) {
                    rightMax = height[right];
                } else {
                    ans += rightMax - height[right];
                }
                --right;
            }
        }
        
        return ans;
    }
}
```

### 方法三：动态规划解法
```java
public class Solution {
    public int trap(int[] height) {
        int n = height.length;
        if (n == 0) {
            return 0;
        }
        
        int[] leftMax = new int[n];
        leftMax[0] = height[0];
        for (int i = 1; i < n; ++i) {
            leftMax[i] = Math.max(leftMax[i - 1], height[i]);
        }
        
        int[] rightMax = new int[n];
        rightMax[n - 1] = height[n - 1];
        for (int i = n - 2; i >= 0; --i) {
            rightMax[i] = Math.max(rightMax[i + 1], height[i]);
        }
        
        int ans = 0;
        for (int i = 0; i < n; ++i) {
            ans += Math.min(leftMax[i], rightMax[i]) - height[i];
        }
        
        return ans;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **单调栈解法**：O(n)，每个元素最多入栈和出栈一次
+ **双指针解法**：O(n)，遍历数组一次
+ **动态规划解法**：O(n)，需要三次遍历

### 空间复杂度
+ **单调栈解法**：O(n)，栈的空间复杂度
+ **双指针解法**：O(1)，只使用常数额外空间
+ **动态规划解法**：O(n)，需要两个辅助数组

## 关键点总结
### 1. 单调栈的应用精髓
+ **单调性维护**：栈中元素保持单调递减
+ **凹槽识别**：当遇到更高的柱子时，形成凹槽
+ **面积计算**：宽度 × 高度 = 接雨水量

### 2. 凹槽的三要素
+ **底部**：被弹出的栈顶元素
+ **左边界**：弹出后的新栈顶元素
+ **右边界**：当前遍历到的元素

### 3. 边界条件处理
+ **栈为空**：无法形成凹槽，跳过
+ **高度相等**：不会接雨水，但要更新栈
+ **数组长度**：小于3无法接雨水

### 4. 不同解法的特点
+ **单调栈**：思路直观，适合理解接雨水的本质
+ **双指针**：空间最优，但理解稍复杂
+ **动态规划**：最容易理解，但空间复杂度较高

## 扩展思考
### 1. 变种问题
+ **柱状图中最大的矩形**：LeetCode 84（单调栈经典应用）
+ **最大矩形**：LeetCode 85
+ **接雨水 II**：LeetCode 407（二维版本）

### 2. 单调栈的其他应用
+ **下一个更大元素**：LeetCode 496, 503
+ **每日温度**：LeetCode 739
+ **去除重复字母**：LeetCode 316

### 3. 优化思路
+ **提前终止**：如果数组单调，可以提前结束
+ **分段处理**：对于超长数组，可以考虑分段计算
+ **并行计算**：某些情况下可以并行处理不同段

### 4. 实际应用
+ **建筑设计**：雨水收集系统设计
+ **地形分析**：地理信息系统中的积水分析
+ **图像处理**：轮廓分析和形状识别

### 5. 解法选择建议
+ **面试推荐**：单调栈解法，能很好展示对栈的理解
+ **空间要求严格**：双指针解法
+ **初学者**：动态规划解法，最容易理解

### 6. 常见错误
+ **宽度计算错误**：忘记减去边界本身的宽度
+ **高度计算错误**：没有正确理解凹槽高度的计算方式
+ **边界处理**：栈为空时的特殊情况处理

这道题是单调栈应用的经典题目，通过它可以深入理解单调栈在解决"寻找左右边界"类问题中的强大能力！



> 更新: 2025-09-19 00:54:37  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/7b9309545b563319033b73ec5c40ff62>