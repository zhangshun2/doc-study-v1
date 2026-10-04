# LeetCode394-字符串解码

# LeetCode 394 - 字符串解码
## 📋 题目描述
**难度：中等**

给定一个经过编码的字符串，返回它解码后的字符串。

编码规则为: `k[encoded_string]`，表示其中方括号内部的 `encoded_string` 正好重复 `k` 次。注意 `k` 保证为正整数。

你可以认为输入字符串总是有效的；输入字符串中没有额外的空格，且输入的方括号总是符合格式要求的。

此外，你可以认为原始数据不包含数字，所有的数字只表示重复的次数 `k` ，例如不会出现像 `3a` 或 `2[4]` 的输入。

### 示例
**示例 1：**

```plain
输入：s = "3[a]2[bc]"
输出："aaabcbc"
```

**示例 2：**

```plain
输入：s = "2[abc]3[cd]ef"
输出："abcabccdcdcdef"
```

**示例 3：**

```plain
输入：s = "abc3[cd]xyz"
输出："abccdcdcdxyz"
```

**示例 4：**

```plain
输入：s = "2[a2[bc]]"
输出："abcbcabcbc"
```

### 约束条件
+ `1 <= s.length <= 30`
+ `s` 由小写英文字母、数字和方括号 `'[]'` 组成
+ `s` 保证是一个有效的输入
+ `s` 中所有整数的取值范围为 `[1, 300]`

## 🎯 解题思路
### 核心问题分析
这是一个典型的**状态栈结构**问题，需要处理：

1. **嵌套结构**：方括号可以嵌套，如 `2[a2[bc]]`
2. **状态保存**：遇到 `[` 时需要保存当前状态
3. **状态恢复**：遇到 `]` 时需要恢复之前的状态
4. **字符串构建**：需要动态构建结果字符串

### 状态栈解法原理
**状态栈的核心思想：**

```plain
状态定义：
- 当前正在构建的字符串
- 当前的重复次数

栈的作用：
1. 保存每一层嵌套的状态
2. 支持任意深度的嵌套
3. 确保正确的状态恢复顺序

状态转换：
遇到数字 → 累积重复次数
遇到字母 → 添加到当前字符串
遇到 '[' → 保存当前状态到栈，重置状态
遇到 ']' → 弹出栈顶状态，构建重复字符串
```

### 算法步骤
```plain
状态栈算法步骤：
1. 初始化：
   - 当前字符串 currentStr = ""
   - 当前数字 currentNum = 0
   - 状态栈 stack = []

2. 遍历字符串中的每个字符：
   a. 如果是数字：累积到 currentNum
   b. 如果是字母：添加到 currentStr
   c. 如果是 '['：
      - 将 (currentStr, currentNum) 压入栈
      - 重置 currentStr = "", currentNum = 0
   d. 如果是 ']'：
      - 弹出栈顶 (prevStr, prevNum)
      - 构建重复字符串：prevStr + currentStr * prevNum
      - 更新 currentStr = 构建的字符串

3. 返回 currentStr
```

### 图解演示
**示例：s = "2[a2[bc]]"**

```plain
输入字符串: 2[a2[bc]]
初始状态: currentStr="", currentNum=0, stack=[]

步骤1: 处理 '2'
操作: currentNum = 2
状态: currentStr="", currentNum=2, stack=[]

步骤2: 处理 '['
操作: 压栈 ("", 2)，重置状态
状态: currentStr="", currentNum=0, stack=[("", 2)]

步骤3: 处理 'a'
操作: currentStr += 'a'
状态: currentStr="a", currentNum=0, stack=[("", 2)]

步骤4: 处理 '2'
操作: currentNum = 2
状态: currentStr="a", currentNum=2, stack=[("", 2)]

步骤5: 处理 '['
操作: 压栈 ("a", 2)，重置状态
状态: currentStr="", currentNum=0, stack=[("", 2), ("a", 2)]

步骤6: 处理 'b'
操作: currentStr += 'b'
状态: currentStr="b", currentNum=0, stack=[("", 2), ("a", 2)]

步骤7: 处理 'c'
操作: currentStr += 'c'
状态: currentStr="bc", currentNum=0, stack=[("", 2), ("a", 2)]

步骤8: 处理 ']'
操作: 弹出 ("a", 2)，构建 "a" + "bc" * 2 = "abcbc"
状态: currentStr="abcbc", currentNum=0, stack=[("", 2)]

步骤9: 处理 ']'
操作: 弹出 ("", 2)，构建 "" + "abcbc" * 2 = "abcbcabcbc"
状态: currentStr="abcbcabcbc", currentNum=0, stack=[]

最终结果: "abcbcabcbc"
```

