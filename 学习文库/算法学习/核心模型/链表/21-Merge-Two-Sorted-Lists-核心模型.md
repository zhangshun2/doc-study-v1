---
schemaVersion: 3
type: "core-model"
leetcodeId: 21
slug: "merge-two-sorted-lists"
titleCn: "合并两个有序链表"
titleEn: "Merge Two Sorted Lists"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/merge-two-sorted-lists/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "54a7bb000fd5f03d786f1ef2019d70e1be81788ccba816e765ab35a3dff78d64"
primaryPattern: "链表"
topics: ["链表", "递归"]
priority: "P0"
problemPath: "题目/链表/21-Merge-Two-Sorted-Lists.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 21. 合并两个有序链表：核心模型

> **双轨阅读：** [[题目/链表/21-Merge-Two-Sorted-Lists.md|标准题解]]

## 一句话本质

因为输入分别有序，全局下一个最小节点只能是两个当前头节点之一。每次选择较小者后，相应链表的下一个节点才成为新候选。这与归并排序的合并阶段完全相同，只是通过修改 next 连接已有节点。

## 直观画面与扩题

像整理一列只能看见下一节的车厢，改线前必须先记住还没接上的部分。

在本题中，对象是 **节点引用和尚未重新连接的剩余链**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：因为输入分别有序，全局下一个最小节点只能是两个当前头节点之一。每次选择较小者后，相应链表的下一个节点才成为新候选。这与归并排序的合并阶段完全相同，只是通过修改 next 连接已有节点。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 节点引用和尚未重新连接的剩余链 | 把题目翻译成一条可执行关系：因为输入分别有序，全局下一个最小节点只能是两个当前头节点之一。 | 使用 dummy 和 tail。当两链表均非空时比较头值，将较小节点挂到 tail.next，随后移动该输入指针和 tail。 | 当两链表均非空时比较头值，将较小节点挂到 tail.next，随后移动该输入指针和 tail。 | 每轮开始时，dummy.next 到 tail 包含两条原链表中已经处理的全部节点，且按非递减顺序排列； | 每轮开始时，dummy.next 到 tail 包含两条原链表中已经处理的全部节点，且按非递减顺序排列； |

## 最小演算

官方首例输入：`l1 = [1,2,4], l2 = [1,3,4]`，输出：`[1,1,2,3,4,4]`。

1. **初始状态：** 使用 dummy 和 tail。
2. **触发事件：** 当两链表均非空时比较头值，将较小节点挂到 tail.next，随后移动该输入指针和 tail。
3. **结束条件：** 每轮开始时，dummy.next 到 tail 包含两条原链表中已经处理的全部节点，且按非递减顺序排列；list1、list2 指向各自未处理部分。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮开始时，dummy.next 到 tail 包含两条原链表中已经处理的全部节点，且按非递减顺序排列；list1、list2 指向各自未处理部分。两个头节点中的较小值是所有未处理节点的最小值，把它接在尾部不会破坏有序性，并且没有漏节点。某一链表为空后，另一部分自身有序且所有值都不小于当前尾值，可以整体拼接。

## 代码映射

```text
1. 使用 dummy 和 tail。
2. 当两链表均非空时比较头值，将较小节点挂到 tail.next，随后移动该输入指针和 tail。
3. 循环后把非空剩余链表直接接上。
```

## 复杂度

- 时间复杂度：O(m+n)。
- 空间复杂度：迭代辅助空间 O(1)；返回链表复用输入节点。

## 30 秒识别信号

- 主题型：`链表`
- 切入点：两个链表头是各自未合并部分的最小值。

## 最小反例与易错点

- 连接节点后要推进被选中的输入指针，否则会形成死循环。
- tail 也必须每轮后移到刚连接的节点。

## 分层入口

- [[题目/链表/21-Merge-Two-Sorted-Lists.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
