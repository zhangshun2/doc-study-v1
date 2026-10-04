# 4.1.3 数组专题(11-15题)-Java版本

# 4.1.3 数组专题(11-15题) - Java版本
> 本文档包含LeetCode热题100中数组专题的第11-15道题目，提供基础解法和进阶优化版本
>

---

## 📊 题目概览
| 题号 | 题目 | 难度 | 标签 |
| --- | --- | --- | --- |
| 56 | 合并区间 | 🟡 中等 | 数组, 排序 |
| 75 | 颜色分类 | 🟡 中等 | 数组, 双指针, 排序 |
| 128 | 最长连续序列 | 🟡 中等 | 并查集, 数组, 哈希表 |
| 215 | 数组中的第K个最大元素 | 🟡 中等 | 数组, 分治, 快速选择, 排序, 堆 |
| 238 | 除自身以外数组的乘积 | 🟡 中等 | 数组, 前缀和 |


---

## 1️⃣ 合并区间 (LeetCode 56)
### 📝 题目描述
以数组 `intervals` 表示若干个区间的集合，其中单个区间为 `intervals[i] = [starti, endi]`。请你合并所有重叠的区间，并返回一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间。

**示例 1：**

```plain
输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
```

**示例 2：**

```plain
输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。
```

### 🔧 基础解法：排序 + 遍历
```java
class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) {
            return intervals;
        }
        
        // 按起始位置排序
        Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
        
        List<int[]> merged = new ArrayList<>();
        
        for (int[] interval : intervals) {
            // 如果结果为空或当前区间与上一个区间不重叠
            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {
                merged.add(interval);
            } else {
                // 重叠，合并区间
                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]);
            }
        }
        
        return merged.toArray(new int[merged.size()][]);
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log n)，主要是排序的时间复杂度
+ 空间复杂度：O(log n)，排序所需的栈空间

### 🚀 进阶解法：优化的合并策略
```java
class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals.length <= 1) return intervals;
        
        // 按起始位置排序
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        
        List<int[]> result = new ArrayList<>();
        int[] current = intervals[0];
        
        for (int i = 1; i < intervals.length; i++) {
            int[] next = intervals[i];
            
            if (current[1] >= next[0]) {
                // 重叠，扩展当前区间
                current[1] = Math.max(current[1], next[1]);
            } else {
                // 不重叠，添加当前区间，更新current
                result.add(current);
                current = next;
            }
        }
        
        // 添加最后一个区间
        result.add(current);
        
        return result.toArray(new int[result.size()][]);
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log n)
+ 空间复杂度：O(log n)

**解题思路：**

1. 按区间起始位置排序
2. 遍历排序后的区间，判断是否与前一个区间重叠
3. 重叠则合并，不重叠则添加到结果中

---

## 2️⃣ 颜色分类 (LeetCode 75)
### 📝 题目描述
给定一个包含红色、白色和蓝色、共 `n` 个元素的数组 `nums`，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

我们使用整数 `0`、`1` 和 `2` 分别表示红色、白色和蓝色。

必须在不使用库的sort函数的情况下解决这个问题。

**示例 1：**

```plain
输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
```

**示例 2：**

```plain
输入：nums = [2,0,1]
输出：[0,1,2]
```

### 🔧 基础解法：计数排序
```java
class Solution {
    public void sortColors(int[] nums) {
        int[] count = new int[3];  // 统计0,1,2的个数
        
        // 第一次遍历：统计每种颜色的数量
        for (int num : nums) {
            count[num]++;
        }
        
        // 第二次遍历：根据统计结果重新填充数组
        int index = 0;
        for (int color = 0; color < 3; color++) {
            for (int i = 0; i < count[color]; i++) {
                nums[index++] = color;
            }
        }
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

### 🚀 进阶解法：荷兰国旗算法（三指针）
```java
class Solution {
    public void sortColors(int[] nums) {
        int left = 0;    // 下一个0应该放置的位置
        int right = nums.length - 1;  // 下一个2应该放置的位置
        int current = 0; // 当前遍历的位置
        
        while (current <= right) {
            if (nums[current] == 0) {
                // 遇到0，与left位置交换
                swap(nums, current, left);
                left++;
                current++;
            } else if (nums[current] == 2) {
                // 遇到2，与right位置交换
                swap(nums, current, right);
                right--;
                // 注意：current不自增，因为交换过来的元素还需要判断
            } else {
                // 遇到1，直接跳过
                current++;
            }
        }
    }
    
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)

