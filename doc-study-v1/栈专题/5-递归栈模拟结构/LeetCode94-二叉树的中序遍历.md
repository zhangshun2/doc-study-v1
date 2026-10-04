# LeetCode94-二叉树的中序遍历

# LeetCode 94 - 二叉树的中序遍历
## 📋 题目描述
**难度：简单**

给定一个二叉树的根节点 `root` ，返回它的 **中序** 遍历结果。

### 示例
**示例 1：**

```plain
输入：root = [1,null,2,3]
输出：[1,3,2]

    1
     \
      2
     /
    3
```

**示例 2：**

```plain
输入：root = []
输出：[]
```

**示例 3：**

```plain
输入：root = [1]
输出：[1]
```

**示例 4：**

```plain
输入：root = [1,2]
输出：[2,1]

    1
   /
  2
```

**示例 5：**

```plain
输入：root = [1,null,2]
输出：[1,2]

    1
     \
      2
```

### 约束条件
+ 树中节点数目在范围 `[0, 100]` 内
+ `-100 <= Node.val <= 100`

### 进阶要求
递归算法很简单，你可以通过迭代算法来实现吗？

## 🎯 解题思路
### 核心问题分析
这是一个典型的**递归栈模拟问题**。关键在于：

1. 理解递归的本质：系统调用栈的管理
2. 使用显式栈来模拟递归过程
3. 掌握中序遍历的访问顺序：左子树 → 根节点 → 右子树

### 递归栈模拟解法原理
```plain
递归过程分析：
1. 递归调用时：参数和局部变量压入系统栈
2. 递归返回时：从系统栈弹出并恢复状态
3. 栈模拟：用显式栈替代系统调用栈

中序遍历的递归逻辑：
inorder(node):
    if node != null:
        inorder(node.left)   // 递归左子树
        visit(node)          // 访问根节点
        inorder(node.right)  // 递归右子树

栈模拟的关键：
- 用栈保存待处理的节点
- 用状态标记节点的处理阶段
- 模拟递归的压栈和出栈过程
```

### 算法步骤
#### 方法一：简单栈模拟
```plain
1. 初始化栈和结果列表
2. 从根节点开始，一直向左走到底，将路径上的节点入栈
3. 弹出栈顶节点，访问它
4. 转向右子树，重复步骤2-3
5. 直到栈为空且当前节点为空
```

#### 方法二：状态栈模拟
```plain
1. 定义节点状态：未访问、左子树已处理、已完成
2. 将根节点以"未访问"状态入栈
3. 循环处理栈中节点：
   - 未访问：标记为"左子树已处理"，右子树、自己、左子树依次入栈
   - 左子树已处理：访问节点值，标记为已完成
4. 直到栈为空
```

### 图解演示
**示例：root = [1,null,2,3]**

```plain
二叉树结构：
    1
     \
      2
     /
    3

递归过程分析：
inorder(1):
    inorder(null)     // 左子树为空，直接返回
    visit(1)          // 访问节点1，输出1
    inorder(2):       // 递归右子树
        inorder(3):   // 递归左子树
            inorder(null)  // 左子树为空
            visit(3)       // 访问节点3，输出3
            inorder(null)  // 右子树为空
        visit(2)      // 访问节点2，输出2
        inorder(null) // 右子树为空

输出顺序：1 → 3 → 2

栈模拟过程（简单栈方法）：

初始状态：
栈: []
当前节点: 1
结果: []

步骤1: 向左走到底
当前节点1没有左子树，将1入栈
栈: [1]
当前节点: null

步骤2: 弹出并访问
弹出节点1，访问它
栈: []
结果: [1]
转向右子树，当前节点: 2

步骤3: 处理右子树
节点2有左子树，将2入栈，向左走
栈: [2]
当前节点: 3

步骤4: 处理左子树
节点3没有左子树，将3入栈
栈: [2, 3]
当前节点: null

步骤5: 弹出并访问
弹出节点3，访问它
栈: [2]
结果: [1, 3]
转向右子树，当前节点: null

步骤6: 继续弹出
弹出节点2，访问它
栈: []
结果: [1, 3, 2]
转向右子树，当前节点: null

步骤7: 结束
栈为空且当前节点为空，遍历完成
最终结果: [1, 3, 2]
```

