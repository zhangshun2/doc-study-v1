# LeetCode224-基本计算器

# LeetCode 224 - 基本计算器
## 📋 题目描述
**难度：困难**

给你一个字符串表达式 `s` ，请你实现一个基本计算器来计算并返回它的值。

**注意：**不允许使用任何将字符串作为数学表达式计算的内置函数，比如 `eval()` 。

### 示例
**示例 1：**

```plain
输入：s = "1 + 1"
输出：2
```

**示例 2：**

```plain
输入：s = " 2-1 + 2 "
输出：3
```

**示例 3：**

```plain
输入：s = "(1+(4+5+2)-3)+(6+8)"
输出：23
```

### 约束条件
+ `1 <= s.length <= 3 * 10^5`
+ `s` 由数字、`'+'`、`'-'`、`'('`、`')'`、和 `' '` 组成
+ `s` 表示一个有效的表达式
+ `'+'` 不能用作一元运算的正号
+ `'-'` 可以用作一元运算的负号
+ 输入中不存在两个连续的操作符

## 🎯 解题思路
### 核心问题分析
这是一个**中缀表达式求值**问题，比逆波兰表达式更复杂，因为：

1. 需要处理括号的优先级
2. 需要处理运算符的优先级（虽然这题只有加减）
3. 需要处理一元负号
4. 需要实时计算而不是转换为后缀表达式

### 表达式栈解法原理
有两种主要方法：

1. **双栈法**：一个栈存数字，一个栈存操作符
2. **单栈法**：只用一个栈，遇到括号时保存当前状态

我们重点讲解**单栈法**，因为它更适合这道题的特点（只有加减法）。

```plain
单栈法核心思想：
1. 用栈保存每一层括号的计算结果和符号
2. 遇到 '(' 时，将当前结果和符号压栈，重新开始计算
3. 遇到 ')' 时，弹出栈顶的结果和符号，与当前结果合并
4. 数字直接参与计算
5. 符号影响下一个数字的正负性

栈的作用：
- 保存括号嵌套时的中间状态
- 实现括号优先级的正确处理
- 支持任意深度的括号嵌套
```

### 算法步骤
```plain
单栈法步骤：
1. 初始化：result = 0, sign = 1, stack = []
2. 遍历字符串：
   a. 数字：累积完整数字，根据当前符号加到result
   b. '+': 设置sign = 1
   c. '-': 设置sign = -1  
   d. '(': 将当前result和sign压栈，重置result=0, sign=1
   e. ')': 弹出栈顶，计算：栈顶result + 栈顶sign * 当前result
3. 返回最终result

双栈法步骤：
1. 初始化：数字栈nums，操作符栈ops
2. 遍历字符串：
   a. 数字：压入nums栈
   b. 操作符：根据优先级决定是否先计算栈顶操作
   c. '(': 压入ops栈
   d. ')': 计算直到遇到'('
3. 处理剩余操作符
4. 返回nums栈顶元素
```

### 图解演示
**示例：s = "(1+(4+5+2)-3)+(6+8)"**

#### 单栈法图解
```plain
表达式: (1+(4+5+2)-3)+(6+8)
初始状态: result=0, sign=1, stack=[]

步骤1: 处理 '('
操作: 压栈当前状态
stack: [0, 1]  (result=0, sign=1)
重置: result=0, sign=1

步骤2: 处理 '1'
操作: result = 0 + 1 * 1 = 1
状态: result=1, sign=1, stack=[0, 1]

步骤3: 处理 '+'
操作: sign = 1
状态: result=1, sign=1, stack=[0, 1]

步骤4: 处理 '('
操作: 压栈当前状态
stack: [0, 1, 1, 1]  (之前的0,1 + 当前的1,1)
重置: result=0, sign=1

步骤5: 处理 '4'
操作: result = 0 + 1 * 4 = 4
状态: result=4, sign=1, stack=[0, 1, 1, 1]

步骤6: 处理 '+'
操作: sign = 1
状态: result=4, sign=1, stack=[0, 1, 1, 1]

步骤7: 处理 '5'
操作: result = 4 + 1 * 5 = 9
状态: result=9, sign=1, stack=[0, 1, 1, 1]

步骤8: 处理 '+'
操作: sign = 1
状态: result=9, sign=1, stack=[0, 1, 1, 1]

步骤9: 处理 '2'
操作: result = 9 + 1 * 2 = 11
状态: result=11, sign=1, stack=[0, 1, 1, 1]

步骤10: 处理 ')'
操作: 弹出栈顶 (prev_sign=1, prev_result=1)
计算: result = 1 + 1 * 11 = 12
状态: result=12, sign=1, stack=[0, 1]

步骤11: 处理 '-'
操作: sign = -1
状态: result=12, sign=-1, stack=[0, 1]

步骤12: 处理 '3'
操作: result = 12 + (-1) * 3 = 9
状态: result=9, sign=-1, stack=[0, 1]

步骤13: 处理 ')'
操作: 弹出栈顶 (prev_sign=1, prev_result=0)
计算: result = 0 + 1 * 9 = 9
状态: result=9, sign=1, stack=[]

步骤14: 处理 '+'
操作: sign = 1
状态: result=9, sign=1, stack=[]

步骤15: 处理 '('
操作: 压栈当前状态
stack: [9, 1]
重置: result=0, sign=1

步骤16: 处理 '6'
操作: result = 0 + 1 * 6 = 6
状态: result=6, sign=1, stack=[9, 1]

步骤17: 处理 '+'
操作: sign = 1
状态: result=6, sign=1, stack=[9, 1]

步骤18: 处理 '8'
操作: result = 6 + 1 * 8 = 14
状态: result=14, sign=1, stack=[9, 1]

步骤19: 处理 ')'
操作: 弹出栈顶 (prev_sign=1, prev_result=9)
计算: result = 9 + 1 * 14 = 23
状态: result=23, sign=1, stack=[]

最终结果: 23
```

