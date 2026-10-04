# 小顶堆解法详解-第K个最大元素

# 小顶堆解法详解：第K个最大元素
> 本文档深入解析使用小顶堆求解"第K个最大元素"问题的算法思路、PriorityQueue特性及时间复杂度分析。
>

---

## 🎯 核心思路分析
### 为什么用小顶堆而不是大顶堆？
这是很多初学者的疑问。让我们从直觉和逻辑两个角度来理解：

#### 直觉理解
想象你是一个班主任，要从50个学生中选出成绩最好的5个学生：

**方法1（大顶堆）：** 把所有学生按成绩排队，取前5个

+ 需要处理所有50个学生
+ 空间占用大

**方法2（小顶堆）：** 只准备5个座位，规则如下：

+ 如果座位没满，新学生直接坐下
+ 如果座位满了，新学生成绩比座位上最差的学生好，就把最差的学生踢出去
+ 最后座位上最差的学生，就是第5名

#### 逻辑分析
```plain
目标：找第K个最大元素
策略：维护一个大小为K的"候选集合"

关键洞察：
- 我们只关心"最大的K个元素"
- 在这K个元素中，最小的那个就是答案
- 用小顶堆，堆顶永远是这K个元素中最小的
```

---

## 🏗️ 算法步骤详解
### 步骤分解
1. **初始化**：创建一个空的小顶堆
2. **遍历数组**：对每个元素执行以下逻辑
3. **判断堆大小**：
    - 如果堆大小 < K：直接加入堆
    - 如果堆大小 = K：比较当前元素与堆顶
4. **更新堆**：如果当前元素 > 堆顶，移除堆顶，加入当前元素
5. **返回结果**：堆顶元素就是第K个最大元素

### 图解过程
以数组 `[3,2,1,5,6,4]`，K=2 为例：

```plain
目标：找第2个最大元素

初始状态：heap = [], k = 2

步骤1：处理元素3
  heap.size() = 0 < 2
  直接加入：heap = [3]

步骤2：处理元素2  
  heap.size() = 1 < 2
  直接加入：heap = [2, 3]  // 小顶堆，2在堆顶

步骤3：处理元素1
  heap.size() = 2 = k
  1 < heap.peek() (2)，不操作
  heap = [2, 3]

步骤4：处理元素5
  heap.size() = 2 = k  
  5 > heap.peek() (2)，移除堆顶2，加入5
  heap = [3, 5]  // 重新调整为小顶堆

步骤5：处理元素6
  heap.size() = 2 = k
  6 > heap.peek() (3)，移除堆顶3，加入6  
  heap = [5, 6]  // 重新调整为小顶堆

步骤6：处理元素4
  heap.size() = 2 = k
  4 < heap.peek() (5)，不操作
  heap = [5, 6]

结果：heap.peek() = 5，即第2个最大元素
```

---

## 📚 PriorityQueue详解
### 基本特性
```java
// Java中的PriorityQueue是小顶堆的实现
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// 如果需要大顶堆，需要提供比较器
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
```

### 核心方法详解
#### 1. offer(E e) - 插入元素
```java
heap.offer(5);  // 将5插入堆中
```

**作用：** 将元素插入堆中，并自动维护堆的性质  
**时间复杂度：** O(log n)  
**内部过程：**

1. 将元素添加到堆的末尾
2. 执行"上浮"操作，与父节点比较并交换
3. 重复直到满足堆的性质

#### 2. poll() - 移除并返回堆顶元素
```java
Integer top = heap.poll();  // 移除并返回最小元素
```

**作用：** 移除堆顶元素（最小值），并返回该元素  
**时间复杂度：** O(log n)  
**内部过程：**

1. 保存堆顶元素
2. 将最后一个元素移到堆顶
3. 执行"下沉"操作，与子节点比较并交换
4. 重复直到满足堆的性质
5. 返回保存的堆顶元素

#### 3. peek() - 查看堆顶元素
```java
Integer top = heap.peek();  // 查看但不移除最小元素
```