## 💻 代码实现
### 方法一：递归解法（基础参考）
```java
import java.util.*;

/**
 * Definition for a binary tree node.
 */
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

public class SolutionRecursive {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }
    
    private void inorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            inorderHelper(node.left, result);   // 递归左子树
            result.add(node.val);               // 访问根节点
            inorderHelper(node.right, result);  // 递归右子树
        }
    }
}
```

### 方法二：简单栈模拟（推荐）
```java
public class SolutionIterativeSimple {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;
        
        while (current != null || !stack.isEmpty()) {
            // 一直向左走到底，将路径上的节点入栈
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            // 弹出栈顶节点并访问
            current = stack.pop();
            result.add(current.val);
            
            // 转向右子树
            current = current.right;
        }
        
        return result;
    }
}
```

### 方法三：状态栈模拟
```java
public class SolutionIterativeWithState {
    
    // 定义节点状态
    private static class NodeState {
        TreeNode node;
        boolean leftProcessed;  // 左子树是否已处理
        
        NodeState(TreeNode node, boolean leftProcessed) {
            this.node = node;
            this.leftProcessed = leftProcessed;
        }
    }
    
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<NodeState> stack = new ArrayDeque<>();
        stack.push(new NodeState(root, false));
        
        while (!stack.isEmpty()) {
            NodeState current = stack.pop();
            
            if (current.leftProcessed) {
                // 左子树已处理，访问当前节点
                result.add(current.node.val);
            } else {
                // 左子树未处理，按中序遍历顺序入栈
                // 注意：栈是后进先出，所以顺序是右、根、左
                
                // 右子树
                if (current.node.right != null) {
                    stack.push(new NodeState(current.node.right, false));
                }
                
                // 根节点（标记为左子树已处理）
                stack.push(new NodeState(current.node, true));
                
                // 左子树
                if (current.node.left != null) {
                    stack.push(new NodeState(current.node.left, false));
                }
            }
        }
        
        return result;
    }
}
```

### 方法四：Morris遍历（空间优化）
```java
public class SolutionMorris {
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        TreeNode current = root;
        
        while (current != null) {
            if (current.left == null) {
                // 没有左子树，直接访问当前节点
                result.add(current.val);
                current = current.right;
            } else {
                // 找到左子树的最右节点
                TreeNode predecessor = current.left;
                while (predecessor.right != null && predecessor.right != current) {
                    predecessor = predecessor.right;
                }
                
                if (predecessor.right == null) {
                    // 建立线索
                    predecessor.right = current;
                    current = current.left;
                } else {
                    // 恢复树结构
                    predecessor.right = null;
                    result.add(current.val);
                    current = current.right;
                }
            }
        }
        
        return result;
    }
}
```

### 方法五：通用递归栈模拟框架
```java
public class SolutionGenericStack {
    
    // 定义操作类型
    private enum Operation {
        VISIT,      // 访问节点
        TRAVERSE    // 遍历节点
    }
    
    private static class StackFrame {
        TreeNode node;
        Operation operation;
        
        StackFrame(TreeNode node, Operation operation) {
            this.node = node;
            this.operation = operation;
        }
    }
    
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<StackFrame> stack = new ArrayDeque<>();
        stack.push(new StackFrame(root, Operation.TRAVERSE));
        
        while (!stack.isEmpty()) {
            StackFrame frame = stack.pop();
            
            if (frame.operation == Operation.VISIT) {
                result.add(frame.node.val);
            } else {
                // 中序遍历：左 → 根 → 右
                // 栈是后进先出，所以入栈顺序是：右 → 根 → 左
                
                if (frame.node.right != null) {
                    stack.push(new StackFrame(frame.node.right, Operation.TRAVERSE));
                }
                
                stack.push(new StackFrame(frame.node, Operation.VISIT));
                
                if (frame.node.left != null) {
                    stack.push(new StackFrame(frame.node.left, Operation.TRAVERSE));
                }
            }
        }
        
        return result;
    }
}
```

