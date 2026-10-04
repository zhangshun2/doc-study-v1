---
schemaVersion: 3
type: "problem"
leetcodeId: 54
slug: "spiral-matrix"
titleCn: "螺旋矩阵"
titleEn: "Spiral Matrix"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/spiral-matrix/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "30883cbb111891d12751304a9bea6743ff3165b82f7b8a75c18dfa654ff04a02"
sourceFactsSha256: "8357c432bbc9f71c6ff2e6f08fae7a4555a6b56b6894fc11e14134feb4f672df"
sourceSectionHashes:
  description: "14ae91b5a3778d3a397acd123b273c696ab4f89b249b40fe68f9b8315bba24c2"
  examples: "7c2621a044bb74bc24ceb8b4a300bed416026cd588ae463eaf0d3d1fe8d2bc06"
  constraints: "050e2822019d2739ba9dd352abc534e9beb362c2e5da00df465fea8259bc9f22"
  hints: "8780853d9e8e0df63049dbc54f3ec8259759ccbde2f11f672ecd730da545c1ef"
  tags: "6030179a05d6e17da679cc94228dbfaa9410b0d2b10b6212f0d0051f595af5a5"
  signature: "e131281732a57fb50fe7a44c1291736b6ebbeaf182d29a59aabe618cf62292b8"
  javaTemplate: "62ceb01f6e92aa65f9f17fe400766b9e86e41477686d0c4ca0e3ff362b60093c"
primaryPattern: "矩阵与模拟"
topics: ["矩阵与模拟","数组","矩阵","模拟"]
priority: "P1"
checklistPriorities: ["P1","P2"]
checklistTags: ["Matrix 矩阵","Simulation 模拟"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 54. 螺旋矩阵 / Spiral Matrix

> **双轨入口：** [[核心模型/矩阵与模拟/54-Spiral-Matrix-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`矩阵与模拟`
- 清单优先级：`P1`、`P2`
- 清单代表标签：`Matrix 矩阵`、`Simulation 模拟`
- LeetCode 当前标签：数组 (Array)、矩阵 (Matrix)、模拟 (Simulation)
- 官方来源：<https://leetcode.cn/problems/spiral-matrix/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`30883cbb111891d12751304a9bea6743ff3165b82f7b8a75c18dfa654ff04a02`
- 主模型：四边界收缩模拟

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个 `m` 行 `n` 列的矩阵 `matrix` ，请按照 **顺时针螺旋顺序** ，返回矩阵中的所有元素。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/11/13/spiral1.jpg)

```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/11/13/spiral.jpg)

```text
输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]
```

## 官方约束


- `m == matrix.length`

- `n == matrix[i].length`

- `1 <= m, n <= 10`

- `-100 <= matrix[i][j] <= 100`

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Well for some problems, the best way really is to come up with some algorithms for simulation. Basically, you need to simulate what the problem asks us to do.
2. We go boundary by boundary and move inwards. That is the essential operation. First row, last column, last row, first column, and then we move inwards by 1 and repeat. That's all. That is all the simulation that we need.
3. Think about when you want to switch the progress on one of the indexes. If you progress on i out of [i, j], you'll shift in the same column. Similarly, by changing values for j, you'd be shifting in the same row.
Also, keep track of the end of a boundary so that you can move inwards and then keep repeating. It's always best to simulate edge cases like a single column or a single row to see if anything breaks or not.

## 学习提示（非官方）

1. 用 `top`、`bottom`、`left`、`right` 表示尚未访问区域的四条边。
2. 每走完一条边，立即把对应边界向内移动。
3. 走下边和左边前必须再次判断边界是否有效，否则单行或单列会重复访问。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 输出本身含 `m * n` 个元素，最优时间下界是 `O(mn)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

尚未访问的区域始终是一个矩形。每轮按“上边从左到右、右边从上到下、下边从右到左、左边从下到上”的次序剥掉最外层。走完上边后 `top++`，走完右边后 `right--`，走完下边后 `bottom--`，走完左边后 `left++`。

## 朴素方案：方向数组加 visited

从 `(0,0)` 开始，用方向数组表示右、下、左、上。下一格越界或已经访问时顺时针转向，并用 `boolean[][] visited` 防止重复。

- 时间复杂度：`O(mn)`。
- 空间复杂度：`O(mn)`。
- 局限：虽然正确，但转向规则和访问标记增加了状态，额外空间没有必要。

## 最优方案推导

边界法不跟踪当前朝向，只处理四个确定线段。关键是两次保护性判断：

- 走下边前检查 `top <= bottom`。若上边走完后已经没有行，不能再次走同一行。
- 走左边前检查 `left <= right`。若右边走完后已经没有列，不能再次走同一列。

循环条件 `top <= bottom && left <= right` 表示尚未访问区域非空。

## 正确性与不变量

每轮开始时，矩形 `[top..bottom] x [left..right]` 恰好包含全部未访问元素。四段遍历只访问该矩形最外圈，并在访问后收缩对应边界。保护性判断保证区域退化成单行或单列时不重复。于是每轮后不变量对更小的矩形继续成立；边界交错时，所有元素恰好访问一次。

## 复杂度

- 时间复杂度：`O(mn)`。
- 空间复杂度：`O(1)` 额外工作空间；返回列表的 `O(mn)` 通常不计入额外空间。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        int top = 0;
        int bottom = matrix.length - 1;
        int left = 0;
        int right = matrix[0].length - 1;

        while (top <= bottom && left <= right) {
            for (int col = left; col <= right; col++) {
                result.add(matrix[top][col]);
            }
            top++;

            for (int row = top; row <= bottom; row++) {
                result.add(matrix[row][right]);
            }
            right--;

            if (top <= bottom) {
                for (int col = right; col >= left; col--) {
                    result.add(matrix[bottom][col]);
                }
                bottom--;
            }

            if (left <= right) {
                for (int row = bottom; row >= top; row--) {
                    result.add(matrix[row][left]);
                }
                left++;
            }
        }
        return result;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        int top = 0;
        int bottom = matrix.length - 1;
        int left = 0;
        int right = matrix[0].length - 1;

        while (top <= bottom && left <= right) {
            for (int col = left; col <= right; col++) {
                result.add(matrix[top][col]);
            }
            top++;

            for (int row = top; row <= bottom; row++) {
                result.add(matrix[row][right]);
            }
            right--;

            if (top <= bottom) {
                for (int col = right; col >= left; col--) {
                    result.add(matrix[bottom][col]);
                }
                bottom--;
            }

            if (left <= right) {
                for (int row = bottom; row >= top; row--) {
                    result.add(matrix[row][left]);
                }
                left++;
            }
        }
        return result;
    }
}

public class Main {
    public static void main(String[] args) {
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };
        System.out.println(new Solution().spiralOrder(matrix));
    }
}
```

## 边界与易错点

- 单行矩阵最容易因缺少 `top <= bottom` 判断而重复。
- 单列矩阵最容易因缺少 `left <= right` 判断而重复。
- 每条边的端点已经由前一条边覆盖时，要利用收缩后的边界避免重复角点。
- `matrix[0].length` 可直接访问，因为题目保证至少一行一列。

## 可扩展变式

- 59. 螺旋矩阵 II：按相同边界顺序向矩阵填入 `1` 到 `n^2`。
- 按逆时针输出：调整四条边的访问次序和方向。
- 任意起点和旋转方向：方向数组方案更容易泛化。
- 矩阵旋转（48）：同样要求准确处理行列坐标和边界。
