# LeetCode 1249 - 移除无效的括号
## 📋 题目描述
**难度：中等**

给你一个由 `'('`、`')'` 和小写字母组成的字符串 `s`。

你需要从字符串中删除最少数目的无效括号，使得结果字符串的括号是匹配的。

返回任意一个合法的字符串。

有效括号字符串应当满足：

+ 任何左括号 `'('` 都有相应的右括号 `')'`。
+ 任何右括号 `')'` 都有相应的左括号 `'('`。
+ 左括号必须在对应的右括号之前。
+ 括号仅影响其他括号的有效性，不会影响字母。

### 示例
**示例 1：**

```plain
输入：s = "()())"
输出："()()"
解释：删除一个右括号使字符串变为 "()()"
```

**示例 2：**

```plain
输入：s = "((("
输出：""
解释：删除所有左括号使字符串变为 ""
```

**示例 3：**

```plain
输入：s = "())"
输出："()"
解释：删除一个右括号使字符串变为 "()"
```

### 约束条件
+ `1 <= s.length <= 10^5`
+ `s[i]` 为 `'('` 或 `')'` 或小写英文字母

## 🎯 解题思路
### 核心问题分析
这是一个典型的**栈+哈希表问题**。关键在于：

1. 使用栈来匹配括号对
2. 使用哈希表（Set）记录需要删除的括号位置
3. 两次遍历：第一次找出无效括号，第二次构建结果

### 栈+哈希表解法原理
```plain
核心思想：
- 第一次遍历：使用栈匹配括号，记录无效括号的索引
- 第二次遍历：根据记录的索引构建有效字符串

栈的作用：
- 存储左括号的索引
- 遇到右括号时尝试匹配
- 无法匹配的括号都是无效的

哈希表的作用：
- 记录所有无效括号的索引
- 快速判断某个位置的字符是否需要删除
```

### 算法步骤
```plain
1. 第一次遍历：
   - 遇到左括号：将索引压入栈
   - 遇到右括号：
     - 如果栈不为空，弹出栈顶（匹配成功）
     - 如果栈为空，记录当前索引为无效右括号
   - 遇到字母：直接跳过

2. 处理剩余左括号：
   - 栈中剩余的都是无效左括号，记录它们的索引

3. 第二次遍历：
   - 跳过所有记录在哈希表中的无效括号索引
   - 构建最终的有效字符串
```

### 图解演示
**示例：s = "()())"**

```plain
第一次遍历 - 括号匹配：

索引: 0 1 2 3 4
字符: ( ) ( ) )
栈:   []

步骤 1: 处理 '(' (索引 0)
栈: [0]
无效集合: {}

步骤 2: 处理 ')' (索引 1)  
栈不为空，弹出 0，匹配成功
栈: []
无效集合: {}

步骤 3: 处理 '(' (索引 2)
栈: [2]
无效集合: {}

步骤 4: 处理 ')' (索引 3)
栈不为空，弹出 2，匹配成功
栈: []
无效集合: {}

步骤 5: 处理 ')' (索引 4)
栈为空，无法匹配，记录为无效
栈: []
无效集合: {4}

处理剩余左括号：
栈为空，无剩余左括号

第二次遍历 - 构建结果：
索引 0: '(' 不在无效集合中，加入结果
索引 1: ')' 不在无效集合中，加入结果  
索引 2: '(' 不在无效集合中，加入结果
索引 3: ')' 不在无效集合中，加入结果
索引 4: ')' 在无效集合中，跳过

最终结果: "()()"
```

