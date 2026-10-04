# LeetCode-234-回文链表

# LeetCode 234 - 回文链表
## 题目描述
**难度：简单**

给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false` 。

### 示例
**示例 1：**

```plain
输入：head = [1,2,2,1]
输出：true
解释：链表为 1 -> 2 -> 2 -> 1，是回文链表
```

**示例 2：**

```plain
输入：head = [1,2]
输出：false
解释：链表为 1 -> 2，不是回文链表
```

**示例 3：**

```plain
输入：head = [1]
输出：true
解释：单节点链表是回文链表
```

### 约束条件
+ 链表中节点数目在范围 `[1, 10^5]` 内
+ `0 <= Node.val <= 9`

**进阶：** 你能否用 O(n) 时间复杂度和 O(1) 空间复杂度解决此题？

## 解题思路
这道题虽然归类在栈专题中，但实际上有多种解法。我们将重点介绍**栈解法**，同时提供其他经典解法作为对比。

### 核心思想：栈 + 快慢指针
使用栈来存储链表的前半部分，然后与后半部分进行比较：

1. **快慢指针定位中点**：找到链表的中间位置
2. **栈存储前半部分**：将前半部分节点值压入栈
3. **比较后半部分**：弹出栈中元素与后半部分逐一比较

### 算法步骤
1. **使用快慢指针找到中点**
2. **将前半部分压入栈**
3. **遍历后半部分，与栈顶元素比较**
4. **所有元素匹配则为回文链表**

### 图解分析
以链表 `[1,2,2,1]` 为例：

```plain
原链表: 1 -> 2 -> 2 -> 1 -> null

步骤1: 快慢指针找中点
slow: 1 -> 2 (停在第2个节点)
fast: 1 -> 2 -> 2 -> 1 -> null (到达末尾)

步骤2: 将前半部分压入栈
遍历到slow位置，将值压入栈
栈: [1, 2] (栈顶是2)

步骤3: 比较后半部分
从slow.next开始遍历: 2 -> 1
- 比较2与栈顶2: 相等，弹出栈顶
- 比较1与栈顶1: 相等，弹出栈顶
栈为空，所有元素匹配

结果: true (是回文链表)
```

以链表 `[1,2,3,2,1]` (奇数长度) 为例：

```plain
原链表: 1 -> 2 -> 3 -> 2 -> 1 -> null

步骤1: 快慢指针找中点
slow: 1 -> 2 -> 3 (停在中间节点)
fast: 1 -> 2 -> 3 -> 2 -> 1 -> null

步骤2: 将前半部分压入栈
遍历到slow位置，将值压入栈
栈: [1, 2] (不包括中间节点3)

步骤3: 比较后半部分
从slow.next开始遍历: 2 -> 1
- 比较2与栈顶2: 相等，弹出栈顶
- 比较1与栈顶1: 相等，弹出栈顶
栈为空，所有元素匹配

结果: true (是回文链表)
```

## 代码实现
### 方法一：栈 + 快慢指针（栈解法）
```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
public class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) {
            return true;
        }
        
        // 使用快慢指针找到中点
        ListNode slow = head;
        ListNode fast = head;
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 将前半部分压入栈，同时移动快慢指针
        while (fast != null && fast.next != null) {
            stack.push(slow.val);
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // 如果链表长度为奇数，跳过中间节点
        if (fast != null) {
            slow = slow.next;
        }
        
        // 比较后半部分与栈中的元素
        while (slow != null) {
            if (stack.isEmpty() || stack.pop() != slow.val) {
                return false;
            }
            slow = slow.next;
        }
        
        return true;
    }
}
```

### 方法二：转换为数组（简单直观）
```java
public class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> vals = new ArrayList<>();
        
        // 将链表值存储到数组中
        ListNode current = head;
        while (current != null) {
            vals.add(current.val);
            current = current.next;
        }
        
        // 使用双指针检查回文
        int left = 0;
        int right = vals.size() - 1;
        
        while (left < right) {
            if (!vals.get(left).equals(vals.get(right))) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
}
```

### 方法三：反转后半部分链表（O(1)空间）
```java
public class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) {
            return true;
        }
        
        // 找到中点
        ListNode slow = head;
        ListNode fast = head;
        
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // 反转后半部分链表
        ListNode secondHalf = reverseList(slow.next);
        
        // 比较前半部分和反转后的后半部分
        ListNode firstHalf = head;
        ListNode secondHalfCopy = secondHalf;
        boolean result = true;
        
        while (secondHalf != null) {
            if (firstHalf.val != secondHalf.val) {
                result = false;
                break;
            }
            firstHalf = firstHalf.next;
            secondHalf = secondHalf.next;
        }
        
        // 恢复链表结构（可选）
        slow.next = reverseList(secondHalfCopy);
        
        return result;
    }
    
    private ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;
        
        while (current != null) {
            ListNode nextNode = current.next;
            current.next = prev;
            prev = current;
            current = nextNode;
        }
        
        return prev;
    }
}
```

### 方法四：递归解法（栈调用）
```java
public class Solution {
    private ListNode frontPointer;
    