#### 双栈法图解
```plain
表达式: (1+(4+5+2)-3)+(6+8)
初始状态: nums=[], ops=[]

步骤1: '(' -> ops=['(']
步骤2: '1' -> nums=[1], ops=['(']
步骤3: '+' -> ops=['(', '+']
步骤4: '(' -> ops=['(', '+', '(']
步骤5: '4' -> nums=[1, 4], ops=['(', '+', '(']
步骤6: '+' -> ops=['(', '+', '(', '+']
步骤7: '5' -> nums=[1, 4, 5], ops=['(', '+', '(', '+']
步骤8: '+' -> 
  计算: 4 + 5 = 9
  nums=[1, 9], ops=['(', '+', '(']
  添加: ops=['(', '+', '(', '+']
步骤9: '2' -> nums=[1, 9, 2], ops=['(', '+', '(', '+']
步骤10: ')' -> 
  计算: 9 + 2 = 11
  nums=[1, 11], ops=['(', '+']
  弹出'('
步骤11: '-' -> 
  计算: 1 + 11 = 12
  nums=[12], ops=['(']
  添加: ops=['(', '-']
步骤12: '3' -> nums=[12, 3], ops=['(', '-']
步骤13: ')' -> 
  计算: 12 - 3 = 9
  nums=[9], ops=[]
步骤14: '+' -> ops=['+']
步骤15: '(' -> ops=['+', '(']
步骤16: '6' -> nums=[9, 6], ops=['+', '(']
步骤17: '+' -> ops=['+', '(', '+']
步骤18: '8' -> nums=[9, 6, 8], ops=['+', '(', '+']
步骤19: ')' -> 
  计算: 6 + 8 = 14
  nums=[9, 14], ops=['+']
  弹出'('
最终计算: 9 + 14 = 23

最终结果: 23
```

## 💻 代码实现
### 方法一：单栈法（推荐）
```java
public class Solution {
    public int calculate(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        int result = 0;
        int sign = 1;  // 1表示正号，-1表示负号
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (Character.isDigit(c)) {
                // 读取完整的数字
                int num = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                i--; // 回退一位，因为for循环会自动i++
                
                // 将数字加到结果中
                result += sign * num;
                
            } else if (c == '+') {
                sign = 1;
            } else if (c == '-') {
                sign = -1;
            } else if (c == '(') {
                // 遇到左括号，保存当前状态到栈中
                stack.push(result);  // 保存当前结果
                stack.push(sign);    // 保存当前符号
                
                // 重置状态，开始新的计算
                result = 0;
                sign = 1;
            } else if (c == ')') {
                // 遇到右括号，恢复之前的状态
                int prevSign = stack.pop();    // 弹出之前的符号
                int prevResult = stack.pop();  // 弹出之前的结果
                
                // 合并结果：之前的结果 + 之前的符号 * 当前结果
                result = prevResult + prevSign * result;
            }
            // 忽略空格
        }
        
        return result;
    }
}
```

### 方法二：双栈法
```java
public class SolutionTwoStacks {
    public int calculate(String s) {
        Deque<Integer> nums = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == ' ') continue;
            
            if (Character.isDigit(c)) {
                // 读取完整数字
                int num = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                i--; // 回退
                nums.push(num);
                
            } else if (c == '(') {
                ops.push(c);
                
            } else if (c == ')') {
                // 计算直到遇到左括号
                while (!ops.isEmpty() && ops.peek() != '(') {
                    calculate(nums, ops);
                }
                ops.pop(); // 弹出左括号
                
            } else if (c == '+' || c == '-') {
                // 处理同级或更高优先级的操作符
                while (!ops.isEmpty() && ops.peek() != '(') {
                    calculate(nums, ops);
                }
                ops.push(c);
            }
        }
        
        // 处理剩余的操作符
        while (!ops.isEmpty()) {
            calculate(nums, ops);
        }
        
        return nums.pop();
    }
    
    private void calculate(Deque<Integer> nums, Deque<Character> ops) {
        if (nums.size() < 2 || ops.isEmpty()) return;
        
        int num2 = nums.pop();
        int num1 = nums.pop();
        char op = ops.pop();
        
        int result = (op == '+') ? num1 + num2 : num1 - num2;
        nums.push(result);
    }
}
```

### 方法三：递归下降解析
```java
public class SolutionRecursive {
    
    private int index = 0;
    
    public int calculate(String s) {
        index = 0;
        return parseExpression(s);
    }
    
    private int parseExpression(String s) {
        int result = parseTerm(s);
        
        while (index < s.length()) {
            skipWhitespace(s);
            if (index >= s.length()) break;
            
            char op = s.charAt(index);
            if (op == '+' || op == '-') {
                index++;
                int term = parseTerm(s);
                result = (op == '+') ? result + term : result - term;
            } else {
                break;
            }
        }
        
        return result;
    }
    
    private int parseTerm(String s) {
        skipWhitespace(s);
        
        if (index >= s.length()) return 0;
        
        char c = s.charAt(index);
        
        if (c == '(') {
            index++; // 跳过 '('
            int result = parseExpression(s);
            skipWhitespace(s);
            index++; // 跳过 ')'
            return result;
        } else if (c == '-') {
            index++; // 跳过 '-'
            return -parseTerm(s);
        } else if (c == '+') {
            index++; // 跳过 '+'
            return parseTerm(s);
        } else if (Character.isDigit(c)) {
            return parseNumber(s);
        }
        
        return 0;
    }
    
    private int parseNumber(String s) {
        int num = 0;
        while (index < s.length() && Character.isDigit(s.charAt(index))) {
            num = num * 10 + (s.charAt(index) - '0');
            index++;
        }
        return num;
    }
    
    private void skipWhitespace(String s) {
        while (index < s.length() && s.charAt(index) == ' ') {
            index++;
        }
    }
}
```