**作用：** 返回堆顶元素但不移除  
**时间复杂度：** O(1)  
**注意：** 如果堆为空，返回null

#### 4. size() - 获取堆大小
```java
int size = heap.size();  // 获取堆中元素个数
```

**作用：** 返回堆中元素的数量  
**时间复杂度：** O(1)

### 堆的内部结构
```plain
小顶堆的数组表示：

       2
      / \
     3   5
    / \
   7   8

数组形式：[2, 3, 5, 7, 8]
索引：     0  1  2  3  4

父子关系：
- 父节点索引：(i-1)/2
- 左子节点索引：2*i+1  
- 右子节点索引：2*i+2

堆的性质：
- 父节点 <= 子节点（小顶堆）
- 完全二叉树结构
```

---

## ⏱️ 时间复杂度详细分析
### 操作复杂度分解
#### 单次操作复杂度
| 操作 | 时间复杂度 | 说明 |
| --- | --- | --- |
| offer() | O(log k) | 插入元素，最多需要log k次比较 |
| poll() | O(log k) | 删除堆顶，最多需要log k次调整 |
| peek() | O(1) | 直接访问数组第一个元素 |
| size() | O(1) | 直接返回计数器值 |


#### 为什么是O(log k)？
```plain
堆是完全二叉树，高度为log k

以k=8为例：
       1
      / \
     2   3  
    / \ / \
   4  5 6  7
  /
 8

高度 = log₂(8) = 3
最坏情况下，元素需要从叶子节点移动到根节点（或相反）
移动次数 = 高度 = log k
```

### 整体算法复杂度
#### 时间复杂度：O(n log k)
**详细计算：**

```plain
总操作次数分析：

1. 前k个元素：
   - 每个元素执行offer()操作
   - 复杂度：k × O(log i)，其中i从1到k
   - 近似为：k × O(log k)

2. 后(n-k)个元素：
   - 每个元素可能执行：peek() + poll() + offer()
   - peek()：O(1)
   - poll()：O(log k)
   - offer()：O(log k)
   - 单次复杂度：O(log k)
   - 总复杂度：(n-k) × O(log k)

总时间复杂度：
T(n) = k × O(log k) + (n-k) × O(log k)
     = O(k log k) + O((n-k) log k)
     = O(n log k)
```

#### 空间复杂度：O(k)
**分析：**

+ 堆最多存储k个元素
+ 其他变量占用常数空间
+ 总空间复杂度：O(k)

### 复杂度对比
| k值 | O(n log k) | O(n log n) | 优势 |
| --- | --- | --- | --- |
| k=10, n=10000 | ~33,000 | ~133,000 | 4倍提升 |
| k=100, n=10000 | ~66,000 | ~133,000 | 2倍提升 |
| k=1000, n=10000 | ~100,000 | ~133,000 | 1.3倍提升 |
| k=5000, n=10000 | ~122,000 | ~133,000 | 微小提升 |


**结论：** k越小，小顶堆的优势越明显

---