## 💻 代码实现
### 方法一：栈+哈希表（推荐）
```java
import java.util.*;

public class Solution {
    public String minRemoveToMakeValid(String s) {
        // 第一步：使用栈找出所有无效括号的索引
        Set<Integer> invalidIndices = new HashSet<>();
        Deque<Integer> stack = new ArrayDeque<>();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            
            if (c == '(') {
                // 左括号入栈
                stack.push(i);
            } else if (c == ')') {
                if (!stack.isEmpty()) {
                    // 匹配成功，弹出左括号
                    stack.pop();
                } else {
                    // 无法匹配的右括号
                    invalidIndices.add(i);
                }
            }
            // 字母直接跳过
        }
        
        // 栈中剩余的都是无效的左括号
        while (!stack.isEmpty()) {
            invalidIndices.add(stack.pop());
        }
        
        // 第二步：构建结果字符串
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            if (!invalidIndices.contains(i)) {
                result.append(s.charAt(i));
            }
        }
        
        return result.toString();
    }
}
```

### 方法二：两次遍历优化版
```java
public class SolutionOptimized {
    public String minRemoveToMakeValid(String s) {
        // 第一次遍历：从左到右，移除无效的右括号
        StringBuilder firstPass = new StringBuilder();
        int leftCount = 0;
        
        for (char c : s.toCharArray()) {
            if (c == '(') {
                firstPass.append(c);
                leftCount++;
            } else if (c == ')') {
                if (leftCount > 0) {
                    firstPass.append(c);
                    leftCount--;
                }
                // 否则跳过这个无效的右括号
            } else {
                firstPass.append(c);
            }
        }
        
        // 第二次遍历：从右到左，移除多余的左括号
        StringBuilder result = new StringBuilder();
        int rightCount = 0;
        
        for (int i = firstPass.length() - 1; i >= 0; i--) {
            char c = firstPass.charAt(i);
            
            if (c == ')') {
                result.append(c);
                rightCount++;
            } else if (c == '(') {
                if (rightCount > 0) {
                    result.append(c);
                    rightCount--;
                }
                // 否则跳过这个多余的左括号
            } else {
                result.append(c);
            }
        }
        
        return result.reverse().toString();
    }
}
```

### 方法三：计数法
```java
public class SolutionCounting {
    public String minRemoveToMakeValid(String s) {
        // 第一步：计算需要删除的括号数量
        int leftToRemove = 0;  // 需要删除的左括号数
        int rightToRemove = 0; // 需要删除的右括号数
        
        // 统计无效的右括号
        for (char c : s.toCharArray()) {
            if (c == '(') {
                leftToRemove++;
            } else if (c == ')') {
                if (leftToRemove > 0) {
                    leftToRemove--;
                } else {
                    rightToRemove++;
                }
            }
        }
        
        // 第二步：构建结果
        StringBuilder result = new StringBuilder();
        
        for (char c : s.toCharArray()) {
            if (c == '(' && leftToRemove > 0) {
                leftToRemove--;
                // 跳过这个左括号
            } else if (c == ')' && rightToRemove > 0) {
                rightToRemove--;
                // 跳过这个右括号
            } else {
                result.append(c);
            }
        }
        
        return result.toString();
    }
}
```

### 方法四：递归解法（理论参考）
```java
public class SolutionRecursive {
    
    public String minRemoveToMakeValid(String s) {
        Set<Integer> toRemove = new HashSet<>();
        findInvalidParentheses(s, 0, 0, new ArrayDeque<>(), toRemove);
        
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            if (!toRemove.contains(i)) {
                result.append(s.charAt(i));
            }
        }
        
        return result.toString();
    }
    
    private void findInvalidParentheses(String s, int index, int balance, 
                                       Deque<Integer> stack, Set<Integer> toRemove) {
        if (index == s.length()) {
            // 处理剩余的左括号
            toRemove.addAll(stack);
            return;
        }
        
        char c = s.charAt(index);
        
        if (c == '(') {
            stack.push(index);
            findInvalidParentheses(s, index + 1, balance + 1, stack, toRemove);
        } else if (c == ')') {
            if (!stack.isEmpty()) {
                stack.pop();
                findInvalidParentheses(s, index + 1, balance - 1, stack, toRemove);
            } else {
                toRemove.add(index);
                findInvalidParentheses(s, index + 1, balance, stack, toRemove);
            }
        } else {
            findInvalidParentheses(s, index + 1, balance, stack, toRemove);
        }
    }
}
```