#### 详细状态转换图
```plain
字符串: 2 [ a 2 [ b c ] ]
索引:   0 1 2 3 4 5 6 7 8

状态栈变化过程:

初始: stack=[], currentStr="", currentNum=0
      ┌─────────────────┐
      │     栈空        │
      └─────────────────┘

处理'2': currentNum=2
      ┌─────────────────┐
      │     栈空        │
      └─────────────────┘
      currentStr="", currentNum=2

处理'[': 压栈("", 2)
      ┌─────────────────┐
      │   ("", 2)       │
      └─────────────────┘
      currentStr="", currentNum=0

处理'a': currentStr="a"
      ┌─────────────────┐
      │   ("", 2)       │
      └─────────────────┘
      currentStr="a", currentNum=0

处理'2': currentNum=2
      ┌─────────────────┐
      │   ("", 2)       │
      └─────────────────┘
      currentStr="a", currentNum=2

处理'[': 压栈("a", 2)
      ┌─────────────────┐
      │   ("a", 2)      │
      ├─────────────────┤
      │   ("", 2)       │
      └─────────────────┘
      currentStr="", currentNum=0

处理'b': currentStr="b"
      ┌─────────────────┐
      │   ("a", 2)      │
      ├─────────────────┤
      │   ("", 2)       │
      └─────────────────┘
      currentStr="b", currentNum=0

处理'c': currentStr="bc"
      ┌─────────────────┐
      │   ("a", 2)      │
      ├─────────────────┤
      │   ("", 2)       │
      └─────────────────┘
      currentStr="bc", currentNum=0

处理']': 弹出("a", 2)，构建"a"+"bc"*2="abcbc"
      ┌─────────────────┐
      │   ("", 2)       │
      └─────────────────┘
      currentStr="abcbc", currentNum=0

处理']': 弹出("", 2)，构建""+"abcbc"*2="abcbcabcbc"
      ┌─────────────────┐
      │     栈空        │
      └─────────────────┘
      currentStr="abcbcabcbc", currentNum=0

最终结果: "abcbcabcbc"
```

## 💻 代码实现
### 方法一：状态栈法（推荐）
```java
public class Solution {
    public String decodeString(String s) {
        Deque<String> stringStack = new ArrayDeque<>();  // 存储字符串状态
        Deque<Integer> numStack = new ArrayDeque<>();    // 存储数字状态
        
        StringBuilder currentStr = new StringBuilder();
        int currentNum = 0;
        
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) {
                // 累积数字（可能是多位数）
                currentNum = currentNum * 10 + (c - '0');
                
            } else if (c == '[') {
                // 遇到左括号，保存当前状态
                stringStack.push(currentStr.toString());
                numStack.push(currentNum);
                
                // 重置状态，开始新的解码
                currentStr = new StringBuilder();
                currentNum = 0;
                
            } else if (c == ']') {
                // 遇到右括号，恢复之前状态并构建结果
                String prevStr = stringStack.pop();
                int repeatCount = numStack.pop();
                
                // 构建重复字符串
                StringBuilder temp = new StringBuilder(prevStr);
                for (int i = 0; i < repeatCount; i++) {
                    temp.append(currentStr);
                }
                
                currentStr = temp;
                
            } else {
                // 普通字符，直接添加
                currentStr.append(c);
            }
        }
        
        return currentStr.toString();
    }
}
```

### 方法二：单栈优化版
```java
public class SolutionOptimized {
    
    static class State {
        StringBuilder str;
        int num;
        
        State(StringBuilder str, int num) {
            this.str = str;
            this.num = num;
        }
    }
    
    public String decodeString(String s) {
        Deque<State> stack = new ArrayDeque<>();
        StringBuilder currentStr = new StringBuilder();
        int currentNum = 0;
        
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) {
                currentNum = currentNum * 10 + (c - '0');
                
            } else if (c == '[') {
                // 保存当前状态
                stack.push(new State(currentStr, currentNum));
                currentStr = new StringBuilder();
                currentNum = 0;
                
            } else if (c == ']') {
                // 恢复状态并构建结果
                State prevState = stack.pop();
                StringBuilder temp = new StringBuilder(prevState.str);
                
                // 重复当前字符串
                for (int i = 0; i < prevState.num; i++) {
                    temp.append(currentStr);
                }
                
                currentStr = temp;
                
            } else {
                currentStr.append(c);
            }
        }
        
        return currentStr.toString();
    }
}
```

