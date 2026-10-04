---
schemaVersion: 3
type: "problem"
leetcodeId: 739
slug: "daily-temperatures"
titleCn: "每日温度"
titleEn: "Daily Temperatures"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/daily-temperatures/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "8a04234d29feab196d50679d4076098255a591c57c43b30d58729c45f0222688"
sourceFactsSha256: "0dbf4b73da59bf04fc87e0ae11a059ea2eab20aacf5b17b769c1a4a3172120de"
sourceSectionHashes:
  description: "2fe03ac7ca619b32516e1fad2adde1c8df80efc0c095e4caac1cd6d8302e4cf6"
  examples: "fc28ac81799e7a91862991de9a1011cbb2639476a3af223cc19722ee6288ea57"
  constraints: "4c9bf6537fd9ef6fc78508a205657dfd58cbba70cce99b822498ffca08dce5b1"
  hints: "4ee69477854979a131fbdb1f5eb9c53fc4778751f2c585f94b86da5b343ce84d"
  tags: "5db4e198a1a71cd76db7d102595f888734a20f9a3dac114362e3fe78d25d3390"
  signature: "46d7dad33f36a039a4b172278748fe00d0d197e1a484cffc940b788a7545a06c"
  javaTemplate: "db83ee8814be495e38335fe0b87b4f863bc5817ec873b3aae09451070b1ba0bd"
primaryPattern: "单调结构"
topics: ["单调结构","栈","数组","单调栈"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Monotonic Stack 单调栈"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 739. 每日温度 / Daily Temperatures

> **双轨入口：** [[核心模型/单调结构/739-Daily-Temperatures-核心模型.md|核心模型]] · [[建模专题/T0/739-Daily-Temperatures-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`单调结构`
- 清单优先级：`P0`
- 清单代表标签：`Monotonic Stack 单调栈`
- LeetCode 当前标签：栈 (Stack)、数组 (Array)、单调栈 (Monotonic Stack)
- 官方来源：<https://leetcode.cn/problems/daily-temperatures/>
- 直观建模专题：[从寻找未来到到来即结算](../../建模专题/T0/739-Daily-Temperatures-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`8a04234d29feab196d50679d4076098255a591c57c43b30d58729c45f0222688`
- **主解法**：保存下标的单调递减栈

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个整数数组 `temperatures` ，表示每天的温度，返回一个数组 `answer` ，其中 `answer[i]` 是指对于第 `i` 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 `0` 来代替。

## 官方示例


**示例 1:**

```text
输入: temperatures = [73,74,75,71,69,72,76,73]
输出: [1,1,4,2,1,1,0,0]
```

**示例 2:**

```text
输入: temperatures = [30,40,50,60]
输出: [1,1,1,0]
```

**示例 3:**

```text
输入: temperatures = [30,60,90]
输出: [1,1,0]
```

## 官方约束


- `1 <= temperatures.length <= 10^5`

- `30 <= temperatures[i] <= 100`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. If the temperature is say, 70 today, then in the future a warmer temperature must be either 71, 72, 73, ..., 99, or 100.  We could remember when all of them occur next.

## 学习提示（非官方）

1. 尚未找到答案的日期需要暂存，未来遇到更高温度时再结算。
2. 栈中保存日期下标，才能计算等待天数。
3. 栈内温度从栈底到栈顶保持单调不增；相等温度不能弹出。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

当扫描到今天 `i`，若今天温度高于栈顶日期 `j` 的温度，那么今天就是 `j` 右侧第一个更高温度：`j` 自入栈后，中间所有日子都没有使它出栈，说明那些温度均不够高。结算 `j` 后，还可能继续结算更早、更低温的日期。

## 朴素方案

对每一天向右逐日寻找首次升温，最坏在单调下降数组中检查约 `n(n-1)/2` 对，时间 `O(n^2)`、空间 `O(1)`。从右向左预处理跳跃信息也能优化，但单调栈是更通用的“下一个更大元素”模板。

## 最优方案推导

从左到右遍历下标 `today`：

1. 栈非空且 `temperatures[today] > temperatures[stack.peek()]` 时，弹出 `previous`。
2. `today` 是 `previous` 第一个更高日，设置 `answer[previous] = today - previous`。
3. 重复弹栈，直到栈空或栈顶温度不低于今天。
4. 将 `today` 压栈，等待未来结算。

遍历结束仍在栈中的日期右侧没有更高温度，输出数组默认值 0 已是答案。

## 正确性与不变量

每轮结束时，栈中下标严格递增，对应温度从栈底到栈顶单调不增，且这些日期尚未遇到右侧更高温度。

当日期 `previous` 被今天弹出时，今天温度更高；而 `previous` 与今天之间若有更高温度，`previous` 早已在那一天弹出。因此今天恰是第一个更高日。未弹出的栈顶温度不低于今天，今天不能成为其答案。故每次结算都正确，且所有有答案的日期最终都会被对应的首次更高日弹出。

## 复杂度

- **时间复杂度**：`O(n)`；每个下标压栈一次、弹栈至多一次。
- **空间复杂度**：`O(n)`；严格下降时所有下标都留在栈中。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int[] answer = new int[temperatures.length];
        Deque<Integer> stack = new ArrayDeque<>();

        for (int today = 0; today < temperatures.length; today++) {
            while (!stack.isEmpty()
                    && temperatures[today] > temperatures[stack.peek()]) {
                int previous = stack.pop();
                answer[previous] = today - previous;
            }
            stack.push(today);
        }
        return answer;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;

class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int[] answer = new int[temperatures.length];
        Deque<Integer> stack = new ArrayDeque<>();

        for (int today = 0; today < temperatures.length; today++) {
            while (!stack.isEmpty()
                    && temperatures[today] > temperatures[stack.peek()]) {
                int previous = stack.pop();
                answer[previous] = today - previous;
            }
            stack.push(today);
        }
        return answer;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(Arrays.toString(solution.dailyTemperatures(
                new int[]{73, 74, 75, 71, 69, 72, 76, 73})));
        System.out.println(Arrays.toString(solution.dailyTemperatures(
                new int[]{30, 40, 50, 60})));
        System.out.println(Arrays.toString(solution.dailyTemperatures(
                new int[]{30, 60, 90})));
    }
}
```

## 边界与易错点

- 比较条件必须是严格 `>`；相等温度不是“更高”。
- 栈保存下标而非温度，否则无法计算天数差。
- 弹栈需要 `while`，一天可能同时解决多个较冷日期。
- 结果数组默认是 0，无需单独处理最终未弹出的日期。
- 单调性的描述取决于观察方向：此实现从栈底到栈顶温度不增。

## 可扩展变式

- 下一个更大元素：同一单调栈模板，只是输出元素值或下标。
- 循环数组的下一个更大元素：遍历下标 `0..2n-1`，用取模模拟两轮。
- 找下一个更小元素：反转比较方向。
- 温度范围很小：也可从右向左记录每个温度最近出现位置，但单调栈更通用。
