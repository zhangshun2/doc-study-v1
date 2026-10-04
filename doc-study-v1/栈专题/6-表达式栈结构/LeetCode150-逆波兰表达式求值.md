# LeetCode150-逆波兰表达式求值

# LeetCode 150 - 逆波兰表达式求值
## 📋 题目描述
**难度：中等**

给你一个字符串数组 `tokens` ，表示一个根据 **逆波兰表示法** 表示的算术表达式。

请你计算该表达式。返回一个表示表达式值的整数。

**注意：**

+ 有效的算符为 `'+'`、`'-'`、`'*'` 和 `'/'` 。
+ 每个操作数（运算对象）都可以是一个整数或者另一个表达式。
+ 两个整数之间的除法总是 **向零截断** 。
+ 表达式中不含除零运算。
+ 输入是一个根据逆波兰表示法表示的算术表达式。
+ 答案及所有中间计算结果可以用 **32 位** 整数表示。

### 示例
**示例 1：**

```plain
输入：tokens = ["2","1","+","3","*"]
输出：9
解释：该算式转化为常见的中缀算术表达式为：((2 + 1) * 3) = 9
```

**示例 2：**

```plain
输入：tokens = ["4","13","5","/","+"]
输出：6
解释：该算式转化为常见的中缀算术表达式为：(4 + (13 / 5)) = 6
```

**示例 3：**

```plain
输入：tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
输出：22
解释：该算式转化为常见的中缀算术表达式为：
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
```

### 约束条件
+ `1 <= tokens.length <= 10^4`
+ `tokens[i]` 是一个算符（`"+"`、`"-"`、`"*"` 或 `"/"`），或是在范围 `[-200, 200]` 内的一个整数

### 逆波兰表示法
逆波兰表示法是一种后缀表达式，所谓后缀就是指算符写在后面。

+ 平常使用的算式则是一种中缀表达式，如 `( 1 + 2 ) * ( 3 + 4 )` 。
+ 该算式的逆波兰表达式写法为 `( ( 1 2 + ) ( 3 4 + ) * )` 。

逆波兰表达式主要有以下两个优点：

+ 去掉括号后表达式无歧义，上式即便写成 `1 2 + 3 4 + *` 也可以依据次序计算出正确结果。
+ 适合用栈操作运算：遇到数字则入栈；遇到算符则取出栈顶两个数字进行计算，并将结果压入栈中。

## 🎯 解题思路
### 核心问题分析
这是一个典型的**表达式栈问题**。关键在于：

1. 理解逆波兰表达式（后缀表达式）的计算规则
2. 使用栈来存储操作数
3. 遇到操作符时弹出操作数进行计算

### 表达式栈解法原理
```plain
逆波兰表达式的计算规则：
1. 从左到右扫描表达式
2. 遇到操作数：压入栈中
3. 遇到操作符：
   - 弹出栈顶两个操作数
   - 进行相应运算（注意操作数的顺序）
   - 将结果压入栈中
4. 扫描完毕后，栈中只剩一个元素，即为结果

栈的作用：
- 存储待运算的操作数
- 保存中间计算结果
- 实现后缀表达式的自然计算顺序
```

### 算法步骤
```plain
1. 初始化一个栈用于存储操作数
2. 遍历tokens数组：
   a. 如果是数字：转换为整数并压入栈
   b. 如果是操作符：
      - 弹出栈顶两个元素（注意顺序）
      - 执行相应运算
      - 将结果压入栈
3. 返回栈中唯一剩余的元素
```

### 图解演示
**示例：tokens = ["2","1","+","3","*"]**

```plain
逆波兰表达式：2 1 + 3 *
对应中缀表达式：(2 + 1) * 3

计算过程：

初始状态：
栈: []
当前token: "2"

步骤1: 处理 "2"
"2" 是数字，压入栈
栈: [2]

步骤2: 处理 "1"
"1" 是数字，压入栈
栈: [2, 1] (底 -> 顶)

步骤3: 处理 "+"
"+" 是操作符，弹出两个操作数
弹出: 1 (右操作数)
弹出: 2 (左操作数)
计算: 2 + 1 = 3
压入结果: 3
栈: [3]

步骤4: 处理 "3"
"3" 是数字，压入栈
栈: [3, 3] (底 -> 顶)

步骤5: 处理 "*"
"*" 是操作符，弹出两个操作数
弹出: 3 (右操作数)
弹出: 3 (左操作数)
计算: 3 * 3 = 9
压入结果: 9
栈: [9]

最终结果: 9
```

**复杂示例：tokens = ["4","13","5","/","+"]**