## 🔍 完整代码实现与注释
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        // 创建小顶堆，默认按自然顺序排序（小的在前）
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        
        // 遍历数组中的每个元素
        for (int num : nums) {
            if (heap.size() < k) {
                // 堆未满，直接加入
                heap.offer(num);
            } else if (num > heap.peek()) {
                // 堆已满且当前元素大于堆顶（最小值）
                // 移除最小值，加入当前元素
                heap.poll();   // O(log k)
                heap.offer(num); // O(log k)
            }
            // 如果num <= heap.peek()，说明num不在前k大中，忽略
        }
        
        // 此时堆中存储的是最大的k个元素
        // 堆顶是这k个元素中最小的，即第k大元素
        return heap.peek();
    }
}
```

### 代码优化版本
```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> heap = new PriorityQueue<>(k);
        
        for (int num : nums) {
            if (heap.size() < k) {
                heap.offer(num);
            } else if (num > heap.peek()) {
                // 可以合并为一行
                heap.offer(heap.poll() < num ? num : heap.peek());
                // 等价于：
                // heap.poll();
                // heap.offer(num);
            }
        }
        
        return heap.peek();
    }
}
```

---

## 🧠 算法思维拓展
### 1. 为什么不用大顶堆？
如果用大顶堆存储所有元素：

```java
// 错误思路
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
for (int num : nums) {
    maxHeap.offer(num);  // O(log n)
}
// 取前k个元素
for (int i = 0; i < k-1; i++) {
    maxHeap.poll();  // O(log n)
}
return maxHeap.peek();
```

**问题：**

+ 时间复杂度：O(n log n) + O(k log n) = O(n log n)
+ 空间复杂度：O(n)
+ 效率不如小顶堆的O(n log k)

### 2. 边界情况处理
```java
// 健壮的实现
class Solution {
    public int findKthLargest(int[] nums, int k) {
        if (nums == null || nums.length == 0 || k <= 0 || k > nums.length) {
            throw new IllegalArgumentException("Invalid input");
        }
        
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

### 3. 泛型版本
```java
public class TopKFinder<T extends Comparable<T>> {
    public T findKthLargest(T[] array, int k) {
        PriorityQueue<T> heap = new PriorityQueue<>();
        
        for (T element : array) {
            if (heap.size() < k) {
                heap.offer(element);
            } else if (element.compareTo(heap.peek()) > 0) {
                heap.poll();
                heap.offer(element);
            }
        }
        
        return heap.peek();
    }
}
```

---

## 📊 性能测试与分析
### 实际性能对比
```java
// 性能测试代码
public class PerformanceTest {
    public static void main(String[] args) {
        int[] sizes = {1000, 10000, 100000};
        int[] kValues = {10, 100, 1000};
        
        for (int n : sizes) {
            for (int k : kValues) {
                if (k > n) continue;
                
                int[] nums = generateRandomArray(n);
                
                long start = System.nanoTime();
                findKthLargestHeap(nums, k);
                long heapTime = System.nanoTime() - start;
                
                start = System.nanoTime();
                findKthLargestSort(nums, k);
                long sortTime = System.nanoTime() - start;
                
                System.out.printf("n=%d, k=%d: Heap=%dns, Sort=%dns, Ratio=%.2f\n",
                    n, k, heapTime, sortTime, (double)sortTime/heapTime);
            }
        }
    }
}
```

### 预期结果分析
```plain
预期性能对比（理论分析）：

n=10000, k=10:
- 堆方法：10000 × log(10) ≈ 33,000 操作
- 排序方法：10000 × log(10000) ≈ 133,000 操作
- 性能提升：4倍

n=10000, k=1000:
- 堆方法：10000 × log(1000) ≈ 100,000 操作  
- 排序方法：10000 × log(10000) ≈ 133,000 操作
- 性能提升：1.3倍

结论：k越小，堆方法优势越明显
```

---

## 🎯 总结
### 核心要点
1. **算法思想**：维护大小为k的小顶堆，堆顶即为第k大元素
2. **关键洞察**：只需关心最大的k个元素，不需要对所有元素排序
3. **数据结构选择**：小顶堆而非大顶堆，空间效率更高
4. **时间复杂度**：O(n log k)，当k << n时显著优于O(n log n)
5. **空间复杂度**：O(k)，空间效率高

### 适用场景
+ **Top K问题**：找出最大/最小的K个元素
+ **流式数据**：数据量大但只需要部分结果
+ **内存受限**：无法存储所有数据的场景
+ **实时系统**：需要快速响应的在线算法

### 记忆技巧
1. **第k大 → 小顶堆**：记住这个对应关系
2. **堆大小 = k**：始终维护k个候选元素
3. **堆顶 = 答案**：小顶堆的堆顶就是第k大元素
4. **比较策略**：新元素 > 堆顶才替换

**一句话总结：** 用大小为k的小顶堆筛选出最大的k个元素，堆顶就是第k大！



> 更新: 2025-08-28 10:40:48  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/lxac0ku6nn1p0n9m>