### 方法四：状态机解法
```java
public class SolutionStateMachine {
    
    enum State {
        EXPECT_NUMBER,    // 期待数字
        EXPECT_OPERATOR,  // 期待操作符
        IN_NUMBER,        // 正在读取数字
        IN_PARENTHESES    // 在括号内
    }
    
    public int calculate(String s) {
        Deque<Integer> values = new ArrayDeque<>();
        Deque<Character> operators = new ArrayDeque<>();
        
        State state = State.EXPECT_NUMBER;
        int currentNumber = 0;
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == ' ') continue;
            
            switch (state) {
                case EXPECT_NUMBER:
                    if (Character.isDigit(c)) {
                        currentNumber = c - '0';
                        state = State.IN_NUMBER;
                    } else if (c == '(') {
                        operators.push(c);
                    } else if (c == '-') {
                        // 一元负号
                        operators.push(c);
                    } else if (c == '+') {
                        // 一元正号，忽略
                    }
                    break;
                    
                case IN_NUMBER:
                    if (Character.isDigit(c)) {
                        currentNumber = currentNumber * 10 + (c - '0');
                    } else {
                        values.push(currentNumber);
                        currentNumber = 0;
                        state = State.EXPECT_OPERATOR;
                        i--; // 重新处理当前字符
                    }
                    break;
                    
                case EXPECT_OPERATOR:
                    if (c == '+' || c == '-') {
                        processOperators(values, operators, c);
                        operators.push(c);
                        state = State.EXPECT_NUMBER;
                    } else if (c == ')') {
                        processUntilLeftParen(values, operators);
                    } else if (c == '(') {
                        operators.push(c);
                        state = State.EXPECT_NUMBER;
                    }
                    break;
            }
        }
        
        // 处理最后一个数字
        if (state == State.IN_NUMBER) {
            values.push(currentNumber);
        }
        
        // 处理剩余操作符
        while (!operators.isEmpty()) {
            processOperator(values, operators);
        }
        
        return values.pop();
    }
    
    private void processOperators(Deque<Integer> values, Deque<Character> operators, char newOp) {
        while (!operators.isEmpty() && operators.peek() != '(' && 
               getPrecedence(operators.peek()) >= getPrecedence(newOp)) {
            processOperator(values, operators);
        }
    }
    
    private void processUntilLeftParen(Deque<Integer> values, Deque<Character> operators) {
        while (!operators.isEmpty() && operators.peek() != '(') {
            processOperator(values, operators);
        }
        if (!operators.isEmpty()) {
            operators.pop(); // 弹出 '('
        }
    }
    
    private void processOperator(Deque<Integer> values, Deque<Character> operators) {
        if (operators.isEmpty()) return;
        
        char op = operators.pop();
        
        if (op == '-' && values.size() == 1) {
            // 一元负号
            int value = values.pop();
            values.push(-value);
        } else if (values.size() >= 2) {
            // 二元操作符
            int right = values.pop();
            int left = values.pop();
            int result = (op == '+') ? left + right : left - right;
            values.push(result);
        }
    }
    
    private int getPrecedence(char op) {
        return (op == '+' || op == '-') ? 1 : 0;
    }
}
```

### 方法五：带详细日志的实现
```java
public class SolutionWithLogging {
    
    public int calculate(String s) {
        System.out.println("🧮 开始计算表达式: \"" + s + "\"");
        System.out.println("=" + "=".repeat(60));
        
        Deque<Integer> stack = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == ' ') continue;
            
            System.out.printf("步骤 %d: 处理字符 '%c'\n", i + 1, c);
            
            if (Character.isDigit(c)) {
                int num = 0;
                int start = i;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                i--;
                
                System.out.printf("  🔢 读取数字: %d (位置 %d-%d)\n", num, start, i);
                result += sign * num;
                System.out.printf("  ⚡ 计算: result = %d + %d * %d = %d\n", 
                                result - sign * num, sign, num, result);
                
            } else if (c == '+') {
                sign = 1;
                System.out.printf("  ➕ 设置符号: sign = %d\n", sign);
                
            } else if (c == '-') {
                sign = -1;
                System.out.printf("  ➖ 设置符号: sign = %d\n", sign);
                
            } else if (c == '(') {
                System.out.printf("  📥 遇到左括号，保存状态到栈\n");
                System.out.printf("    保存 result = %d\n", result);
                System.out.printf("    保存 sign = %d\n", sign);
                
                stack.push(result);
                stack.push(sign);
                
                result = 0;
                sign = 1;
                System.out.printf("    重置: result = %d, sign = %d\n", result, sign);
                
            } else if (c == ')') {
                System.out.printf("  📤 遇到右括号，恢复状态\n");
                
                int prevSign = stack.pop();
                int prevResult = stack.pop();
                
                System.out.printf("    弹出 prevSign = %d\n", prevSign);
                System.out.printf("    弹出 prevResult = %d\n", prevResult);
                System.out.printf("    当前 result = %d\n", result);
                
                result = prevResult + prevSign * result;
                System.out.printf("    合并: result = %d + %d * %d = %d\n", 
                                prevResult, prevSign, result - prevResult, result);
            }
            
            System.out.printf("  📚 当前状态: result=%d, sign=%d, stack=%s\n", 
                            result, sign, stack);
            System.out.println();
        }
        
        System.out.println("🏆 计算完成！最终结果: " + result);
        return result;
    }
    
    public static void main(String[] args) {
        SolutionWithLogging solution = new SolutionWithLogging();
        
        String[] testCases = {
            "1 + 1",
            " 2-1 + 2 ",
            "(1+(4+5+2)-3)+(6+8)"
        };
        
        for (String testCase : testCases) {
            System.out.printf("🧪 测试用例: \"%s\"\n", testCase);
            solution.calculate(testCase);
            System.out.println("\n" + "=".repeat(70) + "\n");
        }
    }
}
```

