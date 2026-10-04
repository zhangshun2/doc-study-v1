---
schemaVersion: 3
type: "problem"
leetcodeId: 301
slug: "remove-invalid-parentheses"
titleCn: "删除无效的括号"
titleEn: "Remove Invalid Parentheses"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/remove-invalid-parentheses/"
sourceCheckedAt: "2026-10-04"
sourceContentSha256: "b3983b7afb06595a98636fd5eec13afdbcf377baedd70fbd7537478ee94b0cb2"
sourceFactsSha256: "e0f38664dac0301af3ef63935562e088a2bbe22ab1020c49e053fd40bd3e9679"
sourceSectionHashes:
  description: "83bb93e1d47c46e20e535cdcfe68756619cd1a0ce0f8b4abee766fe478fc1842"
  examples: "56f316a7829de22f9a5d8a884ca66b0dd7162b70b66536d7dc18072c1ba6262c"
  constraints: "2243431bdab2549ca2cea5fb5dc22083a7ef9109385fffb9c73730e72ae99016"
  hints: "9e5ec2c6716dbd836a6fe095c045165413c8053092dcf6315ec53df57e310fdc"
  tags: "614fd6894ea86dfbc53d763bd18be7806af8448950ccdad7d81be84fbd41aff3"
  signature: "5305e43d9e3e01edecb9cbd8e51f19f4bf5e481e8109eb6401e50d04004f8805"
  javaTemplate: "595424a53123dde641eaf383c58669b331ef4c9d2195ec6ff448e2386277c16b"