### 方法六：函数调用栈精确模拟
```java
public class SolutionExactStackSimulation {
    
    // 模拟递归调用的状态
    private static class CallFrame {
        TreeNode node;
        int phase;  // 0: 开始, 1: 左子树返回, 2: 右子树返回
        
        CallFrame(TreeNode node, int phase) {
            this.node = node;
            this.phase = phase;
        }
    }
    
    public List<Integer> inorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<CallFrame> stack = new ArrayDeque<>();
        stack.push(new CallFrame(root, 0));
        
        while (!stack.isEmpty()) {
            CallFrame frame = stack.peek();
            
            switch (frame.phase) {
                case 0: // 刚进入函数
                    frame.phase = 1;
                    if (frame.node.left != null) {
                        stack.push(new CallFrame(frame.node.left, 0));
                    }
                    break;
                    
                case 1: // 左子树处理完毕
                    result.add(frame.node.val);
                    frame.phase = 2;
                    if (frame.node.right != null) {
                        stack.push(new CallFrame(frame.node.right, 0));
                    }
                    break;
                    
                case 2: // 右子树处理完毕，函数返回
                    stack.pop();
                    break;
            }
        }
        
        return result;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**所有方法：**

+ 每个节点被访问一次
+ 总时间复杂度：O(n)，其中n是树中节点的数量

### 空间复杂度
**递归解法：**

+ 系统调用栈深度等于树的高度
+ 最坏情况（链状树）：O(n)
+ 平均情况（平衡树）：O(log n)

**简单栈模拟：**

+ 显式栈最大深度等于树的高度
+ 最坏情况：O(n)
+ 平均情况：O(log n)

**状态栈模拟：**

+ 栈中最多存储所有节点
+ 空间复杂度：O(n)

**Morris遍历：**

+ 不使用额外栈空间
+ 空间复杂度：O(1)

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的二叉树中序遍历
 */
public class VisualInorderTraversal {
    
    public static List<Integer> inorderTraversalWithVisualization(TreeNode root) {
        System.out.println("🌳 二叉树中序遍历");
        printTree(root);
        System.out.println("=" + "=".repeat(60));
        
        List<Integer> result = new ArrayList<>();
        if (root == null) {
            System.out.println("树为空，返回空列表");
            return result;
        }
        
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode current = root;
        int step = 1;
        
        System.out.println("📊 使用栈模拟递归过程:");
        
        while (current != null || !stack.isEmpty()) {
            System.out.printf("\n步骤 %d:\n", step++);
            
            // 向左走到底
            if (current != null) {
                System.out.printf("  🔍 从节点 %d 开始向左走:\n", current.val);
                
                while (current != null) {
                    System.out.printf("    📥 节点 %d 入栈\n", current.val);
                    stack.push(current);
                    current = current.left;
                    
                    if (current != null) {
                        System.out.printf("    ⬅️ 移动到左子节点 %d\n", current.val);
                    } else {
                        System.out.println("    ⬅️ 到达最左端（null）");
                    }
                }
            }
            
            printStackState(stack);
            
            // 弹出并访问
            if (!stack.isEmpty()) {
                current = stack.pop();
                result.add(current.val);
                System.out.printf("  ✅ 弹出并访问节点 %d\n", current.val);
                System.out.printf("  📝 当前结果: %s\n", result);
                
                // 转向右子树
                current = current.right;
                if (current != null) {
                    System.out.printf("  ➡️ 转向右子树，当前节点: %d\n", current.val);
                } else {
                    System.out.println("  ➡️ 右子树为空");
                }
            }
        }
        
        System.out.println("\n🏆 遍历完成！");
        System.out.println("最终结果: " + result);
        
        return result;
    }
    
    private static void printStackState(Deque<TreeNode> stack) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<TreeNode> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(stackList.get(i).val);
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    private static void printTree(TreeNode root) {
        System.out.println("二叉树结构:");
        if (root == null) {
            System.out.println("  (空树)");
            return;
        }
        
        List<List<String>> levels = new ArrayList<>();
        buildTreeLevels(root, 0, levels);
        
        for (int i = 0; i < levels.size(); i++) {
            System.out.print("  层 " + i + ": ");
            for (String node : levels.get(i)) {
                System.out.print(node + " ");
            }
            System.out.println();
        }
    }
    
    private static void buildTreeLevels(TreeNode node, int level, List<List<String>> levels) {
        if (node == null) return;
        
        if (levels.size() <= level) {
            levels.add(new ArrayList<>());
        }
        
        levels.get(level).add(String.valueOf(node.val));
        
        if (node.left != null || node.right != null) {
            buildTreeLevels(node.left, level + 1, levels);
            buildTreeLevels(node.right, level + 1, levels);
        }
    }
    
    // 构建测试树的辅助方法
    public static TreeNode buildTree(Integer[] values) {
        if (values == null || values.length == 0 || values[0] == null) {
            return null;
        }
        
        TreeNode root = new TreeNode(values[0]);
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        int i = 1;
        while (!queue.isEmpty() && i < values.length) {
            TreeNode current = queue.poll();
            
            if (i < values.length && values[i] != null) {
                current.left = new TreeNode(values[i]);
                queue.offer(current.left);
            }
            i++;
            
            if (i < values.length && values[i] != null) {
                current.right = new TreeNode(values[i]);
                queue.offer(current.right);
            }
            i++;
        }
        
        return root;
    }
    
    public static void main(String[] args) {
        // 测试示例
        Integer[][] testCases = {
            {1, null, 2, 3},
            {1, 2, 3, 4, 5, 6, 7},
            {1, 2, null, 3},
            {5, 3, 8, 2, 4, 7, 9}
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("测试用例 %d: %s\n", i + 1, Arrays.toString(testCases[i]));
            TreeNode root = buildTree(testCases[i]);
            inorderTraversalWithVisualization(root);
            System.out.println("\n" + "=".repeat(70) + "\n");
        }
    }
}
```