```plain
逆波兰表达式：4 13 5 / +
对应中缀表达式：4 + (13 / 5)

计算过程：

步骤1: 处理 "4"
栈: [4]

步骤2: 处理 "13"
栈: [4, 13]

步骤3: 处理 "5"
栈: [4, 13, 5]

步骤4: 处理 "/"
弹出: 5 (右操作数)
弹出: 13 (左操作数)
计算: 13 / 5 = 2 (向零截断)
栈: [4, 2]

步骤5: 处理 "+"
弹出: 2 (右操作数)
弹出: 4 (左操作数)
计算: 4 + 2 = 6
栈: [6]

最终结果: 6
```

## 💻 代码实现
### 方法一：基础栈实现（推荐）
```java
import java.util.*;

public class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isOperator(token)) {
                // 弹出两个操作数（注意顺序）
                int operand2 = stack.pop(); // 右操作数
                int operand1 = stack.pop(); // 左操作数
                
                // 执行运算并压入结果
                int result = calculate(operand1, operand2, token);
                stack.push(result);
            } else {
                // 操作数，转换为整数并压入栈
                stack.push(Integer.parseInt(token));
            }
        }
        
        // 栈中剩余的唯一元素就是结果
        return stack.pop();
    }
    
    private boolean isOperator(String token) {
        return "+".equals(token) || "-".equals(token) || 
               "*".equals(token) || "/".equals(token);
    }
    
    private int calculate(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+":
                return operand1 + operand2;
            case "-":
                return operand1 - operand2;
            case "*":
                return operand1 * operand2;
            case "/":
                return operand1 / operand2; // Java中整数除法自动向零截断
            default:
                throw new IllegalArgumentException("Invalid operator: " + operator);
        }
    }
}
```

### 方法二：使用Set优化操作符判断
```java
public class SolutionOptimized {
    
    private static final Set<String> OPERATORS = Set.of("+", "-", "*", "/");
    
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (OPERATORS.contains(token)) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                stack.push(calculate(operand1, operand2, token));
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        
        return stack.pop();
    }
    
    private int calculate(int a, int b, String op) {
        switch (op) {
            case "+": return a + b;
            case "-": return a - b;
            case "*": return a * b;
            case "/": return a / b;
            default: throw new IllegalArgumentException("Unknown operator: " + op);
        }
    }
}
```

### 方法三：函数式编程风格
```java
import java.util.function.BinaryOperator;

public class SolutionFunctional {
    
    private static final Map<String, BinaryOperator<Integer>> OPERATIONS = Map.of(
        "+", Integer::sum,
        "-", (a, b) -> a - b,
        "*", (a, b) -> a * b,
        "/", (a, b) -> a / b
    );
    
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (OPERATIONS.containsKey(token)) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = OPERATIONS.get(token).apply(operand1, operand2);
                stack.push(result);
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        
        return stack.pop();
    }
}
```

### 方法四：递归实现（理论参考）
```java
public class SolutionRecursive {
    
    private int index;
    
    public int evalRPN(String[] tokens) {
        index = tokens.length - 1;
        return evaluate(tokens);
    }
    
    private int evaluate(String[] tokens) {
        String token = tokens[index--];
        
        if (isOperator(token)) {
            // 注意：递归时操作数的顺序是相反的
            int operand2 = evaluate(tokens);
            int operand1 = evaluate(tokens);
            return calculate(operand1, operand2, token);
        } else {
            return Integer.parseInt(token);
        }
    }
    
    private boolean isOperator(String token) {
        return "+".equals(token) || "-".equals(token) || 
               "*".equals(token) || "/".equals(token);
    }
    
    private int calculate(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+": return operand1 + operand2;
            case "-": return operand1 - operand2;
            case "*": return operand1 * operand2;
            case "/": return operand1 / operand2;
            default: throw new IllegalArgumentException("Invalid operator: " + operator);
        }
    }
}
```

### 方法五：数组模拟栈（性能优化）
```java
public class SolutionArrayStack {
    
    public int evalRPN(String[] tokens) {
        int[] stack = new int[tokens.length / 2 + 1]; // 最多需要这么多空间
        int top = -1; // 栈顶指针
        
        for (String token : tokens) {
            switch (token) {
                case "+":
                    stack[top - 1] += stack[top];
                    top--;
                    break;
                case "-":
                    stack[top - 1] -= stack[top];
                    top--;
                    break;
                case "*":
                    stack[top - 1] *= stack[top];
                    top--;
                    break;
                case "/":
                    stack[top - 1] /= stack[top];
                    top--;
                    break;
                default:
                    stack[++top] = Integer.parseInt(token);
                    break;
            }
        }
        
        return stack[top];
    }
}
```

