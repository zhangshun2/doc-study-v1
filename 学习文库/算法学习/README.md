# 算法学习总索引

本目录采用五层单题结构，并增加概念层与跨题对照层。每一层只承担一种职责，稳定相对链接负责往返，不靠复制正文建立关系。

| 层 | 职责 | 入口 |
| --- | --- | --- |
| 事实层 | 官方题意、示例、约束、签名、哈希 | [problems.json](problems.json) 与标准题解生成区 |
| 核心层 | 人话解释、现实类比、状态与不变量、速查卡 | [核心模型/](核心模型/) |
| 应用层 | 标准解法、Java、复杂度、易错点 | [题目/](题目/) |
| 深挖层 | 完整建模、试错、证明、可迁移模型 | [建模专题/T0/](建模专题/T0/) |
| 工具层 | Java API、复习状态、导航与验证 | [Java速查/](Java速查/)、[学习看板/](学习看板/) |
| 横向概念层 | 跨题的状态、目标、访问范围、回溯与去重模型 | [搜索与回溯概念专题](02-概念专题/README.md) |
| 跨题对照层 | 固定多题事实与代码，直接比较条件、状态、过程和结果时机 | [搜索模型跨题对照](04-跨题对照/README.md) |

## 单题阅读路径

1. 先读同题核心卡，用一句本质、直观画面和最小演算建立模型，不先背代码。
2. 打开标准题解，核对题意、权威 Java 实现、复杂度和边界。
3. 需要知道“为什么能想到”时，再从深挖专题查看完整试错、证明和迁移。

每题最多三次点击即可在核心解释、标准代码和完整推导之间切换。日常复习从
[算法学习看板](学习看板/README.md) 进入；Java 写法遗忘时从
[Java API 速查索引](Java速查/00-索引.md) 进入。

需要把“看懂”转成“能回忆和能迁移”时，从
[高效理解与回忆方法](03-资料/高效理解与回忆方法.md) 进入。它把闭卷重建、先预测后运行、反例、交错练习和间隔复习直接挂到现有五层结构上。

当同一类判断反复出现在多道题中时，从
[搜索与回溯概念专题](02-概念专题/README.md) 进入概念层；当需要把五道题的原题、代码和状态变化并排查看时，从
[搜索模型跨题对照](04-跨题对照/README.md) 进入。概念卡只沉淀可迁移思维模型；对照页可以集中显示题目事实和代码，但其 Java 会逐字对照标准题解。

## 使用方式

- 每道题只有一篇标准主文档，位于 `题目/<主题型>`；物理目录表示主要解题模型，完整标签和 P0/P1/P2 写在属性区。
- `核心模型/` 是独立速查卡，控制篇幅，负责“懂”；`建模专题/T0/` 保留长推理，负责“为什么”。
- 标准题解是提交代码、运行代码和复杂度的唯一权威副本；深挖层引用或使用伪代码，不再维护第二份实现。
- `04-跨题对照/` 是学习型快照，不反向成为事实或代码来源；其中的完整题目和 Java 由自动校验锁定到标准题解。
- 所有当前文档使用 `schemaVersion: 3`。`mastery` 与 `reviewStatus` 分开维护，因此“可迁移”仍可同时处于“待复习”。
- 旧“已完成”保守迁移为“已理解”，只有真实独立作答达到标准后才提升到“可独立实现”。

## 精确性与来源

- [problems.json](problems.json) 保存 66 道题的官方中英文标题、难度、标签、Java 方法签名、题面快照、结构化示例、整体事实哈希与分项哈希。
- 当前难度分布：Easy 13、Medium 42、Hard 11；官方结构化示例共 172 个。
- `sourceFactsSha256` 覆盖题意、示例、约束、提示、标签、签名和 Java 模板；`sourceSectionHashes` 用于定位具体变化。
- Markdown 官方章节由快照生成。人工学习提示、性能推导和补充用例必须明确标为非官方内容。
- Java 分为“LeetCode 可直接提交代码”和“本地可运行示例”；统一入口会编译两者、运行本地 `main`，并逐例断言官方结果。

## 推荐学习主线

1. 数组与哈希：遍历、记录、前缀和。
2. 双指针与滑动窗口：区间伸缩、相向移动。
3. 二分查找：有序性、答案边界、分割线。
4. 链表：反转、合并、虚拟头节点。
5. 栈与单调结构：配对、等待结算、区间贡献。
6. 二叉树、DFS 与 BFS：递归定义、层序和连通分量。
7. 回溯：选择、递归、撤销与剪枝。
8. 动态规划：状态、转移、初始化和遍历顺序。
9. 贪心：局部决策的安全性证明。
10. 排序、堆与选择：通用排序、Top K 和分治选择。

学习树、图和回溯时，可同步使用
[搜索与回溯概念专题](02-概念专题/README.md) 把单题现象提升为跨题判断，再用
[从岛屿数量到四种变化](04-跨题对照/搜索模型对照-从岛屿数量到四种变化.md) 对比五道题的状态增量。

## 单题索引（66/66）

### 数组与哈希（6）

