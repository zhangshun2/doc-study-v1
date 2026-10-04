---
schemaVersion: 3
type: "problem"
leetcodeId: 128
slug: "longest-consecutive-sequence"
titleCn: "最长连续序列"
titleEn: "Longest Consecutive Sequence"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-consecutive-sequence/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "21879121556e53f9ba37c04b78fad577a8aaf21ebd29ea5609dd412717beee36"
sourceFactsSha256: "b10af2b6ea0da0170a4ae07ebdfc62cd499aa272462e4772facf0ee4e8617d73"
sourceSectionHashes:
  description: "0cb896dd7deb363d7909a54b6657bfd89a8481049918a4f96056af28b4baa444"
  examples: "654f7ba04fe671e0ff9e63e26316c8082f784b503502bace380207418db6843e"
  constraints: "f2f7d218aa4892680131b49c68fc3076a1d29750828dd72736ad516774113ded"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "d21a0c8396a34b86906032d585690737802ece00ef3ea9c734dff0a33cfc185b"
  signature: "cc41af5a0612a1156562006ce7fff5527134da8a06a702673d61fcc2bcd3923a"
  javaTemplate: "aab939bbaa3b19ed494a0de24b651df1a0a7fdc727bc41730e938a26262f3319"
primaryPattern: "哈希表"
topics: ["哈希表","并查集","数组"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Union Find 并查集"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 128. 最长连续序列 / Longest Consecutive Sequence

> **双轨入口：** [[核心模型/哈希表/128-Longest-Consecutive-Sequence-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`哈希表`
- 清单优先级：`P1`
- 清单代表标签：`Union Find 并查集`
- LeetCode 当前标签：并查集 (Union Find)、数组 (Array)、哈希表 (Hash Table)
- 官方来源：<https://leetcode.cn/problems/longest-consecutive-sequence/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`21879121556e53f9ba37c04b78fad577a8aaf21ebd29ea5609dd412717beee36`
- 主模型：哈希集合只从序列起点扩张

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个未排序的整数数组 `nums` ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

请你设计并实现时间复杂度为 `O(n)`**的算法解决此问题。

## 官方示例


**示例 1：**

```text
输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
```

**示例 2：**

```text
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
```

**示例 3：**

```text
输入：nums = [1,0,1,2]
输出：3
```

## 官方约束


- `0 <= nums.length <= 10^5`

- `-10^9 <= nums[i] <= 10^9`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 用哈希集合支持常数时间判断某个数是否存在，并自然去重。
2. 只有当 `x-1` 不存在时，`x` 才是一段连续序列的起点。
3. 只从起点向右扩张，可以避免从序列中每个数字重复扫描整段。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 明确要求平均 `O(n)` 时间，排序解法 `O(n log n)` 不满足进阶目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

若集合包含 `[1,2,3,4]`，从每个数都向右扩张会产生 `4+3+2+1` 次检查。加入起点条件后，只有 `1` 满足前驱 `0` 不存在，因此整段只扫描一次。

每个不同数字要么不是起点，只做一次前驱检查；要么属于某个起点发起的唯一连续扫描。所有扫描的总步数不超过集合大小。

## 朴素方案：排序后扫描

先排序，之后跳过重复值；若当前值比前一个大 `1`，延长长度，否则重新计数。

- 时间复杂度：`O(n log n)`。
- 空间复杂度：取决于排序实现，原地排序可视为 `O(log n)` 栈空间。
- 评价：直观且常数较小，但不符合题目要求的 `O(n)`。

另一错误朴素法是对每个元素都在数组中线性寻找下一个值，最坏 `O(n^2)`。

## 最优方案推导

1. 把所有数放入哈希集合，去掉重复项。
2. 遍历集合中的每个值 `value`。
3. 若集合中存在 `value-1`，说明它不是起点，跳过。
4. 否则不断检查 `value+1`、`value+2`，计算该段长度。
5. 更新全局最长值。

代码使用 `Set<Long>`，即使输入边界以后扩展到 `Integer.MIN_VALUE` 或 `Integer.MAX_VALUE`，执行 `value-1`、`value+1` 也不会发生 `int` 回绕。

## 正确性与不变量

每个最大连续序列都有唯一最小值 `start`，且 `start-1` 不在集合中，所以算法一定会从它开始扫描并得到该序列完整长度。序列中的其他值都有前驱，不会另起扫描，因此同一序列不重复计数。所有集合元素恰好属于某个最大连续段，取各段长度最大值即为答案。

## 复杂度

- 时间复杂度：平均 `O(n)`。构建集合为 `O(n)`，每个不同值在所有扩张循环中至多被访问一次。
- 空间复杂度：`O(n)` 用于哈希集合。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Long> values = new HashSet<>();
        for (int num : nums) {
            values.add((long) num);
        }

        int best = 0;
        for (long value : values) {
            if (values.contains(value - 1)) {
                continue;
            }

            int length = 1;
            long current = value;
            while (values.contains(current + 1)) {
                current++;
                length++;
            }
            best = Math.max(best, length);
        }
        return best;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Long> values = new HashSet<>();
        for (int num : nums) {
            values.add((long) num);
        }

        int best = 0;
        for (long value : values) {
            if (values.contains(value - 1)) {
                continue;
            }

            int length = 1;
            long current = value;
            while (values.contains(current + 1)) {
                current++;
                length++;
            }
            best = Math.max(best, length);
        }
        return best;
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {100, 4, 200, 1, 3, 2};
        int answer = new Solution().longestConsecutive(nums);
        System.out.println("nums = " + Arrays.toString(nums));
        System.out.println("longest consecutive length = " + answer);
    }
}
```

## 边界与易错点

- 空数组返回 `0`。
- 重复值不能增加连续序列长度，集合会自动去重。
- 必须先判断前驱不存在再扩张，这是线性复杂度的关键。
- 使用 `int` 直接计算极值的前驱或后继可能溢出；本实现用 `long` 集合规避。
- Java `HashSet` 的 `O(1)` 是平均复杂度，不是严格最坏保证。

## 可扩展变式

- 返回最长序列本身：记录最佳起点和长度，最后生成结果。
- 数据持续流式到达：并查集或“边界长度哈希表”可动态合并相邻区间。
- 允许至多缺失 `k` 个数：排序后使用滑动窗口统计缺口。
- 二维网格连通分量：把相邻数的合并思想推广到 Union Find。
