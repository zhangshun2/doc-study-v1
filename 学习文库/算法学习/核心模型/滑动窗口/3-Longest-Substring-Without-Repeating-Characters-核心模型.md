---
schemaVersion: 3
type: "core-model"
leetcodeId: 3
slug: "longest-substring-without-repeating-characters"
titleCn: "无重复字符的最长子串"
titleEn: "Longest Substring Without Repeating Characters"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-substring-without-repeating-characters/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "d60376fe12d69873855959ae0cead8bc8409683c2f73d85d07dca295da635ee6"
primaryPattern: "滑动窗口"
topics: ["滑动窗口", "哈希表", "字符串"]
priority: "P0"
problemPath: "题目/滑动窗口/3-Longest-Substring-Without-Repeating-Characters.md"
deepDivePath: "建模专题/T0/3-Longest-Substring-Without-Repeating-Characters-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 3. 无重复字符的最长子串：核心模型

> **双轨阅读：** [[题目/滑动窗口/3-Longest-Substring-Without-Repeating-Characters.md|标准题解]] · [[建模专题/T0/3-Longest-Substring-Without-Repeating-Characters-直观建模.md|完整建模]]

## 一句话本质

右端加入新字符时，只可能出现一种冲突：它与窗口内同字符重复；左边界跳到该字符上次位置之后即可恢复合法。

## 直观画面与扩题

像手持可伸缩取景框：右端先纳入新画面；只有新画面与框内重复时，左端才越过那个旧位置。

在本题中，对象是 **连续子串、左右边界、每个字符最近出现的位置**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

以 right 结尾的合法窗口，左边界必须大于等于 right 位置字符上一次出现的下标再加一。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 连续子串、左右边界、每个字符最近出现的位置 | 以 right 结尾的合法窗口，左边界必须大于等于 right 位置字符上一次出现的下标再加一。 | lastIndex 记录每个字符最近出现的位置；left 表示当前合法窗口左边界，best 记录最长长度。 | 右端纳入 current=s[right]，读取它的 previous；若 previous >= left，把 left 移到 previous+1。 | 每轮处理完 right 后，[left,right] 无重复字符，且 left 不能再向左而不产生重复。 | 每轮用 right-left+1 刷新 best；循环结束后的 best 是全局最长长度。 |

## 最小演算

官方首例输入：`s = "abcabcbb"`，输出：`3`。

1. **初始状态：** lastIndex 记录每个字符最近出现的位置；left 表示当前合法窗口左边界，best 记录最长长度。
2. **触发事件：** 右端纳入 current=s[right]，读取它的 previous；若 previous >= left，把 left 移到 previous+1。
3. **结束条件：** 每轮用 right-left+1 刷新 best；循环结束后的 best 是全局最长长度。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

若 current 在窗口内重复，任何包含 previous 的窗口都不合法，所以跳到 previous+1 必要且充分；若旧位置已在窗口外，当前窗口仍然合法。

## 代码映射

```text
1. 初始化空 lastIndex、left=0、best=0。
2. 令 right 从左到右移动。
3. 读取 s[right] 的 previous。
4. 若 previous >= left，令 left=previous+1。
5. 更新 lastIndex 和 best=right-left+1。
```

## 复杂度

- 时间复杂度：O(n)，每个字符作为右端点处理一次。
- 空间复杂度：O(min(n, 字符集大小))。

## 30 秒识别信号

- 主题型：`滑动窗口`
- 切入点：题目要求“最长连续区间”且区间扩展后只有有限几种冲突，冲突又可以由左边界单向修复。

## 最小反例与易错点

- left 只能右移；处理 abba 时，不能因更早的重复位置把 left 拉回。
- 题目要求连续子串；可以跳过字符的子序列不能套这个模型。

## 分层入口

- [[题目/滑动窗口/3-Longest-Substring-Without-Repeating-Characters.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/3-Longest-Substring-Without-Repeating-Characters-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]]
