# LeetCode 496 - 下一个更大元素 I
## 📋 题目描述
**难度：简单**

`nums1` 中数字 `x` 的 **下一个更大元素** 是指 `x` 在 `nums2` 中对应位置 **右侧** 的 **第一个** 比 `x` 大的元素。

给你两个 **没有重复元素** 的数组 `nums1` 和 `nums2`，下标从 **0** 开始计数，其中 `nums1` 是 `nums2` 的子集。

对于每个 `0 <= i < nums1.length`，找出满足 `nums1[i] == nums2[j]` 的下标 `j`，并且在 `nums2` 中确定 `nums2[j]` 的 **下一个更大元素**。如果不存在下一个更大元素，那么本次查询的答案是 `-1`。

返回一个长度为 `nums1.length` 的数组 `ans` 作为答案，满足 `ans[i]` 是如上所述的 **下一个更大元素**。

### 示例
**示例 1：**

```plain
输入：nums1 = [4,1,2], nums2 = [1,3,4,2]
输出：[-1,3,-1]
解释：nums1 中每个数字在 nums2 中的下一个更大元素如下所述：
- 4 在 nums2 中对应下标 2，没有下一个更大元素，所以答案是 -1。
- 1 在 nums2 中对应下标 0，下一个更大元素是 3。
- 2 在 nums2 中对应下标 3，没有下一个更大元素，所以答案是 -1。
```

**示例 2：**

```plain
输入：nums1 = [2,4], nums2 = [1,2,3,4]
输出：[3,-1]
解释：nums1 中每个数字在 nums2 中的下一个更大元素如下所述：
- 2 在 nums2 中对应下标 1，下一个更大元素是 3。
- 4 在 nums2 中对应下标 3，没有下一个更大元素，所以答案是 -1。
```

### 约束条件
+ `1 <= nums1.length <= nums2.length <= 1000`
+ `0 <= nums1[i], nums2[i] <= 10^4`
+ `nums1` 和 `nums2` 中所有整数 **互不相同**
+ `nums1` 中的所有整数同样出现在 `nums2` 中

## 🎯 解题思路
### 核心问题分析
这是一个典型的**单调栈问题**。我们需要：

1. 找到每个元素右侧第一个更大的元素
2. 单调栈正是解决这类问题的最佳工具

### 单调栈的工作原理
```plain
单调栈特点：
- 栈中元素保持单调性（递增或递减）
- 当新元素破坏单调性时，弹出栈顶元素
- 弹出的元素找到了它的"下一个更大元素"

对于"下一个更大元素"问题：
- 使用单调递减栈（栈底到栈顶递减）
- 当遇到更大元素时，栈中较小元素被弹出
- 弹出时，当前元素就是被弹出元素的"下一个更大元素"
```

### 算法步骤
```plain
1. 遍历 nums2，使用单调栈找出每个元素的下一个更大元素
2. 将结果存储在哈希表中：{元素值 -> 下一个更大元素}
3. 遍历 nums1，从哈希表中查询结果
```

### 图解演示
**示例：nums2 = [1,3,4,2]**

```plain
初始状态：
栈: []
结果映射: {}

步骤 1: 处理元素 1
栈: [1]
说明: 栈为空，直接入栈

步骤 2: 处理元素 3
栈: [3]
结果映射: {1 -> 3}
说明: 3 > 1，弹出 1，1 的下一个更大元素是 3

步骤 3: 处理元素 4  
栈: [4]
结果映射: {1 -> 3, 3 -> 4}
说明: 4 > 3，弹出 3，3 的下一个更大元素是 4

步骤 4: 处理元素 2
栈: [4, 2]
结果映射: {1 -> 3, 3 -> 4}
说明: 2 < 4，直接入栈

最终结果：
- 1 的下一个更大元素: 3
- 3 的下一个更大元素: 4  
- 4 的下一个更大元素: 不存在 (-1)
- 2 的下一个更大元素: 不存在 (-1)
```

## 💻 代码实现
### 方法一：单调栈 + 哈希表（推荐）
```java
import java.util.*;

public class Solution {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        // 使用哈希表存储每个元素的下一个更大元素
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        
        // 单调递减栈
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 遍历 nums2，构建下一个更大元素的映射
        for (int num : nums2) {
            // 当栈不为空且当前元素大于栈顶元素时
            while (!stack.isEmpty() && num > stack.peek()) {
                // 弹出栈顶元素，当前元素就是它的下一个更大元素
                int smaller = stack.pop();
                nextGreaterMap.put(smaller, num);
            }
            
            // 当前元素入栈
            stack.push(num);
        }
        
        // 构建结果数组
        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            // 从映射中获取下一个更大元素，不存在则为 -1
            result[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
        }
        
        return result;
    }
}
```

### 方法二：暴力解法（对比参考）
```java
public class SolutionBruteForce {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        int[] result = new int[nums1.length];
        
        for (int i = 0; i < nums1.length; i++) {
            int target = nums1[i];
            int nextGreater = -1;
            
            // 在 nums2 中找到 target 的位置
            boolean found = false;
            for (int j = 0; j < nums2.length; j++) {
                if (nums2[j] == target) {
                    found = true;
                } else if (found && nums2[j] > target) {
                    // 找到下一个更大元素
                    nextGreater = nums2[j];
                    break;
                }
            }
            
            result[i] = nextGreater;
        }
        
        return result;
    }
}
```

