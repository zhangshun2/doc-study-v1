# 4.1.1 数组专题(1-5题)-Java版本

# 4.1.1 数组专题(1-5题) - Java版本
> 本文档包含LeetCode热题100中数组专题的前5道题目，提供基础解法和进阶优化版本
>

---

## 📊 题目概览
| 题号 | 题目 | 难度 | 标签 |
| --- | --- | --- | --- |
| 1 | 两数之和 | 🟢 简单 | 数组, 哈希表 |
| 121 | 买卖股票的最佳时机 | 🟢 简单 | 数组, 动态规划 |
| 169 | 多数元素 | 🟢 简单 | 数组, 哈希表, 分治, 计数, 排序 |
| 283 | 移动零 | 🟢 简单 | 数组, 双指针 |
| 448 | 找到所有数组中消失的数字 | 🟢 简单 | 数组, 哈希表 |


---

## 1️⃣ 两数之和 (LeetCode 1)
### 📝 题目描述
给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出和为目标值 `target` 的那两个整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。

**示例 1：**

```plain
输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
```

**示例 2：**

```plain
输入：nums = [3,2,4], target = 6
输出：[1,2]
```

**约束条件：**

+ 2 ≤ nums.length ≤ 10⁴
+ -10⁹ ≤ nums[i] ≤ 10⁹
+ -10⁹ ≤ target ≤ 10⁹
+ 只会存在一个有效答案

### 🔧 基础解法：暴力枚举
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 暴力枚举：双重循环
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[0]; // 理论上不会执行到这里
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n²)
+ 空间复杂度：O(1)

### 🚀 进阶解法：哈希表优化
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        // 使用HashMap存储值和索引的映射
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            // 如果complement已经在map中，说明找到了答案
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            // 将当前元素和索引存入map
            map.put(nums[i], i);
        }
        
        return new int[0]; // 理论上不会执行到这里
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(n)

**解题思路：**

1. 遍历数组，对于每个元素，计算target与当前元素的差值
2. 检查差值是否已经在哈希表中
3. 如果存在，返回两个索引；否则将当前元素存入哈希表

---

## 2️⃣ 买卖股票的最佳时机 (LeetCode 121)
### 📝 题目描述
给定一个数组 `prices`，它的第 `i` 个元素 `prices[i]` 表示一支给定股票第 `i` 天的价格。

你只能选择某一天买入这只股票，并选择在未来的某一天卖出该股票。设计一个算法来计算你所能获取的最大利润。

返回你可以从这笔交易中获取的最大利润。如果你不能获取任何利润，返回 0 。

**示例 1：**

```plain
输入：[7,1,5,3,6,4]
输出：5
解释：在第 2 天（股票价格 = 1）的时候买入，在第 5 天（股票价格 = 6）的时候卖出，最大利润 = 6-1 = 5 。
```

**示例 2：**

```plain
输入：prices = [7,6,4,3,1]
输出：0
解释：在这种情况下, 没有交易完成, 所以最大利润为 0。
```

### 🔧 基础解法：暴力枚举
```java
class Solution {
    public int maxProfit(int[] prices) {
        int maxProfit = 0;
        
        // 枚举所有可能的买入和卖出组合
        for (int i = 0; i < prices.length; i++) {
            for (int j = i + 1; j < prices.length; j++) {
                int profit = prices[j] - prices[i];
                maxProfit = Math.max(maxProfit, profit);
            }
        }
        
        return maxProfit;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n²)
+ 空间复杂度：O(1)

### 🚀 进阶解法：一次遍历
```java
class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = Integer.MAX_VALUE;  // 记录到目前为止的最低价格
        int maxProfit = 0;                 // 记录最大利润
        
        for (int price : prices) {
            if (price < minPrice) {
                minPrice = price;  // 更新最低价格
            } else {
                // 计算当前价格卖出的利润，并更新最大利润
                maxProfit = Math.max(maxProfit, price - minPrice);
            }
        }
        
        return maxProfit;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

**解题思路：**

1. 维护两个变量：最低价格和最大利润
2. 遍历价格数组，更新最低价格
3. 对于每个价格，计算以当前价格卖出的利润，更新最大利润

---

## 3️⃣ 多数元素 (LeetCode 169)
### 📝 题目描述
给定一个大小为 `n` 的数组 `nums`，返回其中的多数元素。多数元素是指在数组中出现次数大于 `⌊ n/2 ⌋` 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

**示例 1：**

```plain
输入：nums = [3,2,3]
输出：3
```

**示例 2：**