### 方法六：通用表达式计算器框架
```java
/**
 * 通用表达式计算器，支持扩展操作符
 */
public class UniversalCalculator {
    
    // 操作符优先级映射
    private static final Map<Character, Integer> PRECEDENCE = Map.of(
        '+', 1,
        '-', 1,
        '*', 2,
        '/', 2,
        '^', 3  // 幂运算
    );
    
    // 操作符计算函数
    private static final Map<Character, BinaryOperator<Integer>> OPERATIONS = Map.of(
        '+', Integer::sum,
        '-', (a, b) -> a - b,
        '*', (a, b) -> a * b,
        '/', (a, b) -> a / b,
        '^', (a, b) -> (int) Math.pow(a, b)
    );
    
    public int calculate(String s) {
        return evaluateInfix(s);
    }
    
    private int evaluateInfix(String expression) {
        Deque<Integer> values = new ArrayDeque<>();
        Deque<Character> operators = new ArrayDeque<>();
        
        for (int i = 0; i < expression.length(); i++) {
            char c = expression.charAt(i);
            
            if (c == ' ') continue;
            
            if (Character.isDigit(c)) {
                // 读取完整数字
                int num = 0;
                while (i < expression.length() && Character.isDigit(expression.charAt(i))) {
                    num = num * 10 + (expression.charAt(i) - '0');
                    i++;
                }
                i--; // 回退
                values.push(num);
                
            } else if (c == '(') {
                operators.push(c);
                
            } else if (c == ')') {
                // 计算直到左括号
                while (!operators.isEmpty() && operators.peek() != '(') {
                    applyOperation(values, operators);
                }
                operators.pop(); // 弹出左括号
                
            } else if (isOperator(c)) {
                // 处理操作符优先级
                while (!operators.isEmpty() && 
                       operators.peek() != '(' && 
                       hasHigherPrecedence(operators.peek(), c)) {
                    applyOperation(values, operators);
                }
                operators.push(c);
            }
        }
        
        // 处理剩余操作符
        while (!operators.isEmpty()) {
            applyOperation(values, operators);
        }
        
        return values.pop();
    }
    
    private boolean isOperator(char c) {
        return PRECEDENCE.containsKey(c);
    }
    
    private boolean hasHigherPrecedence(char op1, char op2) {
        return PRECEDENCE.get(op1) >= PRECEDENCE.get(op2);
    }
    
    private void applyOperation(Deque<Integer> values, Deque<Character> operators) {
        if (values.size() < 2 || operators.isEmpty()) return;
        
        char operator = operators.pop();
        int operand2 = values.pop();
        int operand1 = values.pop();
        
        int result = OPERATIONS.get(operator).apply(operand1, operand2);
        values.push(result);
    }
    
    // 支持函数的扩展版本
    public double calculateWithFunctions(String expression) {
        // 预处理函数调用
        expression = preprocessFunctions(expression);
        return evaluateInfixDouble(expression);
    }
    
    private String preprocessFunctions(String expression) {
        // 简化实现：将sin(x), cos(x)等函数调用转换为数值
        // 实际实现需要更复杂的解析逻辑
        return expression;
    }
    
    private double evaluateInfixDouble(String expression) {
        // 类似于整数版本，但使用double类型
        // 这里省略具体实现
        return 0.0;
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**单栈法：**

+ 每个字符最多被访问一次
+ 栈操作（push/pop）为O(1)
+ 总时间复杂度：**O(n)**，其中n是字符串长度

**双栈法：**

+ 每个数字和操作符最多入栈出栈一次
+ 总时间复杂度：**O(n)**

**递归下降：**

+ 每个字符被访问一次
+ 递归深度取决于括号嵌套层数
+ 总时间复杂度：**O(n)**

### 空间复杂度
**单栈法：**

+ 栈的大小取决于括号的嵌套深度
+ 最坏情况：O(n)（如"((((1))))"）
+ 平均情况：O(log n)
+ 空间复杂度：**O(n)**

**双栈法：**

+ 需要两个栈分别存储数字和操作符
+ 空间复杂度：**O(n)**

**递归下降：**

+ 递归调用栈的深度等于括号嵌套深度
+ 空间复杂度：**O(n)**

## 🎨 可视化演示
### 详细计算过程演示
```java
/**
 * 可视化基本计算器的计算过程
 */
public class VisualCalculator {
    
    public static int calculateWithVisualization(String s) {
        System.out.println("🧮 基本计算器");
        System.out.println("表达式: \"" + s + "\"");
        System.out.println("=" + "=".repeat(60));
        
        Deque<Integer> stack = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        
        // 创建可视化的表达式
        String cleanExpression = s.replaceAll(" ", "");
        System.out.println("清理后的表达式: " + cleanExpression);
        System.out.println();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == ' ') continue;
            
            System.out.printf("📍 步骤 %d: 处理字符 '%c' (位置 %d)\n", 
                            getCurrentStep(s, i), c, i);
            
            if (Character.isDigit(c)) {
                int num = 0;
                int startPos = i;
                
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                i--;
                
                System.out.printf("  🔢 读取数字: %d (位置 %d-%d)\n", num, startPos, i);
                
                int oldResult = result;
                result += sign * num;
                
                System.out.printf("  ⚡ 计算: %d + (%d) × %d = %d\n", 
                                oldResult, sign, num, result);
                
            } else if (c == '+') {
                sign = 1;
                System.out.printf("  ➕ 设置符号为正: sign = %d\n", sign);
                
            } else if (c == '-') {
                sign = -1;
                System.out.printf("  ➖ 设置符号为负: sign = %d\n", sign);
                
            } else if (c == '(') {
                System.out.printf("  🔓 遇到左括号，保存当前状态\n");
                System.out.printf("    📥 压入 result: %d\n", result);
                System.out.printf("    📥 压入 sign: %d\n", sign);
                
                stack.push(result);
                stack.push(sign);
                
                result = 0;
                sign = 1;
                
                System.out.printf("    🔄 重置状态: result = %d, sign = %d\n", result, sign);
                
            } else if (c == ')') {
                System.out.printf("  🔒 遇到右括号，恢复之前状态\n");
                
                int prevSign = stack.pop();
                int prevResult = stack.pop();
                
                System.out.printf("    📤 弹出 prevSign: %d\n", prevSign);
                System.out.printf("    📤 弹出 prevResult: %d\n", prevResult);
                System.out.printf("    📊 当前括号内结果: %d\n", result);
                
                int oldResult = result;
                result = prevResult + prevSign * result;
                
                System.out.printf("    🔗 合并结果: %d + (%d) × %d = %d\n", 
                                prevResult, prevSign, oldResult, result);
            }
            
