---
schemaVersion: 3
type: "problem"
leetcodeId: 46
slug: "permutations"
titleCn: "全排列"
titleEn: "Permutations"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/permutations/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "1446d1a6fbb15c0f4ffc7be08db4462d908128364fc89ac607214e0aad251677"
sourceFactsSha256: "1a732a1314291077f8f881e3a49e852e03053b522636021581238190ab8e0921"
sourceSectionHashes:
  description: "9da45516cd6e08b0798cf33099a0d2ed165dce66374ef546d7b1df2e9f1489f2"
  examples: "66fd32649e628c4b319cf3597e28d6d54174323f56385b7f956da989754c87a9"
  constraints: "37e68cf0e2ca790a620a31fdd1420531afd865f7b48dec06b61a78b6d537bb82"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "a0247f5a796812355ac9dc9aa24024a2183d647092657060444cd66ecf2652fd"
  signature: "ff98f3831d48f446514dbc62326546d83ff6a50a53b50dee9410ce647e2215b1"
  javaTemplate: "9b58032c48f56b91c1c4b6c8da4beadefc36477d1c360f16110950e1f23bb4e6"
primaryPattern: "回溯"
topics: ["回溯","数组"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Backtracking 回溯"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 46. 全排列 / Permutations

> **双轨入口：** [[核心模型/回溯/46-Permutations-核心模型.md|核心模型]] · [[建模专题/T0/46-Permutations-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`回溯`
- 清单优先级：`P0`
- 清单代表标签：`Backtracking 回溯`
- LeetCode 当前标签：数组 (Array)、回溯 (Backtracking)
- 官方来源：<https://leetcode.cn/problems/permutations/>
- 直观建模专题：[从逐位置选择推导决策树、路径状态与恢复现场](../../建模专题/T0/46-Permutations-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`1446d1a6fbb15c0f4ffc7be08db4462d908128364fc89ac607214e0aad251677`
- 主模型：决策树回溯 + `used` 使用状态

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个不含重复数字的数组 `nums` ，返回其 *所有可能的全排列* 。你可以 **按任意顺序** 返回答案。

## 官方示例


**示例 1：**

```text
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**示例 2：**

```text
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

**示例 3：**

```text
输入：nums = [1]
输出：[[1]]
```

## 官方约束


- `1 <= nums.length <= 6`

- `-10 <= nums[i] <= 10`

- `nums` 中的所有整数 **互不相同**

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 第 0 位可以选择任意元素；选定后，第 1 位从剩余元素中选择。
2. `path` 表示当前已构造的排列前缀。
3. `used[i]` 表示 `nums[i]` 是否已位于当前路径中。
4. 递归返回前必须撤销选择，否则会污染同层后续分支。
5. 加入答案时必须复制 `path`，不能保存同一个可变列表引用。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 答案共有 `n!` 个排列，每个长度为 `n`，仅输出就需要 `Theta(n * n!)` 时间和空间。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

全排列可视为一棵深度为 `n` 的决策树。第 `depth` 层决定排列的第 `depth` 个位置，每层可选择所有尚未使用的元素。当路径长度达到 `n` 时形成一个叶子，也就是一个完整排列。

回溯的固定三步是：

```text
做选择：path.add，used=true
递归：填写下一位置
撤销选择：used=false，path.remove
```

## 朴素方案：枚举所有下标序列再过滤

用 `n` 层循环或递归让每一位都能选择任意元素，会生成 `n^n` 个序列，再过滤包含重复下标的序列。这产生大量注定无效的分支。

- 时间复杂度：约 `O(n^n * n)`。
- 空间复杂度：递归与临时序列至少 `O(n)`，不计输出。

## 最优方案：回溯时只选未使用元素

使用布尔数组在生成阶段剪掉重复使用同一元素的非法分支。到达长度 `n` 时复制路径加入结果。由于输入值互异，不需要额外的同层数值去重。

### 正确性与不变量

进入深度 `depth` 时，`path` 恰含 `depth` 个互不重复的输入元素，且 `used` 与路径成员完全一致。循环逐一尝试所有未使用元素，因此覆盖了该前缀下所有可能的下一项；标记与撤销使不同分支互不干扰。深度 `n` 时路径包含全部元素且各一次，是合法排列。每个排列的选择顺序唯一，所以既不遗漏也不重复。

- 时间复杂度：`O(n * n!)`，主要来自复制 `n!` 个长度为 `n` 的结果。
- 辅助空间复杂度：`O(n)`，包括路径、`used` 和递归深度；输出空间为 `O(n * n!)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> answer = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrack(nums, used, new ArrayList<>(), answer);
        return answer;
    }

    private void backtrack(int[] nums, boolean[] used,
                           List<Integer> path,
                           List<List<Integer>> answer) {
        if (path.size() == nums.length) {
            answer.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (used[i]) {
                continue;
            }

            used[i] = true;
            path.add(nums[i]);
            backtrack(nums, used, path, answer);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.List;

public class Solution {
    public List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> answer = new ArrayList<>();
        boolean[] used = new boolean[nums.length];
        backtrack(nums, used, new ArrayList<>(), answer);
        return answer;
    }

    private void backtrack(int[] nums, boolean[] used,
                           List<Integer> path,
                           List<List<Integer>> answer) {
        if (path.size() == nums.length) {
            answer.add(new ArrayList<>(path));
            return;
        }

        for (int i = 0; i < nums.length; i++) {
            if (used[i]) {
                continue;
            }

            used[i] = true;
            path.add(nums[i]);
            backtrack(nums, used, path, answer);
            path.remove(path.size() - 1);
            used[i] = false;
        }
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.permute(new int[]{1, 2, 3}));
        System.out.println(solution.permute(new int[]{0, 1}));
        System.out.println(solution.permute(new int[]{1}));
    }
}
```

## 边界与易错点

- `answer.add(path)` 会让所有结果引用同一列表，最终内容错误；必须 `new ArrayList<>(path)`。
- `used` 应按输入下标记录，不是按值直接做数组下标，输入允许负数。
- 撤销顺序与选择相反：先移除路径末尾，再清除对应标记，两者都不能漏。
- 本题输入互异；若有重复数字，需要先排序，并在同一树层跳过相同且前一个未使用的元素。

## 可扩展变式

- 全排列 II：加入排序和同层去重条件。
- 子集问题允许每个元素“选或不选”，决策树结构不同。
- 组合问题通常使用 `start` 下标，避免把顺序不同的同一组重复计数。
- 可用原地交换生成排列，省去 `used` 数组，但恢复现场仍不可少。
