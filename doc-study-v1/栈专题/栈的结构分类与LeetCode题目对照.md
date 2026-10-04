# 栈的结构分类与LeetCode题目对照

# 栈的结构分类与LeetCode题目对照
## 栈的结构分类概述
栈作为一种基础数据结构，在算法题中有多种应用形式和变种结构。根据使用方式和功能特点，可以分为以下几种主要类型：

| 栈结构类型 | 核心特点 | 主要用途 | 难度等级 |
| --- | --- | --- | --- |
| **基础栈** | 标准LIFO操作 | 括号匹配、逆序处理 | 简单-中等 |
| **单调栈** | 维护单调性质 | 寻找下一个更大/更小元素 | 中等-困难 |
| **双栈** | 两个栈协同工作 | 队列模拟、复杂状态管理 | 中等 |
| **栈+哈希表** | 栈与映射结合 | 快速查找+LIFO特性 | 中等 |
| **递归栈模拟** | 用栈模拟递归 | 树遍历、DFS | 中等 |
| **表达式栈** | 处理运算符优先级 | 计算器、表达式求值 | 中等-困难 |
| **状态栈** | 保存多种状态信息 | 回溯、路径记录 | 中等-困难 |


## 1. 基础栈结构
### 1.1 结构特点
+ **LIFO特性**：后进先出
+ **基本操作**：push、pop、peek、isEmpty
+ **应用场景**：括号匹配、字符串处理、简单状态管理

### 1.2 Java实现示例
```java
public class BasicStackExample {
    /**
     * 基础栈的标准操作示例
     */
    public boolean isValidParentheses(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : s.toCharArray()) {
            // 左括号入栈
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } 
            // 右括号匹配
            else if (c == ')' || c == ']' || c == '}') {
                if (stack.isEmpty()) return false;
                
                char top = stack.pop();
                if ((c == ')' && top != '(') ||
                    (c == ']' && top != '[') ||
                    (c == '}' && top != '{')) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }
    
    /**
     * 字符串解码问题
     */
    public String decodeString(String s) {
        Deque<Integer> countStack = new ArrayDeque<>();
        Deque<StringBuilder> stringStack = new ArrayDeque<>();
        StringBuilder current = new StringBuilder();
        int count = 0;
        
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) {
                count = count * 10 + (c - '0');
            } else if (c == '[') {
                countStack.push(count);
                stringStack.push(current);
                current = new StringBuilder();
                count = 0;
            } else if (c == ']') {
                int repeatCount = countStack.pop();
                StringBuilder temp = current;
                current = stringStack.pop();
                for (int i = 0; i < repeatCount; i++) {
                    current.append(temp);
                }
            } else {
                current.append(c);
            }
        }
        
        return current.toString();
    }
}
```