### 方法三：递归解法
```java
public class SolutionRecursive {
    
    private int index = 0;
    
    public String decodeString(String s) {
        index = 0;
        return decode(s);
    }
    
    private String decode(String s) {
        StringBuilder result = new StringBuilder();
        int num = 0;
        
        while (index < s.length()) {
            char c = s.charAt(index++);
            
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
                
            } else if (c == '[') {
                // 递归解码括号内容
                String decoded = decode(s);
                
                // 重复解码的字符串
                for (int i = 0; i < num; i++) {
                    result.append(decoded);
                }
                
                num = 0; // 重置数字
                
            } else if (c == ']') {
                // 结束当前层递归
                break;
                
            } else {
                // 普通字符
                result.append(c);
            }
        }
        
        return result.toString();
    }
}
```

### 方法四：字符串替换法（暴力）
```java
public class SolutionBruteForce {
    
    public String decodeString(String s) {
        // 持续替换直到没有括号
        while (s.contains("[")) {
            s = replaceInnermost(s);
        }
        return s;
    }
    
    private String replaceInnermost(String s) {
        // 找到最内层的括号
        int start = -1;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '[') {
                start = i;
            } else if (s.charAt(i) == ']') {
                // 找到对应的数字
                int numStart = start - 1;
                while (numStart >= 0 && Character.isDigit(s.charAt(numStart))) {
                    numStart--;
                }
                numStart++;
                
                // 提取数字和字符串
                int num = Integer.parseInt(s.substring(numStart, start));
                String str = s.substring(start + 1, i);
                
                // 构建重复字符串
                StringBuilder repeated = new StringBuilder();
                for (int j = 0; j < num; j++) {
                    repeated.append(str);
                }
                
                // 替换原字符串
                return s.substring(0, numStart) + repeated.toString() + s.substring(i + 1);
            }
        }
        
        return s;
    }
}
```

### 方法五：状态机解法
```java
public class SolutionStateMachine {
    
    enum State {
        READING_CHAR,    // 读取普通字符
        READING_NUMBER,  // 读取数字
        IN_BRACKETS      // 在括号内
    }
    
    public String decodeString(String s) {
        Deque<StringBuilder> stringStack = new ArrayDeque<>();
        Deque<Integer> numStack = new ArrayDeque<>();
        
        StringBuilder currentStr = new StringBuilder();
        int currentNum = 0;
        State state = State.READING_CHAR;
        
        for (char c : s.toCharArray()) {
            switch (state) {
                case READING_CHAR:
                    if (Character.isDigit(c)) {
                        currentNum = c - '0';
                        state = State.READING_NUMBER;
                    } else {
                        currentStr.append(c);
                    }
                    break;
                    
                case READING_NUMBER:
                    if (Character.isDigit(c)) {
                        currentNum = currentNum * 10 + (c - '0');
                    } else if (c == '[') {
                        stringStack.push(currentStr);
                        numStack.push(currentNum);
                        currentStr = new StringBuilder();
                        currentNum = 0;
                        state = State.IN_BRACKETS;
                    }
                    break;
                    
                case IN_BRACKETS:
                    if (Character.isDigit(c)) {
                        currentNum = c - '0';
                        state = State.READING_NUMBER;
                    } else if (c == '[') {
                        stringStack.push(currentStr);
                        numStack.push(currentNum);
                        currentStr = new StringBuilder();
                        currentNum = 0;
                    } else if (c == ']') {
                        StringBuilder prevStr = stringStack.pop();
                        int repeatCount = numStack.pop();
                        
                        for (int i = 0; i < repeatCount; i++) {
                            prevStr.append(currentStr);
                        }
                        
                        currentStr = prevStr;
                        state = stringStack.isEmpty() ? State.READING_CHAR : State.IN_BRACKETS;
                    } else {
                        currentStr.append(c);
                    }
                    break;
            }
        }
        
        return currentStr.toString();
    }
}
```