**解题思路：**

1. 使用三个指针：left指向下一个0的位置，right指向下一个2的位置，current遍历数组
2. 遇到0与left交换，遇到2与right交换，遇到1跳过
3. 一次遍历完成排序

---

## 3️⃣ 最长连续序列 (LeetCode 128)
### 📝 题目描述
给定一个未排序的整数数组 `nums`，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

请你设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

**示例 1：**

```plain
输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
```

**示例 2：**

```plain
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
```

### 🔧 基础解法：排序
```java
class Solution {
    public int longestConsecutive(int[] nums) {
        if (nums.length == 0) return 0;
        
        Arrays.sort(nums);
        
        int maxLength = 1;
        int currentLength = 1;
        
        for (int i = 1; i < nums.length; i++) {
            if (nums[i] == nums[i - 1]) {
                // 跳过重复元素
                continue;
            } else if (nums[i] == nums[i - 1] + 1) {
                // 连续元素
                currentLength++;
            } else {
                // 不连续，重新开始计数
                maxLength = Math.max(maxLength, currentLength);
                currentLength = 1;
            }
        }
        
        return Math.max(maxLength, currentLength);
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log n)
+ 空间复杂度：O(1)

### 🚀 进阶解法：哈希集合
```java
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> numSet = new HashSet<>();
        
        // 将所有数字加入集合
        for (int num : nums) {
            numSet.add(num);
        }
        
        int maxLength = 0;
        
        for (int num : numSet) {
            // 只有当num-1不在集合中时，num才可能是序列的起点
            if (!numSet.contains(num - 1)) {
                int currentNum = num;
                int currentLength = 1;
                
                // 向后查找连续的数字
                while (numSet.contains(currentNum + 1)) {
                    currentNum++;
                    currentLength++;
                }
                
                maxLength = Math.max(maxLength, currentLength);
            }
        }
        
        return maxLength;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(n)

**解题思路：**

1. 使用哈希集合存储所有数字
2. 对于每个数字，只有当它是序列起点时才开始计算长度
3. 序列起点的特征：num-1不在集合中
4. 从起点开始向后查找连续数字

---

## 4️⃣ 数组中的第K个最大元素 (LeetCode 215)
### 📝 题目描述
给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。

请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。

你必须设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

**示例 1：**

```plain
输入: [3,2,1,5,6,4], k = 2
输出: 5
```

**示例 2：**

```plain
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
```

### 🔧 基础解法：排序
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        Arrays.sort(nums);
        return nums[nums.length - k];
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log n)
+ 空间复杂度：O(1)

