# doc-study-V1

## Table of Contents (TOC)
- [Description](#description)
- [Document Naming Convention](#document-naming-convention)
- [Directory Overview (partial)](#directory-overview-partial)
- [Quick Navigation](#quick-navigation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

## Description
This repository collects daily study notes on algorithms and CS fundamentals, with a focus on topics like Monotonic Stack, Stack & Hash, and Search & Backtracking. All problems follow a “separate Problem and Solution docs” convention to enable fast navigation and systematic review.

## Document Naming Convention
- Problem doc: 问题X.Y.Z (e.g., 问题1.0.0-最长有效括号.md)
- Solution doc: 题解X.Y.Z (e.g., 题解2.0.0-最长有效括号.md)
- For “Search & Backtracking” discussions, all markdown outputs go under the “搜索和回溯” folder; specific categories can use subfolders (e.g., 递归回溯/全排列, 组合总和).

## Directory Overview (partial)
- [单调栈/](单调栈/)
  - [基础模板/](单调栈/基础模板/) (Monotonic Stack basic template)
  - [原理与选择/](单调栈/原理与选择/) (Principles and selection)
  - [记忆与思考/](单调栈/记忆与思考/) (Memory and thinking notes)
  - [哨兵元素/](单调栈/哨兵元素/) (Sentinel mechanism and examples)
  - [下一个更大元素/](单调栈/下一个更大元素/) (LeetCode496, etc.)
  - [接雨水/](单调栈/接雨水/), [最大矩形/](单调栈/最大矩形/), [最长有效括号/](单调栈/最长有效括号/), [双栈结构/](单调栈/双栈结构/), [字符串解码/](单调栈/字符串解码/)
- [搜索和回溯/](搜索和回溯/)
  - [递归回溯/](搜索和回溯/递归回溯/) (Permutation, Subsets, Generate Parentheses, Letter Combinations, Combination Sum)
  - [`搜索与回溯-知识点梳理与题目分类.md`](搜索和回溯/搜索与回溯-知识点梳理与题目分类.md)
- [栈和哈希表/](栈和哈希表/) (Daily Temperatures, Remove Invalid Parentheses, structural notes)
- [学习方法/](学习方法/) (Fast reading & mental modeling guide, stack learning summary)
- [算法优化思想/](算法优化思想/) (Rolling array & incremental update)
- [题解总览/](题解总览/) (题解2.0.0.md)
- [QA/](QA/)
- [框架/springBoot/bean的生命周期/](框架/springBoot/bean的生命周期/)
- [题/](题/) (LeetCode 热题专题分组)


## Quick Navigation
- Monotonic Stack
  - Basic template: [`单调栈/基础模板/单调栈基本模板.md`](单调栈/基础模板/单调栈基本模板.md)
  - Principles & selection: [`单调栈/原理与选择/单调栈结构原理详解.md`](单调栈/原理与选择/单调栈结构原理详解.md), [`单调栈/原理与选择/单调栈选择原则.md`](单调栈/原理与选择/单调栈选择原则.md)
  - Sentinel element: [`单调栈/哨兵元素/单调栈哨兵元素深度解析.md`](单调栈/哨兵元素/单调栈哨兵元素深度解析.md), [`单调栈/哨兵元素/单调栈哨兵元素示例.md`](单调栈/哨兵元素/单调栈哨兵元素示例.md)
  - Memory & thinking: [`单调栈/记忆与思考/单调栈记忆与理解2.0.0.md`](单调栈/记忆与思考/单调栈记忆与理解2.0.0.md), [`单调栈/记忆与思考/单调栈思考1.0.0.md`](单调栈/记忆与思考/单调栈思考1.0.0.md)
  - Problems:
    - Next Greater Element I: [`单调栈/下一个更大元素/LeetCode496-下一个更大元素I.md`](单调栈/下一个更大元素/LeetCode496-下一个更大元素I.md)
    - Trapping Rain Water: [`单调栈/接雨水/题解2.0.0-接雨水详解.md`](单调栈/接雨水/题解2.0.0-接雨水详解.md)
    - Largest Rectangle in Histogram: [`单调栈/最大矩形/题解2.0.0-最大矩形.md`](单调栈/最大矩形/题解2.0.0-最大矩形.md)
    - Longest Valid Parentheses: [`单调栈/最长有效括号/题解2.0.0-最长有效括号.md`](单调栈/最长有效括号/题解2.0.0-最长有效括号.md)
    - Implement Queue using Stacks: [`单调栈/双栈结构/题解2.0.0-用栈实现队列.md`](单调栈/双栈结构/题解2.0.0-用栈实现队列.md)
    - Decode String: [`单调栈/字符串解码/题解2.0.0-字符串解码.md`](单调栈/字符串解码/题解2.0.0-字符串解码.md)
- Search & Backtracking:
  - Overview: [`搜索和回溯/搜索与回溯-知识点梳理与题目分类.md`](搜索和回溯/搜索与回溯-知识点梳理与题目分类.md)
  - Recursion & Backtracking: [`搜索和回溯/递归回溯/`](搜索和回溯/递归回溯/) (Permutation, Subsets, Generate Parentheses, Letter Combinations, Combination Sum)
- Stack & Hash:
  - Daily Temperatures: [`栈和哈希表/LeetCode739-每日温度.md`](栈和哈希表/LeetCode739-每日温度.md), [`栈和哈希表/题解2.0.0-每日温度.md`](栈和哈希表/题解2.0.0-每日温度.md)
  - Remove Invalid Parentheses: [`栈和哈希表/LeetCode1249-移除无效的括号.md`](栈和哈希表/LeetCode1249-移除无效的括号.md), [`栈和哈希表/题解2.0.0-移除无效的括号.md`](栈和哈希表/题解2.0.0-移除无效的括号.md)
- Study Methods: [`学习方法/快速阅读与脑内建模训练指南.md`](学习方法/快速阅读与脑内建模训练指南.md), [`学习方法/栈学习总结.md`](学习方法/栈学习总结.md)
- Algorithm Optimization Ideas: [`算法优化思想/算法优化思想-滚动数组与增量更新.md`](算法优化思想/算法优化思想-滚动数组与增量更新.md)
- Solutions Overview: [`题解总览/题解2.0.0.md`](题解总览/题解2.0.0.md)
- QA: [`QA/QA_0923.md`](QA/QA_0923.md)
- Framework: [`框架/springBoot/bean的生命周期/`](框架/springBoot/bean的生命周期/)
- Topics: [`题/4. LeetCode热题100专题分组.md`](题/4.%20LeetCode热题100专题分组.md)

## Usage
- Suggested reading order: start at “单调栈/基础模板”, then “原理与选择”, “哨兵元素”, “记忆与思考”, and finally enter specific topics like 接雨水, 最大矩形, 下一个更大元素.
- Each problem contains both “问题” and “题解” docs, mostly with Java implementations and comparisons of multiple approaches.

## Contribution
- Branch naming: feat/xxx (feature), docs/xxx (docs), fix/xxx (fix)
- Commit messages: follow type prefixes (feat/docs/fix/chore), e.g., docs: 整理单调栈目录结构
- Sync with remote: prefer `git pull --rebase origin master`; if unrelated history occurs initially, use `--allow-unrelated-histories` (already handled for this repo)

## License
Primarily for personal study and archiving. If you quote or extend, please keep proper references and comply with the original docs’ citation rules.