### 1.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 20 | Valid Parentheses | Easy | [LeetCode 20](https://leetcode.com/problems/valid-parentheses/) | 基础栈操作、括号匹配 |
| 394 | Decode String | Medium | [LeetCode 394](https://leetcode.com/problems/decode-string/) | 嵌套结构处理 |
| 1047 | Remove All Adjacent Duplicates In String | Easy | [LeetCode 1047](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) | 栈的消除操作 |
| 1209 | Remove All Adjacent Duplicates in String II | Medium | [LeetCode 1209](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/) | 计数栈 |
| 71 | Simplify Path | Medium | [LeetCode 71](https://leetcode.com/problems/simplify-path/) | 路径处理 |


## 2. 单调栈结构
### 2.1 结构特点
+ **单调性**：栈内元素保持单调递增或递减
+ **核心思想**：维护栈的单调性，找到每个元素的"下一个更大/更小"元素
+ **应用场景**：寻找边界、计算面积、温度问题

### 2.2 Java实现示例
```java
public class MonotonicStackExample {
    /**
     * 下一个更大元素（单调递减栈）
     */
    public int[] nextGreaterElement(int[] nums) {
        int[] result = new int[nums.length];
        Deque<Integer> stack = new ArrayDeque<>(); // 存储索引
        
        // 从右到左遍历
        for (int i = nums.length - 1; i >= 0; i--) {
            // 维护单调递减栈
            while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
                stack.pop();
            }
            
            result[i] = stack.isEmpty() ? -1 : nums[stack.peek()];
            stack.push(i);
        }
        
        return result;
    }
    
    /**
     * 柱状图中最大的矩形
     */
    public int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0;
        
        for (int i = 0; i <= heights.length; i++) {
            int currentHeight = (i == heights.length) ? 0 : heights[i];
            
            // 当前高度小于栈顶高度时，计算面积
            while (!stack.isEmpty() && heights[stack.peek()] > currentHeight) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            
            stack.push(i);
        }
        
        return maxArea;
    }
    
    /**
     * 接雨水问题
     */
    public int trap(int[] height) {
        Deque<Integer> stack = new ArrayDeque<>();
        int water = 0;
        
        for (int i = 0; i < height.length; i++) {
            while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
                int bottom = stack.pop();
                if (stack.isEmpty()) break;
                
                int distance = i - stack.peek() - 1;
                int boundedHeight = Math.min(height[i], height[stack.peek()]) - height[bottom];
                water += distance * boundedHeight;
            }
            stack.push(i);
        }
        
        return water;
    }
}
```

### 2.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 496 | Next Greater Element I | Easy | [LeetCode 496](https://leetcode.com/problems/next-greater-element-i/) | 基础单调栈 |
| 503 | Next Greater Element II | Medium | [LeetCode 503](https://leetcode.com/problems/next-greater-element-ii/) | 循环数组单调栈 |
| 739 | Daily Temperatures | Medium | [LeetCode 739](https://leetcode.com/problems/daily-temperatures/) | 单调栈应用 |
| 84 | Largest Rectangle in Histogram | Hard | [LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | 单调栈计算面积 |
| 85 | Maximal Rectangle | Hard | [LeetCode 85](https://leetcode.com/problems/maximal-rectangle/) | 二维单调栈 |
| 42 | Trapping Rain Water | Hard | [LeetCode 42](https://leetcode.com/problems/trapping-rain-water/) | 单调栈接雨水 |
| 316 | Remove Duplicate Letters | Medium | [LeetCode 316](https://leetcode.com/problems/remove-duplicate-letters/) | 单调栈+贪心 |


## 3. 双栈结构
### 3.1 结构特点
+ **协同工作**：两个栈配合完成复杂操作
+ **功能分离**：不同栈负责不同功能
+ **应用场景**：队列模拟、最值查询、状态管理

### 3.2 Java实现示例
```java
public class DoubleStackExample {
    /**
     * 用两个栈实现队列
     */
    class MyQueue {
        private Deque<Integer> inStack;
        private Deque<Integer> outStack;
        
        public MyQueue() {
            inStack = new ArrayDeque<>();
            outStack = new ArrayDeque<>();
        }
        
        public void push(int x) {
            inStack.push(x);
        }
        
        public int pop() {
            if (outStack.isEmpty()) {
                while (!inStack.isEmpty()) {
                    outStack.push(inStack.pop());
                }
            }
            return outStack.pop();
        }
        
        public int peek() {
            if (outStack.isEmpty()) {
                while (!inStack.isEmpty()) {
                    outStack.push(inStack.pop());
                }
            }
            return outStack.peek();
        }
        
        public boolean empty() {
            return inStack.isEmpty() && outStack.isEmpty();
        }
    }
    
    /**
     * 包含min函数的栈
     */
    class MinStack {
        private Deque<Integer> dataStack;
        private Deque<Integer> minStack;
        
        public MinStack() {
            dataStack = new ArrayDeque<>();
            minStack = new ArrayDeque<>();
        }
        
        public void push(int val) {
            dataStack.push(val);
            if (minStack.isEmpty() || val <= minStack.peek()) {
                minStack.push(val);
            }
        }
        
        public void pop() {
            int val = dataStack.pop();
            if (val == minStack.peek()) {
                minStack.pop();
            }
        }
        
        public int top() {
            return dataStack.peek();
        }
        
        public int getMin() {
            return minStack.peek();
        }
    }
}
```

### 3.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 232 | Implement Queue using Stacks | Easy | [LeetCode 232](https://leetcode.com/problems/implement-queue-using-stacks/) | 双栈模拟队列 |
| 225 | Implement Stack using Queues | Easy | [LeetCode 225](https://leetcode.com/problems/implement-stack-using-queues/) | 队列模拟栈 |
| 155 | Min Stack | Easy | [LeetCode 155](https://leetcode.com/problems/min-stack/) | 辅助栈维护最值 |
| 716 | Max Stack | Hard | [LeetCode 716](https://leetcode.com/problems/max-stack/) | 双栈+双向链表 |


## 4. 栈+哈希表结构
### 4.1 结构特点
+ **快速查找**：哈希表提供O(1)查找
+ **LIFO特性**：栈提供后进先出特性
+ **应用场景**：频率统计、快速匹配、状态查询

### 4.2 Java实现示例
```java
public class StackWithHashExample {
    /**
     * 下一个更大元素I（使用哈希表优化）
     */
    public int[] nextGreaterElement(int[] nums1, int[] nums2) {
        Map<Integer, Integer> nextGreaterMap = new HashMap<>();
        Deque<Integer> stack = new ArrayDeque<>();
        
        // 构建nums2中每个元素的下一个更大元素映射
        for (int num : nums2) {
            while (!stack.isEmpty() && stack.peek() < num) {
                nextGreaterMap.put(stack.pop(), num);
            }
            stack.push(num);
        }
        
        // 查询nums1中每个元素的结果
        int[] result = new int[nums1.length];
        for (int i = 0; i < nums1.length; i++) {
            result[i] = nextGreaterMap.getOrDefault(nums1[i], -1);
        }
        
        return result;
    }
    
    /**
     * 有效的括号（使用哈希表优化匹配）
     */
    public boolean isValid(String s) {
        Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : s.toCharArray()) {
            if (pairs.containsValue(c)) {
                // 左括号
                stack.push(c);
            } else if (pairs.containsKey(c)) {
                // 右括号
                if (stack.isEmpty() || stack.pop() != pairs.get(c)) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }
}
```

### 4.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 496 | Next Greater Element I | Easy | [LeetCode 496](https://leetcode.com/problems/next-greater-element-i/) | 栈+哈希表优化 |
| 20 | Valid Parentheses | Easy | [LeetCode 20](https://leetcode.com/problems/valid-parentheses/) | 哈希表优化匹配 |
| 1249 | Minimum Remove to Make Valid Parentheses | Medium | [LeetCode 1249](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) | 栈+集合 |


## 5. 递归栈模拟结构
### 5.1 结构特点
+ **递归转迭代**：用栈模拟系统调用栈
+ **状态保存**：保存递归过程中的状态信息
+ **应用场景**：树遍历、图搜索、深度优先搜索

### 5.2 Java实现示例
```java
public class RecursionStackExample {
    /**
     * 二叉树前序遍历（迭代版本）
     */
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            result.add(node.val);
            
            // 先压右子树，再压左子树
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
        
        return result;
    }
    
    /**
     * 二叉树中序遍历（迭代版本）
     */
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;
        
        while (current != null || !stack.isEmpty()) {
            // 一直向左走
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            // 处理栈顶节点
            current = stack.pop();
            result.add(current.val);
            current = current.right;
        }
        
        return result;
    }
    
    /**
     * 图的深度优先搜索
     */
    public boolean hasPath(int[][] graph, int start, int target) {
        boolean[] visited = new boolean[graph.length];
        Deque<Integer> stack = new ArrayDeque<>();
        
        stack.push(start);
        
        while (!stack.isEmpty()) {
            int node = stack.pop();
            
            if (node == target) return true;
            
            if (!visited[node]) {
                visited[node] = true;
                
                // 添加所有邻居节点
                for (int neighbor : graph[node]) {
                    if (!visited[neighbor]) {
                        stack.push(neighbor);
                    }
                }
            }
        }
        
        return false;
    }
}
```

### 5.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 144 | Binary Tree Preorder Traversal | Easy | [LeetCode 144](https://leetcode.com/problems/binary-tree-preorder-traversal/) | 前序遍历迭代 |
| 94 | Binary Tree Inorder Traversal | Easy | [LeetCode 94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | 中序遍历迭代 |
| 145 | Binary Tree Postorder Traversal | Easy | [LeetCode 145](https://leetcode.com/problems/binary-tree-postorder-traversal/) | 后序遍历迭代 |
| 200 | Number of Islands | Medium | [LeetCode 200](https://leetcode.com/problems/number-of-islands/) | DFS迭代实现 |
| 695 | Max Area of Island | Medium | [LeetCode 695](https://leetcode.com/problems/max-area-of-island/) | DFS计算面积 |


## 6. 表达式栈结构
### 6.1 结构特点
+ **运算符优先级**：处理不同优先级的运算符
+ **双栈协作**：操作数栈+操作符栈
+ **应用场景**：计算器、表达式求值、编译器

### 6.2 Java实现示例
```java
public class ExpressionStackExample {
    /**
     * 基本计算器（支持加减乘除）
     */
    public int calculate(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        char operator = '+';
        int num = 0;
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            }
            
            if (c == '+' || c == '-' || c == '*' || c == '/' || i == s.length() - 1) {
                switch (operator) {
                    case '+': stack.push(num); break;
                    case '-': stack.push(-num); break;
                    case '*': stack.push(stack.pop() * num); break;
                    case '/': stack.push(stack.pop() / num); break;
                }
                operator = c;
                num = 0;
            }
        }
        
        return stack.stream().mapToInt(Integer::intValue).sum();
    }
    
    /**
     * 支持括号的计算器
     */
    public int calculateWithParentheses(String s) {
        Deque<Integer> operands = new ArrayDeque<>();
        Deque<Character> operators = new ArrayDeque<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (Character.isDigit(c)) {
                int num = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                i--; // 回退一位
                operands.push(num);
            } else if (c == '(') {
                operators.push(c);
            } else if (c == ')') {
                while (!operators.isEmpty() && operators.peek() != '(') {
                    operands.push(applyOperation(operators.pop(), operands.pop(), operands.pop()));
                }
                operators.pop(); // 移除 '('
            } else if (c == '+' || c == '-' || c == '*' || c == '/') {
                while (!operators.isEmpty() && hasPrecedence(c, operators.peek())) {
                    operands.push(applyOperation(operators.pop(), operands.pop(), operands.pop()));
                }
                operators.push(c);
            }
        }
        
        while (!operators.isEmpty()) {
            operands.push(applyOperation(operators.pop(), operands.pop(), operands.pop()));
        }
        
        return operands.pop();
    }
    
    private boolean hasPrecedence(char op1, char op2) {
        if (op2 == '(' || op2 == ')') return false;
        if ((op1 == '*' || op1 == '/') && (op2 == '+' || op2 == '-')) return false;
        return true;
    }
    
    private int applyOperation(char op, int b, int a) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
        }
        return 0;
    }
}
```

### 6.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 224 | Basic Calculator | Hard | [LeetCode 224](https://leetcode.com/problems/basic-calculator/) | 括号+加减法 |
| 227 | Basic Calculator II | Medium | [LeetCode 227](https://leetcode.com/problems/basic-calculator-ii/) | 四则运算 |
| 772 | Basic Calculator III | Hard | [LeetCode 772](https://leetcode.com/problems/basic-calculator-iii/) | 完整计算器 |
| 150 | Evaluate Reverse Polish Notation | Medium | [LeetCode 150](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | 后缀表达式 |


## 7. 状态栈结构
### 7.1 结构特点
+ **多状态管理**：同时保存多种状态信息
+ **回溯支持**：支持状态回退和恢复
+ **应用场景**：路径搜索、游戏状态、解析器

### 7.2 Java实现示例
```java
public class StateStackExample {
    /**
     * 二叉树的所有路径
     */
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> nodeStack = new ArrayDeque<>();
        Deque<String> pathStack = new ArrayDeque<>();
        
        nodeStack.push(root);
        pathStack.push(String.valueOf(root.val));
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            String path = pathStack.pop();
            
            // 叶子节点
            if (node.left == null && node.right == null) {
                result.add(path);
            }
            
            if (node.left != null) {
                nodeStack.push(node.left);
                pathStack.push(path + "->" + node.left.val);
            }
            
            if (node.right != null) {
                nodeStack.push(node.right);
                pathStack.push(path + "->" + node.right.val);
            }
        }
        
        return result;
    }
    
    /**
     * 路径总和II
     */
    public List<List<Integer>> pathSum(TreeNode root, int targetSum) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> nodeStack = new ArrayDeque<>();
        Deque<List<Integer>> pathStack = new ArrayDeque<>();
        Deque<Integer> sumStack = new ArrayDeque<>();
        
        nodeStack.push(root);
        pathStack.push(Arrays.asList(root.val));
        sumStack.push(root.val);
        
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            List<Integer> path = pathStack.pop();
            int currentSum = sumStack.pop();
            
            if (node.left == null && node.right == null && currentSum == targetSum) {
                result.add(new ArrayList<>(path));
            }
            
            if (node.left != null) {
                nodeStack.push(node.left);
                List<Integer> newPath = new ArrayList<>(path);
                newPath.add(node.left.val);
                pathStack.push(newPath);
                sumStack.push(currentSum + node.left.val);
            }
            
            if (node.right != null) {
                nodeStack.push(node.right);
                List<Integer> newPath = new ArrayList<>(path);
                newPath.add(node.right.val);
                pathStack.push(newPath);
                sumStack.push(currentSum + node.right.val);
            }
        }
        
        return result;
    }
}
```

### 7.3 对应LeetCode题目
| 题号 | 题目名称 | 难度 | 链接 | 核心考点 |
| --- | --- | --- | --- | --- |
| 257 | Binary Tree Paths | Easy | [LeetCode 257](https://leetcode.com/problems/binary-tree-paths/) | 路径状态保存 |
| 113 | Path Sum II | Medium | [LeetCode 113](https://leetcode.com/problems/path-sum-ii/) | 多状态栈 |
| 129 | Sum Root to Leaf Numbers | Medium | [LeetCode 129](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | 数值状态累积 |
| 988 | Smallest String Starting From Leaf | Medium | [LeetCode 988](https://leetcode.com/problems/smallest-string-starting-from-leaf/) | 字符串状态管理 |


## 栈结构选择指南
### 1. 问题类型与栈结构对应关系
| 问题特征 | 推荐栈结构 | 原因 |
| --- | --- | --- |
| 括号/标签匹配 | 基础栈 | 简单的LIFO特性即可 |
| 寻找下一个更大/更小元素 | 单调栈 | 维护单调性，快速找到边界 |
| 需要快速查找 | 栈+哈希表 | 结合O(1)查找和LIFO特性 |
| 模拟递归过程 | 递归栈模拟 | 显式管理调用栈 |
| 表达式计算 | 表达式栈 | 处理运算符优先级 |
| 需要最值查询 | 双栈 | 辅助栈维护最值 |
| 路径/状态回溯 | 状态栈 | 保存多种状态信息 |


### 2. 复杂度分析
| 栈结构类型 | 时间复杂度 | 空间复杂度 | 适用数据规模 |
| --- | --- | --- | --- |
| 基础栈 | O(n) | O(n) | 小到大规模 |
| 单调栈 | O(n) | O(n) | 中到大规模 |
| 双栈 | O(n) | O(n) | 中等规模 |
| 栈+哈希表 | O(n) | O(n) | 中到大规模 |
| 表达式栈 | O(n) | O(n) | 小到中等规模 |
| 状态栈 | O(n) | O(n×k) | 小到中等规模 |


### 3. 实战建议
#### 3.1 选择原则
1. **简单优先**：能用基础栈解决的不用复杂结构
2. **性能考虑**：大数据量时优先考虑单调栈
3. **功能需求**：根据具体功能需求选择合适结构
4. **空间限制**：空间敏感时避免多栈结构

#### 3.2 常见陷阱
+ **空栈检查**：操作前必须检查栈是否为空
+ **索引越界**：使用索引时注意边界检查
+ **状态同步**：多栈结构要保持状态同步
+ **内存泄漏**：及时清理不需要的栈元素

通过掌握这些不同的栈结构类型和对应的LeetCode题目，您可以更系统地学习和应用栈这一重要的数据结构！



> 更新: 2025-09-19 00:54:49  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/92516d23a48c77ffb84f3be7597005f3>