#!/usr/bin/env python3
"""Migrate the first reviewed batch from doc-study-v1 into the v3 library.

The old repository is treated as source material, not as a second library.
This script fetches current official facts, writes schema-v3 standard
solutions and core cards, and updates problems.json.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LIBRARY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = LIBRARY_ROOT / "problems.json"
ENDPOINT = "https://leetcode.cn/graphql/"
SOURCE_CHECKED_AT = "2026-10-04"

GRAPHQL_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    translatedTitle
    translatedContent
    difficulty
    topicTags { name translatedName slug }
    codeSnippets { lang langSlug code }
    hints
    exampleTestcases
    metaData
  }
}
""".strip()


def load_migration_module() -> Any:
    path = LIBRARY_ROOT / "tools" / "migrate_library_v3.py"
    spec = importlib.util.spec_from_file_location("migrate_library_v3", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MIGRATION = load_migration_module()


def text_block(lines: list[str]) -> str:
    return "\n".join(lines).strip()


SUBMISSION_32 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int longestValidParentheses(String s) {
        int best = 0;
        Deque<Integer> unmatched = new ArrayDeque<>();
        unmatched.push(-1);

        for (int index = 0; index < s.length(); index++) {
            if (s.charAt(index) == '(') {
                unmatched.push(index);
            } else {
                unmatched.pop();
                if (unmatched.isEmpty()) {
                    unmatched.push(index);
                } else {
                    best = Math.max(best, index - unmatched.peek());
                }
            }
        }
        return best;
    }
}"""

LOCAL_32 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int longestValidParentheses(String s) {
        int best = 0;
        Deque<Integer> unmatched = new ArrayDeque<>();
        unmatched.push(-1);

        for (int index = 0; index < s.length(); index++) {
            if (s.charAt(index) == '(') {
                unmatched.push(index);
            } else {
                unmatched.pop();
                if (unmatched.isEmpty()) {
                    unmatched.push(index);
                } else {
                    best = Math.max(best, index - unmatched.peek());
                }
            }
        }
        return best;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.longestValidParentheses("(()"));
        System.out.println(solution.longestValidParentheses(")()())"));
        System.out.println(solution.longestValidParentheses(""));
        System.out.println(solution.longestValidParentheses("()(())"));
    }
}"""

SUBMISSION_150 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> values = new ArrayDeque<>();

        for (String token : tokens) {
            if (isOperator(token)) {
                int right = values.pop();
                int left = values.pop();
                values.push(apply(left, right, token));
            } else {
                values.push(Integer.parseInt(token));
            }
        }
        return values.pop();
    }

    private boolean isOperator(String token) {
        return token.length() == 1
                && "+-*/".indexOf(token.charAt(0)) >= 0;
    }

    private int apply(int left, int right, String operator) {
        if ("+".equals(operator)) {
            return left + right;
        }
        if ("-".equals(operator)) {
            return left - right;
        }
        if ("*".equals(operator)) {
            return left * right;
        }
        return left / right;
    }
}"""

LOCAL_150 = SUBMISSION_150 + r"""

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.evalRPN(
                new String[]{"2", "1", "+", "3", "*"}));
        System.out.println(solution.evalRPN(
                new String[]{"4", "13", "5", "/", "+"}));
        System.out.println(solution.evalRPN(new String[]{
                "10", "6", "9", "3", "+", "-11", "*",
                "/", "*", "17", "+", "5", "+"
        }));
        System.out.println(solution.evalRPN(
                new String[]{"3", "4", "-"}));
    }
}"""

SUBMISSION_224 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public int calculate(String s) {
        Deque<Integer> outerResult = new ArrayDeque<>();
        Deque<Integer> outerSign = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        int index = 0;

        while (index < s.length()) {
            char current = s.charAt(index);
            if (Character.isDigit(current)) {
                int number = 0;
                while (index < s.length()
                        && Character.isDigit(s.charAt(index))) {
                    number = number * 10 + (s.charAt(index) - '0');
                    index++;
                }
                result += sign * number;
                continue;
            }
            if (current == '+') {
                sign = 1;
            } else if (current == '-') {
                sign = -1;
            } else if (current == '(') {
                outerResult.push(result);
                outerSign.push(sign);
                result = 0;
                sign = 1;
            } else if (current == ')') {
                result = outerResult.pop()
                        + outerSign.pop() * result;
            }
            index++;
        }
        return result;
    }
}"""

LOCAL_224 = SUBMISSION_224 + r"""

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.calculate("1 + 1"));
        System.out.println(solution.calculate(" 2-1 + 2 "));
        System.out.println(solution.calculate(
                "(1+(4+5+2)-3)+(6+8)"));
        System.out.println(solution.calculate("-(2-3)"));
    }
}"""

SUBMISSION_232 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class MyQueue {
    private final Deque<Integer> inStack = new ArrayDeque<>();
    private final Deque<Integer> outStack = new ArrayDeque<>();

    public MyQueue() {
    }

    public void push(int x) {
        inStack.push(x);
    }

    public int pop() {
        moveIfNeeded();
        return outStack.pop();
    }

    public int peek() {
        moveIfNeeded();
        return outStack.peek();
    }

    public boolean empty() {
        return inStack.isEmpty() && outStack.isEmpty();
    }

    private void moveIfNeeded() {
        if (outStack.isEmpty()) {
            while (!inStack.isEmpty()) {
                outStack.push(inStack.pop());
            }
        }
    }
}"""

LOCAL_232 = SUBMISSION_232 + r"""

public class Main {
    public static void main(String[] args) {
        MyQueue queue = new MyQueue();
        queue.push(1);
        queue.push(2);
        System.out.println(queue.peek());
        System.out.println(queue.pop());
        System.out.println(queue.empty());
        queue.push(3);
        System.out.println(queue.pop());
        System.out.println(queue.empty());
    }
}"""

SUBMISSION_301 = r"""import java.util.ArrayDeque;
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
}"""

LOCAL_301 = SUBMISSION_301 + r"""

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.removeInvalidParentheses("()())()"));
        System.out.println(solution.removeInvalidParentheses("(a)())()"));
        System.out.println(solution.removeInvalidParentheses(")("));
        System.out.println(solution.removeInvalidParentheses("(a)b(c)"));
    }
}"""

SUBMISSION_1249 = r"""import java.util.ArrayDeque;
import java.util.Deque;