- [1. 两数之和 / Two Sum](题目/数组与哈希/1-Two-Sum.md)
- [49. 字母异位词分组 / Group Anagrams](题目/数组与哈希/49-Group-Anagrams.md)
- [169. 多数元素 / Majority Element](题目/数组与哈希/169-Majority-Element.md)
- [238. 除自身以外数组的乘积 / Product of Array Except Self](题目/数组与哈希/238-Product-of-Array-Except-Self.md)
- [287. 寻找重复数 / Find the Duplicate Number](题目/数组与哈希/287-Find-the-Duplicate-Number.md)
- [560. 和为 K 的子数组 / Subarray Sum Equals K](题目/数组与哈希/560-Subarray-Sum-Equals-K.md)

### 哈希表（1）

- [128. 最长连续序列 / Longest Consecutive Sequence](题目/哈希表/128-Longest-Consecutive-Sequence.md)

### 双指针（3）

- [11. 盛最多水的容器 / Container With Most Water](题目/双指针/11-Container-With-Most-Water.md)
- [15. 三数之和 / 3Sum](题目/双指针/15-Three-Sum.md)
- [42. 接雨水 / Trapping Rain Water](题目/双指针/42-Trapping-Rain-Water.md)

### 滑动窗口（3）

- [3. 无重复字符的最长子串 / Longest Substring Without Repeating Characters](题目/滑动窗口/3-Longest-Substring-Without-Repeating-Characters.md)
- [76. 最小覆盖子串 / Minimum Window Substring](题目/滑动窗口/76-Minimum-Window-Substring.md)
- [209. 长度最小的子数组 / Minimum Size Subarray Sum](题目/滑动窗口/209-Minimum-Size-Subarray-Sum.md)

### 二分查找（3）

- [4. 寻找两个正序数组的中位数 / Median of Two Sorted Arrays](题目/二分查找/4-Median-of-Two-Sorted-Arrays.md)
- [33. 搜索旋转排序数组 / Search in Rotated Sorted Array](题目/二分查找/33-Search-in-Rotated-Sorted-Array.md)
- [34. 在排序数组中查找元素的第一个和最后一个位置 / Find First and Last Position of Element in Sorted Array](题目/二分查找/34-Find-First-and-Last-Position-of-Element-in-Sorted-Array.md)

### 字符串（2）

- [5. 最长回文子串 / Longest Palindromic Substring](题目/字符串/5-Longest-Palindromic-Substring.md)
- [14. 最长公共前缀 / Longest Common Prefix](题目/字符串/14-Longest-Common-Prefix.md)

### 数学（2）

- [7. 整数反转 / Reverse Integer](题目/数学/7-Reverse-Integer.md)
- [9. 回文数 / Palindrome Number](题目/数学/9-Palindrome-Number.md)

### 链表（3）

- [2. 两数相加 / Add Two Numbers](题目/链表/2-Add-Two-Numbers.md)
- [21. 合并两个有序链表 / Merge Two Sorted Lists](题目/链表/21-Merge-Two-Sorted-Lists.md)
- [206. 反转链表 / Reverse Linked List](题目/链表/206-Reverse-Linked-List.md)

### 栈（7）

- [20. 有效的括号 / Valid Parentheses](题目/栈/20-Valid-Parentheses.md)
- [32. 最长有效括号 / Longest Valid Parentheses](题目/栈/32-Longest-Valid-Parentheses.md)
- [150. 逆波兰表达式求值 / Evaluate Reverse Polish Notation](题目/栈/150-Evaluate-Reverse-Polish-Notation.md)
- [155. 最小栈 / Min Stack](题目/栈/155-Min-Stack.md)
- [224. 基本计算器 / Basic Calculator](题目/栈/224-Basic-Calculator.md)
- [394. 字符串解码 / Decode String](题目/栈/394-Decode-String.md)
- [1249. 移除无效的括号 / Minimum Remove to Make Valid Parentheses](题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md)

### 单调结构（2）

- [239. 滑动窗口最大值 / Sliding Window Maximum](题目/单调结构/239-Sliding-Window-Maximum.md)
- [739. 每日温度 / Daily Temperatures](题目/单调结构/739-Daily-Temperatures.md)

### 单调栈（1）

- [84. 柱状图中最大的矩形 / Largest Rectangle in Histogram](题目/单调栈/84-Largest-Rectangle-in-Histogram.md)

### 二叉树（7）

- [94. 二叉树的中序遍历 / Binary Tree Inorder Traversal](题目/二叉树/94-Binary-Tree-Inorder-Traversal.md)
- [98. 验证二叉搜索树 / Validate Binary Search Tree](题目/二叉树/98-Validate-Binary-Search-Tree.md)
- [101. 对称二叉树 / Symmetric Tree](题目/二叉树/101-Symmetric-Tree.md)
- [102. 二叉树的层序遍历 / Binary Tree Level Order Traversal](题目/二叉树/102-Binary-Tree-Level-Order-Traversal.md)
- [124. 二叉树中的最大路径和 / Binary Tree Maximum Path Sum](题目/二叉树/124-Binary-Tree-Maximum-Path-Sum.md)
- [226. 翻转二叉树 / Invert Binary Tree](题目/二叉树/226-Invert-Binary-Tree.md)
- [236. 二叉树的最近公共祖先 / Lowest Common Ancestor of a Binary Tree](题目/二叉树/236-Lowest-Common-Ancestor-of-a-Binary-Tree.md)

