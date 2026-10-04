---
schemaVersion: 3
type: "core-model"
leetcodeId: 739
slug: "daily-temperatures"
titleCn: "每日温度"
titleEn: "Daily Temperatures"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/daily-temperatures/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "0dbf4b73da59bf04fc87e0ae11a059ea2eab20aacf5b17b769c1a4a3172120de"
primaryPattern: "单调结构"
topics: ["单调结构", "栈", "数组", "单调栈"]
priority: "P0"
problemPath: "题目/单调结构/739-Daily-Temperatures.md"
deepDivePath: "建模专题/T0/739-Daily-Temperatures-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 739. 每日温度：核心模型

> **双轨阅读：** [[题目/单调结构/739-Daily-Temperatures.md|标准题解]] · [[建模专题/T0/739-Daily-Temperatures-直观建模.md|完整建模]]

## 一句话本质

当扫描到今天 i，若今天温度高于栈顶日期 j 的温度，那么今天就是 j 右侧第一个更高温度：j 自入栈后，中间所有日子都没有使它出栈，说明那些温度均不够高。结算 j 后，还可能继续结算更早、更低温的日期。

## 直观画面与扩题

像候场队伍：当前元素一出现，就能淘汰那些以后再也不可能成为答案的旧候选。

在本题中，对象是 **仍可能成为答案的候选下标或值**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：当扫描到今天 i，若今天温度高于栈顶日期 j 的温度，那么今天就是 j 右侧第一个更高温度：j 自入栈后，中间所有日子都没有使它出栈，说明那些温度均不够高。结算 j 后，还可能继续结算更早、更低温的日期。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 仍可能成为答案的候选下标或值 | 把题目翻译成一条可执行关系：当扫描到今天 i，若今天温度高于栈顶日期 j 的温度，那么今天就是 j 右侧第一个更高温度：j 自入栈后，中间所有日子都没有使它出栈，说明那些温度均不够高。 | 栈非空且 temperatures[today] > temperatures[stack.peek()] 时，弹出 previous。 | 栈非空且 temperatures[today] > temperatures[stack.peek()] 时，弹出 previous。 | 每轮结束时，栈中下标严格递增，对应温度从栈底到栈顶单调不增，且这些日期尚未遇到右侧更高温度。 | 当日期 previous 被今天弹出时，今天温度更高；而 previous 与今天之间若有更高温度，previous 早已在那一天弹出。 |

## 最小演算

官方首例输入：`temperatures = [73,74,75,71,69,72,76,73]`，输出：`[1,1,4,2,1,1,0,0]`。

1. **初始状态：** 栈非空且 temperatures[today] > temperatures[stack.peek()] 时，弹出 previous。
2. **触发事件：** 栈非空且 temperatures[today] > temperatures[stack.peek()] 时，弹出 previous。
3. **结束条件：** 当日期 previous 被今天弹出时，今天温度更高；而 previous 与今天之间若有更高温度，previous 早已在那一天弹出。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

每轮结束时，栈中下标严格递增，对应温度从栈底到栈顶单调不增，且这些日期尚未遇到右侧更高温度。 当日期 previous 被今天弹出时，今天温度更高；而 previous 与今天之间若有更高温度，previous 早已在那一天弹出。因此今天恰是第一个更高日。

## 代码映射

```text
1. 栈非空且 temperatures[today] > temperatures[stack.peek()] 时，弹出 previous。
2. today 是 previous 第一个更高日，设置 answer[previous] = today - previous。
3. 重复弹栈，直到栈空或栈顶温度不低于今天。
4. 将 today 压栈，等待未来结算。
```

## 复杂度

- 时间复杂度：O(n)；每个下标压栈一次、弹栈至多一次。
- 空间复杂度：O(n)；严格下降时所有下标都留在栈中。

## 30 秒识别信号

- 主题型：`单调结构`
- 切入点：尚未找到答案的日期需要暂存，未来遇到更高温度时再结算。

## 最小反例与易错点

- 比较条件必须是严格 >；相等温度不是“更高”。
- 栈保存下标而非温度，否则无法计算天数差。

## 分层入口

- [[题目/单调结构/739-Daily-Temperatures.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/739-Daily-Temperatures-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]] · [[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