## 🔍 复杂度分析
### 时间复杂度
**栈+哈希表解法：**

+ 第一次遍历：O(n)
+ 第二次遍历：O(n)
+ 总时间复杂度：O(n)

**两次遍历优化版：**

+ 第一次遍历：O(n)
+ 第二次遍历：O(n)
+ 字符串反转：O(n)
+ 总时间复杂度：O(n)

**计数法：**

+ 第一次遍历：O(n)
+ 第二次遍历：O(n)
+ 总时间复杂度：O(n)

### 空间复杂度
**栈+哈希表解法：**

+ 栈空间：O(n) 最坏情况下所有字符都是左括号
+ 哈希表空间：O(n) 最坏情况下所有括号都无效
+ 总空间复杂度：O(n)

**两次遍历优化版：**

+ StringBuilder空间：O(n)
+ 总空间复杂度：O(n)

**计数法：**

+ 只使用常数额外空间
+ 总空间复杂度：O(1)

## 🎨 可视化演示
### 详细过程演示
```java
/**
 * 带可视化输出的移除无效括号
 */
public class VisualMinRemove {
    
    public static String minRemoveToMakeValidWithVisualization(String s) {
        System.out.println("🔧 移除无效的括号");
        System.out.println("输入字符串: \"" + s + "\"");
        printStringWithIndices(s);
        System.out.println("=" + "=".repeat(60));
        
        // 第一步：使用栈找出无效括号
        Set<Integer> invalidIndices = new HashSet<>();
        Deque<Integer> stack = new ArrayDeque<>();
        
        System.out.println("📊 第一次遍历 - 使用栈匹配括号:");
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            System.out.printf("\n步骤 %d: 处理字符 '%c' (索引 %d)\n", i + 1, c, i);
            
            if (c == '(') {
                stack.push(i);
                System.out.printf("  📥 左括号入栈\n");
            } else if (c == ')') {
                if (!stack.isEmpty()) {
                    int matched = stack.pop();
                    System.out.printf("  ✅ 右括号匹配成功，与索引 %d 的左括号配对\n", matched);
                } else {
                    invalidIndices.add(i);
                    System.out.printf("  ❌ 右括号无法匹配，标记为无效\n");
                }
            } else {
                System.out.printf("  📝 字母字符，跳过\n");
            }
            
            printStackState(stack);
            printInvalidSet(invalidIndices);
        }
        
        // 处理剩余的左括号
        System.out.println("\n🔚 处理栈中剩余的左括号:");
        while (!stack.isEmpty()) {
            int leftIndex = stack.pop();
            invalidIndices.add(leftIndex);
            System.out.printf("  ❌ 索引 %d 的左括号无法匹配，标记为无效\n", leftIndex);
        }
        
        System.out.println("\n📋 最终无效括号索引: " + invalidIndices);
        
        // 第二步：构建结果
        System.out.println("\n🔨 第二次遍历 - 构建有效字符串:");
        StringBuilder result = new StringBuilder();
        
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (!invalidIndices.contains(i)) {
                result.append(c);
                System.out.printf("  ✅ 索引 %d 字符 '%c' 保留\n", i, c);
            } else {
                System.out.printf("  ❌ 索引 %d 字符 '%c' 删除\n", i, c);
            }
        }
        
        String finalResult = result.toString();
        System.out.println("\n🏆 最终结果: \"" + finalResult + "\"");
        
        // 验证结果
        System.out.println("\n🧪 验证结果:");
        if (isValidParentheses(finalResult)) {
            System.out.println("  ✅ 结果字符串括号匹配有效");
        } else {
            System.out.println("  ❌ 结果字符串括号匹配无效");
        }
        
        return finalResult;
    }
    
    private static void printStringWithIndices(String s) {
        System.out.print("索引: ");
        for (int i = 0; i < s.length(); i++) {
            System.out.printf("%2d ", i);
        }
        System.out.println();
        
        System.out.print("字符: ");
        for (char c : s.toCharArray()) {
            System.out.printf(" %c ", c);
        }
        System.out.println();
    }
    
    private static void printStackState(Deque<Integer> stack) {
        System.out.print("  栈状态: [");
        if (stack.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> stackList = new ArrayList<>(stack);
            Collections.reverse(stackList);
            for (int i = 0; i < stackList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(stackList.get(i));
            }
        }
        System.out.println("] (底 -> 顶)");
    }
    
    private static void printInvalidSet(Set<Integer> invalidSet) {
        System.out.print("  无效索引: {");
        if (invalidSet.isEmpty()) {
            System.out.print("空");
        } else {
            List<Integer> sortedList = new ArrayList<>(invalidSet);
            Collections.sort(sortedList);
            for (int i = 0; i < sortedList.size(); i++) {
                if (i > 0) System.out.print(", ");
                System.out.print(sortedList.get(i));
            }
        }
        System.out.println("}");
    }
    
    private static boolean isValidParentheses(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') {
                count++;
            } else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
    
    public static void main(String[] args) {
        // 测试示例
        String[] testCases = {"()())", "(((", "())", "((a))", "a(b)c)d"};
        
        for (String testCase : testCases) {
            minRemoveToMakeValidWithVisualization(testCase);
            System.out.println("\n" + "=".repeat(70) + "\n");
        }
    }
}
```