### 图与搜索（2）

- [200. 岛屿数量 / Number of Islands](题目/图与搜索/200-Number-of-Islands.md)
- [207. 课程表 / Course Schedule](题目/图与搜索/207-Course-Schedule.md)

### 图与广度优先（1）

- [127. 单词接龙 / Word Ladder](题目/图与广度优先/127-Word-Ladder.md)

### 回溯（4）

- [46. 全排列 / Permutations](题目/回溯/46-Permutations.md)
- [78. 子集 / Subsets](题目/回溯/78-Subsets.md)
- [79. 单词搜索 / Word Search](题目/回溯/79-Word-Search.md)
- [301. 删除无效的括号 / Remove Invalid Parentheses](题目/回溯/301-Remove-Invalid-Parentheses.md)

### 动态规划（7）

- [53. 最大子数组和 / Maximum Subarray](题目/动态规划/53-Maximum-Subarray.md)
- [62. 不同路径 / Unique Paths](题目/动态规划/62-Unique-Paths.md)
- [70. 爬楼梯 / Climbing Stairs](题目/动态规划/70-Climbing-Stairs.md)
- [72. 编辑距离 / Edit Distance](题目/动态规划/72-Edit-Distance.md)
- [139. 单词拆分 / Word Break](题目/动态规划/139-Word-Break.md)
- [300. 最长递增子序列 / Longest Increasing Subsequence](题目/动态规划/300-Longest-Increasing-Subsequence.md)
- [322. 零钱兑换 / Coin Change](题目/动态规划/322-Coin-Change.md)

### 贪心（2）

- [45. 跳跃游戏 II / Jump Game II](题目/贪心/45-Jump-Game-II.md)
- [55. 跳跃游戏 / Jump Game](题目/贪心/55-Jump-Game.md)

### 排序（2）

- [56. 合并区间 / Merge Intervals](题目/排序/56-Merge-Intervals.md)
- [75. 颜色分类 / Sort Colors](题目/排序/75-Sort-Colors.md)

### 堆与选择（3）

- [23. 合并 K 个升序链表 / Merge k Sorted Lists](题目/堆与选择/23-Merge-k-Sorted-Lists.md)
- [215. 数组中的第 K 个最大元素 / Kth Largest Element in an Array](题目/堆与选择/215-Kth-Largest-Element-in-an-Array.md)
- [347. 前 K 个高频元素 / Top K Frequent Elements](题目/堆与选择/347-Top-K-Frequent-Elements.md)

### 矩阵与模拟（2）

- [48. 旋转图像 / Rotate Image](题目/矩阵与模拟/48-Rotate-Image.md)
- [54. 螺旋矩阵 / Spiral Matrix](题目/矩阵与模拟/54-Spiral-Matrix.md)

### 设计（2）

- [146. LRU 缓存 / LRU Cache](题目/设计/146-LRU-Cache.md)
- [232. 用栈实现队列 / Implement Queue using Stacks](题目/设计/232-Implement-Queue-using-Stacks.md)

### 位运算（1）

- [136. 只出现一次的数字 / Single Number](题目/位运算/136-Single-Number.md)

## 专题学习记录

- [T0 算法直观建模专题：生成规范与进度（24/24）](建模专题/README.md)
- [从公式求值到过程建模：面对生活中不直观问题的思考](2026-08-30-从公式求值到过程建模的生活思考.md)
- [每日温度中的过程建模：从题意、状态到结果](2026-08-30-每日温度中的过程建模.md)
- [每日温度：从“记不住”到“宏观建模”的完整拆解](2026-08-30-每日温度单调栈与宏观建模.md)
- [算法题的直观建模方法：以 739. 每日温度为例](2026-08-30-算法题直观建模方法-以每日温度为例.md)

## 校验

跨平台主入口：

```bash
./validate-all.sh
```

它会依次执行：

- `tools/validate_library.py`：检查 UTF-8 无 BOM、schema v3、状态枚举、日期、事实哈希、分项哈希、Markdown/Wiki 链接与标题锚点、核心卡与概念卡长度和语义块、深挖语义覆盖、模板职责。
- `tools/verify_java_examples.py`：用当前 Java 环境编译提交块和本地示例，运行全部本地 `main`，再根据官方签名逐例构造参数并断言 172 个官方结果。
- 若兼容环境存在 Node，可选调用既有来源脚本补充检查。

直接运行 Python 门禁：

```bash
python3 tools/validate_library.py
python3 tools/verify_java_examples.py
```

旧 `validate-docs.ps1` 与 `compile-java-examples.ps1` 保留为兼容包装。官方数据同步与三批迁移说明见 [AGENTS.md](AGENTS.md)；同步需要访问 LeetCode 中文接口。
