---
schemaVersion: 3
type: "problem"
leetcodeId: 48
slug: "rotate-image"
titleCn: "旋转图像"
titleEn: "Rotate Image"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/rotate-image/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "ef47e808bc66c76fc756e0ef1108d71f626b2b4d21fc268f6ebd049d9a28ea0a"
sourceFactsSha256: "c5e4567f556095615a3fc8b13a32ee1cba11ec37e17098e687c754d8f85ebd98"
sourceSectionHashes:
  description: "ecba824537ca67455ae16d70d8a5cc717ad4cde422fcbcba53bd4a3e11cd0094"
  examples: "954b5051be874ec978f32ee50608ae7b327d176b1f6eb07517f1b5aa9b43251e"
  constraints: "3e278577d6bcc006d4e7c8d65ac448f7a6b9e0214ae5458b1cf45c06723321fa"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "0320862d6392266bdb12df5cbbd8b4c455d33ddb879a051e0bd2b54a74e32a61"
  signature: "73c74a8a7a0a494f9e53d8b5950f2f915d027d0df844c5c97c8014ac2fca53b7"
  javaTemplate: "e8d1ce79d44aa1cbd36ae5997ce530bc75b533ea924f342cca2d1c26fa4506bb"
primaryPattern: "矩阵与模拟"
topics: ["矩阵与模拟","数组","数学","矩阵"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Matrix 矩阵"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 48. 旋转图像 / Rotate Image

> **双轨入口：** [[核心模型/矩阵与模拟/48-Rotate-Image-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`矩阵与模拟`
- 清单优先级：`P1`
- 清单代表标签：`Matrix 矩阵`
- LeetCode 当前标签：数组 (Array)、数学 (Math)、矩阵 (Matrix)
- 官方来源：<https://leetcode.cn/problems/rotate-image/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`ef47e808bc66c76fc756e0ef1108d71f626b2b4d21fc268f6ebd049d9a28ea0a`
- 主模型：主对角线转置 + 每行反转

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给定一个 *n *× *n* 的二维矩阵 `matrix` 表示一个图像。请你将图像顺时针旋转 90 度。

你必须在**[原地](https://baike.baidu.com/item/%E5%8E%9F%E5%9C%B0%E7%AE%97%E6%B3%95)** 旋转图像，这意味着你需要直接修改输入的二维矩阵。**请不要**使用另一个矩阵来旋转图像。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/08/28/mat1.jpg)

```text
输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[[7,4,1],[8,5,2],[9,6,3]]
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/08/28/mat2.jpg)

```text
输入：matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
输出：[[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]
```

## 官方约束


- `n == matrix.length == matrix[i].length`

- `1 <= n <= 20`

- `-1000 <= matrix[i][j] <= 1000`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 顺时针旋转后的坐标映射为 `(row,column) -> (column,n-1-row)`。
2. 直接按映射逐格写入会覆盖尚未读取的数据。
3. 顺时针 90 度旋转可拆为：沿主对角线转置，然后水平反转每一行。
4. 转置时只交换主对角线一侧，避免同一对元素交换两次。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 必须原地修改，额外空间应为 `O(1)`，不能分配同尺寸辅助矩阵。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

两步变换的坐标效果：

```text
转置：(row,column) -> (column,row)
行反转：(column,row) -> (column,n-1-row)
```

组合后正好是顺时针旋转映射。每一步都可以通过成对交换在原矩阵内完成。

## 朴素方案：辅助矩阵

创建 `rotated[n][n]`，把 `matrix[row][column]` 写到 `rotated[column][n-1-row]`，最后复制回原矩阵。

- 时间复杂度：`O(n^2)`。
- 空间复杂度：`O(n^2)`。
- 局限：违反原地旋转要求。

另一种原地方案是逐层做四个位置的循环交换，可做到 `O(1)` 空间，但下标推导更容易出错。

## 最优方案：转置后逐行反转

第一阶段对所有 `row < column` 的元素交换 `matrix[row][column]` 与 `matrix[column][row]`。第二阶段对每一行使用左右指针反转。

### 正确性与不变量

转置阶段结束后，原位置 `(r,c)` 的元素位于 `(c,r)`。行反转把该行列号 `r` 映射到 `n-1-r`，所以它最终位于 `(c,n-1-r)`，与顺时针 90 度旋转定义完全一致。所有位置的映射是一一对应，因此没有元素丢失或重复。

- 时间复杂度：`O(n^2)`，每个元素只参与常数次操作。
- 空间复杂度：`O(1)`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Arrays;

class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;

        for (int row = 0; row < n; row++) {
            for (int column = row + 1; column < n; column++) {
                int temporary = matrix[row][column];
                matrix[row][column] = matrix[column][row];
                matrix[column][row] = temporary;
            }
        }

        for (int row = 0; row < n; row++) {
            int left = 0;
            int right = n - 1;
            while (left < right) {
                int temporary = matrix[row][left];
                matrix[row][left] = matrix[row][right];
                matrix[row][right] = temporary;
                left++;
                right--;
            }
        }
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.Arrays;

public class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;

        for (int row = 0; row < n; row++) {
            for (int column = row + 1; column < n; column++) {
                int temporary = matrix[row][column];
                matrix[row][column] = matrix[column][row];
                matrix[column][row] = temporary;
            }
        }

        for (int row = 0; row < n; row++) {
            int left = 0;
            int right = n - 1;
            while (left < right) {
                int temporary = matrix[row][left];
                matrix[row][left] = matrix[row][right];
                matrix[row][right] = temporary;
                left++;
                right--;
            }
        }
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int[][] first = {
                {1, 2, 3},
                {4, 5, 6},
                {7, 8, 9}
        };
        solution.rotate(first);
        System.out.println(Arrays.deepToString(first));

        int[][] second = {{1, 2}, {3, 4}};
        solution.rotate(second);
        System.out.println(Arrays.deepToString(second));
    }
}
```

## 边界与易错点

- 转置内层从 `column=row+1` 开始；包含对角线虽无害，但扫描整个矩阵会把交换做两次而还原。
- 顺时针是“转置 + 行反转”；“转置 + 列反转”得到逆时针旋转。
- 方法返回类型是 `void`，答案通过修改 `matrix` 产生。
- `n=1` 时两阶段都不会产生有效交换，矩阵保持不变。

## 可扩展变式

- 逆时针 90 度：转置后反转每一列。
- 旋转 180 度：先上下翻转，再左右翻转。
- 非方阵无法在相同二维数组形状内完成 90 度旋转，通常需要新建 `columns x rows` 矩阵。
- 图像处理中还需考虑像素对象复制、缓存局部性和并行分块。