### 方法六：带详细日志的实现
```java
public class SolutionWithLogging {
    
    public String decodeString(String s) {
        System.out.println("🔤 开始解码字符串: \"" + s + "\"");
        System.out.println("=" + "=".repeat(60));
        
        Deque<String> stringStack = new ArrayDeque<>();
        Deque<Integer> numStack = new ArrayDeque<>();
        
        StringBuilder currentStr = new StringBuilder();
        int currentNum = 0;
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            System.out.printf("步骤 %d: 处理字符 '%c'\n", i + 1, c);
            
            if (Character.isDigit(c)) {
                currentNum = currentNum * 10 + (c - '0');
                System.out.printf("  🔢 累积数字: currentNum = %d\n", currentNum);
                
            } else if (c == '[') {
                System.out.printf("  📥 遇到左括号，保存状态\n");
                System.out.printf("    保存字符串: \"%s\"\n", currentStr.toString());
                System.out.printf("    保存数字: %d\n", currentNum);
                
                stringStack.push(currentStr.toString());
                numStack.push(currentNum);
                
                currentStr = new StringBuilder();
                currentNum = 0;
                
                System.out.printf("    重置状态: currentStr=\"\", currentNum=0\n");
                
            } else if (c == ']') {
                System.out.printf("  📤 遇到右括号，恢复状态\n");
                
                String prevStr = stringStack.pop();
                int repeatCount = numStack.pop();
                
                System.out.printf("    弹出字符串: \"%s\"\n", prevStr);
                System.out.printf("    弹出数字: %d\n", repeatCount);
                System.out.printf("    当前字符串: \"%s\"\n", currentStr.toString());
                
                StringBuilder temp = new StringBuilder(prevStr);
                for (int j = 0; j < repeatCount; j++) {
                    temp.append(currentStr);
                }
                
                currentStr = temp;
                System.out.printf("    构建结果: \"%s\"\n", currentStr.toString());
                
            } else {
                currentStr.append(c);
                System.out.printf("  🔤 添加字符: currentStr = \"%s\"\n", currentStr.toString());
            }
            
            printCurrentState(currentStr, currentNum, stringStack, numStack);
            System.out.println();
        }
        
        String result = currentStr.toString();
        System.out.println("🏆 解码完成！最终结果: \"" + result + "\"");
        
        return result;
    }
    
    private void printCurrentState(StringBuilder currentStr, int currentNum,
                                 Deque<String> stringStack, Deque<Integer> numStack) {
        System.out.printf("  📊 当前状态:\n");
        System.out.printf("    currentStr = \"%s\"\n", currentStr.toString());
        System.out.printf("    currentNum = %d\n", currentNum);
        System.out.printf("    stringStack = %s\n", formatStringStack(stringStack));
        System.out.printf("    numStack = %s\n", formatNumStack(numStack));
    }
    
    private String formatStringStack(Deque<String> stack) {
        if (stack.isEmpty()) return "[]";
        
        List<String> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < stackList.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append("\"").append(stackList.get(i)).append("\"");
        }
        sb.append("] (底→顶)");
        
        return sb.toString();
    }
    
    private String formatNumStack(Deque<Integer> stack) {
        if (stack.isEmpty()) return "[]";
        
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
        SolutionWithLogging solution = new SolutionWithLogging();
        
        String[] testCases = {
            "3[a]2[bc]",
            "2[abc]3[cd]ef",
            "abc3[cd]xyz",
            "2[a2[bc]]"
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("🧪 测试用例 %d:\n", i + 1);
            solution.decodeString(testCases[i]);
            System.out.println("\n" + "=".repeat(70) + "\n");
        }
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**状态栈法：**

+ 每个字符最多被访问一次
+ 字符串构建操作的总时间与最终结果长度成正比
+ 设最终结果长度为 M，输入长度为 N
+ 时间复杂度：**O(M)**，其中 M 是解码后字符串的长度

**递归法：**

+ 每个字符被访问一次
+ 递归深度等于括号嵌套深度
+ 时间复杂度：**O(M)**

**字符串替换法：**

+ 需要多次遍历字符串
+ 每次替换都需要重新构建字符串
+ 时间复杂度：**O(M × N)**，效率较低

### 空间复杂度
**状态栈法：**

+ 栈的大小取决于括号的嵌套深度
+ 字符串构建需要额外空间
+ 空间复杂度：**O(M + D)**，其中 D 是嵌套深度

**递归法：**

+ 递归调用栈的深度等于括号嵌套深度
+ 空间复杂度：**O(M + D)**

**字符串替换法：**

+ 需要存储中间结果
+ 空间复杂度：**O(M)**

## 🎨 可视化演示
### 详细解码过程演示
```java
/**
 * 可视化字符串解码的详细过程
 */
