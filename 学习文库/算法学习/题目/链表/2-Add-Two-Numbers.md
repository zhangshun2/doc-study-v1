---
schemaVersion: 3
type: "problem"
leetcodeId: 2
slug: "add-two-numbers"
titleCn: "两数相加"
titleEn: "Add Two Numbers"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/add-two-numbers/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "fb53844dfd9f825bf70a94e5cdf18b4ce9020ebc2650e5d837b0bad3d926ead7"
sourceFactsSha256: "76775a3d0b01da90d1f0ae8262accb2dc964bb00b232d178e4dec084c2dfb630"
sourceSectionHashes:
  description: "624582e4733af669ae30ddb8a5db4dbfbf81b9bad1d81ac6c9a70db1e7ace25e"
  examples: "076a13bce312ca5c431d5d5f4b9df533dec4571c6a249b86d95b4f6a1233fbca"
  constraints: "81c6eef27aaabfd18703df6e44255bc60d40209626302cd919bc7716e89a0a88"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "62a8c9467b9ee24982bb927c76877ae3a7d644ce35508ed4683dc77bb842bb5d"
  signature: "ae3970d1ce1e6e5655b597cfeeee3a432263766179fa1ad65e9401f283f992df"
  javaTemplate: "3d2b6ccd1cea8e8f3452725b3df44325713f89dd0daa03d2710a14307e11759e"
primaryPattern: "链表"
topics: ["链表","递归","数学"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Linked List 链表","Recursion 递归"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 2. 两数相加 / Add Two Numbers

> **双轨入口：** [[核心模型/链表/2-Add-Two-Numbers-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`链表`
- 清单优先级：`P0`
- 清单代表标签：`Linked List 链表`、`Recursion 递归`
- LeetCode 当前标签：递归 (Recursion)、链表 (Linked List)、数学 (Math)
- 官方来源：<https://leetcode.cn/problems/add-two-numbers/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`fb53844dfd9f825bf70a94e5cdf18b4ce9020ebc2650e5d837b0bad3d926ead7`
- 主模型：链表同步遍历 + 进位模拟

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你两个 **非空** 的链表，表示两个非负的整数。它们每位数字都是按照 **逆序** 的方式存储的，并且每个节点只能存储 **一位** 数字。

请你将两个数相加，并以相同形式返回一个表示和的链表。

你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.cn/aliyun-lc-upload/uploads/2021/01/02/addtwonumber1.jpg)

```text
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.
```

**示例 2：**

```text
输入：l1 = [0], l2 = [0]
输出：[0]
```

**示例 3：**

```text
输入：l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
输出：[8,9,9,9,0,0,0,1]
```

## 官方约束


- 每个链表中的节点数在范围 `[1, 100]` 内

- `0 <= Node.val <= 9`

- 题目数据保证列表表示的数字不含前导零

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 逆序存储使链表头正好对应十进制最低位。
2. 每一位只需要 `l1` 当前值、`l2` 当前值和上一位进位。
3. 两条链表长度可能不同；遍历条件还必须包含最终的 `carry`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

这就是小学竖式加法从个位向高位进行的过程。逆序链表消除了“先走到尾部”的麻烦。每轮计算：

```text
sum = x + y + carry
当前结果位 = sum % 10
下一轮进位 = sum / 10
```

因为 `x,y <= 9` 且 `carry <= 1`，所以 `sum <= 19`。

## 朴素方案：转换成整数后相加

短数字可以把各位拼成整数，相加后再拆分。但题目允许 100 位，远超 `long` 的表示范围。使用 `BigInteger` 虽能避免溢出，却绕开了链表与进位这一考点，并需要额外的字符串转换。

- 时间复杂度：仍为 `O(m+n)`，但有转换常数。
- 空间复杂度：`O(m+n)`。
- 问题：基本整数会溢出，不是通用解法。

## 最优方案：逐节点模拟进位

使用虚拟头节点 `dummy` 简化结果链表首节点的创建。只要 `l1`、`l2` 或 `carry` 仍有内容，就生成一个结果节点。某条链表已经结束时，该位按 `0` 处理。

### 正确性与不变量

进入第 `k` 轮时，结果链表已经正确保存了答案最低的 `k` 位，`carry` 是这 `k` 位运算产生、需要交给第 `k+1` 位的唯一进位。本轮按十进制加法规则产生第 `k` 位与新进位，因此不变量继续成立。所有节点和进位处理完后，结果的每一位都正确。

- 时间复杂度：`O(max(m,n))`。
- 空间复杂度：除返回链表外为 `O(1)`；返回链表占 `O(max(m,n))`。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        int carry = 0;

        while (l1 != null || l2 != null || carry != 0) {
            int x = l1 == null ? 0 : l1.val;
            int y = l2 == null ? 0 : l2.val;
            int sum = x + y + carry;

            tail.next = new ListNode(sum % 10);
            tail = tail.next;
            carry = sum / 10;

            if (l1 != null) {
                l1 = l1.next;
            }
            if (l2 != null) {
                l2 = l2.next;
            }
        }
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
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        int carry = 0;

        while (l1 != null || l2 != null || carry != 0) {
            int x = l1 == null ? 0 : l1.val;
            int y = l2 == null ? 0 : l2.val;
            int sum = x + y + carry;

            tail.next = new ListNode(sum % 10);
            tail = tail.next;
            carry = sum / 10;

            if (l1 != null) {
                l1 = l1.next;
            }
            if (l2 != null) {
                l2 = l2.next;
            }
        }
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
        print(solution.addTwoNumbers(
                list(new int[]{2, 4, 3}), list(new int[]{5, 6, 4})));
        print(solution.addTwoNumbers(
                list(new int[]{9, 9, 9}), list(new int[]{1})));
    }
}
```

## 边界与易错点

- 循环条件不能只有 `l1 != null && l2 != null`，否则较长链表的剩余部分会丢失。
- 循环条件也不能漏掉 `carry != 0`，例如 `999 + 1` 需要额外节点 `1`。
- 结果应新建节点，避免无意修改输入链表。
- 输入是逆序数字；不要把 `[2,4,3]` 误读为 243。

## 可扩展变式

- 数字按正序存储时，可使用栈或递归从低位开始处理。
- 扩展到任意进制时，把 `% 10` 和 `/ 10` 改为 `% base` 与 `/ base`。
- 多个链表相加时，可维护总和与进位，或逐个合并。
