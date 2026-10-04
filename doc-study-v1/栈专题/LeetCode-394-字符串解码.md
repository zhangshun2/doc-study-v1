# LeetCode-394-字符串解码

# LeetCode 394 - 字符串解码
## 题目描述
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
解释：先解码内层的 "2[bc]" 得到 "bcbc"，然后解码外层的 "2[abcbc]" 得到 "abcbcabcbc"
```

### 约束条件
+ `1 <= s.length <= 30`
+ `s` 由小写英文字母、数字和方括号 `'[]'` 组成
+ `s` 保证是一个有效的输入
+ `s` 中所有整数的取值范围为 `[1, 300]`

## 解题思路
这道题是**栈应用**的经典题目，涉及嵌套结构的处理。核心思想是使用栈来处理嵌套的编码结构。

### 核心思想：双栈解法
使用两个栈来分别存储：

+ **数字栈**：存储重复次数
+ **字符串栈**：存储当前层级的字符串

### 算法步骤
1. **初始化**：创建数字栈和字符串栈，当前数字和当前字符串
2. **遍历字符串**：
    - **数字字符**：累积构建当前数字
    - **左括号 **`[`：将当前数字和字符串压入栈，重置当前状态
    - **右括号 **`]`：弹出栈顶，构建重复字符串
    - **字母字符**：直接添加到当前字符串

### 图解分析
以字符串 `"2[a2[bc]]"` 为例：

```plain
字符串: 2[a2[bc]]
索引:   0123456789

详细步骤分析:

步骤1: i=0, char='2'
- 数字字符，num = 2
数字栈: []
字符串栈: []
当前数字: 2
当前字符串: ""

步骤2: i=1, char='['
- 左括号，压栈并重置
数字栈: [2]
字符串栈: [""]
当前数字: 0
当前字符串: ""

步骤3: i=2, char='a'
- 字母字符，添加到当前字符串
数字栈: [2]
字符串栈: [""]
当前数字: 0
当前字符串: "a"

步骤4: i=3, char='2'
- 数字字符，num = 2
数字栈: [2]
字符串栈: [""]
当前数字: 2
当前字符串: "a"

步骤5: i=4, char='['
- 左括号，压栈并重置
数字栈: [2, 2]
字符串栈: ["", "a"]
当前数字: 0
当前字符串: ""

步骤6: i=5, char='b'
- 字母字符，添加到当前字符串
数字栈: [2, 2]
字符串栈: ["", "a"]
当前数字: 0
当前字符串: "b"

步骤7: i=6, char='c'
- 字母字符，添加到当前字符串
数字栈: [2, 2]
字符串栈: ["", "a"]
当前数字: 0
当前字符串: "bc"

步骤8: i=7, char=']'
- 右括号，弹出栈顶进行解码
- 弹出数字: 2，弹出字符串: "a"
- 重复当前字符串: "bc" * 2 = "bcbc"
- 拼接: "a" + "bcbc" = "abcbc"
数字栈: [2]
字符串栈: [""]
当前数字: 0
当前字符串: "abcbc"

步骤9: i=8, char=']'
- 右括号，弹出栈顶进行解码
- 弹出数字: 2，弹出字符串: ""
- 重复当前字符串: "abcbc" * 2 = "abcbcabcbc"
- 拼接: "" + "abcbcabcbc" = "abcbcabcbc"
数字栈: []
字符串栈: []
当前数字: 0
当前字符串: "abcbcabcbc"

最终结果: "abcbcabcbc"
```

## 代码实现
### 方法一：双栈解法（推荐）
```java
public class Solution {
    public String decodeString(String s) {
        Deque<Integer> numStack = new ArrayDeque<>();
        Deque<String> strStack = new ArrayDeque<>();
        
        int num = 0;
        StringBuilder currentStr = new StringBuilder();
        
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) {
                // 数字字符：构建重复次数
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                // 左括号：保存当前状态，开始新的层级
                numStack.push(num);
                strStack.push(currentStr.toString());
                num = 0;
                currentStr = new StringBuilder();
            } else if (c == ']') {
                // 右括号：弹出栈顶，构建重复字符串
                int repeatTimes = numStack.pop();
                String prevStr = strStack.pop();
                
                StringBuilder temp = new StringBuilder(prevStr);
                for (int i = 0; i < repeatTimes; i++) {
                    temp.append(currentStr);
                }
                currentStr = temp;
            } else {
                // 字母字符：直接添加
                currentStr.append(c);
            }
        }
        
        return currentStr.toString();
    }
}
```

### 方法二：递归解法
```java
public class Solution {
    private int index = 0;
    
    public String decodeString(String s) {
        return decode(s);
    }
    
