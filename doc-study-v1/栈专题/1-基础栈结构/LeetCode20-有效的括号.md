# LeetCode20-有效的括号

# LeetCode 20 - 有效的括号
## 📋 题目描述
**难度：简单**

给定一个只包含 `'('`，`')'`，`'{'`，`'}'`，`'['`，`']'` 的字符串 `s`，判断字符串是否有效。

有效字符串需满足：

1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。
3. 每个右括号都有一个对应的相同类型的左括号。

### 示例
**示例 1：**

```plain
输入：s = "()"
输出：true
```

**示例 2：**

```plain
输入：s = "()[]{}"
输出：true
```

**示例 3：**

```plain
输入：s = "(]"
输出：false
```

**示例 4：**

```plain
输入：s = "([)]"
输出：false
```

**示例 5：**

```plain
输入：s = "{[]}"
输出：true
```

### 约束条件
+ `1 <= s.length <= 10^4`
+ `s` 仅由括号 `'()[]{}'` 组成

## 🎯 解题思路
### 核心思想
这是一个**经典的栈应用问题**。括号匹配的本质是：

+ **后进先出（LIFO）**：最后遇到的左括号应该最先被匹配
+ **配对验证**：每个右括号必须与最近的未匹配左括号配对
+ **完全匹配**：所有括号都必须有对应的配对

### 算法步骤
```plain
1. 创建一个空栈
2. 遍历字符串中的每个字符：
   - 如果是左括号 '(', '[', '{'：推入栈中
   - 如果是右括号 ')', ']', '}'：
     * 检查栈是否为空（无匹配的左括号）
     * 弹出栈顶元素，检查是否与当前右括号匹配
     * 如果不匹配，返回 false
3. 遍历结束后，检查栈是否为空
   - 空栈：所有括号都已匹配，返回 true
   - 非空栈：还有未匹配的左括号，返回 false
```

### 图解演示
**示例：s = "([{}])"**

```plain
步骤 1: 遇到 '('
栈状态: ['(']
说明: 左括号入栈

步骤 2: 遇到 '['  
栈状态: ['(', '[']
说明: 左括号入栈

步骤 3: 遇到 '{'
栈状态: ['(', '[', '{']
说明: 左括号入栈

步骤 4: 遇到 '}'
栈状态: ['(', '[']
说明: 右括号 '}' 与栈顶 '{' 匹配，弹出栈顶

步骤 5: 遇到 ']'
栈状态: ['(']
说明: 右括号 ']' 与栈顶 '[' 匹配，弹出栈顶

步骤 6: 遇到 ')'
栈状态: []
说明: 右括号 ')' 与栈顶 '(' 匹配，弹出栈顶

结果: 栈为空，返回 true
```

**反例：s = "([)]"**

```plain
步骤 1: 遇到 '('
栈状态: ['(']

步骤 2: 遇到 '['
栈状态: ['(', '[']

步骤 3: 遇到 ')'
栈状态: ['(', '[']
说明: 右括号 ')' 与栈顶 '[' 不匹配！
结果: 返回 false
```

## 💻 代码实现
### 方法一：使用 Deque 接口（推荐）
```java
import java.util.*;

public class Solution {
    public boolean isValid(String s) {
        // 奇数长度的字符串不可能有效
        if (s.length() % 2 == 1) {
            return false;
        }
        
        // 使用 Deque 作为栈
        Deque<Character> stack = new ArrayDeque<>();
        
        // 遍历字符串中的每个字符
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                // 左括号：直接入栈
                stack.push(c);
            } else {
                // 右括号：检查匹配
                if (stack.isEmpty()) {
                    // 没有对应的左括号
                    return false;
                }
                
                char top = stack.pop();
                
                // 检查括号类型是否匹配
                if ((c == ')' && top != '(') ||
                    (c == ']' && top != '[') ||
                    (c == '}' && top != '{')) {
                    return false;
                }
            }
        }
        
        // 栈为空说明所有括号都已匹配
        return stack.isEmpty();
    }
}
```