### 运行结果示例
```plain
🌳 二叉树中序遍历
二叉树结构:
  层 0: 1 
  层 1: 2 
  层 2: 3 
============================================================

📊 使用栈模拟递归过程:

步骤 1:
  🔍 从节点 1 开始向左走:
    📥 节点 1 入栈
    ⬅️ 到达最左端（null）
  栈状态: [1] (底 -> 顶)
  ✅ 弹出并访问节点 1
  📝 当前结果: [1]
  ➡️ 转向右子树，当前节点: 2

步骤 2:
  🔍 从节点 2 开始向左走:
    📥 节点 2 入栈
    ⬅️ 移动到左子节点 3
    📥 节点 3 入栈
    ⬅️ 到达最左端（null）
  栈状态: [2, 3] (底 -> 顶)
  ✅ 弹出并访问节点 3
  📝 当前结果: [1, 3]
  ➡️ 右子树为空

步骤 3:
  栈状态: [2] (底 -> 顶)
  ✅ 弹出并访问节点 2
  📝 当前结果: [1, 3, 2]
  ➡️ 右子树为空

🏆 遍历完成！
最终结果: [1, 3, 2]
```

## 🧪 测试用例
### 基础功能测试
```java
public class InorderTraversalTest {
    
    private SolutionIterativeSimple solution = new SolutionIterativeSimple();
    
    @Test
    public void testBasicCases() {
        // 示例 1: [1,null,2,3]
        TreeNode root1 = new TreeNode(1);
        root1.right = new TreeNode(2);
        root1.right.left = new TreeNode(3);
        assertEquals(Arrays.asList(1, 3, 2), solution.inorderTraversal(root1));
        
        // 示例 2: 空树
        assertEquals(Arrays.asList(), solution.inorderTraversal(null));
        
        // 示例 3: 单节点
        TreeNode root3 = new TreeNode(1);
        assertEquals(Arrays.asList(1), solution.inorderTraversal(root3));
    }
    
    @Test
    public void testEdgeCases() {
        // 只有左子树
        TreeNode root1 = new TreeNode(1);
        root1.left = new TreeNode(2);
        assertEquals(Arrays.asList(2, 1), solution.inorderTraversal(root1));
        
        // 只有右子树
        TreeNode root2 = new TreeNode(1);
        root2.right = new TreeNode(2);
        assertEquals(Arrays.asList(1, 2), solution.inorderTraversal(root2));
        
        // 链状树（左倾）
        TreeNode root3 = new TreeNode(3);
        root3.left = new TreeNode(2);
        root3.left.left = new TreeNode(1);
        assertEquals(Arrays.asList(1, 2, 3), solution.inorderTraversal(root3));
        
        // 链状树（右倾）
        TreeNode root4 = new TreeNode(1);
        root4.right = new TreeNode(2);
        root4.right.right = new TreeNode(3);
        assertEquals(Arrays.asList(1, 2, 3), solution.inorderTraversal(root4));
    }
    
    @Test
    public void testComplexCases() {
        // 完全二叉树
        TreeNode root1 = new TreeNode(4);
        root1.left = new TreeNode(2);
        root1.right = new TreeNode(6);
        root1.left.left = new TreeNode(1);
        root1.left.right = new TreeNode(3);
        root1.right.left = new TreeNode(5);
        root1.right.right = new TreeNode(7);
        assertEquals(Arrays.asList(1, 2, 3, 4, 5, 6, 7), 
                    solution.inorderTraversal(root1));
        
        // 不平衡树
        TreeNode root2 = new TreeNode(5);
        root2.left = new TreeNode(3);
        root2.right = new TreeNode(8);
        root2.left.left = new TreeNode(2);
        root2.left.right = new TreeNode(4);
        root2.right.right = new TreeNode(9);
        assertEquals(Arrays.asList(2, 3, 4, 5, 8, 9), 
                    solution.inorderTraversal(root2));
    }
}
```