### 运行结果示例
```plain
🔧 移除无效的括号
输入字符串: "()())"
索引:  0  1  2  3  4 
字符:  (  )  (  )  ) 
============================================================

📊 第一次遍历 - 使用栈匹配括号:

步骤 1: 处理字符 '(' (索引 0)
  📥 左括号入栈
  栈状态: [0] (底 -> 顶)
  无效索引: {空}

步骤 2: 处理字符 ')' (索引 1)
  ✅ 右括号匹配成功，与索引 0 的左括号配对
  栈状态: [空] (底 -> 顶)
  无效索引: {空}

步骤 3: 处理字符 '(' (索引 2)
  📥 左括号入栈
  栈状态: [2] (底 -> 顶)
  无效索引: {空}

步骤 4: 处理字符 ')' (索引 3)
  ✅ 右括号匹配成功，与索引 2 的左括号配对
  栈状态: [空] (底 -> 顶)
  无效索引: {空}

步骤 5: 处理字符 ')' (索引 4)
  ❌ 右括号无法匹配，标记为无效
  栈状态: [空] (底 -> 顶)
  无效索引: {4}

🔚 处理栈中剩余的左括号:

📋 最终无效括号索引: [4]

🔨 第二次遍历 - 构建有效字符串:
  ✅ 索引 0 字符 '(' 保留
  ✅ 索引 1 字符 ')' 保留
  ✅ 索引 2 字符 '(' 保留
  ✅ 索引 3 字符 ')' 保留
  ❌ 索引 4 字符 ')' 删除

🏆 最终结果: "()()"

🧪 验证结果:
  ✅ 结果字符串括号匹配有效
```