class Solution {
    public String minRemoveToMakeValid(String s) {
        Deque<Integer> openIndices = new ArrayDeque<>();
        boolean[] invalid = new boolean[s.length()];

        for (int index = 0; index < s.length(); index++) {
            char current = s.charAt(index);
            if (current == '(') {
                openIndices.push(index);
            } else if (current == ')') {
                if (openIndices.isEmpty()) {
                    invalid[index] = true;
                } else {
                    openIndices.pop();
                }
            }
        }
        while (!openIndices.isEmpty()) {
            invalid[openIndices.pop()] = true;
        }

        StringBuilder answer = new StringBuilder();
        for (int index = 0; index < s.length(); index++) {
            if (!invalid[index]) {
                answer.append(s.charAt(index));
            }
        }
        return answer.toString();
    }
}"""

LOCAL_1249 = SUBMISSION_1249 + r"""

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.minRemoveToMakeValid(
                "lee(t(c)o)de)"));
        System.out.println(solution.minRemoveToMakeValid("a)b(c)d"));
        System.out.println(solution.minRemoveToMakeValid("))(("));
        System.out.println(solution.minRemoveToMakeValid("(a(b)c)"));
    }
}"""


TARGETS: list[dict[str, Any]] = [
    {
        "id": 32,
        "slug": "longest-valid-parentheses",
        "relativePath": "题目/栈/32-Longest-Valid-Parentheses.md",
        "primaryPattern": "栈",
        "priority": "P0",
        "checklistPriorities": ["P0"],
        "checklistTags": ["Stack 栈", "Dynamic Programming 动态规划"],
        "deepDivePath": "建模专题/T0/32-Longest-Valid-Parentheses-直观建模.md",
        "mainSolution": "未匹配位置栈",
        "learningHints": [
            "直接枚举所有子串会重复检查大量前缀；栈只需要保存尚未配对的括号位置。",
            "初始压入 -1，把“当前有效段从下标 0 开始”也统一成一个可计算的基准。",
            "每遇到一个无法配对的右括号，它右侧才可能开始新的有效段。",
        ],
        "standard": {
            "core": (
                "有效括号段只会在两种边界之间出现：最近一个未匹配括号之后，"
                "以及当前扫描位置之前。若把每个未匹配右括号的下标也留在栈里，"
                "栈顶就是当前有效段左侧的第一条边界。"
            ),
            "brute": (
                "可以枚举每个起点和终点，再用一次扫描判断子串是否有效；"
                "共有 O(n^2) 个区间，每个区间最坏检查 O(n)，因此为 O(n^3)。"
                "也可以定义 dp[i] 为以 i 结尾的最长有效长度，时间 O(n)，"
                "但需要分别处理 ...() 与 ...)) 两种转移。"
            ),
            "optimalTitle": "索引栈：把未匹配位置变成区间边界",
            "optimal": (
                "栈不保存括号字符，只保存尚未结算的下标。初始放入 -1。"
                "遇到左括号时压入其下标；遇到右括号时先弹出栈顶，表示尝试完成最近匹配。"
                "若弹出后栈为空，说明这个右括号没有可配对的左括号，"
                "于是把它的下标压入，作为后续有效段的新基准。"
                "若栈不为空，则当前下标减去新的栈顶，就是以当前字符结尾的最长有效段长度。"
            ),
            "correctness": (
                "处理任意前缀后，栈中保存的是尚未匹配的左括号下标；"
                "当存在未匹配右括号时，栈底还会保留最近一个无法匹配的右括号下标。"
                "因此栈顶始终是当前有效段左边界之前的位置。"
                "成功匹配一个右括号时，区间长度恰好覆盖从该边界之后的全部成对内容；"
                "没有可匹配左括号时，新基准左侧内容不可能再与未来字符组成有效段。"
                "取遍所有结束位置的最大值即全局最长长度。"
            ),
            "time": "O(n)，每个字符只处理一次，每个下标最多入栈和出栈一次。",
            "space": "O(n)，最坏情况字符串全部是左括号。",
            "boundaries": [
                "空字符串应返回 0，初始哨兵 -1 使循环自然跳过。",
                "栈为空时不能直接计算长度，应把当前右括号下标作为新基准。",
                "长度用下标差计算，不再额外加一，因为栈顶本身位于有效区间之外。",
            ],
            "extensions": [
                "动态规划把 dp[i] 解释为以 i 结尾的最长有效后缀。",
                "双向计数扫描可以用 O(1) 额外空间求最长长度，但不能直接定位区间。",
            ],
        },
        "core": {
            "essence": (
                "把每个未匹配位置都看成一道断点；当前下标减去最近断点，"
                "就是在这里结束的最长有效括号长度。"
            ),
            "analogy": (
                "像沿绳记录无法闭合的结：新结会隔断它之前的区域，"
                "每次成功配对就量一下从最后一个断点到当前位置的长度。"
            ),
            "teaching": (
                "本题的困难不在括号配对本身，而在于答案是最长连续子串。"
                "若只记录是否配对成功，仍不知道有效段从哪里开始；"
                "若保存所有左括号，也无法直接处理多余右括号造成的断点。"
                "把下标压栈后，栈顶同时承担“最近未完成匹配”和“区间边界”两种含义。"
            ),
            "objects": "括号字符、字符下标、未匹配位置、当前有效段边界",
            "relation": (
                "每个右括号优先匹配最近一个尚未匹配的左括号；"
                "匹配失败时，当前右括号成为新的不可跨越边界。"
            ),
            "state": "单调递增的下标栈，初始包含 -1；best 保存当前最大长度",
            "event": (
                "遇到左括号压入下标；遇到右括号先弹出栈顶，"
                "栈空则压入当前下标，否则用下标差更新 best"
            ),
            "invariant": (
                "每轮结束，栈顶是当前有效段左侧最近断点，"
                "栈内其余下标是尚未匹配的左括号"
            ),
            "result": "扫描结束后 best 是所有结束位置中的最大有效长度",
            "calculationInput": 's = ")()())"',
            "calculationSteps": [
                "初始栈为 [-1]。扫描到下标 0 的右括号，弹出 -1 后栈空，压入 0。",
                "下标 1 的左括号入栈，栈变成 [0, 1]；下标 2 的右括号匹配 1，长度为 2-0=2。",
                "下标 3 的左括号入栈；下标 4 的右括号匹配 3，长度为 4-0=4。",
                "下标 5 的右括号弹掉基准 0 后栈空，它成为新基准，最终答案保持 4。",
            ],
            "why": (
                "最近打开的左括号必须最先匹配，所以只检查栈顶即可判断当前右括号是否合法。"
                "一旦右括号在栈空时失败，它左侧的任意片段都无法被未来字符补齐，"
                "因此把它当作新基准不会漏掉右侧可能出现的更长有效段。"
            ),
            "pseudocode": [
                "best=0，未匹配栈放入 -1。",
                "下标 index 从左到右扫描。",
                "若当前是 '('，把 index 压栈。",
                "否则先弹出栈顶。",
                "若弹出后栈空，把 index 作为新基准压栈。",
                "否则用 index 减栈顶更新 best。",
                "返回 best。",
            ],
            "trigger": (
                "题目要求最长连续有效括号段，而不是只判断整个字符串是否有效时，"
                "优先考虑用下标栈记录未匹配位置和段边界。"
            ),
            "traps": [
                "只保存字符不保存下标，无法计算区间长度。",
                "栈空计算长度会把断点自身算进有效段；哨兵与下标差正好避免这个错误。",
            ],
            "java": ["[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]"],
        },
    },
    {
        "id": 150,
        "slug": "evaluate-reverse-polish-notation",
        "relativePath": "题目/栈/150-Evaluate-Reverse-Polish-Notation.md",
        "primaryPattern": "栈",
        "priority": "P0",
        "checklistPriorities": ["P0"],
        "checklistTags": ["Stack 栈", "Array 数组", "Math 数学"],
        "deepDivePath": None,
        "mainSolution": "操作数栈",
        "learningHints": [
            "后缀表达式没有括号，运算顺序已经由 token 排列决定。",
            "运算符总作用于此前最近两个尚未合并的完整子表达式。",
            "减法和除法必须按弹出顺序还原左右操作数。",
        ],
        "standard": {
            "core": (
                "逆波兰表达式从左到右隐藏了括号：每读到一个运算符，"
                "它恰好合并此前最近完成的两个子表达式。栈顶天然保存这两个结果。"
            ),
            "brute": (
                "可以递归寻找表达式根节点，但需要先确定哪一段属于左子树、"
                "哪一段属于右子树；对数组做线性切分后递归也可行，"
                "却增加了边界状态和重复解释 token 的成本。"
            ),
            "optimalTitle": "一次扫描操作数栈",
            "optimal": (
                "遇到数字时解析整数并压栈。遇到运算符时弹出栈顶作为右操作数，"
                "再弹出新的栈顶作为左操作数，计算后把结果压回。"
                "扫描结束时，整个表达式已经合并成一个值，栈顶就是答案。"
            ),
            "correctness": (
                "每个数字本身代表一个完整子表达式。每次遇到运算符时，"
                "栈顶两个值恰是以该运算符为根的两个已求值子树；"
                "按照后缀顺序弹出右、左操作数并计算，"
                "就把这两棵子树合并为一棵。归纳可知扫描到任意前缀时，"
                "栈中保存的是该前缀无法再局部合并的完整子表达式；"
                "最终只剩一个值即原表达式结果。"
            ),
            "time": "O(n)，每个 token 只读取和计算一次。",
            "space": "O(n)，栈中最多保存线性数量的中间表达式值。",
            "boundaries": [
                "负数 token 例如 -11 要先用 Integer.parseInt 解析，不能按单字符判断。",
                "除法按 Java 整数规则向零截断，不能用 Math.floorDiv，后者向负无穷取整。",
                "运算符判断不能只看首字符，否则负数字符串可能被误判。",
            ],
            "extensions": [
                "中缀表达式求值通常还需要处理运算符优先级和括号现场。",
                "编译器可把中缀表达式先转换为后缀，再用同一模型求值。",
            ],
        },
        "core": {
            "essence": (
                "每个运算符都负责合并栈顶两个已经求值的子表达式；"
                "压回结果后，这段表达式对上层而言又变成一个数字。"
            ),
            "analogy": (
                "像把散落的积木两两拼成新积木：运算符到来时，"
                "只取最近两块已经拼好的结果，合成后再放回桌面。"
            ),
            "teaching": (
                "后缀表达式把人类习惯的括号和优先级改写成了顺序。"
                "因此不需要比较运算符优先级，也不需要保存操作符栈；"
                "问题只剩“最近两个完整结果在哪里”。"
                "这个访问模式正是后进先出，而真正容易错的是左右操作数顺序。"
            ),
            "objects": "token、已求值的子表达式、待合并的中间结果",
            "relation": (
                "每个运算符的左操作数是第二近的完整结果，"
                "右操作数是最新一轮计算后留在栈顶的完整结果。"
            ),
            "state": "Deque<Integer> values，保存尚未被上层运算符合并的表达式值",
            "event": (
                "数字 token 解析后入栈；运算符 token 弹出右值和左值，"
                "计算后压回一个新的表达式值"
            ),
            "invariant": (
                "扫描到任意前缀后，栈中每个值都对应一个已经完整求值、"
                "但尚未被后续运算符合并的子表达式"
            ),
            "result": "全部 token 处理完后，栈中唯一的整数就是表达式值",
            "calculationInput": 'tokens = ["4","13","5","/","+"]',
            "calculationSteps": [
                "依次压入 4、13、5，栈顶是最近的完整子表达式 5。",
                "遇到 /，弹出右操作数 5，再弹出左操作数 13，计算 13/5 得到 2 并压回。",
                "栈变成 [4, 2]；遇到 +，弹出右操作数 2 和左操作数 4。",
                "计算 4+2 得到 6；扫描结束，栈顶 6 就是答案。",
            ],
            "why": (
                "后缀表示法保证运算符出现时，它需要的两个子表达式都已经计算完毕。"
                "栈顶顺序与表达式的右、左子树顺序一致，"
                "所以连续弹出两次不会漏掉任何待处理子树，也不会提前合并外层运算。"
            ),
            "pseudocode": [
                "建立空的整数栈。",
                "从左到右读取 token。",
                "若 token 是数字，解析后压栈。",
                "否则弹出 right，再弹出 left。",
                "按 token 计算并压回结果。",
                "所有 token 处理完后返回栈顶。",
            ],
            "trigger": (
                "输入已经按无括号、无歧义的运算顺序排列，"
                "且每个操作符只依赖最近两个完整结果时，考虑操作数栈。"
            ),
            "traps": [
                "先弹出的是右侧操作数，减法和除法不能反过来。",
                "负号只属于数字 token，不属于运算符；解析顺序要覆盖多位数和负数。",
            ],
            "java": ["[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]"],
        },
    },
    {
        "id": 224,
        "slug": "basic-calculator",
        "relativePath": "题目/栈/224-Basic-Calculator.md",
        "primaryPattern": "栈",
        "priority": "P0",
        "checklistPriorities": ["P0"],
        "checklistTags": ["Stack 栈", "Recursion 递归", "Math 数学"],
        "deepDivePath": "建模专题/T0/224-Basic-Calculator-直观建模.md",
        "mainSolution": "括号现场栈",
        "learningHints": [
            "只有加减时，表达式可以从左到右累加；括号改变的是每层计算的起点。",
            "遇到左括号时保存外层已有结果和括号前符号，然后从零开始计算内层。",
            "遇到右括号时把内层结果乘以外层符号，再加回保存的外层结果。",
        ],
        "standard": {
            "core": (
                "加减表达式可以边扫描边合并；括号不是为了优先级重新排序，"
                "而是在当前位置开启一个独立的子表达式。"
            ),
            "brute": (
                "可先把表达式转换为抽象语法树或后缀表达式，再统一求值；"
                "这能处理更完整的运算符集合，但本题只有加减和括号，"
                "构建额外结构会引入不必要的优先级与转换状态。"
            ),
            "optimalTitle": "单栈保存括号外现场",
            "optimal": (
                "维护当前层 result 和下一个数字的 sign。数字解析完整后，"
                "按 sign 加入 result。遇到左括号，把外层 result 和外层 sign 压栈，"
                "再把当前层重置为 0 和正号；遇到右括号，先得到当前层结果，"
                "再弹出外层现场，用 外层结果 + 外层符号 * 当前层结果 合并。"
                "一元负号自然表现为括号或数字前的 sign=-1。"
            ),
            "correctness": (
                "在不含括号的任意连续片段中，从左到右累加配合当前 sign "
                "与普通加减意义一致。每遇到左括号，当前 result 和 sign "
                "正好完整描述括号左侧的外层现场，可以暂停并保存。"
                "括号内部独立计算结束后，它作为外层的一个带符号操作数合并返回；"
                "嵌套括号通过同样规则逐层弹出，因此最终结果唯一且正确。"
            ),
            "time": "O(n)，每个字符只读取一次，数字也只解析一次。",
            "space": "O(d)，d 为括号最大嵌套深度。",
            "boundaries": [
                "空格必须跳过，不能当作数字或运算符。",
                "多位数字要累积解析，解析结束后当前下标仍要停留在最后一个数字字符。",
                "左括号前的负号要一并保存；否则 -(1+2) 会丢掉外层取反。",
            ],
            "extensions": [
                "加入乘法除法时，需要再引入优先级栈或先转换为后缀表达式。",
                "递归下降法使用函数调用栈表达同样的括号现场。",
            ],
        },
        "core": {
            "essence": (
                "括号开启一层独立求和；左括号保存外层结果与符号，"
                "右括号把内层结果作为一个带符号操作数加回外层。"
            ),
            "analogy": (
                "像做账时遇到一个子账本：先记下母账本当前余额和处理下一步的符号，"
                "把子账本算完后，再按原符号并回母账本。"
            ),
            "teaching": (
                "本题只有加减，本来不需要普通运算符优先级栈。"
                "真正打断线性计算的是括号，因为它要求先完成一段内部表达式，"
                "再把这个整体放回外层原来的位置。"
                "所以栈保存的对象不是每个数字，而是一层尚未恢复的外层现场。"
            ),
            "objects": "字符、当前层结果、下一位数字符号、外层括号现场",
            "relation": (
                "左括号把当前 result 和 sign 变成父层现场；"
                "右括号把子层 result 乘父层 sign 后并回父层 result。"
            ),
            "state": "result 表示当前层已完成部分，sign 表示下一个数字符号；两个栈保存父层现场",
            "event": (
                "数字按 sign 累加；左括号压入现场并重置当前层；"
                "右括号弹出父层，合并当前层结果"
            ),
            "invariant": (
                "处理任意字符后，result 是当前最内层括号已经求值的部分，"
                "栈中从底到顶保存所有尚未恢复的外层结果和符号"
            ),
            "result": "扫描结束后栈必为空，result 就是完整表达式值",
            "calculationInput": 's = "(1+(4+5+2)-3)+(6+8)"',
            "calculationSteps": [
                "最外层左括号保存 result=0、sign=1；当前层从 0、+1 开始。",
                "读入 1 后当前层为 1；遇到内部左括号，再保存父层 1 与 +1。",
                "4+5+2 得到 11，遇到右括号后并回父层，当前层变为 1+11=12。",
                "继续 -3 得到 9，再遇右括号并回最外层；随后处理 +(6+8)，最终得到 23。",
            ],
            "why": (
                "括号内部的字符与外部互不影响；只要保存外层已算结果和进入括号前的符号，"
                "就可以安全地把内层当成从零开始的独立表达式。"
                "右括号到来时内层已经完整，因此一次合并即可恢复父层全部信息。"
            ),
            "pseudocode": [
                "result=0，sign=1，并准备两个现场栈。",
                "从左到右扫描字符。",
                "若读到数字，解析完整数字并按 sign 累加。",
                "若读到 '('，保存 result 与 sign，再重置当前层。",
                "若读到 ')'，弹出现场并合并当前层结果。",
                "否则更新 sign。扫描结束返回 result。",
            ],
            "trigger": (
                "表达式只有加减或括号，并且遇到括号时需要先完成内部、"
                "再作为一个值回到外层时，考虑保存括号现场。"
            ),
            "traps": [
                "右括号只合并一层，不能用全局累加替代嵌套现场。",
                "括号前的负号属于父层符号，必须先保存再进入子层。",
            ],
            "java": [
                "[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]",
                "[[Java速查/基础工具/Math-位运算.md|Math / 位运算]]",
            ],
        },
    },
    {
        "id": 232,
        "slug": "implement-queue-using-stacks",
        "relativePath": "题目/设计/232-Implement-Queue-using-Stacks.md",
        "primaryPattern": "设计",
        "priority": "P1",
        "checklistPriorities": ["P1"],
        "checklistTags": ["Stack 栈", "Design 设计题", "Queue 队列"],
        "deepDivePath": None,
        "mainSolution": "输入栈与输出栈",
        "learningHints": [
            "入队顺序与出队顺序相反；若让元素整体反转一次，最早元素就会来到栈顶。",
            "输出栈不为空时不能把输入栈的新元素搬进去，否则会插到旧元素前面。",
            "每个元素一生只从输入栈搬到输出栈一次，因此总时间仍为线性。",
        ],
        "standard": {
            "core": (
                "一个栈把元素反转一次就会变成相反顺序。"
                "输入栈保存新到达元素，输出栈保存已经反转、可直接作为队头的元素。"
            ),
            "brute": (
                "每次 push 都把新元素放到栈底可以维持队列顺序，"
                "但需要反复倒栈，单个操作最坏 O(n)。"
                "每次都找最底部元素也会重复搬运已有数据。"
            ),
            "optimalTitle": "延迟转移的双栈结构",
            "optimal": (
                "push 只把新元素压入 inStack。pop 或 peek 前检查 outStack："
                "只有 outStack 为空时，才把 inStack 的全部元素逐个弹出并压入 outStack。"
                "这次整体反转后，最早进入 inStack 的元素位于 outStack 栈顶，"
                "随后 pop、peek 都直接操作 outStack。"
            ),
            "correctness": (
                "当 outStack 非空时，其栈顶正是尚未出队元素中最早进入者；"
                "新 push 的元素在输入栈中，不可能比已转移元素更早出队。"
                "当 outStack 为空时，一次完整转移把 inStack 的入栈顺序反转，"
                "使最早元素到达栈顶，同时保持其余元素的先后关系。"
                "因此每次 pop 和 peek 都符合队列语义，empty 只需检查两个栈。"
            ),
            "time": (
                "push、empty 为 O(1)；pop、peek 单次最坏 O(n)，"
                "但每个元素最多转移一次，n 次操作总时间为 O(n)，均摊 O(1)。"
            ),
            "space": "O(n)，两个栈共同保存全部队列元素。",
            "boundaries": [
                "必须延迟转移：outStack 非空时转移会破坏旧元素的出队顺序。",
                "empty 要同时检查两个栈，不能只看某一个栈。",
                "题目保证空队列不会调用 pop 或 peek，但实现仍应尊重队列契约。",
            ],
            "extensions": [
                "可用 LinkedList 实现同一逻辑，但 ArrayDeque 更轻量。",
                "用栈模拟队列的逆问题是队列模拟栈，可用一个队列旋转完成。",
            ],
        },
        "core": {
            "essence": (
                "把元素从输入栈整体倒进输出栈会反转一次顺序，"
                "原本最早进入的元素因此来到栈顶，可以按队列头弹出。"
            ),
            "analogy": (
                "像把一摞盘子整体搬到另一张桌上：搬运会倒序，"
                "原来最底下的盘子搬到新桌后反而在最上面。"
            ),
            "teaching": (
                "本题不是寻找一个新的容器，而是组合已有操作。"
                "难点在于控制转移时机：如果每来一个新元素就搬运，"
                "新元素可能跑到尚未出队的旧元素前面。"
                "因此输出栈必须一次搬空，之后持续消费，直到再次为空。"
            ),
            "objects": "队列元素、输入栈、输出栈、当前队头",
            "relation": (
                "输入栈按到达顺序反向保存新元素；一次完整转移后，"
                "输出栈栈顶与队列头元素一一对应。"
            ),
            "state": "inStack 承接 push，outStack 提供 pop/peek，二者和为零表示空队列",
            "event": (
                "push 只进入输入栈；读取或删除前若输出栈为空，"
                "就完整倒栈一次，再操作输出栈顶"
            ),
            "invariant": (
                "两个栈拼起来时，outStack 中尚未弹出的元素总是早于 "
                "inStack 中全部元素；outStack 栈顶是队头"
            ),
            "result": "pop 返回并删除队头，peek 只读取队头，empty 报告两栈是否都空",
            "calculationInput": 'push(1), push(2), peek(), pop(), empty()',
            "calculationSteps": [
                "两次 push 后 inStack 从底到顶为 [1,2]，outStack 为空。",
                "peek 触发倒栈，1、2 依次弹出并压入 outStack，栈顶变成 1。",
                "peek 返回 1；pop 删除 1，outStack 剩余栈顶 2。",
                "此时两个栈不全为空，empty 返回 false。",
            ],
            "why": (
                "一次完整转移相当于反转一段序列，恰好把先进先出关系映射成后进先出关系。"
                "只要输出栈不空就优先服务旧元素，新 push 不会越过它们。"
                "每个元素最多搬运一次，频繁倒栈的担忧也因此消失。"
            ),
            "pseudocode": [
                "建立 inStack 与 outStack。",
                "push(x): 把 x 压入 inStack。",
                "prepare(): 若 outStack 为空，循环弹出 inStack 并压入 outStack。",
                "pop(): prepare 后弹出 outStack 栈顶。",
                "peek(): prepare 后读取 outStack 栈顶。",
                "empty(): 返回两个栈是否都为空。",
            ],
            "trigger": (
                "要求用后进先出的操作实现先进先出，"
                "并且允许把搬移成本摊到多次操作上时，考虑双栈反转。"
            ),
            "traps": [
                "outStack 非空时继续搬运会让新元素压住旧元素。",
                "pop 和 peek 都要共享同一套 prepare 逻辑，否则状态容易不一致。",
            ],
            "java": ["[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]"],
        },
    },
    {
        "id": 301,
        "slug": "remove-invalid-parentheses",
        "relativePath": "题目/回溯/301-Remove-Invalid-Parentheses.md",
        "primaryPattern": "回溯",
        "priority": "P0",
        "checklistPriorities": ["P0"],
        "checklistTags": [
            "Breadth-First Search 广度优先搜索",
            "String 字符串",
            "Backtracking 回溯",
        ],
        "deepDivePath": "建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md",
        "mainSolution": "按删除层数扩展的 BFS",
        "learningHints": [
            "所有删除一个括号后的结果构成初始字符串的邻接状态，最少量删除就是最短距离。",
            "同一层第一次发现有效字符串，说明已经找到最小删除数，其他更长的删除都不需要。",
            "不同删除顺序可能得到同一个字符串，必须在入队前去重。",
        ],
        "standard": {
            "core": (
                "把删除一个括号看成图上走一条边，最少量删除就是到任意有效字符串的最短距离。"
                "BFS 首次到达有效节点时，距离最短。"
            ),
            "brute": (
                "也可以直接枚举所有 2^b 个括号子集，其中 b 是括号数量，"
                "检查每个结果是否有效，再保留删除数最少者。"
                "这种做法会重复计算不同删除顺序得到的同一字符串，"
                "还会枚举大量已经超过当前最优删除数的状态。"
            ),
            "optimalTitle": "按层 BFS 寻找第一组合法字符串",
            "optimal": (
                "队列初始只有原字符串，记为第 0 层。每处理一层，"
                "若某个字符串已经有效，就加入答案并标记本层找到了结果；"
                "对无效字符串，尝试删除任意一个括号，得到下一层候选。"
                "visited 防止同一字符串从不同删除顺序重复入队。"
                "一旦本层出现有效结果，就停止扩展更低层，因为继续删除不可能更少。"
            ),
            "correctness": (
                "从字符串到删除一个括号后的字符串构成无向搜索图，"
                "每条边对应一次删除。BFS 按删除次数从少到多访问，"
                "因此第一次出现有效字符串的层号就是最小删除数。"
                "该层的所有有效字符串都只删除了这个最小数量，"
                "而更浅层没有有效结果，所以它们正是完整答案集合。"
            ),
            "time": (
                "最坏为 O(n * 2^n)，其中 n 为括号数量，"
                "因为每个字符串要生成 O(n) 个删除候选并做 O(n) 有效性检查。"
            ),
            "space": "O(2^n * n)，visited 和队列最坏保存指数数量的字符串。",
            "boundaries": [
                "结果顺序任意，不能依赖队列生成顺序匹配固定数组。",
                "必须在本层全部处理完后停止，不能发现第一个结果就只返回它。",
                "visited 要在入队时标记，否则同一层不同父状态会重复添加。",
            ],
            "extensions": [
                "先统计最少删除的左、右括号数量，再用回溯做同级剪枝。",
                "连续相同括号只删除一个位置可以进一步减少重复分支。",
            ],
        },
        "core": {
            "essence": (
                "每个字符串都是删除图上的节点，删除一个括号是一层边；"
                "第一次到达合法节点的那一层就是最少删除方案。"
            ),
            "analogy": (
                "像从一个词开始每次改掉一个字母，第一次走到目标词的最短路径；"
                "这里每次只删一个括号，合法字符串就是目标。"
            ),
            "teaching": (
                "题目要求所有最优答案，因此不能只保留一条搜索路径。"
                "BFS 的价值不是遍历得快，而是层号直接表示已删除数量，"
                "让我们知道何时必须停止。"
                "去重则保证不同删除顺序得到的同一字符串只被解释一次。"
            ),
            "objects": "括号字符串、删一个括号后的邻接状态、删除层数、合法判定",
            "relation": (
                "字符串 A 删除一个括号得到 B 时，A 与 B 之间存在一条搜索边；"
                "初始字符串到合法节点的最短路径长度就是最少删除数。"
            ),
            "state": "队列保存某一删除层的字符串，visited 保存所有已发现字符串",
            "event": (
                "逐层取出字符串，合法的加入答案，"
                "不合法的删除一个括号并生成未访问的下一层候选"
            ),
            "invariant": (
                "处理到第 d 层前，visited 中的合法结果若尚未出现，"
                "说明少于 d 次删除不可能得到有效字符串"
            ),
            "result": "第一次出现有效字符串的整层结果全部加入答案后立即停止",
            "calculationInput": 's = "()())()"',
            "calculationSteps": [
                "第 0 层只有 ()())()，检查后无效，继续删除一个括号。",
                "第 1 层候选包括删掉不同右括号得到的结果，但没有合法字符串。",
                "第 2 层生成 (())() 与 ()()() 等候选，检查发现它们都合法。",
                "整层合法结果加入答案；不再扩展到第 3 层，因为它们已是最少删除。",
            ],
            "why": (
                "BFS 的层号等于从原字符串到当前字符串的最少删除次数。"
                "若第 d 层首次出现合法字符串，则所有更少删除的字符串都已检查失败，"
                "而同一层每个合法结果都恰好删除了 d 个括号，所以得到全部最优解。"
            ),
            "pseudocode": [
                "queue 放入原串，visited 记录原串。",
                "while queue 非空且尚未找到合法层:",
                "    记录本层长度。",
                "    处理本层每个字符串。",
                "    若合法，加入答案并标记 found。",
                "    若本层未 found，删除一个括号生成下一层。",
                "返回答案。",
            ],
            "trigger": (
                "题目要求最少次数操作后的所有结果，"
                "且一次操作可以自然生成相邻状态时，考虑按层 BFS。"
            ),
            "traps": [
                "不能发现首个合法字符串就立刻返回，它会漏掉同层其他答案。",
                "不能等出队时才去重，否则重复状态会先占满队列。",
            ],
            "java": ["[[Java速查/集合/Map-Set.md|Map / Set]]"],
        },
    },
    {
        "id": 1249,
        "slug": "minimum-remove-to-make-valid-parentheses",
        "relativePath": "题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md",
        "primaryPattern": "栈",
        "priority": "P0",
        "checklistPriorities": ["P0"],
        "checklistTags": ["Stack 栈", "String 字符串"],
        "deepDivePath": None,
        "mainSolution": "标记无效括号",
        "learningHints": [
            "从左到右无法匹配的右括号一定无效；扫描结束后栈内剩余左括号也一定无效。",
            "先记录无效位置，再统一构建结果，不会误删可以参与后续匹配的左括号。",
            "任意一个最少删除结果都可行，因此无需枚举组合。",
        ],
        "standard": {
            "core": (
                "有效括号要求任意前缀中左括号数量不少于右括号。"
                "扫描过程中所有无法匹配的右括号，以及结束后仍留在栈里的左括号，"
                "就是必须删除的最小集合。"
            ),
            "brute": (
                "可以枚举要删除的括号子集，再检查剩余字符串是否有效，"
                "保留删除数最少的组合。其数量为 O(2^n)，"
                "还可能在已经不可能成为最优解时继续搜索。"
            ),
            "optimalTitle": "一次标记无效括号，再一次构建结果",
            "optimal": (
                "第一遍扫描只记录左括号下标。遇到右括号时，"
                "若栈非空就弹出最近的左括号，表示两者匹配；"
                "若栈为空，则当前右括号没有对应左括号，直接标记为无效。"
                "扫描结束后，栈中剩余下标都是未被匹配的左括号，也标记为无效。"
                "第二遍按原顺序拼接未标记字符。"
            ),
            "correctness": (
                "遇到右括号时，若左侧还有未匹配左括号，"
                "弹出最近者即可形成合法嵌套；若没有，则无论保留哪个字符都无法让这个右括号合法。"
                "第一遍结束后还在栈中的左括号右侧没有足够右括号，也必须删除。"
                "其余弹掉的括号都有配对关系，且嵌套顺序由栈保证，"
                "所以删除标记集合后得到的字符串有效；任何无效括号不删除都不可能形成有效结果，"
                "因此删除数量也最少。"
            ),
            "time": "O(n)，两次线性扫描。",
            "space": "O(n)，最坏保存全部左括号下标与布尔标记。",
            "boundaries": [
                "字母直接保留，不参与匹配也不加入无效集合。",
                "空字符串本身有效，构建结果自然为空。",
                "匹配右括号时只能删除一个左括号，不能一次清空栈。",
            ],
            "extensions": [
                "两次计数扫描可用 O(1) 栈空间删除多余右括号和多余额左括号。",
                "若要求字典序最小的最优结果，标记法还需要额外选择规则。",
            ],
        },
        "core": {
            "essence": (
                "扫描时匹配成功的括号都保留，无法配对的右括号和最终剩余左括号"
                "恰好构成必须删除的最小集合。"
            ),
            "analogy": (
                "像检查一串门锁：遇到关门时若有可用的最近钥匙就配掉；"
                "没有钥匙的门和结束时仍未使用的钥匙都属于坏零件。"
            ),
            "teaching": (
                "本题只要求返回任意一个最优结果，因此不需要枚举方案。"
                "关键是把“最少删除”转化为“哪些括号注定无法参与任何合法匹配”。"
                "一次栈扫描可以完整找出这两类括号，之后只需过滤。"
            ),
            "objects": "括号字符、字符下标、未匹配左括号、无效位置标记",
            "relation": (
                "右括号优先匹配最近未配对左括号；匹配失败的右括号"
                "和扫描结束时剩余左括号都必须删除。"
            ),
            "state": "栈保存尚未匹配左括号下标，boolean 数组标记无效位置",
            "event": (
                "左括号入栈；右括号能配则弹栈，否则标记；"
                "扫描结束后剩余栈元素全部标记"
            ),
            "invariant": (
                "第一遍处理任意前缀后，栈中下标都是仍未找到右括号的左侧括号，"
                "标记位置都是已经证明无法保留的字符"
            ),
            "result": "第二遍跳过所有标记位置，拼接出的字符串就是最小删除结果",
            "calculationInput": 's = "lee(t(c)o)de)"',
            "calculationSteps": [
                "依次匹配括号；最后一个多余右括号出现时栈为空，于是标记它的下标。",
                "继续之前的左括号都已经和更早右括号配对，结束时栈为空。",
                "第二遍保留字母和全部已匹配括号，跳过标记的末尾右括号。",
                "得到 lee(t(c)o)de，删除数量为 1。",
            ],
            "why": (
                "栈匹配的括号满足最近闭合和前缀平衡要求，因此保留它们不会互相冲突。"
                "无法匹配的右括号左侧没有可用左括号，剩余左括号右侧也没有可配右括号，"
                "这两类字符在任何有效结果中都不能保留，删除它们既必要又充分。"
            ),
            "pseudocode": [
                "建立左括号下标栈和 invalid 数组。",
                "从左到右扫描字符。",
                "遇到 '(' 压入下标。",
                "遇到 ')'：栈空则标记，否则弹出一个左括号。",
                "扫描结束后标记栈中剩余左括号。",
                "再次扫描，拼接所有未标记字符并返回。",
            ],
            "trigger": (
                "题目只要任意一个最少删除结果，并允许保留普通字符时，"
                "用栈标记无效括号通常比枚举更直接。"
            ),
            "traps": [
                "不能在第一次遇到多余右括号时立即从构建结果中删除后就忘记记录位置；"
                "统一标记更清晰。",
                "剩余左括号必须在扫描结束后再处理，不能在中间提前删除。",
            ],
            "java": [
                "[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]",
                "[[Java速查/集合/Map-Set.md|Map / Set]]",
            ],
        },
    },
]


def fetch_question(slug: str) -> dict[str, Any]:
    payload = json.dumps(
        {
            "operationName": "questionData",
            "variables": {"titleSlug": slug},
            "query": GRAPHQL_QUERY,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={
            "content-type": "application/json",
            "referer": f"https://leetcode.cn/problems/{slug}/",
            "user-agent": "Codex doc-study-v1 migration/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors") or not result.get("data", {}).get("question"):
        raise RuntimeError(f"{slug}: {result.get('errors') or 'question missing'}")
    return result["data"]["question"]


def plain_html_text(value: str) -> str:
    return MIGRATION.html_to_text(value).replace("\u00a0", " ").strip()


def extract_official_examples(html: str) -> list[dict[str, str | None]]:
    fragments = re.findall(r"<pre\b[^>]*>([\s\S]*?)</pre>", html, re.I)
    fragments.extend(
        re.findall(
            r"<div\b[^>]*class=[\"'][^\"']*example-block[^\"']*[\"'][^>]*>"
            r"([\s\S]*?)</div>",
            html,
            re.I,
        )
    )
    examples: list[dict[str, str | None]] = []
    for fragment in fragments:
        text = plain_html_text(fragment)
        match = re.search(
            r"(?:\*\*)?输入[：:]?(?:\*\*)?\s*([\s\S]*?)\n"
            r"(?:\*\*)?输出[：:]?(?:\*\*)?\s*([\s\S]*?)"
            r"(?:\n(?:\*\*)?解释[：:]?(?:\*\*)?\s*([\s\S]*))?$",
            text,
        )
        if not match:
            continue
        examples.append(
            {
                "input": match.group(1).strip(),
                "output": match.group(2).strip(),
                "explanation": (match.group(3) or "").strip() or None,
            }
        )
    return examples


def build_record(target: dict[str, Any], question: dict[str, Any]) -> dict[str, Any]:
    question_id = int(question["questionFrontendId"])
    if question_id != target["id"]:
        raise RuntimeError(
            f"{target['slug']}: expected id {target['id']}, got {question_id}"
        )
    signature = json.loads(question["metaData"])
    java_template = next(
        (
            snippet["code"]
            for snippet in question.get("codeSnippets") or []
            if snippet.get("langSlug") == "java"
        ),
        None,
    )
    return {
        "id": question_id,
        "slug": question["titleSlug"],
        "titleCn": question["translatedTitle"],
        "titleEn": question["title"],
        "difficulty": question["difficulty"],
        "sourceUrl": f"https://leetcode.cn/problems/{question['titleSlug']}/",
        "sourceCheckedAt": SOURCE_CHECKED_AT,
        "sourceContentSha256": MIGRATION.sha256_text(
            question.get("translatedContent") or ""
        ),
        "relativePath": target["relativePath"],
        "primaryPattern": target["primaryPattern"],
        "checklistPriorities": target["checklistPriorities"],
        "checklistTags": target["checklistTags"],
        "officialTags": question.get("topicTags") or [],
        "signature": signature,
        "javaTemplate": java_template,
        "officialHints": question.get("hints") or [],
        "exampleTestcases": question.get("exampleTestcases") or "",
        "officialExamples": extract_official_examples(
            question.get("translatedContent") or ""
        ),
        "translatedContentHtml": question.get("translatedContent") or "",
    }


def topic_names(record: dict[str, Any]) -> list[str]:
    topics = [record["primaryPattern"]]
    for tag in record.get("officialTags") or []:
        name = tag.get("translatedName") or tag.get("name")
        if name and name not in topics:
            topics.append(name)
    return topics


def render_frontmatter(
    values: dict[str, Any],
    source_sections: dict[str, str] | None = None,
) -> str:
    return MIGRATION.frontmatter(values, source_sections)


def render_list(items: list[str], ordered: bool = False) -> str:
    lines: list[str] = []
    for index, item in enumerate(items, start=1):
        prefix = f"{index}. " if ordered else "- "
        lines.append(prefix + item)
    return "\n".join(lines)


def render_official_hints(hints: list[str]) -> str:
    if not hints:
        return "- 当前官方接口未提供额外算法提示。"
    lines: list[str] = []
    for index, hint in enumerate(hints, start=1):
        lines.append(f"{index}. {hint}")
    return "\n".join(lines)


def render_problem(
    record: dict[str, Any],
    target: dict[str, Any],
    source_hash: str,
    source_sections: dict[str, str],
    split: dict[str, str],
) -> str:
    values = {
        "schemaVersion": 3,
        "type": "problem",
        "leetcodeId": record["id"],
        "slug": record["slug"],
        "titleCn": record["titleCn"],
        "titleEn": record["titleEn"],
        "difficulty": record["difficulty"],
        "sourceUrl": record["sourceUrl"],
        "sourceCheckedAt": record["sourceCheckedAt"],
        "sourceContentSha256": record["sourceContentSha256"],
        "sourceFactsSha256": source_hash,
        "sourceSectionHashes": source_sections,
        "primaryPattern": record["primaryPattern"],
        "topics": topic_names(record),
        "priority": target["priority"],
        "checklistPriorities": record["checklistPriorities"],
        "checklistTags": record["checklistTags"],
        "mastery": "已理解",
        "reviewStatus": "未安排",
        "nextReview": None,
        "lastReviewed": None,
        "errorTags": [],
        "independentAttempts": 0,
    }
    standard = target["standard"]
    core_path = f"核心模型/{record['primaryPattern']}/"
    core_name = (
        f"{record['id']}-{record['titleEn'].replace(' ', '-')}-核心模型.md"
    )
    core_relative = core_path + core_name
    deep_relative = target.get("deepDivePath")

    entry_lines = [f"> **双轨入口：** [[{core_relative}|核心模型]]"]
    if deep_relative:
        entry_lines[0] += f" · [[{deep_relative}|完整建模]]"

    tags = "、".join(
        (
            f"{tag.get('translatedName') or tag.get('name')} "
            f"({tag.get('name')})"
            if tag.get("translatedName") and tag.get("translatedName") != tag.get("name")
            else str(tag.get("translatedName") or tag.get("name"))
        )
        for tag in record.get("officialTags") or []
    )
    body = [
        f"# {record['id']}. {record['titleCn']} / {record['titleEn']}",
        "",
        text_block(entry_lines),
        "",
        "## 题目信息",
        "",
        f"- 官方难度：`{record['difficulty']}`",
        f"- 主归档题型：`{record['primaryPattern']}`",
        "- 清单优先级：" + "、".join(f"`{item}`" for item in record["checklistPriorities"]),
        "- 清单代表标签：" + "、".join(f"`{item}`" for item in record["checklistTags"]),
        f"- LeetCode 当前标签：{tags}",
        f"- 官方来源：<{record['sourceUrl']}>",
    ]
    if deep_relative:
        body.append(
            f"- 直观建模专题：[完整推导](../../{deep_relative})"
        )
    body.extend(
        [
            f"- 题面核验日期：`{record['sourceCheckedAt']}`",
            f"- 官方内容 SHA-256：`{record['sourceContentSha256']}`",
            f"- **主解法**：{target['mainSolution']}",
            "",
            "## 官方题意（LeetCode 中文题面）",
            "",
            "> 以下题意由官方中文题面快照转换为 Markdown；"
            "来源、核验日期和内容哈希见上方元信息。",
            "",
            split["description"],
            "",
            "## 官方示例",
            "",
            split["examplesMarkdown"],
            "",
            "## 官方约束",
            "",
            split["constraints"],
            "",
            "## 官方额外提示",
            "",
            "> 以下内容来自官方接口的额外提示字段；保留接口返回语言，"
            "不把学习提示冒充为官方提示。",
            "",
            render_official_hints(record.get("officialHints") or []),
            "",
            "## 学习提示（非官方）",
            "",
            render_list(target["learningHints"], ordered=True),
            "",
            "## 性能目标与约束推导",
            "",
            "> 本节根据官方输入规模和推荐解法推导，不属于官方题面原文。",
            "",
            f"- 时间复杂度目标：{standard['time']}",
            f"- 空间复杂度目标：{standard['space']}",
            "",
            "## 补充自测用例",
            "",
            "- 复测全部官方示例。",
            "- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。",
            "- 此处属于学习测试建议，不属于官方题面。",
            "",
            "## 核心观察",
            "",
            standard["core"],
            "",
            "## 朴素方案",
            "",
            standard["brute"],
            "",
            f"## 最优方案：{standard['optimalTitle']}",
            "",
            standard["optimal"],
            "",
            "### 正确性与不变量",
            "",
            standard["correctness"],
            "",
            "## 复杂度",
            "",
            f"- **时间复杂度**：{standard['time']}",
            f"- **空间复杂度**：{standard['space']}",
            "",
            "## Java 实现",
            "",
            "### LeetCode 可直接提交代码",
            "",
            "> 入口类与方法已根据 "
            f"{record['sourceCheckedAt']} 的官方 Java 模板核验。"
            "本代码不包含本地 `main`。",
            "",
            "```java",
            target["submissionJava"],
            "```",
            "",
            "### 本地可运行示例",
            "",
            "> 下面的代码包含完整数据构造和 `main`，"
            "用于本地编译、运行与观察输出。",
            "",
            "```java",
            target["localJava"],
            "```",
            "",
            "## 边界与易错点",
            "",
            render_list(standard["boundaries"]),
            "",
            "## 可扩展变式",
            "",
            render_list(standard["extensions"]),
            "",
        ]
    )
    return render_frontmatter(values, source_sections) + "\n\n" + "\n".join(body).rstrip() + "\n"


def render_core(
    record: dict[str, Any],
    target: dict[str, Any],
    source_hash: str,
) -> str:
    core = target["core"]
    values = {
        "schemaVersion": 3,
        "type": "core-model",
        "leetcodeId": record["id"],
        "slug": record["slug"],
        "titleCn": record["titleCn"],
        "titleEn": record["titleEn"],
        "difficulty": record["difficulty"],
        "sourceUrl": record["sourceUrl"],
        "sourceCheckedAt": record["sourceCheckedAt"],
        "sourceFactsSha256": source_hash,
        "primaryPattern": record["primaryPattern"],
        "topics": topic_names(record),
        "priority": target["priority"],
        "problemPath": record["relativePath"],
        "deepDivePath": target.get("deepDivePath"),
        "mastery": "已理解",
        "reviewStatus": "未安排",
        "nextReview": None,
        "lastReviewed": None,
        "errorTags": [],
        "independentAttempts": 0,
    }
    entry = (
        f"> **双轨阅读：** [[{record['relativePath']}|标准题解]]"
    )
    if target.get("deepDivePath"):
        entry += f" · [[{target['deepDivePath']}|完整建模]]"
    pseudocode = "\n".join(core["pseudocode"])
    table_cells = [
        core["objects"],
        core["relation"],
        core["state"],
        core["event"],
        core["invariant"],
        core["result"],
    ]
    table_cells = [cell.rstrip("，；：、（") for cell in table_cells]
    calculation_lines = [
        f"官方首例输入：`{core['calculationInput']}`。",
        "",
    ]
    calculation_lines.extend(
        f"{index}. {line}" for index, line in enumerate(core["calculationSteps"], 1)
    )
    java_links = " · ".join(core["java"]) if core["java"] else "本题复用标准库容器"
    body = [
        f"# {record['id']}. {record['titleCn']}：核心模型",
        "",
        entry,
        "",
        "## 一句话本质",
        "",
        core["essence"],
        "",
        "## 直观画面与扩题",
        "",
        core["analogy"],
        "",
        core["teaching"],
        "",
        "## 关系重写",
        "",
        core["relation"],
        "",
        "## 模型要素",
        "",
        "| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |",
        "| --- | --- | --- | --- | --- | --- |",
        "| " + " | ".join(table_cells) + " |",
        "",
        "## 最小演算",
        "",
        "\n".join(calculation_lines),
        "",
        "## 为什么成立",
        "",
        core["why"],
        "",
        "## 代码映射",
        "",
        "```text",
        pseudocode,
        "```",
        "",
        "## 复杂度",
        "",
        f"- 时间复杂度：{target['standard']['time']}",
        f"- 空间复杂度：{target['standard']['space']}",
        "",
        "## 30 秒识别信号",
        "",
        core["trigger"],
        "",
        "## 最小反例与易错点",
        "",
        render_list(core["traps"]),
        "",
        "## 分层入口",
        "",
        f"- [[{record['relativePath']}|标准题解：题意、代码、边界]]",
    ]
    if target.get("deepDivePath"):
        body.append(
            f"- [[{target['deepDivePath']}|完整建模：试错、证明与迁移]]"
        )
    body.extend(
        [
            f"- Java 速查：{java_links}",
            "",
        ]
    )
    return render_frontmatter(values) + "\n\n" + "\n".join(body).rstrip() + "\n"


def update_manifest(new_records: list[dict[str, Any]]) -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    by_id = {int(problem["id"]): problem for problem in manifest["problems"]}
    for record in new_records:
        by_id[int(record["id"])] = record
    manifest["problems"] = [by_id[key] for key in sorted(by_id)]
    manifest["generatedAt"] = datetime.now(timezone.utc).isoformat(
        timespec="milliseconds"
    ).replace("+00:00", "Z")
    manifest["source"]["sourceCheckedAt"] = SOURCE_CHECKED_AT
    manifest["source"]["problemCount"] = len(manifest["problems"])
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def main() -> int:
    fetched: list[tuple[dict[str, Any], dict[str, Any]]] = []
    java_blocks = {
        32: (SUBMISSION_32, LOCAL_32),
        150: (SUBMISSION_150, LOCAL_150),
        224: (SUBMISSION_224, LOCAL_224),
        232: (SUBMISSION_232, LOCAL_232),
        301: (SUBMISSION_301, LOCAL_301),
        1249: (SUBMISSION_1249, LOCAL_1249),
    }
    for target in TARGETS:
        print(f"fetching {target['id']} {target['slug']}", flush=True)
        question = fetch_question(target["slug"])
        record = build_record(target, question)
        target["submissionJava"], target["localJava"] = java_blocks[target["id"]]
        fetched.append((target, record))

    for target, record in fetched:
        if not record["officialExamples"]:
            raise RuntimeError(f"{record['id']}: official examples are empty")
        source_hash, source_sections = MIGRATION.source_hashes(record)
        record["sourceFactsSha256"] = source_hash
        record["sourceSectionHashes"] = source_sections
        split = MIGRATION.split_official_sections(record)
        problem_path = LIBRARY_ROOT / record["relativePath"]
        core_path = (
            LIBRARY_ROOT
            / "核心模型"
            / record["primaryPattern"]
            / f"{record['id']}-{record['titleEn'].replace(' ', '-')}-核心模型.md"
        )
        problem_path.parent.mkdir(parents=True, exist_ok=True)
        core_path.parent.mkdir(parents=True, exist_ok=True)
        with problem_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(
                render_problem(
                    record, target, source_hash, source_sections, split
                )
            )
        with core_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(render_core(record, target, source_hash))
        print(
            f"wrote {record['relativePath']} and "
            f"{core_path.relative_to(LIBRARY_ROOT)}",
            flush=True,
        )

    update_manifest([record for _, record in fetched])
    print(f"manifest now contains {len(json.loads(MANIFEST_PATH.read_text())['problems'])} problems")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except urllib.error.URLError as error:
        print(f"network error: {error}", file=sys.stderr)
        sys.exit(1)