### 算法对比测试
```java
public class AlgorithmComparisonTest {
    
    @Test
    public void compareAllMethods() {
        // 构建测试树
        TreeNode root = buildLargeTree(1000);
        
        // 测试所有方法
        SolutionRecursive solution1 = new SolutionRecursive();
        SolutionIterativeSimple solution2 = new SolutionIterativeSimple();
        SolutionIterativeWithState solution3 = new SolutionIterativeWithState();
        SolutionMorris solution4 = new SolutionMorris();
        SolutionGenericStack solution5 = new SolutionGenericStack();
        
        // 性能测试
        long startTime, endTime;
        
        startTime = System.nanoTime();
        List<Integer> result1 = solution1.inorderTraversal(root);
        endTime = System.nanoTime();
        System.out.printf("递归解法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        startTime = System.nanoTime();
        List<Integer> result2 = solution2.inorderTraversal(root);
        endTime = System.nanoTime();
        System.out.printf("简单栈模拟: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        startTime = System.nanoTime();
        List<Integer> result3 = solution3.inorderTraversal(root);
        endTime = System.nanoTime();
        System.out.printf("状态栈模拟: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        startTime = System.nanoTime();
        List<Integer> result4 = solution4.inorderTraversal(root);
        endTime = System.nanoTime();
        System.out.printf("Morris遍历: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        startTime = System.nanoTime();
        List<Integer> result5 = solution5.inorderTraversal(root);
        endTime = System.nanoTime();
        System.out.printf("通用栈框架: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        assertEquals(result1, result3);
        assertEquals(result1, result4);
        assertEquals(result1, result5);
        
        System.out.println("所有方法结果一致 ✅");
    }
    
    private TreeNode buildLargeTree(int size) {
        if (size <= 0) return null;
        
        TreeNode root = new TreeNode(size / 2);
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        int value = 1;
        while (!queue.isEmpty() && value < size) {
            TreeNode current = queue.poll();
            
            if (value < size) {
                current.left = new TreeNode(value++);
                queue.offer(current.left);
            }
            
            if (value < size) {
                current.right = new TreeNode(value++);
                queue.offer(current.right);
            }
        }
        
        return root;
    }
}
```

### 内存使用测试
```java
public class MemoryUsageTest {
    
    @Test
    public void testMemoryUsage() {
        // 构建深度较大的树
        TreeNode deepTree = buildDeepTree(1000);
        
        Runtime runtime = Runtime.getRuntime();
        
        // 测试递归方法的内存使用
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        try {
            SolutionRecursive solution1 = new SolutionRecursive();
            solution1.inorderTraversal(deepTree);
        } catch (StackOverflowError e) {
            System.out.println("递归方法栈溢出，深度过大");
        }
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("递归方法内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        
        // 测试迭代方法的内存使用
        runtime.gc();
        memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        SolutionIterativeSimple solution2 = new SolutionIterativeSimple();
        solution2.inorderTraversal(deepTree);
        
        memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("迭代方法内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        
        // 测试Morris方法的内存使用
        runtime.gc();
        memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        SolutionMorris solution3 = new SolutionMorris();
        solution3.inorderTraversal(deepTree);
        
        memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("Morris方法内存使用: %d KB\n", (memAfter - memBefore) / 1024);
    }
    
    private TreeNode buildDeepTree(int depth) {
        if (depth <= 0) return null;
        
        TreeNode root = new TreeNode(1);
        TreeNode current = root;
        
        for (int i = 2; i <= depth; i++) {
            current.left = new TreeNode(i);
            current = current.left;
        }
        
        return root;
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 144 - 二叉树的前序遍历
```java
/**
 * 前序遍历：根 → 左 → 右
 */