### 方法二：使用 HashMap 优化匹配逻辑
```java
import java.util.*;

public class Solution {
    public boolean isValid(String s) {
        if (s.length() % 2 == 1) {
            return false;
        }
        
        // 括号映射表
        Map<Character, Character> pairs = new HashMap<Character, Character>() {{
            put(')', '(');
            put(']', '[');
            put('}', '{');
        }};
        
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : s.toCharArray()) {
            if (pairs.containsKey(c)) {
                // 右括号：检查匹配
                if (stack.isEmpty() || !stack.pop().equals(pairs.get(c))) {
                    return false;
                }
            } else {
                // 左括号：入栈
                stack.push(c);
            }
        }
        
        return stack.isEmpty();
    }
}
```

### 方法三：字符串替换法（不推荐，仅作思路扩展）
```java
public class Solution {
    public boolean isValid(String s) {
        // 不断移除成对的括号
        while (s.contains("()") || s.contains("[]") || s.contains("{}")) {
            s = s.replace("()", "")
                 .replace("[]", "")
                 .replace("{}", "");
        }
        
        // 如果最终字符串为空，说明所有括号都已匹配
        return s.isEmpty();
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
+ **O(n)**：需要遍历字符串中的每个字符一次
+ 每个字符的栈操作（push/pop）都是 O(1)

### 空间复杂度
+ **O(n)**：最坏情况下，所有字符都是左括号，栈的大小为 n
+ 平均情况下，空间复杂度约为 O(n/2)

## 🎨 可视化演示
### 动态过程演示
```java
/**
 * 带可视化输出的括号匹配验证
 */
public class VisualBracketValidator {
    
    public static boolean isValidWithVisualization(String s) {
        System.out.println("验证字符串: \"" + s + "\"");
        System.out.println("=" + "=".repeat(50));
        
        if (s.length() % 2 == 1) {
            System.out.println("❌ 字符串长度为奇数，直接返回 false");
            return false;
        }
        
        Deque<Character> stack = new ArrayDeque<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            System.out.printf("步骤 %d: 处理字符 '%c'\n", i + 1, c);
            
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
                System.out.println("  → 左括号入栈");
            } else {
                if (stack.isEmpty()) {
                    System.out.println("  → ❌ 栈为空，无匹配的左括号");
                    printResult(false);
                    return false;
                }
                
                char top = stack.pop();
                boolean isMatch = (c == ')' && top == '(') ||
                                (c == ']' && top == '[') ||
                                (c == '}' && top == '{');
                
                if (isMatch) {
                    System.out.printf("  → ✅ 右括号 '%c' 与栈顶 '%c' 匹配\n", c, top);
                } else {
                    System.out.printf("  → ❌ 右括号 '%c' 与栈顶 '%c' 不匹配\n", c, top);
                    printResult(false);
                    return false;
                }
            }
            
            printStackState(stack);
            System.out.println();
        }
        
        boolean result = stack.isEmpty();
        printResult(result);
        return result;
    }
    
    private static void printStackState(Deque<Character> stack) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Character> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList); // 显示从底到顶
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print("'" + stackList.get(i) + "'");
            }
        }
        System.out.println("]");
    }
    
    private static void printResult(boolean result) {
        System.out.println("=" + "=".repeat(50));
        if (result) {
            System.out.println("🎉 结果: 有效的括号序列");
        } else {
            System.out.println("❌ 结果: 无效的括号序列");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        String[] testCases = {
            "()",
            "()[]{}", 
            "(]",
            "([)]",
            "{[]}",
            "(((",
            ")))",
            ""
        };
        
        for (String testCase : testCases) {
            isValidWithVisualization(testCase);
        }
    }
}
```

## 🧪 测试用例
### 基础测试
```java
public class BracketValidatorTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 有效括号
        assertTrue(solution.isValid("()"));
        assertTrue(solution.isValid("[]"));
        assertTrue(solution.isValid("{}"));
        assertTrue(solution.isValid("()[]{}"));
        assertTrue(solution.isValid("{[]}"));
        assertTrue(solution.isValid("((()))"));
        
        // 无效括号
        assertFalse(solution.isValid("(]"));
        assertFalse(solution.isValid("([)]"));
        assertFalse(solution.isValid("((("));
        assertFalse(solution.isValid(")))"));
        assertFalse(solution.isValid("(()"));
        assertFalse(solution.isValid("())"));
    }
    
    @Test
    public void testEdgeCases() {
        // 边界情况
        assertTrue(solution.isValid(""));  // 空字符串
        assertFalse(solution.isValid("("));  // 单个左括号
        assertFalse(solution.isValid(")"));  // 单个右括号
        assertFalse(solution.isValid("()("));  // 奇数长度
    }
    
    @Test
    public void testComplexCases() {
        // 复杂嵌套
        assertTrue(solution.isValid("(((())))"));
        assertTrue(solution.isValid("([{}])"));
        assertTrue(solution.isValid("{[()]}"));
        assertFalse(solution.isValid("([{})]"));
        assertFalse(solution.isValid("{[(])}"));
    }
}
```

### 性能测试
```java
public class PerformanceTest {
    
