---
schemaVersion: 3
type: "core-model"
leetcodeId: 76
slug: "minimum-window-substring"
titleCn: "最小覆盖子串"
titleEn: "Minimum Window Substring"
difficulty: "Hard"
sourceUrl: "https://leetcode.cn/problems/minimum-window-substring/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "d6923b53db5be884732c19a7c0c7621a8bad8cd6c59ba7186a29362b7ad51927"
primaryPattern: "滑动窗口"
topics: ["滑动窗口", "哈希表", "字符串"]
priority: "P0"
problemPath: "题目/滑动窗口/76-Minimum-Window-Substring.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 76. 最小覆盖子串：核心模型

> **双轨阅读：** [[题目/滑动窗口/76-Minimum-Window-Substring.md|标准题解]]

## 一句话本质

用 need[c] 表示当前窗口还欠字符 c 几个。初始根据 t 计数，并令 missing = t.length()。 右端加入字符 c 时： 若 need[c] > 0，这个字符偿还了一笔欠账，missing--。

## 直观画面与扩题

像手持一个可伸缩的取景框，右边纳入新画面，左边只在规则被破坏时收缩。

在本题中，对象是 **连续区间及其左右边界**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：用 need[c] 表示当前窗口还欠字符 c 几个。初始根据 t 计数，并令 missing = t.length()。 右端加入字符 c 时： 若 need[c] > 0，这个字符偿还了一笔欠账，missing--。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 连续区间及其左右边界 | 把题目翻译成一条可执行关系：用 need[c] 表示当前窗口还欠字符 c 几个。初始根据 t 计数，并令 missing = t.length()。 | 一旦 missing == 0，当前窗口覆盖了 t，记录其长度。在合法期间不断右移左指针，寻找同一右端点下最短的合法窗口。 | 右指针逐字符扩张，并更新欠账。 | 任意时刻 need[c] 等于 t 对字符 c 的需求量减去当前窗口中的数量，missing 等于所有正欠账之和。 | 任意时刻 need[c] 等于 t 对字符 c 的需求量减去当前窗口中的数量，missing 等于所有正欠账之和。 |

## 最小演算

官方首例输入：`s = "ADOBECODEBANC", t = "ABC"`，输出：`"BANC"`。

1. **初始状态：** 一旦 missing == 0，当前窗口覆盖了 t，记录其长度。
2. **触发事件：** 右指针逐字符扩张，并更新欠账。
3. **结束条件：** 任意时刻 need[c] 等于 t 对字符 c 的需求量减去当前窗口中的数量，missing 等于所有正欠账之和。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

任意时刻 need[c] 等于 t 对字符 c 的需求量减去当前窗口中的数量，missing 等于所有正欠账之和。故 missing == 0 当且仅当窗口覆盖 t。固定右端点时，内层循环不断收缩左端，检查了以该右端点结尾的所有可能最优合法窗口；第一次变非法后，更右的左端也不可能合法。遍历所有右端点并取最短，得到全局最小覆盖。

## 代码映射

```text
1. 右指针逐字符扩张，并更新欠账。
2. 一旦 missing == 0，当前窗口覆盖了 t，记录其长度。
3. 在合法期间不断右移左指针，寻找同一右端点下最短的合法窗口。
4. 移出必需字符后窗口非法，回到扩张阶段。
```

## 复杂度

- 时间复杂度：O(|s| + |t|)，两个指针各最多走过 s 一次。
- 空间复杂度：O(1)，题目限定英文字母，使用固定大小数组；推广到任意字符集时为 O(字符种类数)。

## 30 秒识别信号

- 主题型：`滑动窗口`
- 切入点：右指针负责把字符纳入窗口，直到窗口合法。

## 最小反例与易错点

- 重复字符必须按数量覆盖，不能只用 Set。
- need[c] < 0 表示冗余，不代表错误。

## 分层入口

- [[题目/滑动窗口/76-Minimum-Window-Substring.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