### 方法六：带详细日志的实现
```java
public class SolutionWithLogging {
    
    public int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        System.out.println("🧮 开始计算逆波兰表达式: " + Arrays.toString(tokens));
        System.out.println("=" + "=".repeat(60));
        
        for (int i = 0; i < tokens.length; i++) {
            String token = tokens[i];
            System.out.printf("步骤 %d: 处理 '%s'\n", i + 1, token);
            
            if (isOperator(token)) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = calculate(operand1, operand2, token);
                
                System.out.printf("  🔢 弹出操作数: %d, %d\n", operand1, operand2);
                System.out.printf("  ⚡ 计算: %d %s %d = %d\n", operand1, token, operand2, result);
                
                stack.push(result);
                System.out.printf("  📥 压入结果: %d\n", result);
            } else {
                int number = Integer.parseInt(token);
                stack.push(number);
                System.out.printf("  📥 压入数字: %d\n", number);
            }
            
            System.out.printf("  栈状态: %s\n", stack);
            System.out.println();
        }
        
        int finalResult = stack.pop();
        System.out.println("🏆 最终结果: " + finalResult);
        
        return finalResult;
    }
    
    private boolean isOperator(String token) {
        return "+".equals(token) || "-".equals(token) || 
               "*".equals(token) || "/".equals(token);
    }
    
    private int calculate(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+": return operand1 + operand2;
            case "-": return operand1 - operand2;
            case "*": return operand1 * operand2;
            case "/": return operand1 / operand2;
            default: throw new IllegalArgumentException("Invalid operator: " + operator);
        }
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**所有方法：**

+ 需要遍历tokens数组一次
+ 每个token的处理时间为O(1)
+ 总时间复杂度：**O(n)**，其中n是tokens的长度

### 空间复杂度
**栈实现：**

+ 最坏情况下，所有token都是操作数，栈的大小为n
+ 空间复杂度：**O(n)**

**数组模拟栈：**

+ 使用固定大小的数组，大小为n/2+1
+ 空间复杂度：**O(n)**

**递归实现：**

+ 递归调用栈的深度取决于操作符的数量
+ 空间复杂度：**O(n)**

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 可视化逆波兰表达式计算过程
 */
public class VisualRPNCalculator {
    
    public static int evalRPNWithVisualization(String[] tokens) {
        System.out.println("🧮 逆波兰表达式计算器");
        System.out.println("表达式: " + String.join(" ", tokens));
        System.out.println("=" + "=".repeat(60));
        
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < tokens.length; i++) {
            String token = tokens[i];
            
            System.out.printf("\n📍 步骤 %d: 处理 '%s'\n", i + 1, token);
            
            if (isOperator(token)) {
                if (stack.size() < 2) {
                    throw new IllegalArgumentException("表达式格式错误：操作符缺少操作数");
                }
                
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                
                System.out.printf("  🔢 弹出操作数:\n");
                System.out.printf("    右操作数: %d\n", operand2);
                System.out.printf("    左操作数: %d\n", operand1);
                
                int result = calculate(operand1, operand2, token);
                
                System.out.printf("  ⚡ 执行运算: %d %s %d = %d\n", 
                                operand1, token, operand2, result);
                
                stack.push(result);
                System.out.printf("  📥 压入结果: %d\n", result);
                
            } else {
                int number = Integer.parseInt(token);
                stack.push(number);
                System.out.printf("  📥 压入数字: %d\n", number);
            }
            
            printStackState(stack);
            printExpressionTree(tokens, i + 1);
        }
        
        if (stack.size() != 1) {
            throw new IllegalArgumentException("表达式格式错误：计算完成后栈中应只有一个元素");
        }
        
        int result = stack.pop();
        System.out.println("\n🏆 计算完成！");
        System.out.println("最终结果: " + result);
        
        return result;
    }
    
    private static void printStackState(Deque<Integer> stack) {
        System.out.print("  📚 栈状态: ");
        if (stack.isEmpty()) {
            System.out.println("[空栈]");
        } else {
            List<Integer> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            System.out.print("[");
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(stackList.get(i));
            }
            System.out.println("] (底 -> 顶)");
        }
    }
    
    private static void printExpressionTree(String[] tokens, int processed) {
        System.out.print("  🌳 已处理: ");
        for (int i = 0; i < processed; i++) {
            System.out.print(tokens[i]);
            if (i < processed - 1) System.out.print(" ");
        }
        
        if (processed < tokens.length) {
            System.out.print(" | 待处理: ");
            for (int i = processed; i < tokens.length; i++) {
                System.out.print(tokens[i]);
                if (i < tokens.length - 1) System.out.print(" ");
            }
        }
        System.out.println();
    }
    
    private static boolean isOperator(String token) {
        return "+".equals(token) || "-".equals(token) || 
               "*".equals(token) || "/".equals(token);
    }
    
    private static int calculate(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+": return operand1 + operand2;
            case "-": return operand1 - operand2;
            case "*": return operand1 * operand2;
            case "/": 
                if (operand2 == 0) {
                    throw new ArithmeticException("除零错误");
                }
                return operand1 / operand2;
            default: 
                throw new IllegalArgumentException("未知操作符: " + operator);
        }
    }
    
    public static void main(String[] args) {
        // 测试用例
        String[][] testCases = {
            {"2", "1", "+", "3", "*"},
            {"4", "13", "5", "/", "+"},
            {"10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"}
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("🧪 测试用例 %d:\n", i + 1);
            try {
                evalRPNWithVisualization(testCases[i]);
            } catch (Exception e) {
                System.out.println("❌ 错误: " + e.getMessage());
            }
            System.out.println("\n" + "=".repeat(70) + "\n");
        }
    }
}
```