public class VisualDecoder {
    
    public static String decodeWithVisualization(String s) {
        System.out.println("🔤 字符串解码器");
        System.out.println("输入字符串: \"" + s + "\"");
        System.out.println("=" + "=".repeat(60));
        
        Deque<String> stringStack = new ArrayDeque<>();
        Deque<Integer> numStack = new ArrayDeque<>();
        
        StringBuilder currentStr = new StringBuilder();
        int currentNum = 0;
        
        // 显示初始状态
        System.out.println("初始状态:");
        printVisualization(s, -1, currentStr, currentNum, stringStack, numStack);
        System.out.println();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            System.out.printf("📍 步骤 %d: 处理字符 '%c' (位置 %d)\n", i + 1, c, i);
            
            if (Character.isDigit(c)) {
                currentNum = currentNum * 10 + (c - '0');
                System.out.printf("  🔢 数字累积: %d\n", currentNum);
                
            } else if (c == '[') {
                System.out.printf("  📥 左括号: 保存状态并重置\n");
                System.out.printf("    保存: (\"%s\", %d)\n", currentStr.toString(), currentNum);
                
                stringStack.push(currentStr.toString());
                numStack.push(currentNum);
                
                currentStr = new StringBuilder();
                currentNum = 0;
                
            } else if (c == ']') {
                System.out.printf("  📤 右括号: 恢复状态并构建\n");
                
                String prevStr = stringStack.pop();
                int repeatCount = numStack.pop();
                
                System.out.printf("    恢复: (\"%s\", %d)\n", prevStr, repeatCount);
                System.out.printf("    当前内容: \"%s\"\n", currentStr.toString());
                
                StringBuilder temp = new StringBuilder(prevStr);
                String repeated = currentStr.toString();
                
                System.out.printf("    重复构建: \"%s\" + \"%s\" × %d\n", 
                                prevStr, repeated, repeatCount);
                
                for (int j = 0; j < repeatCount; j++) {
                    temp.append(repeated);
                }
                
                currentStr = temp;
                System.out.printf("    构建结果: \"%s\"\n", currentStr.toString());
                
            } else {
                currentStr.append(c);
                System.out.printf("  🔤 字符添加: \"%s\"\n", currentStr.toString());
            }
            
            printVisualization(s, i, currentStr, currentNum, stringStack, numStack);
            System.out.println();
        }
        
        String result = currentStr.toString();
        System.out.println("🏆 解码完成！");
        System.out.println("最终结果: \"" + result + "\"");
        
