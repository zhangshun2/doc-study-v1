---
schemaVersion: 3
type: "core-model"
leetcodeId: 48
slug: "rotate-image"
titleCn: "旋转图像"
titleEn: "Rotate Image"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/rotate-image/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "c5e4567f556095615a3fc8b13a32ee1cba11ec37e17098e687c754d8f85ebd98"
primaryPattern: "矩阵与模拟"
topics: ["矩阵与模拟", "数组", "数学", "矩阵"]
priority: "P1"
problemPath: "题目/矩阵与模拟/48-Rotate-Image.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 48. 旋转图像：核心模型

> **双轨阅读：** [[题目/矩阵与模拟/48-Rotate-Image.md|标准题解]]

## 一句话本质

两步变换的坐标效果： 转置：(row,column) -> (column,row) 行反转：(column,row) -> (column,n-1-row) 组合后正好是顺时针旋转映射。每一步都可以通过成对交换在原矩阵内完成。

## 直观画面与扩题

像按边界剥洋葱，每次完整走完外圈后就缩小尚未处理的矩形。

在本题中，对象是 **四个边界和当前遍历方向**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：两步变换的坐标效果： 转置：(row,column) -> (column,row) 行反转：(column,row) -> (column,n-1-row) 组合后正好是顺时针旋转映射。每一步都可以通过成对交换在原矩阵内完成。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 四个边界和当前遍历方向 | 把题目翻译成一条可执行关系：两步变换的坐标效果： 转置：(row,column) -> (column,row) 行反转：(column,row) -> (column,n-1-row) 组合后正好是顺时针旋转映射。 | 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。 | 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。 | 转置阶段结束后，原位置 (r,c) 的元素位于 (c,r)。行反转把该行列号 r 映射到 n-1-r，所以它最终位于 (c,n-1-r)，与顺时针 90 度旋转定义完全一致。 | 转置阶段结束后，原位置 (r,c) 的元素位于 (c,r)。行反转把该行列号 r 映射到 n-1-r，所以它最终位于 (c,n-1-r)，与顺时针 90 度旋转定义完全一致。 |

## 最小演算

官方首例输入：`matrix = [[1,2,3],[4,5,6],[7,8,9]]`，输出：`[[7,4,1],[8,5,2],[9,6,3]]`。

1. **初始状态：** 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。
2. **触发事件：** 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。
3. **结束条件：** 转置阶段结束后，原位置 (r,c) 的元素位于 (c,r)。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

转置阶段结束后，原位置 (r,c) 的元素位于 (c,r)。行反转把该行列号 r 映射到 n-1-r，所以它最终位于 (c,n-1-r)，与顺时针 90 度旋转定义完全一致。所有位置的映射是一一对应，因此没有元素丢失或重复。

## 代码映射

```text
1. 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。
2. 第二阶段对每一行使用左右指针反转。
3. 第一阶段对所有 row < column 的元素交换 matrix[row][column] 与 matrix[column][row]。第二阶段对每一行使用左右指针反转。
```

## 复杂度

- 时间复杂度：O(n^2)，每个元素只参与常数次操作。
- 空间复杂度：O(1)。

## 30 秒识别信号

- 主题型：`矩阵与模拟`
- 切入点：顺时针旋转后的坐标映射为 (row,column) -> (column,n-1-row)。

## 最小反例与易错点

- 转置内层从 column=row+1 开始；包含对角线虽无害，但扫描整个矩阵会把交换做两次而还原。
- 顺时针是“转置 + 行反转”；“转置 + 列反转”得到逆时针旋转。

## 分层入口

- [[题目/矩阵与模拟/48-Rotate-Image.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