### 运行结果示例
```plain
🧪 测试用例 1:
🧮 逆波兰表达式计算器
表达式: 2 1 + 3 *
============================================================

📍 步骤 1: 处理 '2'
  📥 压入数字: 2
  📚 栈状态: [2] (底 -> 顶)
  🌳 已处理: 2 | 待处理: 1 + 3 *

📍 步骤 2: 处理 '1'
  📥 压入数字: 1
  📚 栈状态: [2, 1] (底 -> 顶)
  🌳 已处理: 2 1 | 待处理: + 3 *

📍 步骤 3: 处理 '+'
  🔢 弹出操作数:
    右操作数: 1
    左操作数: 2
  ⚡ 执行运算: 2 + 1 = 3
  📥 压入结果: 3
  📚 栈状态: [3] (底 -> 顶)
  🌳 已处理: 2 1 + | 待处理: 3 *

📍 步骤 4: 处理 '3'
  📥 压入数字: 3
  📚 栈状态: [3, 3] (底 -> 顶)
  🌳 已处理: 2 1 + 3 | 待处理: *

📍 步骤 5: 处理 '*'
  🔢 弹出操作数:
    右操作数: 3
    左操作数: 3
  ⚡ 执行运算: 3 * 3 = 9
  📥 压入结果: 9
  📚 栈状态: [9] (底 -> 顶)
  🌳 已处理: 2 1 + 3 *

🏆 计算完成！
最终结果: 9
```

## 🧪 测试用例
### 基础功能测试
```java
public class RPNCalculatorTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicOperations() {
        // 加法
        assertEquals(3, solution.evalRPN(new String[]{"2", "1", "+"}));
        
        // 减法
        assertEquals(1, solution.evalRPN(new String[]{"2", "1", "-"}));
        
        // 乘法
        assertEquals(6, solution.evalRPN(new String[]{"2", "3", "*"}));
        
        // 除法
        assertEquals(2, solution.evalRPN(new String[]{"6", "3", "/"}));
    }
    
    @Test
    public void testExampleCases() {
        // 示例 1: ["2","1","+","3","*"]
        assertEquals(9, solution.evalRPN(new String[]{"2", "1", "+", "3", "*"}));
        
        // 示例 2: ["4","13","5","/","+"]
        assertEquals(6, solution.evalRPN(new String[]{"4", "13", "5", "/", "+"}));
        
        // 示例 3: 复杂表达式
        assertEquals(22, solution.evalRPN(new String[]{
            "10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"
        }));
    }
    
    @Test
    public void testSingleNumber() {
        // 单个数字
        assertEquals(42, solution.evalRPN(new String[]{"42"}));
        assertEquals(-5, solution.evalRPN(new String[]{"-5"}));
        assertEquals(0, solution.evalRPN(new String[]{"0"}));
    }
    
    @Test
    public void testNegativeNumbers() {
        // 负数运算
        assertEquals(-1, solution.evalRPN(new String[]{"2", "-3", "+"}));
        assertEquals(5, solution.evalRPN(new String[]{"-2", "-3", "-"}));
        assertEquals(6, solution.evalRPN(new String[]{"-2", "-3", "*"}));
        assertEquals(2, solution.evalRPN(new String[]{"-6", "-3", "/"}));
    }
    
    @Test
    public void testDivisionTruncation() {
        // 测试除法向零截断
        assertEquals(2, solution.evalRPN(new String[]{"7", "3", "/"}));      // 7/3 = 2.33... -> 2
        assertEquals(-2, solution.evalRPN(new String[]{"-7", "3", "/"}));    // -7/3 = -2.33... -> -2
        assertEquals(-2, solution.evalRPN(new String[]{"7", "-3", "/"}));    // 7/-3 = -2.33... -> -2
        assertEquals(2, solution.evalRPN(new String[]{"-7", "-3", "/"}));    // -7/-3 = 2.33... -> 2
    }
    
    @Test
    public void testComplexExpressions() {
        // 复杂表达式测试
        
        // ((1 + 2) * 3) - 4 = 5
        assertEquals(5, solution.evalRPN(new String[]{"1", "2", "+", "3", "*", "4", "-"}));
        
        // (1 + 2) * (3 - 4) = -3
        assertEquals(-3, solution.evalRPN(new String[]{"1", "2", "+", "3", "4", "-", "*"}));
        
        // 1 + 2 * 3 - 4 / 2 = 5
        assertEquals(5, solution.evalRPN(new String[]{"1", "2", "3", "*", "+", "4", "2", "/", "-"}));
    }
}
```