## 🧪 测试用例
### 基础功能测试
```java
public class MinRemoveTest {
    
    private Solution solution = new Solution();
    
    @Test
    public void testBasicCases() {
        // 示例 1
        assertEquals("()()", solution.minRemoveToMakeValid("()())"));
        
        // 示例 2
        assertEquals("", solution.minRemoveToMakeValid("((("));
        
        // 示例 3
        assertEquals("()", solution.minRemoveToMakeValid("())"));
    }
    
    @Test
    public void testEdgeCases() {
        // 空字符串
        assertEquals("", solution.minRemoveToMakeValid(""));
        
        // 只有字母
        assertEquals("abc", solution.minRemoveToMakeValid("abc"));
        
        // 只有左括号
        assertEquals("", solution.minRemoveToMakeValid("(((("));
        
        // 只有右括号
        assertEquals("", solution.minRemoveToMakeValid("))))"));
        
        // 已经有效的字符串
        assertEquals("(a)(b)", solution.minRemoveToMakeValid("(a)(b)"));
    }
    
    @Test
    public void testComplexCases() {
        // 包含字母的复杂情况
        assertEquals("a(b)c", solution.minRemoveToMakeValid("a(b)c)d"));
        assertEquals("(a(b)", solution.minRemoveToMakeValid("((a(b)"));
        assertEquals("a(b(c)d)e", solution.minRemoveToMakeValid("a(b(c)d)e"));
        
        // 交替的括号和字母
        assertEquals("a(b)c(d)", solution.minRemoveToMakeValid("a(b)c(d))"));
        assertEquals("(a)(b)", solution.minRemoveToMakeValid("((a)(b)"));
    }
    
    @Test
    public void testLargeInput() {
        // 大输入测试
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb.append("(");
        }
        for (int i = 0; i < 500; i++) {
            sb.append(")");
        }
        
        String result = solution.minRemoveToMakeValid(sb.toString());
        
        // 验证结果有效性
        assertTrue(isValidParentheses(result));
        assertEquals(1000, result.length()); // 500对有效括号
    }
    
    private boolean isValidParentheses(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') count++;
            else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
}
```

### 性能对比测试
```java
public class PerformanceComparisonTest {
    
    @Test
    public void compareAlgorithms() {
        // 生成测试数据
        String testString = generateTestString(10000);
        
        // 测试栈+哈希表解法
        long startTime = System.nanoTime();
        Solution solution1 = new Solution();
        String result1 = solution1.minRemoveToMakeValid(testString);
        long time1 = System.nanoTime() - startTime;
        
        // 测试两次遍历解法
        startTime = System.nanoTime();
        SolutionOptimized solution2 = new SolutionOptimized();
        String result2 = solution2.minRemoveToMakeValid(testString);
        long time2 = System.nanoTime() - startTime;
        
        // 测试计数法
        startTime = System.nanoTime();
        SolutionCounting solution3 = new SolutionCounting();
        String result3 = solution3.minRemoveToMakeValid(testString);
        long time3 = System.nanoTime() - startTime;
        
        // 验证结果一致性
        assertTrue(isValidParentheses(result1));
        assertTrue(isValidParentheses(result2));
        assertTrue(isValidParentheses(result3));
        
        System.out.printf("栈+哈希表解法: %.2f ms\n", time1 / 1_000_000.0);
        System.out.printf("两次遍历解法: %.2f ms\n", time2 / 1_000_000.0);
        System.out.printf("计数法: %.2f ms\n", time3 / 1_000_000.0);
    }
    
    private String generateTestString(int length) {
        Random random = new Random(42);
        StringBuilder sb = new StringBuilder();
        
        for (int i = 0; i < length; i++) {
            int choice = random.nextInt(4);
            switch (choice) {
                case 0: sb.append('('); break;
                case 1: sb.append(')'); break;
                case 2: sb.append('a'); break;
                case 3: sb.append('b'); break;
            }
        }
        
        return sb.toString();
    }
    
    private boolean isValidParentheses(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') count++;
            else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
}
```

## 🔧 相关问题扩展
### 1. LeetCode 20 - 有效的括号
```java
/**
 * 判断括号字符串是否有效
 */
public class ValidParentheses {
    
    public boolean isValid(String s) {
        Map<Character, Character> mapping = new HashMap<>();
        mapping.put(')', '(');
        mapping.put('}', '{');
        mapping.put(']', '[');
        
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : s.toCharArray()) {
            if (mapping.containsKey(c)) {
                // 右括号
                if (stack.isEmpty() || stack.pop() != mapping.get(c)) {
                    return false;
                }
            } else {
                // 左括号
                stack.push(c);
            }
        }
        
        return stack.isEmpty();
    }
}
```

