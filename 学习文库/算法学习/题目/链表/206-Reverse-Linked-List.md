---
schemaVersion: 3
type: "problem"
leetcodeId: 206
slug: "reverse-linked-list"
titleCn: "反转链表"
titleEn: "Reverse Linked List"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/reverse-linked-list/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "29204268c2d7cc385a2ff0ecd449e039e49bc75396bec596b46015573ba63ac7"
sourceFactsSha256: "96c7cc26276c01c0fc9536730deae9e0ca098b00ffa35ab4f16c9117519e26d3"
sourceSectionHashes:
  description: "7dcc5a70b72d7798e2289a12301ab2f074f28d6845a92fa0f4d8a8bb9a0e8221"
  examples: "c1434896e1a77b075420e6c8c2cc9101be329618395e48a69c7347242642992d"
  constraints: "c8edba821d6484d6561f1481d4213b9419de78b84af78bf49d3bbc8b43e90a18"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "fbc2945614367e85ec03aacadb3529f7bdb94367d1550bad26a6b750388944c9"
  signature: "1303ad6c9f6fd61e36e10cf54f71b0b1f18194c2baef88dae137d292c1764c5c"
  javaTemplate: "a3a325d2b2e01fe12730ac8157ff0300604d13654c56106179616929bb7ce702"
primaryPattern: "链表"
topics: ["链表","递归"]
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
# 206. 反转链表 / Reverse Linked List

> **双轨入口：** [[核心模型/链表/206-Reverse-Linked-List-核心模型.md|核心模型]] · [[建模专题/T0/206-Reverse-Linked-List-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Easy`
- 主归档题型：`链表`
- 清单优先级：`P0`
- 清单代表标签：`Linked List 链表`、`Recursion 递归`
- LeetCode 当前标签：递归 (Recursion)、链表 (Linked List)
- 官方来源：<https://leetcode.cn/problems/reverse-linked-list/>
- 直观建模专题：[在改写方向之前保住下一站](../../建模专题/T0/206-Reverse-Linked-List-直观建模.md)
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`29204268c2d7cc385a2ff0ecd449e039e49bc75396bec596b46015573ba63ac7`
- **主解法**：迭代双指针

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你单链表的头节点 `head` ，请你反转链表，并返回反转后的链表。

## 官方示例


**示例 1：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/02/19/rev1ex1.jpg)

```text
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

**示例 2：**

![Official problem illustration](https://assets.leetcode.com/uploads/2021/02/19/rev1ex2.jpg)

```text
输入：head = [1,2]
输出：[2,1]
```

**示例 3：**

```text
输入：head = []
输出：[]
```

## 官方约束


- 链表中节点的数目范围是 `[0, 5000]`

- `-5000 <= Node.val <= 5000`

**进阶：**链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 改写 `current.next` 前，必须先保存原来的下一个节点，否则会丢失未处理部分。
2. 维护两个区域：已经反转的前缀、尚未处理的后缀。
3. 原头节点最终变成尾节点，其 `next` 应为 `null`。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

单链表每个节点只有一条向后的边。反转一条边 `current -> next` 时，需要把它改成 `current -> previous`，再继续处理原来的 `next`。因此三个引用 `previous`、`current`、`next` 就足够完成原地反转。

## 朴素方案

先把所有节点放入数组或栈，再按逆序重新连接。时间为 `O(n)`，但需要 `O(n)` 额外空间。若只把节点值逆序写回，则并未真正反转节点结构，在要求保留节点身份的扩展场景中不正确。

## 最优方案推导

初始 `previous = null`、`current = head`。循环执行：

1. `next = current.next`，保存后缀入口。
2. `current.next = previous`，反转当前边。
3. `previous = current`，扩展已反转前缀。
4. `current = next`，进入未处理后缀。

当 `current == null` 时，`previous` 指向原尾节点，也就是新头节点。

## 正确性与不变量

每轮开始时：

- `previous` 是已处理前缀反转后的头；这部分连接方向已经正确。
- `current` 是未处理后缀的第一个节点；后缀仍保持原顺序。
- 两部分合计恰好包含原链表全部节点且没有重复。

一轮操作将 `current` 从后缀移到反转前缀头部，不变量保持。循环结束时后缀为空，全部节点都在已反转部分，故 `previous` 是正确的新头。

## 复杂度

- **时间复杂度**：`O(n)`。
- **空间复杂度**：`O(1)`，只使用固定数量引用。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode previous = null;
        ListNode current = head;
        while (current != null) {
            ListNode next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        return previous;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
class ListNode {
    int val;
    ListNode next;

    ListNode() {
    }

    ListNode(int val) {
        this.val = val;
    }

    ListNode(int val, ListNode next) {
        this.val = val;
        this.next = next;
    }
}

class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode previous = null;
        ListNode current = head;
        while (current != null) {
            ListNode next = current.next;
            current.next = previous;
            previous = current;
            current = next;
        }
        return previous;
    }
}

public class Main {
    private static ListNode build(int[] values) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int value : values) {
            tail.next = new ListNode(value);
            tail = tail.next;
        }
        return dummy.next;
    }

    private static void print(ListNode head) {
        System.out.print("[");
        for (ListNode node = head; node != null; node = node.next) {
            System.out.print(node.val);
            if (node.next != null) {
                System.out.print(", ");
            }
        }
        System.out.println("]");
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        print(solution.reverseList(build(new int[]{1, 2, 3, 4, 5})));
        print(solution.reverseList(build(new int[]{1, 2})));
        print(solution.reverseList(null));
    }
}
```

## 边界与易错点

- 空链表和单节点链表无需特殊分支，循环自然处理。
- 必须在改写 `current.next` 之前保存 `next`。
- 返回的是 `previous`，不是已经为 `null` 的 `current`。
- 若链表可能有环，本算法不会终止；应先检测并明确环的处理规则。

## 可扩展变式

- 递归反转：递归反转 `head.next`，再令 `head.next.next = head`，空间为 `O(n)` 调用栈。
- 反转区间 `[left, right]`：使用虚拟头节点定位区间前驱，再做局部头插。
- 每 `k` 个节点一组反转：先检查剩余长度，再逐组反转并连接。
- 回文链表：快慢指针找中点，反转后半段进行比较，之后可恢复结构。
