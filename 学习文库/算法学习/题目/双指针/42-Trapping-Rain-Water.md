---
schemaVersion: 3
type: "problem"
leetcodeId: 42
slug: "trapping-rain-water"
titleCn: "接雨水"
titleEn: "Trapping Rain Water"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/trapping-rain-water/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "93009ac3e27997b87a5d4445ef802b27d224ddf13285070cd41aaa958c40b133"
sourceFactsSha256: "f80b40d341f0c9f5042ef29773ff6d8420701db424a38e83bf30d55430c32866"
sourceSectionHashes:
  description: "f6df04da86c8fc0a2ee9a5ac399800c2f01da181e4f4a8184de40a6f0bf6afb7"
  examples: "29ff5b4f0cc32c658ecaee6844fcaf1ec4350d5d224da4426b6c243754dda2e0"
  constraints: "4e9aa739c8492fcc44e2a63a3ef8dd7cc94bfb4ac64e20cd1b8bdba71f0cbfa1"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "ffe107a1e75cbd256097b15a20607f411d88b00d82dfec3c4c57837cc5461117"
  signature: "f163dd2b412fe77b15aa9c83e44dc403d0f71ddf3bfbc6da5b41b0bca54dc7c6"
  javaTemplate: "b6cf58481c3ee8343558243959c214d8dfe8cf307d641e13ca74b9cc07adc395"
primaryPattern: "双指针"
topics: ["双指针","栈","数组","动态规划","单调栈"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Array 数组","Two Pointers 双指针","Monotonic Stack 单调栈"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 42. 接雨水 / Trapping Rain Water

> **双轨入口：** [[核心模型/双指针/42-Trapping-Rain-Water-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`双指针`
- 清单优先级：`P0`
- 清单代表标签：`Array 数组`、`Two Pointers 双指针`、`Monotonic Stack 单调栈`
- LeetCode 当前标签：栈 (Stack)、数组 (Array)、双指针 (Two Pointers)、动态规划 (Dynamic Programming)、单调栈 (Monotonic Stack)
- 官方来源：<https://leetcode.cn/problems/trapping-rain-water/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`93009ac3e27997b87a5d4445ef802b27d224ddf13285070cd41aaa958c40b133`
- 主模型：双指针维护两侧最高墙，按确定的一侧逐列结算

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定 `n` 个非负整数表示每个宽度为 `1` 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.cn/aliyun-lc-upload/uploads/2018/10/22/rainwatertrap.png)

```text
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。
```

**示例 2：**

```text
输入：height = [4,2,0,3,2,5]
输出：9
```

## 官方约束


- `n == height.length`

- `1 <= n <= 2 * 10^4`

- `0 <= height[i] <= 10^5`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 位置 `i` 的水量为 `min(leftMax[i], rightMax[i]) - height[i]`，结果不会为负。
2. 前后缀最大值数组能先把时间降到 `O(n)`。
3. 若当前 `leftMax <= rightMax`，左侧位置的水位已由 `leftMax` 确定，右边未来是否更高不再影响它。
4. 每轮结算较小最高墙所在的一侧，然后移动对应指针。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 期望由暴力 `O(n^2)` 优化为 `O(n)`；最优双指针空间为 `O(1)`。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：height = [1,2,3]
输出：0
解释：单调上升，没有形成左右封闭的低洼。
```

## 核心观察

单个位置能接水必须同时有左墙和右墙，水位取两边最高墙的较小值。双指针不显式保存每个位置的左右最大值，而是维护当前区间外已经看到的 `leftMax` 与 `rightMax`。

当 `leftMax <= rightMax` 时，左指针位置右侧至少存在一面高为 `rightMax` 的墙，因此短板确定为 `leftMax`，该位置可立即结算 `leftMax-height[left]`。另一侧完全对称。

## 朴素方案与中间优化

**逐位置向两边扫描**：对每个位置重新寻找左、右最高墙。

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(1)`。

**前后缀最大值**：预处理 `leftMax[i]`、`rightMax[i]`，再按公式累加。

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(n)`。

前后缀方案是理解双指针的良好过渡，已经可以通过题目。

## 最优方案：双指针逐侧结算

令 `left=0`、`right=n-1`，并维护两侧扫描历史最高值。每轮更新两个最高值：

- `leftMax <= rightMax`：结算 `left`，然后 `left++`。
- 否则：结算 `right`，然后 `right--`。

当前位置高度已参与最高值更新，因此减法结果必不为负。

### 正确性与不变量

循环开始时，区间外位置均已正确结算；`leftMax` 与 `rightMax` 分别是从数组两端到当前指针的最大高度。若 `leftMax <= rightMax`，当前左位置的左侧上界为 `leftMax`，右侧又已确认存在高度至少为 `rightMax` 的柱子，所以最终水位恰为 `leftMax`，可安全结算。右侧情况对称。每轮永久解决一个位置，直至所有位置处理完毕，因此总和正确。

- 时间复杂度：`O(n)`。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public int trap(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int leftMax = 0;
        int rightMax = 0;
        int water = 0;

        while (left <= right) {
            leftMax = Math.max(leftMax, height[left]);
            rightMax = Math.max(rightMax, height[right]);

            if (leftMax <= rightMax) {
                water += leftMax - height[left];
                left++;
            } else {
                water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
public class Solution {
    public int trap(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int leftMax = 0;
        int rightMax = 0;
        int water = 0;

        while (left <= right) {
            leftMax = Math.max(leftMax, height[left]);
            rightMax = Math.max(rightMax, height[right]);

            if (leftMax <= rightMax) {
                water += leftMax - height[left];
                left++;
            } else {
                water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.trap(
                new int[]{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1})); // 6
        System.out.println(solution.trap(new int[]{4, 2, 0, 3, 2, 5})); // 9
        System.out.println(solution.trap(new int[]{1, 2, 3})); // 0
    }
}
```

## 边界与易错点

- 本题是逐列累加水量，不是选择两根柱子求矩形面积；不要与第 11 题混淆。
- 必须使用两侧“历史最高值”，不能只比较 `height[left]` 和 `height[right]` 后随意套公式。
- 先更新 `leftMax/rightMax` 再结算，可保证水量非负。
- 全相等、单调上升、单调下降、长度小于 3 时答案自然为 0。
- 单调栈方案在弹栈时按“宽度 × 有效高度”结算横向水层，时间与空间分别为 `O(n)`、`O(n)`。

## 可扩展变式

- 返回每列水量时，使用前后缀数组更直观。
- 二维接雨水需要从边界出发的最小堆与洪水填充，不能直接套一维双指针。
- 柱宽不等时，逐列水量还需乘以相应宽度。