### 边界条件测试
```java
public class RPNBoundaryTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testMinMaxValues() {
        // 测试最大最小值
        assertEquals(200, solution.evalRPN(new String[]{"200"}));
        assertEquals(-200, solution.evalRPN(new String[]{"-200"}));
        
        // 大数运算
        assertEquals(400, solution.evalRPN(new String[]{"200", "2", "*"}));
        assertEquals(-400, solution.evalRPN(new String[]{"-200", "2", "*"}));
    }
    
    @Test
    public void testZeroDivision() {
        // 注意：题目保证不会有除零运算，但我们可以测试接近零的情况
        assertEquals(0, solution.evalRPN(new String[]{"0", "5", "*"}));
        assertEquals(0, solution.evalRPN(new String[]{"5", "0", "*"}));
        assertEquals(0, solution.evalRPN(new String[]{"0", "5", "/"}));
    }
    
    @Test
    public void testLongExpressions() {
        // 测试长表达式
        String[] longExpression = new String[10001]; // 最大长度
        
        // 构造表达式: 1 + 1 + 1 + ... + 1 (5000个1相加)
        for (int i = 0; i < 5000; i++) {
            longExpression[i] = "1";
        }
        for (int i = 5000; i < 9999; i++) {
            longExpression[i] = "+";
        }
        longExpression[9999] = "0";
        longExpression[10000] = "+";
        
        assertEquals(4999, solution.evalRPN(longExpression));
    }
    
    @Test
    public void testAllOperators() {
        // 测试所有操作符的组合
        String[] expression = {
            "15", "7", "+", "1", "-", "3", "/", "2", "*"
        };
        // ((15 + 7) - 1) / 3 * 2 = 21 / 3 * 2 = 7 * 2 = 14
        assertEquals(14, solution.evalRPN(expression));
    }
}
```

### 性能测试
```java
public class RPNPerformanceTest {
    
    @Test
    public void testPerformance() {
        // 构造大型表达式进行性能测试
        List<String> tokens = new ArrayList<>();
        
        // 添加大量操作数
        for (int i = 1; i <= 5000; i++) {
            tokens.add(String.valueOf(i));
        }
        
        // 添加操作符使其成为有效的RPN表达式
        for (int i = 0; i < 4999; i++) {
            tokens.add("+");
        }
        
        String[] expression = tokens.toArray(new String[0]);
        
        // 测试不同实现的性能
        Solution solution1 = new Solution();
        SolutionOptimized solution2 = new SolutionOptimized();
        SolutionArrayStack solution3 = new SolutionArrayStack();
        
        long startTime, endTime;
        
        // 基础实现
        startTime = System.nanoTime();
        int result1 = solution1.evalRPN(expression);
        endTime = System.nanoTime();
        System.out.printf("基础实现: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 优化实现
        startTime = System.nanoTime();
        int result2 = solution2.evalRPN(expression);
        endTime = System.nanoTime();
        System.out.printf("优化实现: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 数组栈实现
        startTime = System.nanoTime();
        int result3 = solution3.evalRPN(expression);
        endTime = System.nanoTime();
        System.out.printf("数组栈实现: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        assertEquals(result1, result3);
        
        // 预期结果：1+2+3+...+5000 = 5000*5001/2 = 12502500
        assertEquals(12502500, result1);
        
        System.out.println("性能测试通过 ✅");
    }
    
    @Test
    public void testMemoryUsage() {
        // 内存使用测试
        Runtime runtime = Runtime.getRuntime();
        
        // 构造测试表达式
        String[] expression = new String[10001];
        for (int i = 0; i < 5000; i++) {
            expression[i] = "1";
        }
        for (int i = 5000; i < 9999; i++) {
            expression[i] = "+";
        }
        expression[9999] = "0";
        expression[10000] = "+";
        
        // 测试内存使用
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        Solution solution = new Solution();
        solution.evalRPN(expression);
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("内存使用: %d KB\n", (memAfter - memBefore) / 1024);
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 224 - 基本计算器
```java
/**
 * 基本计算器 - 中缀表达式转后缀表达式再求值
 */