    @Test
    public void testLargeInput() {
        Solution solution = new Solution();
        
        // 生成大规模测试数据
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5000; i++) {
            sb.append("()[]{}");
        }
        String largeValid = sb.toString();
        
        long startTime = System.nanoTime();
        boolean result = solution.isValid(largeValid);
        long endTime = System.nanoTime();
        
        assertTrue(result);
        System.out.printf("处理 %d 个字符耗时: %.2f ms\n", 
                         largeValid.length(), 
                         (endTime - startTime) / 1_000_000.0);
    }
}
```

## 🔧 变体问题
### 1. 返回第一个无效位置
```java
public class BracketValidatorWithPosition {
    
    public int findFirstInvalidPosition(String s) {
        if (s.length() % 2 == 1) {
            return s.length() - 1; // 最后一个字符无法匹配
        }
        
        Deque<Integer> stack = new ArrayDeque<>(); // 存储位置
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == '(' || c == '[' || c == '{') {
                stack.push(i);
            } else {
                if (stack.isEmpty()) {
                    return i; // 当前位置无匹配的左括号
                }
                
                int leftPos = stack.pop();
                char leftChar = s.charAt(leftPos);
                
                if ((c == ')' && leftChar != '(') ||
                    (c == ']' && leftChar != '[') ||
                    (c == '}' && leftChar != '{')) {
                    return i; // 当前位置括号类型不匹配
                }
            }
        }
        
        return stack.isEmpty() ? -1 : stack.peek(); // 返回第一个未匹配的左括号位置
    }
}
```

### 2. 计算需要添加的最少括号数
```java
public class MinimumBracketsToAdd {
    
    public int minAddToMakeValid(String s) {
        int leftNeeded = 0;  // 需要添加的左括号数
        int rightNeeded = 0; // 需要添加的右括号数
        
        for (char c : s.toCharArray()) {
            if (c == '(') {
                rightNeeded++;
            } else if (c == ')') {
                if (rightNeeded > 0) {
                    rightNeeded--;
                } else {
                    leftNeeded++;
                }
            }
        }
        
        return leftNeeded + rightNeeded;
    }
}
```

## 💡 解题技巧总结
### 1. 栈的选择
+ **推荐使用 **`ArrayDeque`：性能最佳
+ **避免使用 **`Stack`：基于 Vector，性能较差
+ **可以使用 **`LinkedList`：但不如 ArrayDeque 高效

### 2. 优化技巧
+ **提前判断**：奇数长度直接返回 false
+ **使用 HashMap**：简化括号匹配逻辑
+ **字符数组**：避免重复调用 charAt()

### 3. 常见错误
+ **忘记检查栈空**：弹出前必须检查栈是否为空
+ **最终状态检查**：遍历结束后要检查栈是否为空
+ **括号类型混淆**：确保左右括号类型匹配

### 4. 扩展思考
+ **多种括号类型**：可以轻松扩展到更多括号类型
+ **嵌套深度限制**：可以添加最大嵌套深度检查
+ **错误位置定位**：可以返回具体的错误位置信息

这道题是栈数据结构的经典应用，掌握了这个问题的解法，就能很好地理解栈的 LIFO 特性在实际问题中的应用！



> 更新: 2025-09-19 00:53:57  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/5676f104458651c44b6497175f2dd6f5>