```plain
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

### 🔧 基础解法：哈希表计数
```java
class Solution {
    public int majorityElement(int[] nums) {
        Map<Integer, Integer> count = new HashMap<>();
        
        // 统计每个元素的出现次数
        for (int num : nums) {
            count.put(num, count.getOrDefault(num, 0) + 1);
        }
        
        // 找到出现次数超过n/2的元素
        int majority = nums.length / 2;
        for (Map.Entry<Integer, Integer> entry : count.entrySet()) {
            if (entry.getValue() > majority) {
                return entry.getKey();
            }
        }
        
        return -1; // 理论上不会执行到这里
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(n)

### 🚀 进阶解法：Boyer-Moore投票算法
```java
class Solution {
    public int majorityElement(int[] nums) {
        int candidate = nums[0];
        int count = 1;
        
        // Boyer-Moore投票算法
        for (int i = 1; i < nums.length; i++) {
            if (count == 0) {
                candidate = nums[i];
                count = 1;
            } else if (nums[i] == candidate) {
                count++;
            } else {
                count--;
            }
        }
        
        return candidate;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

**解题思路：**

1. Boyer-Moore投票算法的核心思想：多数元素的出现次数大于n/2
2. 维护一个候选者和计数器
3. 遇到相同元素计数+1，不同元素计数-1
4. 计数为0时更换候选者

---

## 4️⃣ 移动零 (LeetCode 283)
### 📝 题目描述
给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。

请注意，必须在不复制数组的情况下原地对数组进行操作。

**示例 1：**

```plain
输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
```

**示例 2：**

```plain
输入: nums = [0]
输出: [0]
```

### 🔧 基础解法：两次遍历
```java
class Solution {
    public void moveZeroes(int[] nums) {
        int insertPos = 0;
        
        // 第一次遍历：将所有非零元素移到前面
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] != 0) {
                nums[insertPos++] = nums[i];
            }
        }
        
        // 第二次遍历：将剩余位置填充为0
        while (insertPos < nums.length) {
            nums[insertPos++] = 0;
        }
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

### 🚀 进阶解法：双指针一次遍历
```java
class Solution {
    public void moveZeroes(int[] nums) {
        int left = 0;  // 指向下一个非零元素应该放置的位置
        
        // 一次遍历，使用双指针
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] != 0) {
                // 只有当left != right时才需要交换
                if (left != right) {
                    // 交换元素
                    int temp = nums[left];
                    nums[left] = nums[right];
                    nums[right] = temp;
                }
                left++;
            }
        }
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

**解题思路：**

1. 使用双指针，left指向下一个非零元素的位置
2. right遍历整个数组
3. 遇到非零元素时，与left位置交换，并移动left指针

---

## 5️⃣ 找到所有数组中消失的数字 (LeetCode 448)
### 📝 题目描述
给你一个含 `n` 个整数的数组 `nums`，其中 `nums[i]` 在区间 `[1, n]` 内。请你找出所有在 `[1, n]` 范围内但没有出现在 `nums` 中的数字，并以数组的形式返回结果。

**示例 1：**

```plain
输入：nums = [4,3,2,7,8,2,3,1]
输出：[5,6]
```

**示例 2：**

```plain
输入：nums = [1,1]
输出：[2]
```

### 🔧 基础解法：哈希集合
```java
class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        Set<Integer> numSet = new HashSet<>();
        
        // 将所有数字加入集合
        for (int num : nums) {
            numSet.add(num);
        }
        
        List<Integer> result = new ArrayList<>();
        
        // 检查1到n中哪些数字不在集合中
        for (int i = 1; i <= nums.length; i++) {
            if (!numSet.contains(i)) {
                result.add(i);
            }
        }
        
        return result;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(n)

### 🚀 进阶解法：原地标记
```java
class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        // 第一次遍历：将出现的数字对应位置标记为负数
        for (int i = 0; i < nums.length; i++) {
            int index = Math.abs(nums[i]) - 1;  // 数字对应的索引
            if (nums[index] > 0) {
                nums[index] = -nums[index];  // 标记为负数
            }
        }
        
        List<Integer> result = new ArrayList<>();
        
        // 第二次遍历：正数位置对应的数字就是消失的数字
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] > 0) {
                result.add(i + 1);
            }
        }
        
        return result;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1) (不计算返回结果的空间)

**解题思路：**

1. 利用数组索引和数字值的对应关系
2. 第一次遍历：将出现数字对应位置标记为负数
3. 第二次遍历：仍为正数的位置对应的数字就是消失的数字

---

## 📚 总结
### 🎯 核心知识点
1. **哈希表优化**：将O(n²)的查找优化为O(n)
2. **双指针技巧**：原地操作，节省空间复杂度
3. **Boyer-Moore算法**：经典的投票算法
4. **原地标记**：利用数组本身存储额外信息
5. **贪心思想**：股票问题的最优策略

### 💡 解题模式
+ **数组查找**：哈希表是常用优化手段
+ **原地操作**：双指针、标记法避免额外空间
+ **计数问题**：考虑投票算法等O(1)空间解法
+ **缺失元素**：利用索引与值的对应关系

### 🔄 刷题建议
1. 先掌握基础解法，理解题目本质
2. 学习进阶优化，关注时空复杂度
3. 总结解题模式，举一反三
4. 多练习类似题目，加深理解

---

**下一篇：** [4.1.2 数组专题(6-10题) - Java版本](./4.1.2%20数组专题(6-10题)-Java版本.md)



> 更新: 2025-08-25 19:00:19  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/1a6c28096d8c5427954d93fc41de653a>