### 🚀 进阶解法：快速选择算法
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 第k大元素等于第(n-k)小元素
        return quickSelect(nums, 0, nums.length - 1, nums.length - k);
    }
    
    private int quickSelect(int[] nums, int left, int right, int k) {
        if (left == right) {
            return nums[left];
        }
        
        // 随机选择pivot避免最坏情况
        Random random = new Random();
        int pivotIndex = left + random.nextInt(right - left + 1);
        
        // 分区操作
        pivotIndex = partition(nums, left, right, pivotIndex);
        
        if (k == pivotIndex) {
            return nums[k];
        } else if (k < pivotIndex) {
            return quickSelect(nums, left, pivotIndex - 1, k);
        } else {
            return quickSelect(nums, pivotIndex + 1, right, k);
        }
    }
    
    private int partition(int[] nums, int left, int right, int pivotIndex) {
        int pivot = nums[pivotIndex];
        
        // 将pivot移到末尾
        swap(nums, pivotIndex, right);
        
        int storeIndex = left;
        for (int i = left; i < right; i++) {
            if (nums[i] < pivot) {
                swap(nums, i, storeIndex);
                storeIndex++;
            }
        }
        
        // 将pivot放到正确位置
        swap(nums, storeIndex, right);
        return storeIndex;
    }
    
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
}
```

**复杂度分析：**

+ 时间复杂度：平均O(n)，最坏O(n²)
+ 空间复杂度：O(1)

**解题思路：**

1. 使用快速选择算法，类似快速排序的分区过程
2. 每次分区后，根据pivot位置决定在哪一半继续查找
3. 平均情况下每次能排除一半元素，达到O(n)时间复杂度

---

## 5️⃣ 除自身以外数组的乘积 (LeetCode 238)
### 📝 题目描述
给你一个整数数组 `nums`，返回数组 `answer`，其中 `answer[i]` 等于 `nums` 中除 `nums[i]` 之外其余各元素的乘积。

题目数据保证数组 `nums` 之中任意元素的全部前缀元素和后缀元素的乘积都在 32 位整数范围内。

请不要使用除法，且在 `O(n)` 时间复杂度内完成此题。

**示例 1：**

```plain
输入: nums = [1,2,3,4]
输出: [24,12,8,6]
```

**示例 2：**

```plain
输入: nums = [-1,1,0,-3,3]
输出: [0,0,9,0,0]
```

### 🔧 基础解法：左右乘积数组
```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];   // 左侧乘积
        int[] right = new int[n];  // 右侧乘积
        int[] answer = new int[n];
        
        // 计算左侧乘积
        left[0] = 1;
        for (int i = 1; i < n; i++) {
            left[i] = left[i - 1] * nums[i - 1];
        }
        
        // 计算右侧乘积
        right[n - 1] = 1;
        for (int i = n - 2; i >= 0; i--) {
            right[i] = right[i + 1] * nums[i + 1];
        }
        
        // 计算最终结果
        for (int i = 0; i < n; i++) {
            answer[i] = left[i] * right[i];
        }
        
        return answer;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(n)

### 🚀 进阶解法：空间优化
```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] answer = new int[n];
        
        // 第一次遍历：计算左侧乘积
        answer[0] = 1;
        for (int i = 1; i < n; i++) {
            answer[i] = answer[i - 1] * nums[i - 1];
        }
        
        // 第二次遍历：计算右侧乘积并得到最终结果
        int rightProduct = 1;
        for (int i = n - 1; i >= 0; i--) {
            answer[i] = answer[i] * rightProduct;
            rightProduct *= nums[i];
        }
        
        return answer;
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n)
+ 空间复杂度：O(1)（不计算返回数组）

**解题思路：**

1. 第一次遍历：在结果数组中存储每个位置左侧所有元素的乘积
2. 第二次遍历：用一个变量维护右侧乘积，与左侧乘积相乘得到最终结果
3. 巧妙利用输出数组作为临时存储空间，实现空间优化

---

## 📚 总结
### 🎯 核心知识点
1. **区间合并**：排序 + 贪心合并策略
2. **荷兰国旗算法**：三指针实现三路快排
3. **哈希集合优化**：O(n)时间找最长连续序列
4. **快速选择算法**：平均O(n)时间找第K大元素
5. **前缀后缀技巧**：巧妙计算除自身外的乘积

### 💡 解题模式
+ **区间问题**：排序后贪心处理
+ **分类排序**：多指针技巧
+ **序列问题**：哈希表 + 智能起点选择
+ **选择问题**：分治思想的快速选择
+ **乘积问题**：分解为前缀和后缀乘积

### 🔄 刷题建议
1. **排序预处理**：很多问题排序后会变简单
2. **多指针技巧**：掌握双指针、三指针的应用场景
3. **分治思想**：理解快速选择等分治算法
4. **空间优化**：学会用输出数组作为临时存储
5. **哈希表应用**：O(1)查找的强大威力

---

**上一篇：** [4.1.2 数组专题(6-10题) - Java版本](./4.1.2%20数组专题(6-10题)-Java版本.md)  
**下一篇：** [4.1.4 数组专题(16-20题) - Java版本](./4.1.4%20数组专题(16-20题)-Java版本.md)



> 更新: 2025-08-25 19:00:46  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/5857855f8866de5313e3e70737b4c252>