            printCurrentState(result, sign, stack, s, i);
            System.out.println();
        }
        
        System.out.println("🏆 计算完成！");
        System.out.println("最终结果: " + result);
        
        return result;
    }
    
    private static int getCurrentStep(String s, int currentIndex) {
        int step = 1;
        for (int i = 0; i <= currentIndex; i++) {
            if (s.charAt(i) != ' ') {
                if (i == currentIndex) return step;
                step++;
            }
        }
        return step;
    }
    
    private static void printCurrentState(int result, int sign, Deque<Integer> stack, 
                                        String expression, int currentIndex) {
        System.out.printf("  📊 当前状态:\n");
        System.out.printf("    result = %d\n", result);
        System.out.printf("    sign = %d\n", sign);
        System.out.printf("    stack = %s\n", formatStack(stack));
        
        // 显示处理进度
        System.out.printf("    进度: ");
        for (int i = 0; i < expression.length(); i++) {
            if (expression.charAt(i) == ' ') continue;
            
            if (i <= currentIndex) {
                System.out.printf("✅");
            } else {
                System.out.printf("⬜");
            }
        }
        System.out.println();
        
        System.out.printf("    表达式: ");
        for (int i = 0; i < expression.length(); i++) {
            if (expression.charAt(i) == ' ') continue;
            
            if (i == currentIndex) {
                System.out.printf("[%c]", expression.charAt(i));
            } else {
                System.out.printf(" %c ", expression.charAt(i));
            }
        }
        System.out.println();
    }
    
    private static String formatStack(Deque<Integer> stack) {
        if (stack.isEmpty()) {
            return "[]";
        }
        
        List<Integer> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < stackList.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append(stackList.get(i));
        }
        sb.append("] (底→顶)");
        
        return sb.toString();
    }
    
    public static void main(String[] args) {
        String[] testCases = {
            "1 + 1",
            " 2-1 + 2 ",
            "(1+(4+5+2)-3)+(6+8)",
            "2-(1+2)",
            "((1+2)*3-4)/2"
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("🧪 测试用例 %d:\n", i + 1);
            try {
                calculateWithVisualization(testCases[i]);
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
🧪 测试用例 3:
🧮 基本计算器
表达式: "(1+(4+5+2)-3)+(6+8)"
============================================================
清理后的表达式: (1+(4+5+2)-3)+(6+8)

📍 步骤 1: 处理字符 '(' (位置 0)
  🔓 遇到左括号，保存当前状态
    📥 压入 result: 0
    📥 压入 sign: 1
    🔄 重置状态: result = 0, sign = 1
  📊 当前状态:
    result = 0
    sign = 1
    stack = [0, 1] (底→顶)
    进度: ✅⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    表达式: [(] 1  +  (  4  +  5  +  2  )  -  3  )  +  (  6  +  8  ) 

📍 步骤 2: 处理字符 '1' (位置 1)
  🔢 读取数字: 1 (位置 1-1)
  ⚡ 计算: 0 + (1) × 1 = 1
  📊 当前状态:
    result = 1
    sign = 1
    stack = [0, 1] (底→顶)
    进度: ✅✅⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    表达式:  (  [1] +  (  4  +  5  +  2  )  -  3  )  +  (  6  +  8  ) 

📍 步骤 3: 处理字符 '+' (位置 2)
  ➕ 设置符号为正: sign = 1
  📊 当前状态:
    result = 1
    sign = 1
    stack = [0, 1] (底→顶)
    进度: ✅✅✅⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
    表达式:  (   1  [+] (  4  +  5  +  2  )  -  3  )  +  (  6  +  8  ) 

... (继续显示每一步的详细过程)

🏆 计算完成！
最终结果: 23
```

## 🧪 测试用例
### 基础功能测试
```java
public class BasicCalculatorTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicOperations() {
        // 基本加法
        assertEquals(2, solution.calculate("1 + 1"));
        
        // 基本减法
        assertEquals(1, solution.calculate("2 - 1"));
        
        // 多项运算
        assertEquals(3, solution.calculate(" 2-1 + 2 "));
        
        // 单个数字
        assertEquals(42, solution.calculate("42"));
        assertEquals(0, solution.calculate("0"));
    }
    
    @Test
    public void testParentheses() {
        // 简单括号
        assertEquals(3, solution.calculate("(1 + 2)"));
        assertEquals(-1, solution.calculate("(1 - 2)"));
        
        // 嵌套括号
        assertEquals(23, solution.calculate("(1+(4+5+2)-3)+(6+8)"));
        assertEquals(2, solution.calculate("((1+2)*3-4)/2"));
        
        // 多层嵌套
        assertEquals(10, solution.calculate("(((1+2)+3)+4)"));
        assertEquals(-2, solution.calculate("(((1-2)-3)-4)"));
    }
    
    @Test
    public void testNegativeNumbers() {
        // 一元负号
        assertEquals(-1, solution.calculate("-1"));
        assertEquals(-3, solution.calculate("-(1+2)"));
        
        // 负数运算
        assertEquals(1, solution.calculate("2 + (-1)"));
        assertEquals(3, solution.calculate("2 - (-1)"));
        
        // 复杂负数表达式
        assertEquals(-5, solution.calculate("-(2+3)"));
        assertEquals(1, solution.calculate("-(2-3)"));
    }
    
    @Test
    public void testWhitespace() {
        // 各种空格情况
        assertEquals(3, solution.calculate("1+2"));
        assertEquals(3, solution.calculate(" 1 + 2 "));
        assertEquals(3, solution.calculate("  1  +  2  "));
        assertEquals(3, solution.calculate("\t1\n+\r2\f"));
    }
    
    @Test
    public void testComplexExpressions() {
        // 复杂表达式
        assertEquals(14, solution.calculate("1 + 2 + 3 + 4 + 5 - 1"));
        assertEquals(0, solution.calculate("1 - 1 + 1 - 1"));
        assertEquals(10, solution.calculate("(1+2)+(3+4)"));
        assertEquals(-2, solution.calculate("(1+2)-(3+4)"));
        
        // 长表达式
        assertEquals(55, solution.calculate("1+2+3+4+5+6+7+8+9+10"));
        assertEquals(-53, solution.calculate("1-2-3-4-5-6-7-8-9-10"));
    }
}
```

### 边界条件测试
```java
public class BasicCalculatorBoundaryTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testMinimalCases() {
        // 最小输入
        assertEquals(0, solution.calculate("0"));
        assertEquals(1, solution.calculate("1"));
        assertEquals(-1, solution.calculate("-1"));
    }
    
    @Test
    public void testMaximalNesting() {
        // 深度嵌套括号
        StringBuilder sb = new StringBuilder();
        int depth = 1000;
        
        // 构造 ((((...((1))...))))
        for (int i = 0; i < depth; i++) {
            sb.append("(");
        }
        sb.append("1");
        for (int i = 0; i < depth; i++) {
            sb.append(")");
        }
        
        assertEquals(1, solution.calculate(sb.toString()));
    }
    
    @Test
    public void testLargeNumbers() {
        // 大数字
        assertEquals(1000000, solution.calculate("1000000"));
        assertEquals(2000000, solution.calculate("1000000 + 1000000"));
        assertEquals(0, solution.calculate("1000000 - 1000000"));
    }
    
    @Test
    public void testLongExpressions() {
        // 长表达式
        StringBuilder sb = new StringBuilder();
        int expected = 0;
        
        for (int i = 1; i <= 100; i++) {
            if (i > 1) sb.append(" + ");
            sb.append(i);
            expected += i;
        }
        
        assertEquals(expected, solution.calculate(sb.toString()));
    }
    
    @Test
    public void testAlternatingOperations() {
        // 交替运算
        assertEquals(1, solution.calculate("1 + 1 - 1"));
        assertEquals(1, solution.calculate("1 - 1 + 1"));
        assertEquals(0, solution.calculate("1 + 1 - 1 - 1"));
        assertEquals(2, solution.calculate("1 + 1 + 1 - 1"));
    }
    
    @Test
    public void testEmptyParentheses() {
        // 空括号（实际上不会出现，但测试健壮性）
        assertEquals(1, solution.calculate("1 + (0)"));
        assertEquals(1, solution.calculate("(1) + (0)"));
        assertEquals(2, solution.calculate("(1) + (1)"));
    }
}
```

### 性能测试
```java
public class BasicCalculatorPerformanceTest {
    
    @Test
    public void testPerformanceComparison() {
        // 构造大型表达式
        StringBuilder sb = new StringBuilder();
        int size = 10000;
        
        // 构造形如 "1+1+1+...+1" 的表达式
        for (int i = 0; i < size; i++) {
            if (i > 0) sb.append("+");
            sb.append("1");
        }
        
        String expression = sb.toString();
        
        // 测试不同实现的性能
        Solution solution1 = new Solution();
        SolutionTwoStacks solution2 = new SolutionTwoStacks();
        SolutionRecursive solution3 = new SolutionRecursive();
        
        long startTime, endTime;
        
        // 单栈法
        startTime = System.nanoTime();
        int result1 = solution1.calculate(expression);
        endTime = System.nanoTime();
        System.out.printf("单栈法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 双栈法
        startTime = System.nanoTime();
        int result2 = solution2.calculate(expression);
        endTime = System.nanoTime();
        System.out.printf("双栈法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 递归法
        startTime = System.nanoTime();
        int result3 = solution3.calculate(expression);
        endTime = System.nanoTime();
        System.out.printf("递归法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        assertEquals(result1, result3);
        assertEquals(size, result1); // 预期结果
        
        System.out.println("性能测试通过 ✅");
    }
    
    @Test
    public void testMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // 构造深度嵌套的表达式
        StringBuilder sb = new StringBuilder();
        int depth = 5000;
        
        for (int i = 0; i < depth; i++) {
            sb.append("(");
        }
        sb.append("1");
        for (int i = 0; i < depth; i++) {
            sb.append(")");
        }
        
        String expression = sb.toString();
        
        // 测试内存使用
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        Solution solution = new Solution();
        solution.calculate(expression);
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        System.out.printf("栈深度: %d\n", depth);
    }
    
    @Test
    public void testScalability() {
        Solution solution = new Solution();
        
        // 测试不同规模的表达式
        int[] sizes = {100, 1000, 10000, 100000};
        
        for (int size : sizes) {
            StringBuilder sb = new StringBuilder();
            
            // 构造表达式
            for (int i = 0; i < size; i++) {
                if (i > 0) sb.append("+");
                sb.append("1");
            }
            
            String expression = sb.toString();
            
            long startTime = System.nanoTime();
            int result = solution.calculate(expression);
            long endTime = System.nanoTime();
            
            double timeMs = (endTime - startTime) / 1_000_000.0;
            
            System.out.printf("规模 %6d: %8.2f ms, 结果: %d\n", size, timeMs, result);
            assertEquals(size, result);
        }
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 227 - 基本计算器 II（支持乘除法）
```java
/**
 * 基本计算器 II - 支持 +, -, *, / 运算
 */
public class BasicCalculatorII {
    
    public int calculate(String s) {
        Deque<Integer> stack = new ArrayDeque<>();
        char operation = '+';
        int num = 0;
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            }
            
            if (!Character.isDigit(c) && c != ' ' || i == s.length() - 1) {
                switch (operation) {
                    case '+':
                        stack.push(num);
                        break;
                    case '-':
                        stack.push(-num);
                        break;
                    case '*':
                        stack.push(stack.pop() * num);
                        break;
                    case '/':
                        stack.push(stack.pop() / num);
                        break;
                }
                operation = c;
                num = 0;
            }
        }
        
        int result = 0;
        while (!stack.isEmpty()) {
            result += stack.pop();
        }
        
        return result;
    }
}
```

### 2. LeetCode 772 - 基本计算器 III（支持括号和乘除法）
```java
/**
 * 基本计算器 III - 支持 +, -, *, /, () 运算
 */
public class BasicCalculatorIII {
    
    public int calculate(String s) {
        return calculate(s, new int[]{0});
    }
    
    private int calculate(String s, int[] index) {
        Deque<Integer> stack = new ArrayDeque<>();
        char operation = '+';
        int num = 0;
        
        while (index[0] < s.length()) {
            char c = s.charAt(index[0]++);
            
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '(') {
                num = calculate(s, index); // 递归处理括号内容
            } else if (c == ')') {
                break; // 结束当前括号
            }
            
            if (!Character.isDigit(c) && c != ' ' || index[0] == s.length()) {
                switch (operation) {
                    case '+':
                        stack.push(num);
                        break;
                    case '-':
                        stack.push(-num);
                        break;
                    case '*':
                        stack.push(stack.pop() * num);
                        break;
                    case '/':
                        stack.push(stack.pop() / num);
                        break;
                }
                operation = c;
                num = 0;
            }
        }
        
        int result = 0;
        while (!stack.isEmpty()) {
            result += stack.pop();
        }
        
        return result;
    }
}
```

### 3. 支持变量的表达式计算器
```java
/**
 * 支持变量的表达式计算器
 */
public class VariableCalculator {
    
    private Map<String, Integer> variables;
    
    public VariableCalculator() {
        this.variables = new HashMap<>();
    }
    
    public void setVariable(String name, int value) {
        variables.put(name, value);
    }
    
    public int calculate(String expression) {
        List<String> tokens = tokenize(expression);
        List<String> postfix = infixToPostfix(tokens);
        return evaluatePostfix(postfix);
    }
    
    private List<String> tokenize(String expression) {
        List<String> tokens = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        
        for (char c : expression.toCharArray()) {
            if (Character.isWhitespace(c)) {
                if (current.length() > 0) {
                    tokens.add(current.toString());
                    current.setLength(0);
                }
            } else if (isOperator(c) || c == '(' || c == ')') {
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
        List<String> output = new ArrayList<>();
        Deque<String> operators = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isNumber(token) || isVariable(token)) {
                output.add(token);
            } else if (token.equals("(")) {
                operators.push(token);
            } else if (token.equals(")")) {
                while (!operators.isEmpty() && !operators.peek().equals("(")) {
                    output.add(operators.pop());
                }
                operators.pop(); // 弹出 '('
            } else if (isOperatorString(token)) {
                while (!operators.isEmpty() && 
                       !operators.peek().equals("(") &&
                       precedence(operators.peek()) >= precedence(token)) {
                    output.add(operators.pop());
                }
                operators.push(token);
            }
        }
        
        while (!operators.isEmpty()) {
            output.add(operators.pop());
        }
        
        return output;
    }
    
    private int evaluatePostfix(List<String> tokens) {
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (String token : tokens) {
            if (isNumber(token)) {
                stack.push(Integer.parseInt(token));
            } else if (isVariable(token)) {
                if (!variables.containsKey(token)) {
                    throw new IllegalArgumentException("未定义的变量: " + token);
                }
                stack.push(variables.get(token));
            } else if (isOperatorString(token)) {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = applyOperator(token, operand1, operand2);
                stack.push(result);
            }
        }
        
        return stack.pop();
    }
    
    private boolean isNumber(String token) {
        try {
            Integer.parseInt(token);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
    
    private boolean isVariable(String token) {
        return token.matches("[a-zA-Z][a-zA-Z0-9]*");
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
    
    private int applyOperator(String operator, int operand1, int operand2) {
        switch (operator) {
            case "+": return operand1 + operand2;
            case "-": return operand1 - operand2;
            case "*": return operand1 * operand2;
            case "/": return operand1 / operand2;
            default: throw new IllegalArgumentException("未知操作符: " + operator);
        }
    }
    
    // 使用示例
    public static void main(String[] args) {
        VariableCalculator calculator = new VariableCalculator();
        
        // 设置变量
        calculator.setVariable("x", 10);
        calculator.setVariable("y", 5);
        calculator.setVariable("z", 2);
        
        // 计算表达式
        System.out.println(calculator.calculate("x + y")); // 15
        System.out.println(calculator.calculate("x * y - z")); // 48
        System.out.println(calculator.calculate("(x + y) * z")); // 30
    }
}
```

### 4. 表达式优化器
```java
/**
 * 表达式优化器 - 对表达式进行代数优化
 */
public class ExpressionOptimizer {
    
    static class ExpressionNode {
        String value;
        ExpressionNode left;
        ExpressionNode right;
        
        ExpressionNode(String value) {
            this.value = value;
        }
        
        boolean isOperator() {
            return "+".equals(value) || "-".equals(value) || 
                   "*".equals(value) || "/".equals(value);
        }
        
        boolean isNumber() {
            try {
                Integer.parseInt(value);
                return true;
            } catch (NumberFormatException e) {
                return false;
            }
        }
        
        int getNumber() {
            return Integer.parseInt(value);
        }
    }
    
    public String optimize(String expression) {
        ExpressionNode tree = parseExpression(expression);
        ExpressionNode optimized = optimizeTree(tree);
        return treeToString(optimized);
    }
    
    private ExpressionNode optimizeTree(ExpressionNode node) {
        if (node == null || !node.isOperator()) {
            return node;
        }
        
        // 递归优化子树
        node.left = optimizeTree(node.left);
        node.right = optimizeTree(node.right);
        
        // 常量折叠优化
        if (node.left.isNumber() && node.right.isNumber()) {
            int left = node.left.getNumber();
            int right = node.right.getNumber();
            int result;
            
            switch (node.value) {
                case "+": result = left + right; break;
                case "-": result = left - right; break;
                case "*": result = left * right; break;
                case "/": result = left / right; break;
                default: return node;
            }
            
            return new ExpressionNode(String.valueOf(result));
        }
        
        // 代数优化
        return applyAlgebraicOptimizations(node);
    }
    
    private ExpressionNode applyAlgebraicOptimizations(ExpressionNode node) {
        // x + 0 = x
        if ("+".equals(node.value) && node.right.isNumber() && node.right.getNumber() == 0) {
            return node.left;
        }
        
        // 0 + x = x
        if ("+".equals(node.value) && node.left.isNumber() && node.left.getNumber() == 0) {
            return node.right;
        }
        
        // x - 0 = x
        if ("-".equals(node.value) && node.right.isNumber() && node.right.getNumber() == 0) {
            return node.left;
        }
        
        // x * 1 = x
        if ("*".equals(node.value) && node.right.isNumber() && node.right.getNumber() == 1) {
            return node.left;
        }
        
        // 1 * x = x
        if ("*".equals(node.value) && node.left.isNumber() && node.left.getNumber() == 1) {
            return node.right;
        }
        
        // x * 0 = 0
        if ("*".equals(node.value) && 
            ((node.left.isNumber() && node.left.getNumber() == 0) ||
             (node.right.isNumber() && node.right.getNumber() == 0))) {
            return new ExpressionNode("0");
        }
        
        // x / 1 = x
        if ("/".equals(node.value) && node.right.isNumber() && node.right.getNumber() == 1) {
            return node.left;
        }
        
        return node;
    }
    
    private ExpressionNode parseExpression(String expression) {
        // 简化实现，实际需要完整的表达式解析器
        return new ExpressionNode(expression);
    }
    
    private String treeToString(ExpressionNode node) {
        if (node == null) return "";
        
        if (!node.isOperator()) {
            return node.value;
        }
        
        return "(" + treeToString(node.left) + " " + node.value + " " + treeToString(node.right) + ")";
    }
}
```

## 🎯 解题技巧总结
### 核心技巧
1. **栈的选择策略**
    - 单栈法：适合只有加减法的情况
    - 双栈法：适合有运算符优先级的情况
    - 递归法：适合复杂嵌套的情况
2. **括号处理技巧**

```java
// 遇到 '(' 时保存状态
stack.push(result);
stack.push(sign);
result = 0;
sign = 1;

// 遇到 ')' 时恢复状态
int prevSign = stack.pop();
int prevResult = stack.pop();
result = prevResult + prevSign * result;
```

3. **数字读取技巧**

```java
// 读取完整的多位数字
int num = 0;
while (i < s.length() && Character.isDigit(s.charAt(i))) {
    num = num * 10 + (s.charAt(i) - '0');
    i++;
}
i--; // 重要：回退一位
```

4. **符号处理技巧**

```java
// 用sign变量记录下一个数字的符号
int sign = 1;  // 1表示正，-1表示负

if (c == '+') sign = 1;
else if (c == '-') sign = -1;

result += sign * num;  // 应用符号
```

### 常见陷阱
1. **忘记处理空格**

```java
if (c == ' ') continue;  // 跳过空格
```

2. **数字读取后忘记回退**

```java
while (i < s.length() && Character.isDigit(s.charAt(i))) {
    num = num * 10 + (s.charAt(i) - '0');
    i++;
}
i--; // 必须回退，否则会跳过下一个字符
```

3. **栈操作顺序错误**

```java
// 正确的顺序
stack.push(result);  // 先压入结果
stack.push(sign);    // 再压入符号

// 弹出时顺序相反
int prevSign = stack.pop();    // 先弹出符号
int prevResult = stack.pop();  // 再弹出结果
```

4. **一元负号处理**

```java
// 表达式开头的负号是一元负号
// 括号后的负号也可能是一元负号
if (c == '-' && (i == 0 || s.charAt(i-1) == '(')) {
    sign = -1;
}
```

### 扩展应用
1. **支持更多运算符**
    - 乘法和除法：需要考虑运算符优先级
    - 幂运算：右结合性
    - 取模运算：与乘除同级
2. **支持函数调用**
    - sin, cos, tan等三角函数
    - log, exp等对数指数函数
    - max, min等聚合函数
3. **支持变量和常量**
    - 变量替换
    - 常量定义
    - 符号计算
4. **表达式优化**
    - 常量折叠
    - 代数简化
    - 公共子表达式消除

### 最佳实践
1. **代码结构清晰**

```java
// 将不同功能分离到不同方法
private int parseNumber(String s, int[] index) { ... }
private void skipWhitespace(String s, int[] index) { ... }
private void processOperator(char op) { ... }
```

2. **错误处理完善**

```java
// 检查除零错误
if (operator == '/' && operand2 == 0) {
    throw new ArithmeticException("除零错误");
}

// 检查栈空错误
if (stack.isEmpty()) {
    throw new IllegalStateException("表达式格式错误");
}
```

3. **测试覆盖全面**
    - 基础运算测试
    - 边界条件测试
    - 错误情况测试
    - 性能压力测试
4. **文档注释详细**

```java
/**
 * 计算基本数学表达式的值
 * @param s 包含数字、+、-、(、)和空格的字符串表达式
 * @return 表达式的计算结果
 * @throws IllegalArgumentException 当表达式格式不正确时
 */
public int calculate(String s) { ... }
```

通过掌握这些技巧和最佳实践，你可以轻松应对各种表达式计算问题，并且能够扩展到更复杂的场景。记住，表达式栈结构的核心是**正确处理运算符优先级和括号嵌套**，这是所有表达式求值问题的基础。



> 更新: 2025-09-19 00:54:18  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/24d9279aef3fc8bbafc58aad4c7f2bbd>