---
schemaVersion: 3
type: "core-model"
leetcodeId: 206
slug: "reverse-linked-list"
titleCn: "反转链表"
titleEn: "Reverse Linked List"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/reverse-linked-list/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "96c7cc26276c01c0fc9536730deae9e0ca098b00ffa35ab4f16c9117519e26d3"
primaryPattern: "链表"
topics: ["链表", "递归"]
priority: "P0"
problemPath: "题目/链表/206-Reverse-Linked-List.md"
deepDivePath: "建模专题/T0/206-Reverse-Linked-List-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 206. 反转链表：核心模型

> **双轨阅读：** [[题目/链表/206-Reverse-Linked-List.md|标准题解]] · [[建模专题/T0/206-Reverse-Linked-List-直观建模.md|完整建模]]

## 一句话本质

单链表每个节点只有一条向后的边。反转一条边 current -> next 时，需要把它改成 current -> previous，再继续处理原来的 next。因此三个引用 previous、current、next 就足够完成原地反转。

## 直观画面与扩题

像整理一列只能看见下一节的车厢，改线前必须先记住还没接上的部分。

在本题中，对象是 **节点引用和尚未重新连接的剩余链**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：单链表每个节点只有一条向后的边。反转一条边 current -> next 时，需要把它改成 current -> previous，再继续处理原来的 next。因此三个引用 previous、current、next 就足够完成原地反转。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 节点引用和尚未重新连接的剩余链 | 把题目翻译成一条可执行关系：单链表每个节点只有一条向后的边。反转一条边 current -> next 时，需要把它改成 current -> previous，再继续处理原来的 next。 | next = current.next，保存后缀入口。current.next = previous，反转当前边。 | current.next = previous，反转当前边。 | 每轮开始时： previous 是已处理前缀反转后的头；这部分连接方向已经正确。current 是未处理后缀的第一个节点； | 一轮操作将 current 从后缀移到反转前缀头部，不变量保持。循环结束时后缀为空，全部节点都在已反转部分，故 previous 是正确的新头。 |

## 最小演算

官方首例输入：`head = [1,2,3,4,5]`，输出：`[5,4,3,2,1]`。

1. **初始状态：** next = current.next，保存后缀入口。
2. **触发事件：** current.next = previous，反转当前边。
3. **结束条件：** 一轮操作将 current 从后缀移到反转前缀头部，不变量保持。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮开始时： previous 是已处理前缀反转后的头；这部分连接方向已经正确。

## 代码映射

```text
1. next = current.next，保存后缀入口。
2. current.next = previous，反转当前边。
3. previous = current，扩展已反转前缀。
4. current = next，进入未处理后缀。
```

## 复杂度

- 时间复杂度：O(n)。
- 空间复杂度：O(1)，只使用固定数量引用。

## 30 秒识别信号

- 主题型：`链表`
- 切入点：改写 current.next 前，必须先保存原来的下一个节点，否则会丢失未处理部分。

## 最小反例与易错点

- 空链表和单节点链表无需特殊分支，循环自然处理。
- 必须在改写 current.next 之前保存 next。

## 分层入口

- [[题目/链表/206-Reverse-Linked-List.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/206-Reverse-Linked-List-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]