        return result;
    }
    
    private static void printVisualization(String s, int currentIndex, 
                                         StringBuilder currentStr, int currentNum,
                                         Deque<String> stringStack, Deque<Integer> numStack) {
        
        // 显示处理进度
        System.out.printf("  进度: ");
        for (int i = 0; i < s.length(); i++) {
            if (i <= currentIndex) {
                System.out.printf("✅");
            } else {
                System.out.printf("⬜");
            }
        }
        System.out.println();
        
        // 显示字符串和当前位置
        System.out.printf("  字符串: ");
        for (int i = 0; i < s.length(); i++) {
            if (i == currentIndex) {
                System.out.printf("[%c]", s.charAt(i));
            } else {
                System.out.printf(" %c ", s.charAt(i));
            }
        }
        System.out.println();
        
        // 显示当前状态
        System.out.printf("  当前字符串: \"%s\"\n", currentStr.toString());
        System.out.printf("  当前数字: %d\n", currentNum);
        
        // 显示栈状态
        System.out.printf("  字符串栈: %s\n", formatStringStack(stringStack));
        System.out.printf("  数字栈: %s\n", formatNumStack(numStack));
        
        // 显示栈的可视化
        if (!stringStack.isEmpty() || !numStack.isEmpty()) {
            System.out.println("  栈可视化:");
            printStackVisualization(stringStack, numStack);
        }
    }
    
    private static void printStackVisualization(Deque<String> stringStack, Deque<Integer> numStack) {
        List<String> strings = new ArrayList<>(stringStack);
        List<Integer> numbers = new ArrayList<>(numStack);
        
        Collections.reverse(strings);
        Collections.reverse(numbers);
        
        for (int i = strings.size() - 1; i >= 0; i--) {
            System.out.printf("    ┌─────────────────┐\n");
            System.out.printf("    │ \"%s\" × %d%s │\n", 
                            strings.get(i), 
                            numbers.get(i),
                            " ".repeat(Math.max(0, 10 - strings.get(i).length() - String.valueOf(numbers.get(i)).length())));
            System.out.printf("    └─────────────────┘\n");
        }
        
        if (!strings.isEmpty()) {
            System.out.printf("    ↑ 栈顶\n");
        }
    }
    
    private static String formatStringStack(Deque<String> stack) {
        if (stack.isEmpty()) return "[]";
        
        List<String> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < stackList.size(); i++) {
            if (i > 0) sb.append(", ");
            sb.append("\"").append(stackList.get(i)).append("\"");
        }
        sb.append("]");
        
        return sb.toString();
    }
    
    private static String formatNumStack(Deque<Integer> stack) {
        if (stack.isEmpty()) return "[]";
        
        List<Integer> stackList = new ArrayList<>(stack);
        Collections.reverse(stackList);
        
        return stackList.toString();
    }
    
    public static void main(String[] args) {
        String[] testCases = {
            "3[a]",
            "2[bc]",
            "3[a]2[bc]",
            "2[a2[bc]]",
            "abc3[cd]xyz"
        };
        
        for (int i = 0; i < testCases.length; i++) {
            System.out.printf("🧪 测试用例 %d:\n", i + 1);
            try {
                decodeWithVisualization(testCases[i]);
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
🧪 测试用例 4:
🔤 字符串解码器
输入字符串: "2[a2[bc]]"
============================================================

初始状态:
  进度: ⬜⬜⬜⬜⬜⬜⬜⬜⬜
  字符串:  2  [  a  2  [  b  c  ]  ] 
  当前字符串: ""
  当前数字: 0
  字符串栈: []
  数字栈: []

📍 步骤 1: 处理字符 '2' (位置 0)
  🔢 数字累积: 2
  进度: ✅⬜⬜⬜⬜⬜⬜⬜⬜
  字符串: [2] [  a  2  [  b  c  ]  ] 
  当前字符串: ""
  当前数字: 2
  字符串栈: []
  数字栈: []

📍 步骤 2: 处理字符 '[' (位置 1)
  📥 左括号: 保存状态并重置
    保存: ("", 2)
  进度: ✅✅⬜⬜⬜⬜⬜⬜⬜
  字符串:  2 [[] a  2  [  b  c  ]  ] 
  当前字符串: ""
  当前数字: 0
  字符串栈: [""]
  数字栈: [2]
  栈可视化:
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 3: 处理字符 'a' (位置 2)
  🔤 字符添加: "a"
  进度: ✅✅✅⬜⬜⬜⬜⬜⬜
  字符串:  2  [ [a] 2  [  b  c  ]  ] 
  当前字符串: "a"
  当前数字: 0
  字符串栈: [""]
  数字栈: [2]
  栈可视化:
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 4: 处理字符 '2' (位置 3)
  🔢 数字累积: 2
  进度: ✅✅✅✅⬜⬜⬜⬜⬜
  字符串:  2  [  a [2] [  b  c  ]  ] 
  当前字符串: "a"
  当前数字: 2
  字符串栈: [""]
  数字栈: [2]
  栈可视化:
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 5: 处理字符 '[' (位置 4)
  📥 左括号: 保存状态并重置
    保存: ("a", 2)
  进度: ✅✅✅✅✅⬜⬜⬜⬜
  字符串:  2  [  a  2 [[] b  c  ]  ] 
  当前字符串: ""
  当前数字: 0
  字符串栈: ["", "a"]
  数字栈: [2, 2]
  栈可视化:
    ┌─────────────────┐
    │ "a" × 2         │
    └─────────────────┘
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 6: 处理字符 'b' (位置 5)
  🔤 字符添加: "b"
  进度: ✅✅✅✅✅✅⬜⬜⬜
  字符串:  2  [  a  2  [ [b] c  ]  ] 
  当前字符串: "b"
  当前数字: 0
  字符串栈: ["", "a"]
  数字栈: [2, 2]
  栈可视化:
    ┌─────────────────┐
    │ "a" × 2         │
    └─────────────────┘
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 7: 处理字符 'c' (位置 6)
  🔤 字符添加: "bc"
  进度: ✅✅✅✅✅✅✅⬜⬜
  字符串:  2  [  a  2  [  b [c] ]  ] 
  当前字符串: "bc"
  当前数字: 0
  字符串栈: ["", "a"]
  数字栈: [2, 2]
  栈可视化:
    ┌─────────────────┐
    │ "a" × 2         │
    └─────────────────┘
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 8: 处理字符 ']' (位置 7)
  📤 右括号: 恢复状态并构建
    恢复: ("a", 2)
    当前内容: "bc"
    重复构建: "a" + "bc" × 2
    构建结果: "abcbc"
  进度: ✅✅✅✅✅✅✅✅⬜
  字符串:  2  [  a  2  [  b  c []] ] 
  当前字符串: "abcbc"
  当前数字: 0
  字符串栈: [""]
  数字栈: [2]
  栈可视化:
    ┌─────────────────┐
    │ "" × 2          │
    └─────────────────┘
    ↑ 栈顶

📍 步骤 9: 处理字符 ']' (位置 8)
  📤 右括号: 恢复状态并构建
    恢复: ("", 2)
    当前内容: "abcbc"
    重复构建: "" + "abcbc" × 2
    构建结果: "abcbcabcbc"
  进度: ✅✅✅✅✅✅✅✅✅
  字符串:  2  [  a  2  [  b  c  ] []] 
  当前字符串: "abcbcabcbc"
  当前数字: 0
  字符串栈: []
  数字栈: []

🏆 解码完成！
最终结果: "abcbcabcbc"
```

## 🧪 测试用例
### 基础功能测试
```java
public class StringDecodeTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicDecoding() {
        // 简单重复
        assertEquals("aaa", solution.decodeString("3[a]"));
        assertEquals("bcbc", solution.decodeString("2[bc]"));
        
        // 多段重复
        assertEquals("aaabcbc", solution.decodeString("3[a]2[bc]"));
        assertEquals("abcabccdcdcdef", solution.decodeString("2[abc]3[cd]ef"));
        
        // 混合字符
        assertEquals("abccdcdcdxyz", solution.decodeString("abc3[cd]xyz"));
    }
    
    @Test
    public void testNestedDecoding() {
        // 简单嵌套
        assertEquals("abcbc", solution.decodeString("2[a2[bc]]"));
        assertEquals("accaccacc", solution.decodeString("3[a2[c]]"));
        
        // 复杂嵌套
        assertEquals("abcabccdcdcdcdcdcd", solution.decodeString("2[abc]3[cd]ef"));
        assertEquals("aaabcbcaaabcbc", solution.decodeString("2[a3[bc]]"));
        
        // 深度嵌套
        assertEquals("abcabcabcabc", solution.decodeString("4[abc]"));
        assertEquals("abcdefabcdefabcdef", solution.decodeString("3[abcdef]"));
    }
    
    @Test
    public void testEdgeCases() {
        // 单个字符
        assertEquals("a", solution.decodeString("1[a]"));
        assertEquals("", solution.decodeString("0[a]")); // 如果支持0
        
        // 无括号
        assertEquals("abc", solution.decodeString("abc"));
        assertEquals("", solution.decodeString(""));
        
        // 大数字
        assertEquals("a".repeat(100), solution.decodeString("100[a]"));
        assertEquals("ab".repeat(50), solution.decodeString("50[ab]"));
    }
    
    @Test
    public void testComplexCases() {
        // 复杂组合
        assertEquals("leetcodeleetcodeleetcodeleetcode", 
                    solution.decodeString("4[leetcode]"));
        
        // 多层嵌套
        assertEquals("aaabcbcaaabcbc", 
                    solution.decodeString("2[a3[bc]]"));
        
        // 混合模式
        assertEquals("xyzabcabcabcdefdefdef", 
                    solution.decodeString("xyz3[abc]3[def]"));
    }
}
```

### 边界条件测试
```java
public class StringDecodeBoundaryTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testMinimalCases() {
        // 最小有效输入
        assertEquals("a", solution.decodeString("1[a]"));
        assertEquals("aa", solution.decodeString("2[a]"));
        assertEquals("aaa", solution.decodeString("3[a]"));
    }
    
    @Test
    public void testMaximalNesting() {
        // 深度嵌套
        String input = "2[2[2[a]]]";
        String expected = "aaaaaaaa"; // 2^3 = 8个a
        assertEquals(expected, solution.decodeString(input));
        
        // 更深嵌套
        input = "3[2[a]]";
        expected = "aaaaaa"; // 3*2 = 6个a
        assertEquals(expected, solution.decodeString(input));
    }
    
    @Test
    public void testLargeNumbers() {
        // 大重复次数
        assertEquals("a".repeat(300), solution.decodeString("300[a]"));
        assertEquals("ab".repeat(150), solution.decodeString("150[ab]"));
        
        // 组合大数字
        assertEquals("abc".repeat(100) + "def".repeat(100), 
                    solution.decodeString("100[abc]100[def]"));
    }
    
    @Test
    public void testLongStrings() {
        // 长字符串
        StringBuilder sb = new StringBuilder();
        for (char c = 'a'; c <= 'z'; c++) {
            sb.append(c);
        }
        String alphabet = sb.toString();
        
        assertEquals(alphabet.repeat(5), 
                    solution.decodeString("5[" + alphabet + "]"));
    }
    
    @Test
    public void testComplexNesting() {
        // 复杂嵌套模式
        assertEquals("abcabcdefdefdefdef", 
                    solution.decodeString("2[abc]4[def]"));
        
        assertEquals("abcdefabcdefabcdefabcdef", 
                    solution.decodeString("4[abcdef]"));
        
        // 不规则嵌套
        assertEquals("aabbaabbaabb", 
                    solution.decodeString("3[a2[b]]"));
    }
}
```

### 性能测试
```java
public class StringDecodePerformanceTest {
    
    @Test
    public void testPerformanceComparison() {
        // 构造大型嵌套字符串
        String input = "100[a10[b]]";
        
        Solution solution1 = new Solution();
        SolutionOptimized solution2 = new SolutionOptimized();
        SolutionRecursive solution3 = new SolutionRecursive();
        
        long startTime, endTime;
        
        // 状态栈法
        startTime = System.nanoTime();
        String result1 = solution1.decodeString(input);
        endTime = System.nanoTime();
        System.out.printf("状态栈法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 优化版
        startTime = System.nanoTime();
        String result2 = solution2.decodeString(input);
        endTime = System.nanoTime();
        System.out.printf("优化版: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 递归法
        startTime = System.nanoTime();
        String result3 = solution3.decodeString(input);
        endTime = System.nanoTime();
        System.out.printf("递归法: %.2f ms\n", (endTime - startTime) / 1_000_000.0);
        
        // 验证结果一致性
        assertEquals(result1, result2);
        assertEquals(result1, result3);
        
        System.out.println("性能测试通过 ✅");
    }
    
    @Test
    public void testMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // 构造深度嵌套的字符串
        String input = "10[a10[b10[c]]]";
        
        runtime.gc();
        long memBefore = runtime.totalMemory() - runtime.freeMemory();
        
        Solution solution = new Solution();
        String result = solution.decodeString(input);
        
        long memAfter = runtime.totalMemory() - runtime.freeMemory();
        System.out.printf("内存使用: %d KB\n", (memAfter - memBefore) / 1024);
        System.out.printf("结果长度: %d\n", result.length());
        System.out.printf("嵌套深度: 3\n");
    }
    
    @Test
    public void testScalability() {
        Solution solution = new Solution();
        
        // 测试不同规模的输入
        int[] repeatCounts = {10, 50, 100, 200};
        
        for (int count : repeatCounts) {
            String input = count + "[a]";
            
            long startTime = System.nanoTime();
            String result = solution.decodeString(input);
            long endTime = System.nanoTime();
            
            double timeMs = (endTime - startTime) / 1_000_000.0;
            
            System.out.printf("重复 %3d 次: %6.2f ms, 结果长度: %d\n", 
                            count, timeMs, result.length());
            assertEquals(count, result.length());
        }
    }
}
```



> 更新: 2025-09-19 00:54:21  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/b38980cffb8bb94c92a5f084abca06d8>