---
schemaVersion: 3
type: "problem"
leetcodeId: 347
slug: "top-k-frequent-elements"
titleCn: "前 K 个高频元素"
titleEn: "Top K Frequent Elements"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/top-k-frequent-elements/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "ee3eaf4f4ac0a56d6496868addc2ea11bfedf662b61e9538e3dd16db8fe02d98"
sourceFactsSha256: "57d470c4c316a3ece730dc46b6a103937d1456043a2353eafdecbf42b9d51277"
sourceSectionHashes:
  description: "4cce0cc64fc6087009362f4a48d021f1dc69641da9fdc1cae6c386040cc5a416"
  examples: "78a0320f651fc107d794be70dd7c8d5cb01282b1bd8a531eb04723a3a406202c"
  constraints: "08618092da00d1ad5dd16576a40d62129546fb0131579af7173faa083110b1de"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "ded0430d66f4f679d1cbdd5ec4d58f5bbf4e4545565f76e47a57263f35a7e233"
  signature: "97ddc8ac86a99bae63b409f18bf3ae2a9e5996d9332591672ff730f10858a1db"
  javaTemplate: "c530dda464d57b260bccd96499c9e0c9a59d96322c7c2e3641af1fa54afb6300"
primaryPattern: "堆与选择"
topics: ["堆与选择","数组","哈希表","分治","桶排序","计数","快速选择","排序","堆（优先队列）"]
priority: "P0"
checklistPriorities: ["P0","P2"]
checklistTags: ["Heap (Priority Queue) 堆","Counting 计数","Bucket Sort 桶排序","Quickselect 快速选择"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 347. 前 K 个高频元素 / Top K Frequent Elements

> **双轨入口：** [[核心模型/堆与选择/347-Top-K-Frequent-Elements-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`堆与选择`
- 清单优先级：`P0`、`P2`
- 清单代表标签：`Heap (Priority Queue) 堆`、`Counting 计数`、`Bucket Sort 桶排序`、`Quickselect 快速选择`
- LeetCode 当前标签：数组 (Array)、哈希表 (Hash Table)、分治 (Divide and Conquer)、桶排序 (Bucket Sort)、计数 (Counting)、快速选择 (Quickselect)、排序 (Sorting)、堆（优先队列） (Heap (Priority Queue))
- 官方来源：<https://leetcode.cn/problems/top-k-frequent-elements/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`ee3eaf4f4ac0a56d6496868addc2ea11bfedf662b61e9538e3dd16db8fe02d98`
- **主解法**：哈希计数 + 频率桶

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。

## 官方示例


**示例 1：**

输入：nums = [1,1,1,2,2,3], k = 2

**输出：**[1,2]

**示例 2：**

输入：nums = [1], k = 1

输出：[1]

**示例 3：**

输入：nums = [1,2,1,2,1,2,3,1,3,2], k = 2

**输出：**[1,2]

## 官方约束


- `1 <= nums.length <= 10^5`

- `-10^4 <= nums[i] <= 10^4`

- `k` 的取值范围是 `[1, 数组中不相同的元素的个数]`

- 题目数据保证答案唯一，换句话说，数组中前 `k` 个高频元素的集合是唯一的

**进阶：**你所设计算法的时间复杂度 **必须** 优于 `O(n log n)` ，其中 `n`* *是数组大小。

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 任何元素的出现次数范围都在 `[1,n]`。
2. 先用哈希表得到“元素 -> 频率”。
3. 以频率作为桶下标，从高频桶向低频桶收集即可。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 算法时间复杂度必须优于 `O(n log n)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：nums = [4,4,4,5,5,6,6,7], k = 3
输出：[4,5,6]
解释：5 和 6 频率相同，答案顺序不限。
```

## 核心观察

排序的是频率，而频率是有界整数，最大不超过数组长度 `n`。因此无需比较排序：建立 `n+1` 个桶，`buckets[f]` 保存频率为 `f` 的所有元素。倒序遍历桶就是按频率降序。

## 朴素方案

- 统计后对所有不同元素按频率排序：设不同元素数为 `m`，时间 `O(n + m log m)`。
- 维护大小为 `k` 的小顶堆：`O(n + m log k)` 时间、`O(m+k)` 空间，适合 `k` 很小或无法分配 `n` 个桶时。
- 对每个不同元素重新扫描数组计数：最坏 `O(nm)`。

## 最优方案推导

1. 一次扫描建立 `frequency` 哈希表。
2. 创建长度 `n+1` 的列表数组。
3. 对每个 `(num,count)`，把 `num` 加到 `buckets[count]`。
4. 从 `n` 递减扫描频率，将桶内元素加入答案，收够 `k` 个停止。

由于题目保证前 `k` 高频元素的答案唯一，不会在选择边界产生无法决定的频率并列问题。

## 正确性与不变量

哈希表准确统计每个不同元素频率，因此元素被放入且只放入与真实频率相等的桶。从最大下标向下扫描时，任何尚未扫描桶中的频率都不高于当前已扫描频率。因此收集到的前 `k` 个元素就是频率最高的 `k` 个，顺序不影响正确性。

## 复杂度

- **时间复杂度**：`O(n)`，计数、分桶和扫描桶均为线性级别。
- **空间复杂度**：`O(n)`，哈希表、桶和答案合计线性空间。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> frequency = new HashMap<>();
        for (int num : nums) {
            frequency.merge(num, 1, Integer::sum);
        }

        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new List[nums.length + 1];
        for (Map.Entry<Integer, Integer> entry : frequency.entrySet()) {
            int count = entry.getValue();
            if (buckets[count] == null) {
                buckets[count] = new ArrayList<>();
            }
            buckets[count].add(entry.getKey());
        }

        int[] answer = new int[k];
        int index = 0;
        for (int count = nums.length; count >= 1 && index < k; count--) {
            if (buckets[count] == null) {
                continue;
            }
            for (int num : buckets[count]) {
                answer[index++] = num;
                if (index == k) {
                    break;
                }
            }
        }
        return answer;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> frequency = new HashMap<>();
        for (int num : nums) {
            frequency.merge(num, 1, Integer::sum);
        }

        @SuppressWarnings("unchecked")
        List<Integer>[] buckets = new List[nums.length + 1];
        for (Map.Entry<Integer, Integer> entry : frequency.entrySet()) {
            int count = entry.getValue();
            if (buckets[count] == null) {
                buckets[count] = new ArrayList<>();
            }
            buckets[count].add(entry.getKey());
        }

        int[] answer = new int[k];
        int index = 0;
        for (int count = nums.length; count >= 1 && index < k; count--) {
            if (buckets[count] == null) {
                continue;
            }
            for (int num : buckets[count]) {
                answer[index++] = num;
                if (index == k) {
                    break;
                }
            }
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(solution.topKFrequent(
                new int[]{1, 1, 1, 2, 2, 3}, 2)));
        System.out.println(Arrays.toString(solution.topKFrequent(
                new int[]{1}, 1)));
        System.out.println(Arrays.toString(solution.topKFrequent(
                new int[]{4, 4, 4, 5, 5, 6, 6, 7}, 3)));
    }
}
```

## 边界与易错点

- 桶数组长度要是 `n + 1`，因为频率可能正好为 `n`。
- Java 不能直接创建泛型数组，需创建 `List<Integer>[]` 并抑制受控警告。
- 频率相同的元素在桶内顺序不确定，题目允许任意顺序。
- `k` 是元素个数，不是频率阈值。
- 若业务要求稳定输出，需要增加次级排序规则，复杂度也会相应变化。

## 可扩展变式

- 内存受限且 `k` 很小：使用大小为 `k` 的小顶堆。
- 要求平均线性且不分配 `n` 个桶：对 `(元素,频率)` 数组做快速选择。
- 数据流实时 Top K：维护计数并配合堆，但频率更新后需要支持调整或延迟删除。
- 单词 Top K 且同频按字典序：自定义堆比较器处理频率和字典序双规则。