public class PreorderTraversal {
    
    // 递归解法
    public List<Integer> preorderTraversalRecursive(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }
    
    private void preorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            result.add(node.val);              // 访问根节点
            preorderHelper(node.left, result); // 递归左子树
            preorderHelper(node.right, result);// 递归右子树
        }
    }
    
    // 迭代解法
    public List<Integer> preorderTraversalIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> stack = new ArrayDeque<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            result.add(node.val);
            
            // 先压右子树，再压左子树（栈是后进先出）
            if (node.right != null) {
                stack.push(node.right);
            }
            if (node.left != null) {
                stack.push(node.left);
            }
        }
        
        return result;
    }
}
```

### 2. LeetCode 145 - 二叉树的后序遍历
```java
/**
 * 后序遍历：左 → 右 → 根
 */
public class PostorderTraversal {
    
    // 递归解法
    public List<Integer> postorderTraversalRecursive(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }
    
    private void postorderHelper(TreeNode node, List<Integer> result) {
        if (node != null) {
            postorderHelper(node.left, result); // 递归左子树
            postorderHelper(node.right, result);// 递归右子树
            result.add(node.val);               // 访问根节点
        }
    }
    
    // 迭代解法（双栈）
    public List<Integer> postorderTraversalIterative(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> stack1 = new ArrayDeque<>();
        Deque<TreeNode> stack2 = new ArrayDeque<>();
        
        stack1.push(root);
        
        while (!stack1.isEmpty()) {
            TreeNode node = stack1.pop();
            stack2.push(node);
            
            if (node.left != null) {
                stack1.push(node.left);
            }
            if (node.right != null) {
                stack1.push(node.right);
            }
        }
        
        while (!stack2.isEmpty()) {
            result.add(stack2.pop().val);
        }
        
        return result;
    }
    
    // 迭代解法（单栈+状态）
    public List<Integer> postorderTraversalSingleStack(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode lastVisited = null;
        TreeNode current = root;
        
        while (current != null || !stack.isEmpty()) {
            if (current != null) {
                stack.push(current);
                current = current.left;
            } else {
                TreeNode peekNode = stack.peek();
                if (peekNode.right != null && lastVisited != peekNode.right) {
                    current = peekNode.right;
                } else {
                    result.add(peekNode.val);
                    lastVisited = stack.pop();
                }
            }
        }
        
        return result;
    }
}
```

### 3. LeetCode 102 - 二叉树的层序遍历
```java
/**
 * 层序遍历：逐层从左到右
 */
public class LevelOrderTraversal {
    
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                currentLevel.add(node.val);
                
                if (node.left != null) {
                    queue.offer(node.left);
                }
                if (node.right != null) {
                    queue.offer(node.right);
                }
            }
            
            result.add(currentLevel);
        }
        
        return result;
    }
}
```

### 4. 通用遍历框架
```java
/**
 * 通用的二叉树遍历框架
 */
public class UniversalTraversalFramework {
    
    public enum TraversalType {
        PREORDER,   // 前序
        INORDER,    // 中序
        POSTORDER   // 后序
    }
    
    public List<Integer> traverse(TreeNode root, TraversalType type) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;
        
        Deque<StackFrame> stack = new ArrayDeque<>();
        stack.push(new StackFrame(root, Operation.TRAVERSE));
        
        while (!stack.isEmpty()) {
            StackFrame frame = stack.pop();
            
            if (frame.operation == Operation.VISIT) {
                result.add(frame.node.val);
            } else {
                // 根据遍历类型确定入栈顺序
                switch (type) {
                    case PREORDER:
                        // 前序：根 → 左 → 右，入栈顺序：右 → 左 → 根
                        if (frame.node.right != null) {
                            stack.push(new StackFrame(frame.node.right, Operation.TRAVERSE));
                        }
                        if (frame.node.left != null) {
                            stack.push(new StackFrame(frame.node.left, Operation.TRAVERSE));
                        }
                        stack.push(new StackFrame(frame.node, Operation.VISIT));
                        break;
                        
                    case INORDER:
                        // 中序：左 → 根 → 右，入栈顺序：右 → 根 → 左
                        if (frame.node.right != null) {
                            stack.push(new StackFrame(frame.node.right, Operation.TRAVERSE));
                        }
                        stack.push(new StackFrame(frame.node, Operation.VISIT));
                        if (frame.node.left != null) {
                            stack.push(new StackFrame(frame.node.left, Operation.TRAVERSE));
                        }
                        break;
                        
                    case POSTORDER:
                        // 后序：左 → 右 → 根，入栈顺序：根 → 右 → 左
                        stack.push(new StackFrame(frame.node, Operation.VISIT));
                        if (frame.node.right != null) {
                            stack.push(new StackFrame(frame.node.right, Operation.TRAVERSE));
                        }
                        if (frame.node.left != null) {
                            stack.push(new StackFrame(frame.node.left, Operation.TRAVERSE));
                        }
                        break;
                }
            }
        }
        