### 方法三：优化的单调栈（存储索引）
```java
public class SolutionWithIndex {
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>(); // 存储索引
        
        // 遍历 nums2
        for (int i = 0; i < nums2.length; i++) {
            // 当栈不为空且当前元素大于栈顶索引对应的元素时
            while (!stack.isEmpty() && nums2[i] > nums2[stack.peek()]) {
                int index = stack.pop();
                nextGreaterMap.put(nums2[index], nums2[i]);
            }
            
            stack.push(i);
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

## 🔍 复杂度分析
### 时间复杂度
+ **单调栈解法**：O(n + m)
    - n 是 nums2 的长度，m 是 nums1 的长度
    - 每个元素最多入栈和出栈一次
    - 查询结果需要 O(m) 时间
+ **暴力解法**：O(n × m)
    - 对于 nums1 中的每个元素，都要在 nums2 中搜索

### 空间复杂度
+ **单调栈解法**：O(n)
    - 栈的空间：最多存储 n 个元素
    - 哈希表空间：最多存储 n 个映射关系
+ **暴力解法**：O(1)
    - 只使用常数额外空间

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的下一个更大元素求解
 */
public class VisualNextGreaterElement {
    
    public static int[] nextGreaterElementWithVisualization(int[] nums1, int[] nums2) {
        System.out.println("🔍 寻找下一个更大元素");
        System.out.println("nums1: " + Arrays.toString(nums1));
        System.out.println("nums2: " + Arrays.toString(nums2));
        System.out.println("=" + "=".repeat(60));
        
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        
        System.out.println("📊 使用单调栈处理 nums2:");
        
        for (int i = 0; i < nums2.length; i++) {
            int num = nums2[i];
            System.out.printf("\n步骤 %d: 处理元素 %d\n", i + 1, num);
            
            // 处理栈中比当前元素小的元素
            while (!stack.isEmpty() && num > stack.peek()) {
                int smaller = stack.pop();
                nextGreaterMap.put(smaller, num);
                System.out.printf("  ✅ 发现: %d 的下一个更大元素是 %d\n", smaller, num);
            }
            
            stack.push(num);
            System.out.printf("  📥 元素 %d 入栈\n", num);
            printStackState(stack);
        }
        
        // 处理栈中剩余元素
        System.out.println("\n🔚 处理栈中剩余元素:");
        while (!stack.isEmpty()) {
            int remaining = stack.pop();
            System.out.printf("  ❌ 元素 %d 没有下一个更大元素\n", remaining);
        }
        
        System.out.println("\n📋 映射关系:");
        for (Map.Entry<Integer, Integer> entry : nextGreaterMap.entrySet()) {
            System.out.printf("  %d -> %d\n", entry.getKey(), entry.getValue());
        }
        
        // 构建结果
        int[] result = new int[nums1.length];
        System.out.println("\n🎯 构建最终结果:");
        for (int i = 0; i < nums1.length; i++) {
            result[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
            System.out.printf("  nums1[%d] = %d -> %d\n", 
                             i, nums1[i], result[i]);
        }
        
        System.out.println("\n🏆 最终结果: " + Arrays.toString(result));
        return result;
    }
    
    private static void printStackState(Deque<Integer> stack) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(stackList.get(i));
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    public static void main(String[] args) {
        // 测试示例
        int[] nums1 = {4, 1, 2};
        int[] nums2 = {1, 3, 4, 2};
        nextGreaterElementWithVisualization(nums1, nums2);
        
        System.out.println("\n" + "=".repeat(70) + "\n");
        
        int[] nums1_2 = {2, 4};
        int[] nums2_2 = {1, 2, 3, 4};
        nextGreaterElementWithVisualization(nums1_2, nums2_2);
    }
}
```

### 运行结果示例
```plain
🔍 寻找下一个更大元素
nums1: [4, 1, 2]
nums2: [1, 3, 4, 2]
============================================================

📊 使用单调栈处理 nums2:

步骤 1: 处理元素 1
  📥 元素 1 入栈
  栈状态: [1] (底 -> 顶)

步骤 2: 处理元素 3
  ✅ 发现: 1 的下一个更大元素是 3
  📥 元素 3 入栈
  栈状态: [3] (底 -> 顶)

步骤 3: 处理元素 4
  ✅ 发现: 3 的下一个更大元素是 4
  📥 元素 4 入栈
  栈状态: [4] (底 -> 顶)

步骤 4: 处理元素 2
  📥 元素 2 入栈
  栈状态: [4, 2] (底 -> 顶)

🔚 处理栈中剩余元素:
  ❌ 元素 2 没有下一个更大元素
  ❌ 元素 4 没有下一个更大元素

📋 映射关系:
  1 -> 3
  3 -> 4

🎯 构建最终结果:
  nums1[0] = 4 -> -1
  nums1[1] = 1 -> 3
  nums1[2] = 2 -> -1

🏆 最终结果: [-1, 3, -1]
```

