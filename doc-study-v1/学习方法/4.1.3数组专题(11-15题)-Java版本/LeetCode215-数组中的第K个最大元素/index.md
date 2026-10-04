# LeetCode215-数组中的第K个最大元素

# LeetCode 215. 数组中的第K个最大元素
> 本文档详细解析LeetCode第215题：数组中的第K个最大元素，提供多种解法和优化思路。
>

---

## 📝 题目描述
给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。

请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。

**要求：** 你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

### 示例
**示例 1:**

```plain
输入: [3,2,1,5,6,4], k = 2
输出: 5
解释: 排序后数组为 [6,5,4,3,2,1]，第2个最大元素是5
```

**示例 2:**

```plain
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
解释: 排序后数组为 [6,5,5,4,3,3,2,2,1]，第4个最大元素是4
```

### 约束条件
+ `1 <= k <= nums.length <= 10^5`
+ `-10^4 <= nums[i] <= 10^4`

---

## 🎯 解题思路
这道题有多种解法，从简单到复杂，时间复杂度也不同：

1. **排序法** - O(n log n)
2. **堆排序法** - O(n log k)
3. **快速选择法** - O(n) 平均情况，O(n²) 最坏情况
4. **优化快速选择法** - O(n) 保证

---

## 🔧 解法一：排序法（最简单）
### 思路
直接对数组进行排序，然后返回第k个最大的元素。

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 降序排序
        Arrays.sort(nums);
        // 返回第k个最大元素（从右边数第k个）
        return nums[nums.length - k];
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log n)
+ 空间复杂度：O(1)

**优缺点：**

+ ✅ 代码简单，易于理解
+ ❌ 时间复杂度不满足题目要求的O(n)

---

## 🚀 解法二：小顶堆（推荐）
### 思路
使用大小为k的小顶堆，遍历数组：

+ 如果堆大小小于k，直接加入
+ 如果堆大小等于k且当前元素大于堆顶，移除堆顶并加入当前元素
+ 最后堆顶就是第k个最大元素

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 创建小顶堆
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        
        for (int num : nums) {
            if (heap.size() < k) {
                heap.offer(num);
            } else if (num > heap.peek()) {
                heap.poll();
                heap.offer(num);
            }
        }
        
        return heap.peek();
    }
}
```

**复杂度分析：**

+ 时间复杂度：O(n log k)
+ 空间复杂度：O(k)

**优缺点：**

+ ✅ 空间效率高，特别是当k很小时
+ ✅ 代码清晰，逻辑简单
+ ❌ 时间复杂度仍不是最优的O(n)

### 执行过程示例
输入：`[3,2,1,5,6,4]`, k=2

| 步骤 | 当前元素 | 堆状态 | 操作 |
| --- | --- | --- | --- |
| 1 | 3 | [3] | 直接加入 |
| 2 | 2 | [2,3] | 直接加入 |
| 3 | 1 | [2,3] | 1 < 2，不操作 |
| 4 | 5 | [3,5] | 5 > 2，移除2，加入5 |
| 5 | 6 | [5,6] | 6 > 3，移除3，加入6 |
| 6 | 4 | [5,6] | 4 < 5，不操作 |


**结果：** 堆顶元素5就是第2个最大元素

---

## ⚡ 解法三：快速选择算法（最优）
### 思路
基于快速排序的分区思想，但只需要处理包含第k大元素的那一部分。

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 转换为寻找第 nums.length - k 小的元素
        return quickSelect(nums, 0, nums.length - 1, nums.length - k);
    }
    
    private int quickSelect(int[] nums, int left, int right, int k) {
        if (left == right) {
            return nums[left];
        }
        
        // 随机选择pivot，避免最坏情况
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
                swap(nums, storeIndex, i);
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

+ 时间复杂度：O(n) 平均情况，O(n²) 最坏情况
+ 空间复杂度：O(1)

**算法优势：**

+ ✅ 满足题目要求的O(n)时间复杂度
+ ✅ 原地算法，空间复杂度最优
+ ✅ 实际性能很好

---

## 🧠 算法对比
| 算法 | 时间复杂度 | 空间复杂度 | 优点 | 缺点 |
| --- | --- | --- | --- | --- |
| 排序法 | O(n log n) | O(1) | 简单易懂 | 时间复杂度高 |
| 小顶堆 | O(n log k) | O(k) | k小时效率高 | 不是最优时间复杂度 |
| 快速选择 | O(n) | O(1) | 时间空间都最优 | 实现复杂 |


---

## 💡 关键知识点
### 1. 第k大 vs 第k小
+ 第k大元素 = 第(n-k+1)小元素
+ 在升序数组中，第k大元素的索引是 `n-k`

### 2. 堆的选择
+ 求第k大元素 → 使用**小顶堆**（大小为k）
+ 求第k小元素 → 使用**大顶堆**（大小为k）

### 3. 快速选择的优化
+ **随机化pivot**：避免最坏情况O(n²)
+ **三数取中**：选择首、中、尾三个数的中位数作为pivot
+ **Median of Medians**：保证O(n)时间复杂度

---

## 🎨 图解快速选择过程
以 `[3,2,1,5,6,4]`, k=2 为例：

```plain
目标：找第2大元素（即第5小元素，索引4）