        return result;
    }
    
    private enum Operation {
        VISIT, TRAVERSE
    }
    
    private static class StackFrame {
        TreeNode node;
        Operation operation;
        
        StackFrame(TreeNode node, Operation operation) {
            this.node = node;
            this.operation = operation;
        }
    }
}
```

### 5. 递归转迭代的通用方法
```java
/**
 * 递归转迭代的通用方法
 */
public class RecursionToIterationConverter {
    
    /**
     * 将任意递归函数转换为迭代实现的通用框架
     */
    public static class RecursiveFunction<T, R> {
        
        // 定义递归函数的接口
        public interface RecursiveCall<T, R> {
            R call(T input, RecursiveFunction<T, R> self);
        }
        
        private final RecursiveCall<T, R> function;
        
        public RecursiveFunction(RecursiveCall<T, R> function) {
            this.function = function;
        }
        
        // 递归调用
        public R callRecursive(T input) {
            return function.call(input, this);
        }
        
        // 迭代实现
        public R callIterative(T input) {
            Deque<CallFrame<T, R>> stack = new ArrayDeque<>();
            stack.push(new CallFrame<>(input, null));
            
            while (!stack.isEmpty()) {
                CallFrame<T, R> frame = stack.peek();
                
                if (frame.result != null) {
                    // 已有结果，返回给调用者
                    stack.pop();
                    if (!stack.isEmpty()) {
                        stack.peek().handleSubResult(frame.result);
                    } else {
                        return frame.result;
                    }
                } else {
                    // 执行函数逻辑
                    frame.execute(stack, function);
                }
            }
            
            return null;
        }
        
        private static class CallFrame<T, R> {
            T input;
            R result;
            int phase;
            
            CallFrame(T input, R result) {
                this.input = input;
                this.result = result;
                this.phase = 0;
            }
            
            void execute(Deque<CallFrame<T, R>> stack, RecursiveCall<T, R> function) {
                // 这里需要根据具体的递归函数来实现
                // 这是一个简化的框架示例
            }
            
            void handleSubResult(R subResult) {
                // 处理子调用的结果
            }
        }
    }
}
```

## 💡 解题技巧总结
### 1. 递归栈模拟的核心思想
+ **理解递归本质**：递归就是系统自动管理的栈操作
+ **显式栈替代**：用自己的栈来模拟系统调用栈
+ **状态保存**：保存递归调用的参数和局部变量

### 2. 栈模拟的通用步骤
```java
// 递归栈模拟的通用模板
Deque<State> stack = new ArrayDeque<>();
stack.push(initialState);

while (!stack.isEmpty()) {
    State current = stack.pop();
    
    if (current.isBaseCase()) {
        // 处理基础情况
        handleBaseCase(current);
    } else {
        // 将递归调用转换为栈操作
        pushSubproblems(stack, current);
    }
}
```

### 3. 不同模拟方式的选择
+ **简单栈模拟**：适用于简单的递归逻辑
+ **状态栈模拟**：适用于需要记录执行阶段的复杂递归
+ **精确模拟**：完全模拟函数调用的每个阶段

### 4. 优化技巧
+ **Morris遍历**：利用树的空指针实现O(1)空间
+ **状态压缩**：减少栈中存储的状态信息
+ **尾递归优化**：将递归转换为循环

### 5. 应用场景
+ **深度优先搜索**：树和图的遍历
+ **回溯算法**：组合、排列、子集问题
+ **分治算法**：归并排序、快速排序
+ **动态规划**：记忆化搜索

这道题是理解递归栈模拟的绝佳入门例题，掌握了这个技巧后，可以将任何递归算法转换为迭代实现！



> 更新: 2025-09-19 00:54:13  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/35570faef2f44c1c93df2aa170cd03c8>