## 🧪 测试用例
### 基础功能测试
```java
public class NextGreaterElementTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 示例 1
        int[] nums1 = {4, 1, 2};
        int[] nums2 = {1, 3, 4, 2};
        int[] expected = {-1, 3, -1};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
        
        // 示例 2
        nums1 = new int[]{2, 4};
        nums2 = new int[]{1, 2, 3, 4};
        expected = new int[]{3, -1};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
    }
    
    @Test
    public void testEdgeCases() {
        // 单个元素
        int[] nums1 = {1};
        int[] nums2 = {1};
        int[] expected = {-1};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
        
        // 递增序列
        nums1 = new int[]{1, 2, 3};
        nums2 = new int[]{1, 2, 3, 4};
        expected = new int[]{2, 3, 4};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
        
        // 递减序列
        nums1 = new int[]{4, 3, 2};
        nums2 = new int[]{4, 3, 2, 1};
        expected = new int[]{-1, -1, -1};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
    }
    
    @Test
    public void testComplexCases() {
        // 复杂情况
        int[] nums1 = {1, 3, 5, 2, 4};
        int[] nums2 = {6, 5, 4, 3, 2, 1, 7};
        int[] expected = {7, 7, 7, 7, 7};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
        
        // 没有更大元素
        nums1 = new int[]{5, 4, 3};
        nums2 = new int[]{5, 4, 3, 2, 1};
        expected = new int[]{-1, -1, -1};
        assertArrayEquals(expected, solution.nextGreaterElement(nums1, nums2));
    }
}
```

### 性能对比测试
```java
public class PerformanceComparisonTest {
    
    @Test
    public void compareAlgorithms() {
        // 生成测试数据
        int[] nums2 = new int[1000];
        for (int i = 0; i < 1000; i++) {
            nums2[i] = i;
        }
        
        int[] nums1 = new int[500];
        for (int i = 0; i < 500; i++) {
            nums1[i] = i * 2;
        }
        
        // 测试单调栈解法
        long startTime = System.nanoTime();
        Solution solution = new Solution();
        int[] result1 = solution.nextGreaterElement(nums1, nums2);
        long time1 = System.nanoTime() - startTime;
        
        // 测试暴力解法
        startTime = System.nanoTime();
        SolutionBruteForce bruteForceSolution = new SolutionBruteForce();
        int[] result2 = bruteForceSolution.nextGreaterElement(nums1, nums2);
        long time2 = System.nanoTime() - startTime;
        
        // 验证结果一致性
        assertArrayEquals(result1, result2);
        
        System.out.printf("单调栈解法: %.2f ms\n", time1 / 1_000_000.0);
        System.out.printf("暴力解法: %.2f ms\n", time2 / 1_000_000.0);
        System.out.printf("性能提升: %.2fx\n", (double) time2 / time1);
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 503 - 下一个更大元素 II（循环数组）
```java
/**
 * 处理循环数组的下一个更大元素
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
                int index = stack.pop();
                result[index] = num;
            }
            
            // 只在第一遍时入栈
            if (i < n) {
                stack.push(i);
            }
        }
        
        return result;
    }
}
```

### 2. 下一个更小元素
```java
/**
 * 寻找下一个更小元素
 */
public class NextSmallerElement {
    
    public int[] nextSmallerElement(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        Deque<Integer> stack = new ArrayDeque<>(); // 单调递增栈
        
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] > nums[i]) {
                int index = stack.pop();
                result[index] = nums[i];
            }
            
            stack.push(i);
        }
        
        return result;
    }
}
```

### 3. 前一个更大元素
```java
/**
 * 寻找前一个更大元素
 */
public class PreviousGreaterElement {
    
    public int[] previousGreaterElement(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        
        Deque<Integer> stack = new ArrayDeque<>(); // 单调递减栈
        
        for (int i = 0; i < n; i++) {
            // 弹出比当前元素小的元素
            while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
                stack.pop();
            }
            
            // 栈顶就是前一个更大元素
            if (!stack.isEmpty()) {
                result[i] = nums[stack.peek()];
            }
            
            stack.push(i);
        }
        
        return result;
    }
}
```

## 💡 解题技巧总结
### 1. 单调栈的核心思想
+ **维护单调性**：栈中元素保持单调递减（或递增）
+ **及时弹出**：当新元素破坏单调性时，弹出不符合条件的元素
+ **记录答案**：弹出元素时，当前元素就是答案

### 2. 问题变体的处理
+ **循环数组**：遍历两遍数组
+ **更小元素**：使用单调递增栈
+ **前一个元素**：从左到右遍历，栈顶是答案

### 3. 实现技巧
+ **存储索引**：便于记录位置信息
+ **哈希表映射**：快速查询结果
+ **边界处理**：注意空栈和数组边界

### 4. 时间复杂度分析
+ **均摊 O(n)**：每个元素最多入栈出栈一次
+ **空间复杂度 O(n)**：栈和哈希表的空间

单调栈是解决"下一个更大/更小元素"类问题的标准工具，掌握了这个模板，就能轻松解决很多相关的算法问题！