初始数组: [3, 2, 1, 5, 6, 4]
索引:      0  1  2  3  4  5

第1次分区（选择pivot=4）:
分区后: [3, 2, 1, 4, 6, 5]
        小于4的 |4| 大于4的
        索引0-2  3  索引4-5

pivot索引=3，目标索引=4，在右半部分

第2次分区（在[6,5]中选择pivot=5）:
分区后: [3, 2, 1, 4, 5, 6]
                    |5|
                    索引4

pivot索引=4，正好等于目标索引=4
返回 nums[4] = 5
```

---

## 🔍 代码优化技巧
### 1. 使用内置API（Java 8+）
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        return Arrays.stream(nums)
                     .boxed()
                     .sorted(Collections.reverseOrder())
                     .skip(k - 1)
                     .findFirst()
                     .get();
    }
}
```

### 2. 使用计数排序（当数值范围小时）
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 题目约束：-10^4 <= nums[i] <= 10^4
        int[] count = new int[20001]; // -10000 到 10000
        
        for (int num : nums) {
            count[num + 10000]++;
        }
        
        int remain = k;
        for (int i = count.length - 1; i >= 0; i--) {
            remain -= count[i];
            if (remain <= 0) {
                return i - 10000;
            }
        }
        
        return -1;
    }
}
```

**时间复杂度：** O(n + range)，当range较小时接近O(n)

---

## 🚀 实战应用
### 相关题目
1. **LeetCode 703** - 数据流中的第K大元素
2. **LeetCode 347** - 前K个高频元素  
3. **LeetCode 973** - 最接近原点的K个点

### 应用场景
+ **Top K问题**：找出最大/最小的K个元素
+ **数据流处理**：实时维护第K大元素
+ **推荐系统**：找出评分最高的K个商品
+ **性能监控**：找出响应时间最长的K个请求

---

## 📚 总结
### 最佳实践
1. **面试场景**：优先使用堆解法，代码简洁且易于解释
2. **性能要求高**：使用快速选择算法
3. **数值范围小**：考虑计数排序
4. **代码简洁性**：直接排序（如果时间复杂度要求不严格）

### 记忆要点
+ 第k大 → 小顶堆（堆大小为k）
+ 快速选择 → 类似快排但只处理一边
+ 随机化pivot → 避免最坏情况
+ 时间复杂度：排序 O(n log n) > 堆 O(n log k) > 快选 O(n)

**核心思想：** 不需要完全排序，只需要找到第k个位置的元素！



> 更新: 2025-08-28 09:52:06  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/hyg7mnoaxp9aly3m>