public class BasicCalculator {
    
    public int calculate(String s) {
        // 第一步：中缀转后缀
        List<String> postfix = infixToPostfix(s);
        
        // 第二步：计算后缀表达式
        return evalRPN(postfix.toArray(new String[0]));
    }
    
    private List<String> infixToPostfix(String s) {
        List<String> result = new ArrayList<>();
        Deque<Character> operators = new ArrayDeque<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == ' ') continue;
            
            if (Character.isDigit(c)) {
                // 读取完整的数字
                StringBuilder num = new StringBuilder();
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num.append(s.charAt(i++));
                }
                i--; // 回退一位
                result.add(num.toString());
            } else if (c == '(') {
                operators.push(c);
            } else if (c == ')') {
                while (!operators.isEmpty() && operators.peek() != '(') {
                    result.add(String.valueOf(operators.pop()));
                }
                operators.pop(); // 弹出 '('
            } else if (isOperator(c)) {
                while (!operators.isEmpty() && 
                       operators.peek() != '(' && 
                       precedence(operators.peek()) >= precedence(c)) {
                    result.add(String.valueOf(operators.pop()));
                }
                operators.push(c);
            }
        }
        
        while (!operators.isEmpty()) {
            result.add(String.valueOf(operators.pop()));
        }
        
        return result;
    }
    
    private boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/';
    }
    
    private int precedence(char op) {
        switch (op) {
            case '+':
            case '-':
                return 1;
            case '*':
            case '/':
                return 2;
            default:
                return 0;
        }
    }
    
    private int evalRPN(String[] tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isOperatorString(token)) {
                int b = stack.pop();
                int a = stack.pop();
                stack.push(calculate(a, b, token.charAt(0)));
            } else {
                stack.push(Integer.parseInt(token));
            }
        }
        
        return stack.pop();
    }
    
    private boolean isOperatorString(String token) {
        return token.length() == 1 && isOperator(token.charAt(0));
    }
    
    private int calculate(int a, int b, char op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            default: throw new IllegalArgumentException("Unknown operator: " + op);
        }
    }
}
```

### 2. 表达式求值器（支持函数）
```java
/**
 * 支持函数的表达式求值器
 */
public class AdvancedExpressionEvaluator {
    
    private static final Map<String, Function<List<Double>, Double>> FUNCTIONS = Map.of(
        "sin", args -> Math.sin(args.get(0)),
        "cos", args -> Math.cos(args.get(0)),
        "sqrt", args -> Math.sqrt(args.get(0)),
        "max", args -> Collections.max(args),
        "min", args -> Collections.min(args),
        "avg", args -> args.stream().mapToDouble(Double::doubleValue).average().orElse(0.0)
    );
    
    public double evaluate(String expression) {
        List<String> tokens = tokenize(expression);
        List<String> postfix = infixToPostfix(tokens);
        return evalRPN(postfix);
    }
    
    private List<String> tokenize(String expression) {
        List<String> tokens = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < expression.length(); i++) {
            char c = expression.charAt(i);
            
            if (Character.isWhitespace(c)) {
                if (current.length() > 0) {
                    tokens.add(current.toString());
                    current.setLength(0);
                }
            } else if (isOperator(c) || c == '(' || c == ')' || c == ',') {
                if (current.length() > 0) {
                    tokens.add(current.toString());
                    current.setLength(0);
                }
                tokens.add(String.valueOf(c));
            } else {
                current.append(c);
            }
        }
        
        if (current.length() > 0) {
            tokens.add(current.toString());
        }
        
