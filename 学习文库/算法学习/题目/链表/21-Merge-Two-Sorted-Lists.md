---
schemaVersion: 3
type: "problem"
leetcodeId: 21
slug: "merge-two-sorted-lists"
titleCn: "合并两个有序链表"
titleEn: "Merge Two Sorted Lists"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/merge-two-sorted-lists/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "0a4a3059e9c9ad65708e278629265d321fd6c2ca4999665002a8f2d10bed32e9"
sourceFactsSha256: "54a7bb000fd5f03d786f1ef2019d70e1be81788ccba816e765ab35a3dff78d64"
sourceSectionHashes:
  description: "064bd2023cd517a82195cde8263c9fe0af9dcaba46ac3559065faa01d4a462f5"
  examples: "b7a576a76151fc19c57e56c0734d3e07153435084ac4d808ff701e23ae6eea19"
  constraints: "457fafa52db674e320f61cacc6c796f29dc263cc24916e2506f42ef938892f56"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "fbc2945614367e85ec03aacadb3529f7bdb94367d1550bad26a6b750388944c9"
  signature: "1648790a475bda3ba491f1581f4698e904dc436864e3791b0b44c9d8b47ad848"
  javaTemplate: "24b0488464ae9efefd3f8787df3bc341367c3ffeffcff73dc8bbb5a93ca0d8c5"
primaryPattern: "链表"
topics: ["链表","递归"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Recursion 递归"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 21. 合并两个有序链表 / Merge Two Sorted Lists

> **双轨入口：** [[核心模型/链表/21-Merge-Two-Sorted-Lists-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`链表`
- 清单优先级：`P0`
- 清单代表标签：`Recursion 递归`
- LeetCode 当前标签：递归 (Recursion)、链表 (Linked List)
- 官方来源：<https://leetcode.cn/problems/merge-two-sorted-lists/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`0a4a3059e9c9ad65708e278629265d321fd6c2ca4999665002a8f2d10bed32e9`
- 主模型：双指针归并 + 虚拟头节点

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

将两个升序链表合并为一个新的 **升序** 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg)

```text
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

**示例 2：**

```text
输入：l1 = [], l2 = []
输出：[]
```

**示例 3：**

```text
输入：l1 = [], l2 = [0]
输出：[0]
```

## 官方约束


- 两个链表的节点数目范围是 `[0, 50]`

- `-100 <= Node.val <= 100`

- `l1` 和 `l2` 均按 **非递减顺序** 排列

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 两个链表头是各自未合并部分的最小值。
2. 比较两个头节点，把较小者接到结果尾部，并推进对应链表。
3. 一条链表耗尽后，另一条剩余部分已经有序，可整体接上。
4. 虚拟头节点可消除“结果第一个节点”的特殊分支。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 线性归并可达到 `O(m+n)`；不应把节点收集后再进行 `O((m+n)log(m+n))` 排序。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：list1 = [1,2,4], list2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

### 补充用例 2

```text
输入：list1 = [], list2 = []
输出：[]
```

### 补充用例 3

```text
输入：list1 = [], list2 = [0]
输出：[0]
```

## 核心观察

因为输入分别有序，全局下一个最小节点只能是两个当前头节点之一。每次选择较小者后，相应链表的下一个节点才成为新候选。这与归并排序的合并阶段完全相同，只是通过修改 `next` 连接已有节点。

## 朴素方案：收集、排序、重建

遍历两条链表，把值放入数组，排序后新建链表。

- 时间复杂度：`O((m+n) log(m+n))`。
- 空间复杂度：`O(m+n)`。
- 局限：浪费了输入已排序的信息，也没有复用节点。

## 最优方案：迭代归并

使用 `dummy` 和 `tail`。当两链表均非空时比较头值，将较小节点挂到 `tail.next`，随后移动该输入指针和 `tail`。循环后把非空剩余链表直接接上。

### 正确性与不变量

每轮开始时，`dummy.next` 到 `tail` 包含两条原链表中已经处理的全部节点，且按非递减顺序排列；`list1`、`list2` 指向各自未处理部分。两个头节点中的较小值是所有未处理节点的最小值，把它接在尾部不会破坏有序性，并且没有漏节点。某一链表为空后，另一部分自身有序且所有值都不小于当前尾值，可以整体拼接。

- 时间复杂度：`O(m+n)`。
- 空间复杂度：迭代辅助空间 `O(1)`；返回链表复用输入节点。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                tail.next = list1;
                list1 = list1.next;
            } else {
                tail.next = list2;
                list2 = list2.next;
            }
            tail = tail.next;
        }

        tail.next = list1 != null ? list1 : list2;
        return dummy.next;
    }

    private static ListNode list(int[] values) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int value : values) {
            tail.next = new ListNode(value);
            tail = tail.next;
        }
        return dummy.next;
    }

    private static void print(ListNode head) {
        for (ListNode node = head; node != null; node = node.next) {
            System.out.print(node.val);
            System.out.print(node.next == null ? System.lineSeparator() : " -> ");
        }
    }

    
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class ListNode {
    int val;
    ListNode next;

    ListNode() {}

    ListNode(int val) {
        this.val = val;
    }

    ListNode(int val, ListNode next) {
        this.val = val;
        this.next = next;
    }
}

public class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;

        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                tail.next = list1;
                list1 = list1.next;
            } else {
                tail.next = list2;
                list2 = list2.next;
            }
            tail = tail.next;
        }

        tail.next = list1 != null ? list1 : list2;
        return dummy.next;
    }

    private static ListNode list(int[] values) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int value : values) {
            tail.next = new ListNode(value);
            tail = tail.next;
        }
        return dummy.next;
    }

    private static void print(ListNode head) {
        for (ListNode node = head; node != null; node = node.next) {
            System.out.print(node.val);
            System.out.print(node.next == null ? System.lineSeparator() : " -> ");
        }
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        print(solution.mergeTwoLists(
                list(new int[]{1, 2, 4}), list(new int[]{1, 3, 4})));
        print(solution.mergeTwoLists(null, list(new int[]{0})));
        print(solution.mergeTwoLists(null, null));
    }
}
```

## 边界与易错点

- 连接节点后要推进被选中的输入指针，否则会形成死循环。
- `tail` 也必须每轮后移到刚连接的节点。
- 最后可以整体接入剩余链表，无需逐节点复制。
- 该实现会重排输入节点的 `next`，调用后原链表结构不再独立；若要求输入不可变，需要新建节点。
- 递归写法更短，但空间复杂度会因调用栈变为 `O(m+n)`。

## 可扩展变式

- 合并 K 个有序链表可用最小堆或分治归并。
- 合并有序数组时，从尾部写入可在原数组上完成。
- 归并排序链表可用快慢指针拆分，再复用本题合并函数。
