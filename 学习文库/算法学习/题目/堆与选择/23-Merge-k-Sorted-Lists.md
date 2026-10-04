---
schemaVersion: 3
type: "problem"
leetcodeId: 23
slug: "merge-k-sorted-lists"
titleCn: "合并 K 个升序链表"
titleEn: "Merge k Sorted Lists"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/merge-k-sorted-lists/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "6bd72c15d3fbca887d870b15d6cb8c4d064ee4baa59228499129ae11669ef478"
sourceFactsSha256: "1195bc95be14d94554d3e21404f367885286b8f02775e688a1bd285561290c5b"
sourceSectionHashes:
  description: "2dcfc151891f3045ac6c222e84678ec00d8942d9daf833554afe00dd70a17e9d"
  examples: "7a1c116847e23f4dca3c35397a902f084ba23b1f9ef86793a221eaf0d98c36ca"
  constraints: "bcc8d83bce3bd8e6c381695156df12dfed7c28529d145b71d69cb98ae1d05ac5"
  hints: "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
  tags: "e92c64b9e9d79310cf3b2e812fdaa049b20e2376f5c4020f3a7f34e2f355fcb7"
  signature: "a15cc7025e818f6d3ff0ee45c3fd1637a956510eec51b1131498b9cd3930916a"
  javaTemplate: "f7e5742c791cd5f61866f1240432a4299d3ea13ea7251f624070d5fae6d55bff"
primaryPattern: "堆与选择"
topics: ["堆与选择","链表","分治","堆（优先队列）","归并排序","锦标赛排序"]
priority: "P0"
checklistPriorities: ["P0","P2"]
checklistTags: ["Linked List 链表","Heap (Priority Queue) 堆","Divide and Conquer 分治","Merge Sort 归并排序"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 23. 合并 K 个升序链表 / Merge k Sorted Lists

> **双轨入口：** [[核心模型/堆与选择/23-Merge-k-Sorted-Lists-核心模型.md|核心模型]]


## 题目信息

- 官方难度：`Hard`
- 主归档题型：`堆与选择`
- 清单优先级：`P0`、`P2`
- 清单代表标签：`Linked List 链表`、`Heap (Priority Queue) 堆`、`Divide and Conquer 分治`、`Merge Sort 归并排序`
- LeetCode 当前标签：链表 (Linked List)、分治 (Divide and Conquer)、堆（优先队列） (Heap (Priority Queue))、归并排序 (Merge Sort)、锦标赛排序
- 官方来源：<https://leetcode.cn/problems/merge-k-sorted-lists/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`6bd72c15d3fbca887d870b15d6cb8c4d064ee4baa59228499129ae11669ef478`
- 主模型：最小堆维护 K 条链表的当前最小头节点

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个链表数组，每个链表都已经按升序排列。

请你将所有链表合并到一个升序链表中，返回合并后的链表。

## 官方示例


**示例 1：**

```text
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
解释：链表数组如下：
[
  1->4->5,
  1->3->4,
  2->6
]
将它们合并到一个有序链表中得到。
1->1->2->3->4->4->5->6
```

**示例 2：**

```text
输入：lists = []
输出：[]
```

**示例 3：**

```text
输入：lists = [[]]
输出：[]
```

## 官方约束


- `k == lists.length`

- `0 <= k <= 10^4`

- `0 <= lists[i].length <= 500`

- `-10^4 <= lists[i][j] <= 10^4`

- `lists[i]` 按 **升序** 排列

- `lists[i].length` 的总和不超过 `10^4`

## 官方额外提示


- 当前官方接口未提供额外算法提示。

## 学习提示（非官方）

1. 任意时刻，全局最小未处理节点一定是某条链表的当前头节点。
2. 最小堆可在 `O(log k)` 内找出并替换这个最小候选。
3. 堆中每条非空链表最多保留一个候选节点，因此堆大小不超过 `k`。
4. 另一条同阶路线是两两分治归并。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 设节点总数为 `N`，目标复杂度应达到 `O(N log k)`。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

两链表归并时比较两个头；K 条链表时需要在最多 K 个头中选最小。最小堆正是动态维护这组候选的结构：弹出某节点后，只有它所在链表的下一个节点会成为新候选，因此只需压入一个后继。

## 朴素方案

**收集全部节点值再排序**：遍历所有节点，把值放入数组，排序后新建链表。

- 时间复杂度：`O(N log N)`。
- 空间复杂度：`O(N)`。

**逐条合并**：从空结果开始依次合并每条链表。结果链表会反复被扫描，极端情况下可到 `O(Nk)`。

## 最优方案：最小堆多路归并

先把所有非空链表头加入优先队列。重复弹出最小节点接到答案末尾；若该节点有后继，就把后继加入堆，直至堆空。

### 正确性与不变量

每轮开始时，堆中恰好包含每条尚有未处理节点的链表的第一个未处理节点。由于每条链表有序，其余节点都不小于自己的头，所以所有未处理节点的全局最小值一定是堆顶。弹出堆顶并加入其后继后，不变量恢复。归纳可知输出顺序非递减，且每个原节点恰好输出一次。

- 时间复杂度：`O(N log k)`；每个节点入堆、出堆各一次。
- 空间复杂度：`O(k)` 堆空间，不计返回链表。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
                Comparator.comparingInt(node -> node.val));

        for (ListNode head : lists) {
            if (head != null) {
                minHeap.offer(head);
            }
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            tail.next = smallest;
            tail = tail.next;
            if (smallest.next != null) {
                minHeap.offer(smallest.next);
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
import java.util.Comparator;
import java.util.PriorityQueue;

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
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> minHeap = new PriorityQueue<>(
                Comparator.comparingInt(node -> node.val));

        for (ListNode head : lists) {
            if (head != null) {
                minHeap.offer(head);
            }
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!minHeap.isEmpty()) {
            ListNode smallest = minHeap.poll();
            tail.next = smallest;
            tail = tail.next;
            if (smallest.next != null) {
                minHeap.offer(smallest.next);
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
        ListNode[] lists = {
                list(new int[]{1, 4, 5}),
                list(new int[]{1, 3, 4}),
                list(new int[]{2, 6})
        };
        print(solution.mergeKLists(lists));
        print(solution.mergeKLists(new ListNode[0]));
    }
}
```

## 边界与易错点

- `lists` 可为空数组，元素也可为 `null`；`PriorityQueue` 不接受 `null`。
- 比较器不要写 `a.val - b.val`，通用数据范围下可能整数溢出；使用 `Integer.compare` 或 `comparingInt`。
- 弹出节点后应加入 `smallest.next`，而不是再次加入当前节点。
- 代码复用并重新连接原节点；若输入不可变，需要复制节点。

## 可扩展变式

- 分治两两归并同样是 `O(N log k)`，额外空间可做到 `O(log k)` 递归栈，常数往往较好。
- K 个有序数组、多个有序日志流都可使用相同多路归并模型。
- 若数据流无限，应只在堆中保存每个流的当前元素，并设计阻塞或结束协议。