    public boolean isPalindrome(ListNode head) {
        frontPointer = head;
        return recursivelyCheck(head);
    }
    
    private boolean recursivelyCheck(ListNode currentNode) {
        if (currentNode != null) {
            if (!recursivelyCheck(currentNode.next)) {
                return false;
            }
            if (currentNode.val != frontPointer.val) {
                return false;
            }
            frontPointer = frontPointer.next;
        }
        return true;
    }
}
```

### 方法五：栈存储全部元素（最直观的栈解法）
```java
public class Solution {
    public boolean isPalindrome(ListNode head) {
        Deque<Integer> stack = new ArrayDeque<>();
        ListNode current = head;
        
        // 将所有元素压入栈
        while (current != null) {
            stack.push(current.val);
            current = current.next;
        }
        
        // 重新遍历链表，与栈中元素比较
        current = head;
        while (current != null) {
            if (stack.pop() != current.val) {
                return false;
            }
            current = current.next;
        }
        
        return true;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **栈 + 快慢指针**：O(n)，遍历链表一次
+ **转换为数组**：O(n)，遍历链表一次，数组比较一次
+ **反转后半部分**：O(n)，遍历链表和反转操作
+ **递归解法**：O(n)，递归调用n次
+ **栈存储全部**：O(n)，遍历链表两次

### 空间复杂度
+ **栈 + 快慢指针**：O(n/2) = O(n)，栈存储前半部分
+ **转换为数组**：O(n)，数组存储所有元素
+ **反转后半部分**：O(1)，只使用常数额外空间
+ **递归解法**：O(n)，递归调用栈的深度
+ **栈存储全部**：O(n)，栈存储所有元素

## 关键点总结
### 1. 栈解法的核心思想
+ **对称性利用**：回文的对称特性天然适合栈的LIFO特性
+ **空间优化**：只存储一半元素，减少空间使用
+ **快慢指针配合**：精确定位链表中点

### 2. 快慢指针的巧妙应用
+ **中点定位**：fast走两步，slow走一步
+ **奇偶处理**：通过fast的最终位置判断链表长度奇偶性
+ **边界处理**：正确处理空链表和单节点链表

### 3. 不同解法的权衡
+ **栈解法**：思路清晰，空间复杂度O(n)
+ **数组解法**：最直观，但需要额外数组空间
+ **反转解法**：空间最优O(1)，但会修改原链表结构
+ **递归解法**：代码简洁，但递归深度可能导致栈溢出

### 4. 边界情况处理
+ **空链表**：直接返回true
+ **单节点**：单节点总是回文
+ **两节点**：比较两个节点值
+ **奇偶长度**：正确处理中间节点

## 扩展思考
### 1. 相关问题
+ **回文数**：LeetCode 9（数字回文判断）
+ **验证回文字符串**：LeetCode 125（字符串回文）
+ **回文子串**：LeetCode 647（子串回文计数）
+ **最长回文子串**：LeetCode 5

### 2. 变种问题
+ **删除一个字符后的回文**：允许删除一个字符
+ **回文链表的最长子序列**：找到最长的回文子序列
+ **构造回文链表**：给定数组构造回文链表

### 3. 优化方向
+ **早期终止**：一旦发现不匹配立即返回
+ **内存优化**：使用位运算或其他技巧减少空间
+ **并行处理**：对于超长链表的并行比较

### 4. 实际应用场景
+ **数据验证**：检查数据的对称性
+ **字符串处理**：文本回文检测
+ **算法设计**：回文相关算法的基础
+ **面试题目**：链表和栈结合的经典题目

### 5. 栈在回文问题中的应用模式
```java
// 回文检测的栈模式模板
public boolean isPalindrome(数据结构 data) {
    Deque<ElementType> stack = new ArrayDeque<>();
    
    // 1. 将前半部分压入栈
    for (前半部分元素) {
        stack.push(element);
    }
    
    // 2. 比较后半部分与栈中元素
    for (后半部分元素) {
        if (stack.isEmpty() || stack.pop() != element) {
            return false;
        }
    }
    
    return true;
}
```

### 6. 面试要点
+ **多种解法**：能够提供不同时空复杂度的解法
+ **权衡分析**：分析各种解法的优缺点
+ **边界处理**：正确处理各种边界情况
+ **代码质量**：代码简洁、可读性强

### 7. 调试技巧
+ **可视化**：画出链表结构和栈的变化
+ **分步验证**：先测试简单的回文和非回文情况
+ **边界测试**：测试空链表、单节点等边界情况
+ **性能测试**：对比不同解法的实际性能

### 8. 扩展思考
+ **为什么用栈**：栈的LIFO特性与回文的对称性完美匹配
+ **空间优化**：如何在保持栈思想的同时优化空间
+ **时间优化**：如何减少不必要的比较操作
+ **通用性**：这种栈解法如何推广到其他回文问题

这道题虽然看似简单，但展示了栈在处理对称性问题中的强大能力，是理解栈应用的优秀例题！



> 更新: 2025-09-19 00:54:33  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/679ed330b46c5d5fdad5113025f00b93>