    private String decode(String s) {
        StringBuilder result = new StringBuilder();
        int num = 0;
        
        while (index < s.length()) {
            char c = s.charAt(index);
            
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                index++; // 跳过 '['
                String str = decode(s); // 递归解码
                for (int i = 0; i < num; i++) {
                    result.append(str);
                }
                num = 0;
            } else if (c == ']') {
                break; // 结束当前层级的递归
            } else {
                result.append(c);
            }
            index++;
        }
        
        return result.toString();
    }
}
```

### 方法三：单栈解法
```java
public class Solution {
    public String decodeString(String s) {
        Deque<String> stack = new ArrayDeque<>();
        stack.push("");
        
        int num = 0;
        
        for (char c : s.toCharArray()) {
            if (Character.isDigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                stack.push(String.valueOf(num));
                stack.push("");
                num = 0;
            } else if (c == ']') {
                String str = stack.pop();
                int repeatTimes = Integer.parseInt(stack.pop());
                String prevStr = stack.pop();
                
                StringBuilder temp = new StringBuilder(prevStr);
                for (int i = 0; i < repeatTimes; i++) {
                    temp.append(str);
                }
                stack.push(temp.toString());
            } else {
                stack.push(stack.pop() + c);
            }
        }
        
        return stack.pop();
    }
}
```

### 方法四：正则表达式解法（另类思路）
```java
public class Solution {
    public String decodeString(String s) {
        while (s.contains("[")) {
            s = s.replaceAll("(\\d+)\\[([a-z]*)\\]", 
                m -> {
                    int count = Integer.parseInt(m.group(1));
                    String str = m.group(2);
                    return str.repeat(count);
                });
        }
        return s;
    }
}
```

## 复杂度分析
### 时间复杂度
+ **双栈解法**：O(n)，其中 n 是解码后字符串的长度
+ **递归解法**：O(n)，每个字符最多被处理一次
+ **单栈解法**：O(n)，类似双栈解法
+ **正则表达式**：O(n²)，可能需要多次替换

### 空间复杂度
+ **双栈解法**：O(n)，栈的空间复杂度
+ **递归解法**：O(n)，递归调用栈的深度
+ **单栈解法**：O(n)，栈的空间复杂度
+ **正则表达式**：O(n)，字符串替换的空间

## 关键点总结
### 1. 栈的应用精髓
+ **嵌套结构处理**：栈天然适合处理嵌套的括号结构
+ **状态保存**：每层嵌套都需要保存当前的数字和字符串状态
+ **层级管理**：通过栈来管理不同层级的解码过程

### 2. 双栈设计的优势
+ **职责分离**：数字栈和字符串栈各司其职
+ **逻辑清晰**：每种类型的数据有专门的栈管理
+ **易于理解**：代码结构清晰，便于调试

### 3. 字符处理的四种情况
+ **数字**：累积构建重复次数
+ **左括号**：保存状态，开始新层级
+ **右括号**：弹出状态，构建重复字符串
+ **字母**：直接添加到当前字符串

### 4. 常见错误
+ **数字累积错误**：多位数字的正确处理
+ **栈操作顺序**：压栈和弹栈的顺序要正确
+ **字符串拼接**：注意拼接的顺序和方式
+ **边界处理**：空字符串和单字符的特殊情况

## 扩展思考
### 1. 变种问题
+ **括号匹配**：LeetCode 20（基础括号问题）
+ **基本计算器**：LeetCode 224, 227（表达式解析）
+ **移除无效的括号**：LeetCode 301

### 2. 优化方向
+ **内存优化**：减少字符串创建和拷贝
+ **性能优化**：使用 StringBuilder 而不是字符串拼接
+ **并发处理**：对于超长字符串的并行解码

### 3. 实际应用
+ **配置文件解析**：处理嵌套的配置结构
+ **模板引擎**：解析模板中的重复结构
+ **编译器**：语法分析中的嵌套结构处理

### 4. 解法选择建议
+ **面试推荐**：双栈解法，思路清晰，易于解释
+ **递归爱好者**：递归解法，体现分治思想
+ **空间优化**：单栈解法，减少栈的使用
+ **特殊场景**：正则表达式解法，适合简单情况

### 5. 设计模式体现
+ **状态模式**：不同字符对应不同的处理状态
+ **栈模式**：使用栈管理嵌套结构
+ **递归模式**：自相似问题的递归解决

### 6. 调试技巧
+ **状态跟踪**：打印每步的栈状态和当前字符串
+ **分步验证**：先处理简单的非嵌套情况
+ **边界测试**：测试空字符串、单层嵌套等边界情况

这道题完美展示了栈在处理嵌套结构问题中的强大能力，是理解栈应用的绝佳例题！



> 更新: 2025-09-19 00:54:36  
> 原文: <https://www.yuque.com/zhangshun-xxqvr/vg2bou/9573775702e996959ccf4016d62a9039>