        return tokens;
    }
    
    private List<String> infixToPostfix(List<String> tokens) {
        List<String> result = new ArrayList<>();
        Deque<String> operators = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isNumber(token)) {
                result.add(token);
            } else if (FUNCTIONS.containsKey(token)) {
                operators.push(token);
            } else if (token.equals("(")) {
                operators.push(token);
            } else if (token.equals(")")) {
                while (!operators.isEmpty() && !operators.peek().equals("(")) {
                    result.add(operators.pop());
                }
                operators.pop(); // 弹出 '('
                
                // 如果栈顶是函数，也要弹出
                if (!operators.isEmpty() && FUNCTIONS.containsKey(operators.peek())) {
                    result.add(operators.pop());
                }
            } else if (token.equals(",")) {
                while (!operators.isEmpty() && !operators.peek().equals("(")) {
                    result.add(operators.pop());
                }
            } else if (isOperatorString(token)) {
                while (!operators.isEmpty() && 
                       !operators.peek().equals("(") && 
                       !FUNCTIONS.containsKey(operators.peek()) &&
                       precedence(operators.peek()) >= precedence(token)) {
                    result.add(operators.pop());
                }
                operators.push(token);
            }
        }
        
        while (!operators.isEmpty()) {
            result.add(operators.pop());
        }
        
        return result;
    }
    
    private double evalRPN(List<String> tokens) {
        Deque<Double> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isNumber(token)) {
                stack.push(Double.parseDouble(token));
            } else if (FUNCTIONS.containsKey(token)) {
                // 函数调用，参数数量根据函数确定
                List<Double> args = new ArrayList<>();
                int argCount = getFunctionArgCount(token);
                
                for (int i = 0; i < argCount; i++) {
                    args.add(0, stack.pop()); // 逆序添加参数
                }
                
                double result = FUNCTIONS.get(token).apply(args);
                stack.push(result);
            } else if (isOperatorString(token)) {
                double b = stack.pop();
                double a = stack.pop();
                double result = calculate(a, b, token.charAt(0));
                stack.push(result);
            }
        }
        
        return stack.pop();
    }
    
    private int getFunctionArgCount(String function) {
        switch (function) {
            case "sin":
            case "cos":
            case "sqrt":
                return 1;
            case "max":
            case "min":
            case "avg":
                return 2; // 简化处理，实际应该支持可变参数
            default:
                return 1;
        }
    }
    
    private boolean isNumber(String token) {
        try {
            Double.parseDouble(token);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
    
    private boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/';
    }
    
    private boolean isOperatorString(String token) {
        return token.length() == 1 && isOperator(token.charAt(0));
    }
    
    private int precedence(String op) {
        switch (op) {
            case "+":
            case "-":
                return 1;
            case "*":
            case "/":
                return 2;
            default:
                return 0;
        }
    }
    
    private double calculate(double a, double b, char op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            default: throw new IllegalArgumentException("Unknown operator: " + op);
        }
    }
}
```

### 3. 表达式语法树构建
```java
/**
 * 表达式语法树构建器
 */
public class ExpressionTreeBuilder {
    
    static class TreeNode {
        String val;
        TreeNode left;
        TreeNode right;
        
        TreeNode(String val) {
            this.val = val;
        }
        
        boolean isOperator() {
            return "+".equals(val) || "-".equals(val) || "*".equals(val) || "/".equals(val);
        }
    }
    
    public TreeNode buildFromRPN(String[] tokens) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            TreeNode node = new TreeNode(token);
            
            if (node.isOperator()) {
                node.right = stack.pop();
                node.left = stack.pop();
            }
            
            stack.push(node);
        }
        
        return stack.pop();
    }
    
    public TreeNode buildFromInfix(String expression) {
        String[] rpnTokens = infixToRPN(expression);
        return buildFromRPN(rpnTokens);
    }
    
    public int evaluate(TreeNode root) {
        if (root == null) return 0;
        
        if (!root.isOperator()) {
            return Integer.parseInt(root.val);
        }
        
        int left = evaluate(root.left);
        int right = evaluate(root.right);
        
        switch (root.val) {
            case "+": return left + right;
            case "-": return left - right;
            case "*": return left * right;
            case "/": return left / right;
            default: throw new IllegalArgumentException("Unknown operator: " + root.val);
        }
    }
    
    public void printInorder(TreeNode root) {
        if (root == null) return;
        
        if (root.isOperator()) System.out.print("(");
        printInorder(root.left);
        System.out.print(root.val);
        printInorder(root.right);
        if (root.isOperator()) System.out.print(")");
    }
    
    public void printTree(TreeNode root) {
        printTree(root, "", true);
    }
    
    private void printTree(TreeNode node, String prefix, boolean isLast) {
        if (node == null) return;
        
        System.out.println(prefix + (isLast ? "└── " : "├── ") + node.val);
        
        if (node.left != null || node.right != null) {
            if (node.left != null) {
                printTree(node.left, prefix + (isLast ? "    " : "│   "), node.right == null);
            }
            if (node.right != null) {
                printTree(node.right, prefix + (isLast ? "    " : "│   "), true);
            }
        }
    }
    
    private String[] infixToRPN(String expression) {
        // 简化实现，实际应该完整解析中缀表达式
        return expression.split(" ");
    }
}
```

### 4. 通用表达式求值框架
```java
/**
 * 通用表达式求值框架
 */
public abstract class ExpressionEvaluator<T> {
    
