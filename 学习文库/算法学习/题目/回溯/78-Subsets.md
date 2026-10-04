---
schemaVersion: 3
type: "problem"
leetcodeId: 78
slug: "subsets"
titleCn: "子集"
titleEn: "Subsets"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/subsets/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "e0dd269dd5682d6fb54e15f3279e0781bf1aae64808895ff8773280565f8b849"
sourceFactsSha256: "b766d9043316f491a3feb72f98747c37319aa07331c6b02b99eedbcae1a386be"
sourceSectionHashes:
  description: "8f6720af4707e311351e82d0feff242f821b0b4b78c6380f93a7335688ca1e01"
  examples: "9324dfee550d7a2817ea49f20bc33cda12cb79570c7f06b176b6ba948f380293"
  constraints: "760842e89508d7084765045e10244d5a43ac147a85039d1affab8fcf65747583"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "209350f8d8d456540ec612ff94ed480bce110af80dc5f5684474123e16cac160"
  signature: "f374bb524a14c0227be27d3d3d64562edc6d5a03c01bf6d1bd209a0dd4d587ab"
  javaTemplate: "4676f0cb199693727567d5bef47331c603817b0e3381f927b132171207c9f7f6"
primaryPattern: "回溯"
topics: ["回溯","位运算","数组"]
priority: "P0"
checklistPriorities: ["P0","P1"]
checklistTags: ["Backtracking 回溯","Bit Manipulation 位运算"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 78. 子集 / Subsets

> **双轨入口：** [[核心模型/回溯/78-Subsets-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`回溯`
- 清单优先级：`P0`、`P1`
- 清单代表标签：`Backtracking 回溯`、`Bit Manipulation 位运算`
- LeetCode 当前标签：位运算 (Bit Manipulation)、数组 (Array)、回溯 (Backtracking)
- 官方来源：<https://leetcode.cn/problems/subsets/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`e0dd269dd5682d6fb54e15f3279e0781bf1aae64808895ff8773280565f8b849`
- 主模型：选择树回溯

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个整数数组 `nums` ，数组中的元素 **互不相同** 。返回该数组所有可能的子集（幂集）。

解集 **不能** 包含重复的子集。你可以按 **任意顺序** 返回解集。

## 官方示例


**示例 1：**

```text
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**示例 2：**

```text
输入：nums = [0]
输出：[[],[0]]
```

## 官方约束


- `1 <= nums.length <= 10`

- `-10 <= nums[i] <= 10`

- `nums` 中的所有元素 **互不相同**

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 对每个元素都有“选”与“不选”两种决定，因此有 `2^n` 个叶子状态。
2. 也可以把“当前路径本身就是一个子集”作为每个递归节点的答案。
3. 加入元素后递归，返回时删除最后一个元素，恢复现场。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 不要求子集中的元素按值排序；按原数组下标递增选择即可。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

若当前已选择的下标严格递增，就不会以不同顺序生成同一个子集。例如生成 `[1,2]` 后不会再生成 `[2,1]`。函数 `backtrack(start)` 表示：当前路径已经确定，下一次只能从下标 `start` 及其右侧选择。

每进入一个递归节点，当前路径就是一个合法子集，应立即复制到结果。之后枚举下一项，形成更长子集。

## 朴素方案：枚举位掩码

从 `mask = 0` 到 `(1 << n) - 1`，二进制第 `i` 位为 `1` 表示选择 `nums[i]`。这个方案其实也是最优枚举方式之一，结构简单且自然对应 Bit Manipulation 标签。

- 时间复杂度：`O(n * 2^n)`，每个掩码检查 `n` 位。
- 空间复杂度：除输出外 `O(n)` 用于构造当前子集。

它并不比回溯差，但当题目加入剪枝、目标和或重复元素时，回溯更容易扩展。

## 最优方案推导

回溯过程如下：

1. 把当前路径的副本加入结果，包括初始空路径。
2. 从 `start` 到数组末尾依次选择一个元素。
3. 把元素加入路径，递归时将下一起点设为 `i+1`。
4. 递归返回后删除最后一个元素，继续尝试同层下一个选择。

“复制路径”是必要操作，因为 `path` 会在后续递归中不断变化。

## 正确性与不变量

每个递归节点的 `path` 包含一组下标严格递增的元素，因此是合法子集且不会含重复元素。任意目标子集都能按其元素在原数组中的下标从小到大，沿唯一一条选择路径到达，所以不会遗漏；下标序列唯一，又保证不会重复生成。回溯删除最后一项后恢复到进入该分支前的状态，使同层后续分支互不污染。

## 复杂度

- 时间复杂度：`O(n * 2^n)`。共有 `2^n` 个子集，复制一个子集最多需要 `O(n)`。
- 空间复杂度：不计返回结果为 `O(n)`，包括递归深度和当前路径；输出占 `O(n * 2^n)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(
            int[] nums,
            int start,
            List<Integer> path,
            List<List<Integer>> result) {
        result.add(new ArrayList<>(path));

        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }

    private void backtrack(
            int[] nums,
            int start,
            List<Integer> path,
            List<List<Integer>> result) {
        result.add(new ArrayList<>(path));

        for (int i = start; i < nums.length; i++) {
            path.add(nums[i]);
            backtrack(nums, i + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        int[] nums = {1, 2, 3};
        List<List<Integer>> answer = new Solution().subsets(nums);
        System.out.println("nums = " + Arrays.toString(nums));
        System.out.println("subsets = " + answer);
    }
}
```

## 边界与易错点

- 空集必须加入，通常在第一次进入递归时完成。
- 必须 `new ArrayList<>(path)`；直接加入 `path` 会让结果中的所有项引用同一对象。
- 递归参数用 `i + 1`，不是 `start + 1`，否则会重复或漏选。
- 回溯时只删除最后一个元素，对应最近一次选择。
- 本题保证元素互异；存在重复元素时，需要先排序并做同层去重。

## 可扩展变式

- 90. 子集 II：元素可能重复，排序后跳过同层相同值。
- 77. 组合：只收集长度恰好为 `k` 的路径，并可按剩余数量剪枝。
- 39. 组合总和：加入目标和约束，决定元素是否可以重复使用。
- 位掩码枚举：适合 `n` 较小且需要用二进制状态参与后续计算的场景。