### 2. LeetCode 301 - 删除无效的括号（返回所有可能结果）
```java
/**
 * 删除最少的括号使字符串有效，返回所有可能的结果
 */
public class RemoveInvalidParenthesesAll {
    
    public List<String> removeInvalidParentheses(String s) {
        List<String> result = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        Queue<String> queue = new LinkedList<>();
        
        queue.offer(s);
        visited.add(s);
        boolean found = false;
        
        while (!queue.isEmpty() && !found) {
            int size = queue.size();
            
            for (int i = 0; i < size; i++) {
                String current = queue.poll();
                
                if (isValid(current)) {
                    result.add(current);
                    found = true;
                }
                
                if (!found) {
                    // 尝试删除每个括号
                    for (int j = 0; j < current.length(); j++) {
                        char c = current.charAt(j);
                        if (c == '(' || c == ')') {
                            String next = current.substring(0, j) + 
                                         current.substring(j + 1);
                            if (!visited.contains(next)) {
                                visited.add(next);
                                queue.offer(next);
                            }
                        }
                    }
                }
            }
        }
        
        return result.isEmpty() ? Arrays.asList("") : result;
    }
    
    private boolean isValid(String s) {
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') count++;
            else if (c == ')') {
                count--;
                if (count < 0) return false;
            }
        }
        return count == 0;
    }
}
```

### 3. 括号序列的最长有效长度
```java
/**
 * LeetCode 32 - 最长有效括号
 */
public class LongestValidParentheses {
    
    public int longestValidParentheses(String s) {
        int maxLen = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(-1); // 哨兵
        
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else {
                stack.pop();
                if (stack.isEmpty()) {
                    stack.push(i);
                } else {
                    maxLen = Math.max(maxLen, i - stack.peek());
                }
            }
        }
        
        return maxLen;
    }
}
```

### 4. 平衡括号的生成
```java
/**
 * LeetCode 22 - 括号生成
 */
public class GenerateParentheses {
    
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(result, new StringBuilder(), 0, 0, n);
        return result;
    }
    
    private void backtrack(List<String> result, StringBuilder current, 
                          int open, int close, int max) {
        if (current.length() == max * 2) {
            result.add(current.toString());
            return;
        }
        
        if (open < max) {
            current.append('(');
            backtrack(result, current, open + 1, close, max);
            current.deleteCharAt(current.length() - 1);
        }
        
        if (close < open) {
            current.append(')');
            backtrack(result, current, open, close + 1, max);
            current.deleteCharAt(current.length() - 1);
        }
    }
}
```

## 💡 解题技巧总结
### 1. 栈+哈希表的核心思想
+ **栈的作用**：匹配括号对，记录未匹配的左括号位置
+ **哈希表的作用**：快速记录和查询无效括号的位置
+ **两次遍历**：第一次找问题，第二次解决问题

### 2. 括号匹配的通用模式
```java
// 标准括号匹配模板
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    if (c == '(') {
        stack.push(i);  // 记录位置而不是字符
    } else if (c == ')') {
        if (!stack.isEmpty()) {
            stack.pop();  // 匹配成功
        } else {
            // 处理无效右括号
        }
    }
}
// 处理栈中剩余的左括号
```

### 3. 优化技巧
+ **计数法**：当只需要删除而不需要知道具体位置时
+ **两次遍历**：分别处理左括号和右括号的过量问题
+ **空间优化**：使用计数器代替栈和哈希表

### 4. 扩展应用
+ **多种括号**：扩展到 `()[]{}` 的匹配
+ **嵌套深度**：计算括号的最大嵌套深度
+ **生成问题**：生成所有有效的括号组合

### 5. 复杂度分析要点
+ **时间复杂度**：通常是 O(n)，每个字符最多访问常数次
+ **空间复杂度**：取决于是否需要记录位置信息
+ **均摊分析**：栈操作的均摊复杂度

这道题展示了栈和哈希表结合使用的经典场景，是理解括号匹配问题和字符串处理的重要例题！