    protected abstract boolean isOperand(String token);
    protected abstract boolean isOperator(String token);
    protected abstract T parseOperand(String token);
    protected abstract T applyOperator(String operator, T operand1, T operand2);
    protected abstract int getOperatorPrecedence(String operator);
    protected abstract boolean isLeftAssociative(String operator);
    
    public T evaluateRPN(String[] tokens) {
        Deque<T> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isOperand(token)) {
                stack.push(parseOperand(token));
            } else if (isOperator(token)) {
                T operand2 = stack.pop();
                T operand1 = stack.pop();
                T result = applyOperator(token, operand1, operand2);
                stack.push(result);
            }
        }
        
        return stack.pop();
    }
    
    public T evaluateInfix(String expression) {
        String[] rpnTokens = infixToRPN(expression);
        return evaluateRPN(rpnTokens);
    }
    
    private String[] infixToRPN(String expression) {
        List<String> output = new ArrayList<>();
        Deque<String> operators = new ArrayDeque<>();
        String[] tokens = tokenize(expression);
        
        for (String token : tokens) {
            if (isOperand(token)) {
                output.add(token);
            } else if (token.equals("(")) {
                operators.push(token);
            } else if (token.equals(")")) {
                while (!operators.isEmpty() && !operators.peek().equals("(")) {
                    output.add(operators.pop());
                }
                operators.pop(); // 弹出 '('
            } else if (isOperator(token)) {
                while (!operators.isEmpty() && 
                       !operators.peek().equals("(") &&
                       (getOperatorPrecedence(operators.peek()) > getOperatorPrecedence(token) ||
                        (getOperatorPrecedence(operators.peek()) == getOperatorPrecedence(token) && 
                         isLeftAssociative(token)))) {
                    output.add(operators.pop());
                }
                operators.push(token);
            }
        }
        
        while (!operators.isEmpty()) {
            output.add(operators.pop());
        }
        
        return output.toArray(new String[0]);
    }
    
    private String[] tokenize(String expression) {
        // 简化的分词实现
        return expression.replaceAll("\\s+", "").split("(?<=[-+*/()])|(?=[-+*/()])");
    }
}

// 整数表达式求值器实现
class IntegerExpressionEvaluator extends ExpressionEvaluator<Integer> {
    
    @Override
    protected boolean isOperand(String token) {
        try {
            Integer.parseInt(token);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
    
    @Override
    protected boolean isOperator(String token) {
        return "+".equals(token) || "-".equals(token) || "*".equals(token) || "/".equals(token);
    }
    
    @Override
    protected Integer parseOperand(String token) {
        return Integer.parseInt(token);
    }
    
    @Override
    protected Integer applyOperator(String operator, Integer operand1, Integer operand2) {
        switch (operator) {
            case "+": return operand1 + operand2;
            case "-": return operand1 - operand2;
            case "*": return operand1 * operand2;
            case "/": return operand1 / operand2;
            default: throw new IllegalArgumentException("Unknown operator: " + operator);
        }
    }
    
    @Override
    protected int getOperatorPrecedence(String operator) {
        switch (operator) {
            case "+":
            case "-":
                return 1;
            case "*":
            case "/":
                return 2;
            default:
                return 0;
        }
    }
    
    @Override
    protected boolean isLeftAssociative(String operator) {
        return true; // 所有基本运算符都是左结合的
    }
}
```

## 💡 解题技巧总结
### 1. 逆波兰表达式的核心特点
+ **无需括号**：操作符的位置决定了运算顺序
+ **栈天然适配**：后缀表达式的计算过程就是栈操作
+ **线性时间**：一次遍历即可完成计算

### 2. 栈操作的关键点
+ **操作数顺序**：弹出时要注意左右操作数的顺序
+ **栈空检查**：确保有足够的操作数进行运算
+ **结果唯一**：计算完成后栈中应只有一个元素

### 3. 实现优化技巧
+ **数组模拟栈**：避免对象创建开销
+ **操作符预处理**：使用Set或Map提高判断效率
+ **异常处理**：处理除零、栈空等边界情况

### 4. 扩展应用场景
+ **编译器设计**：表达式解析和代码生成
+ **计算器实现**：科学计算器的核心算法
+ **公式引擎**：电子表格、数据库查询优化
+ **语法分析**：编程语言的表达式求值

### 5. 相关算法模式
+ **中缀转后缀**：调度场算法（Shunting Yard）
+ **表达式树**：语法分析树的构建
+ **递归下降**：表达式解析的另一种方法

这道题是理解表达式栈应用的经典例题，掌握了逆波兰表达式的求值，就能理解更复杂的表达式处理算法！



> 更新: 2025-09-19 00:54:16  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/281c14a5d007467d12f2f20188e63e27>