primaryPattern: "回溯"
topics: ["回溯","广度优先搜索","字符串"]
priority: "P0"
checklistPriorities: ["P0"]
checklistTags: ["Breadth-First Search 广度优先搜索","String 字符串","Backtracking 回溯"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---

# 301. 删除无效的括号 / Remove Invalid Parentheses

> **双轨入口：** [[核心模型/回溯/301-Remove-Invalid-Parentheses-核心模型.md|核心模型]] · [[建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md|完整建模]]

## 题目信息

- 官方难度：`Hard`
- 主归档题型：`回溯`
- 清单优先级：`P0`
- 清单代表标签：`Breadth-First Search 广度优先搜索`、`String 字符串`、`Backtracking 回溯`
- LeetCode 当前标签：广度优先搜索 (Breadth-First Search)、字符串 (String)、回溯 (Backtracking)
- 官方来源：<https://leetcode.cn/problems/remove-invalid-parentheses/>
- 直观建模专题：[完整推导](../../建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md)
- 题面核验日期：`2026-10-04`
- 官方内容 SHA-256：`b3983b7afb06595a98636fd5eec13afdbcf377baedd70fbd7537478ee94b0cb2`
- **主解法**：按删除层数扩展的 BFS

## 官方题意（LeetCode 中文题面）

> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

给你一个由若干括号和字母组成的字符串 `s` ，删除最小数量的无效括号，使得输入的字符串有效。

返回所有可能的结果。答案可以按 **任意顺序** 返回。

## 官方示例

**示例 1：**

```text
输入：s = "()())()"
输出：["(())()","()()()"]
```

**示例 2：**

```text
输入：s = "(a)())()"
输出：["(a())()","(a)()()"]
```

**示例 3：**

```text
输入：s = ")("
输出：[""]
```

## 官方约束

- `1 <= s.length <= 25`

- `s` 由小写英文字母以及括号 `'('` 和 `')'` 组成

- `s` 中至多含 `20` 个括号

## 官方额外提示

> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. Since we do not know which brackets can be removed, we try all the options! We can use recursion.
2. In the recursion, for each bracket, we can either use it or remove it.
3. Recursion will generate all the valid parentheses strings but we want the ones with the least number of parentheses deleted.
4. We can count the number of invalid brackets to be deleted and only generate the valid strings in the recusrion.

## 学习提示（非官方）

1. 所有删除一个括号后的结果构成初始字符串的邻接状态，最少量删除就是最短距离。
2. 同一层第一次发现有效字符串，说明已经找到最小删除数，其他更长的删除都不需要。
3. 不同删除顺序可能得到同一个字符串，必须在入队前去重。

## 性能目标与约束推导

> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。

- 时间复杂度目标：最坏为 O(n * 2^n)，其中 n 为括号数量，因为每个字符串要生成 O(n) 个删除候选并做 O(n) 有效性检查。
- 空间复杂度目标：O(2^n * n)，visited 和队列最坏保存指数数量的字符串。

## 补充自测用例

- 复测全部官方示例。
- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。
- 此处属于学习测试建议，不属于官方题面。

## 核心观察

把删除一个括号看成图上走一条边，最少量删除就是到任意有效字符串的最短距离。BFS 首次到达有效节点时，距离最短。

## 朴素方案

也可以直接枚举所有 2^b 个括号子集，其中 b 是括号数量，检查每个结果是否有效，再保留删除数最少者。这种做法会重复计算不同删除顺序得到的同一字符串，还会枚举大量已经超过当前最优删除数的状态。

## 最优方案：按层 BFS 寻找第一组合法字符串

队列初始只有原字符串，记为第 0 层。每处理一层，若某个字符串已经有效，就加入答案并标记本层找到了结果；对无效字符串，尝试删除任意一个括号，得到下一层候选。visited 防止同一字符串从不同删除顺序重复入队。一旦本层出现有效结果，就停止扩展更低层，因为继续删除不可能更少。

### 正确性与不变量

从字符串到删除一个括号后的字符串构成无向搜索图，每条边对应一次删除。BFS 按删除次数从少到多访问，因此第一次出现有效字符串的层号就是最小删除数。该层的所有有效字符串都只删除了这个最小数量，而更浅层没有有效结果，所以它们正是完整答案集合。

## 复杂度

- **时间复杂度**：最坏为 O(n * 2^n)，其中 n 为括号数量，因为每个字符串要生成 O(n) 个删除候选并做 O(n) 有效性检查。
- **空间复杂度**：O(2^n * n)，visited 和队列最坏保存指数数量的字符串。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-10-04 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

class Solution {
    public List<String> removeInvalidParentheses(String s) {
        List<String> answer = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        Queue<String> frontier = new ArrayDeque<>();
        frontier.offer(s);
        visited.add(s);
        boolean foundValidLayer = false;

        while (!frontier.isEmpty() && !foundValidLayer) {
            int layerSize = frontier.size();
            for (int count = 0; count < layerSize; count++) {
                String current = frontier.poll();
                if (isValid(current)) {
                    answer.add(current);
                    foundValidLayer = true;
                    continue;
                }
                for (int index = 0; index < current.length(); index++) {
                    char bracket = current.charAt(index);
                    if (bracket != '(' && bracket != ')') {
                        continue;
                    }
                    String next = current.substring(0, index)
                            + current.substring(index + 1);
                    if (visited.add(next)) {
                        frontier.offer(next);
                    }
                }
            }
        }
        return answer;
    }

    private boolean isValid(String candidate) {
        int balance = 0;
        for (int index = 0; index < candidate.length(); index++) {
            char current = candidate.charAt(index);
            if (current == '(') {
                balance++;
            } else if (current == ')') {
                balance--;
                if (balance < 0) {
                    return false;
                }
            }
        }
        return balance == 0;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Queue;
import java.util.Set;

class Solution {
    public List<String> removeInvalidParentheses(String s) {
        List<String> answer = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        Queue<String> frontier = new ArrayDeque<>();
        frontier.offer(s);
        visited.add(s);
        boolean foundValidLayer = false;

        while (!frontier.isEmpty() && !foundValidLayer) {
            int layerSize = frontier.size();
            for (int count = 0; count < layerSize; count++) {
                String current = frontier.poll();
                if (isValid(current)) {
                    answer.add(current);
                    foundValidLayer = true;
                    continue;
                }
                for (int index = 0; index < current.length(); index++) {
                    char bracket = current.charAt(index);
                    if (bracket != '(' && bracket != ')') {
                        continue;
                    }
                    String next = current.substring(0, index)
                            + current.substring(index + 1);
                    if (visited.add(next)) {
                        frontier.offer(next);
                    }
                }
            }
        }
        return answer;
    }

    private boolean isValid(String candidate) {
        int balance = 0;
        for (int index = 0; index < candidate.length(); index++) {
            char current = candidate.charAt(index);
            if (current == '(') {
                balance++;
            } else if (current == ')') {
                balance--;
                if (balance < 0) {
                    return false;
                }
            }
        }
        return balance == 0;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.removeInvalidParentheses("()())()"));
        System.out.println(solution.removeInvalidParentheses("(a)())()"));
        System.out.println(solution.removeInvalidParentheses(")("));
        System.out.println(solution.removeInvalidParentheses("(a)b(c)"));
    }
}
```

## 边界与易错点

- 结果顺序任意，不能依赖队列生成顺序匹配固定数组。
- 必须在本层全部处理完后停止，不能发现第一个结果就只返回它。
- visited 要在入队时标记，否则同一层不同父状态会重复添加。

## 可扩展变式

- 先统计最少删除的左、右括号数量，再用回溯做同级剪枝。
- 连续相同括号只删除一个位置可以进一步减少重复分支。
