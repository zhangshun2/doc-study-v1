---
schemaVersion: 3
type: "core-model"
leetcodeId: 5
slug: "longest-palindromic-substring"
titleCn: "最长回文子串"
titleEn: "Longest Palindromic Substring"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/longest-palindromic-substring/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "ed0fb1c22be6f57fa565940a9aa6deb3c5228e7bc635249aab898ec9654a6898"
primaryPattern: "字符串"
topics: ["字符串", "双指针", "动态规划", "Manacher 算法"]
priority: "P1"
problemPath: "题目/字符串/5-Longest-Palindromic-Substring.md"
deepDivePath: null
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 5. 最长回文子串：核心模型

> **双轨阅读：** [[题目/字符串/5-Longest-Palindromic-Substring.md|标准题解]]

## 一句话本质

长度为 L 的字符串有 n 个单字符中心和 n-1 个双字符中心，总计 2n-1 个。枚举所有中心，就不会漏掉任何回文子串。对中心 (left,right)，只要 s[left] == s[right] 就继续扩张。

## 直观画面与扩题

像从两端同时检查印章是否对称，先找到稳定中心，再向两侧扩张。

在本题中，对象是 **字符、中心位置或已经匹配的前缀**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

把题目翻译成一条可执行关系：长度为 L 的字符串有 n 个单字符中心和 n-1 个双字符中心，总计 2n-1 个。枚举所有中心，就不会漏掉任何回文子串。对中心 (left,right)，只要 s[left] == s[right] 就继续扩张。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 字符、中心位置或已经匹配的前缀 | 把题目翻译成一条可执行关系：长度为 L 的字符串有 n 个单字符中心和 n-1 个双字符中心，总计 2n-1 个。 | 对每个位置 center 做两次扩展： expand(center, center)：寻找奇数长度回文。 | 对每个位置 center 做两次扩展： expand(center, center)：寻找奇数长度回文。 | 任意回文串都有唯一的几何中心：奇数回文落在字符上，偶数回文落在字符间。算法枚举了这两类全部中心。 | 扩展函数返回最大合法长度，据此计算当前回文的起止下标。 |

## 最小演算

官方首例输入：`s = "babad"`，输出：`"bab"`。

1. **初始状态：** 对每个位置 center 做两次扩展： expand(center, center)：寻找奇数长度回文。
2. **触发事件：** 对每个位置 center 做两次扩展： expand(center, center)：寻找奇数长度回文。
3. **结束条件：** 扩展函数返回最大合法长度，据此计算当前回文的起止下标。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

任意回文串都有唯一的几何中心：奇数回文落在字符上，偶数回文落在字符间。算法枚举了这两类全部中心。扩展过程中，区间 [left+1,right-1] 始终是以该中心为轴的回文；相邻两字符相等时扩大后仍是回文。停止时已得到该中心的最长回文。因此所有中心中的最大者就是全局最长回文。

## 代码映射

```text
1. 对每个位置 center 做两次扩展：
2. 对每个位置 center 做两次扩展： expand(center, center)：寻找奇数长度回文。
3. 扩展函数返回最大合法长度，据此计算当前回文的起止下标。
```

## 复杂度

- 时间复杂度：最坏 O(n^2)，如字符串全为同一字符。
- 空间复杂度：O(1)，不计返回结果。

## 30 秒识别信号

- 主题型：`字符串`
- 切入点：每个回文串都围绕一个中心对称。

## 最小反例与易错点

- 不能只枚举单字符中心，否则会漏掉 "bb" 这类偶数回文。
- 循环停止时 left、right 已各多走一步，长度是 right-left-1。

## 分层入口

- [[题目/字符串/5-Longest-Palindromic-Substring.md|标准题解：题意、代码、边界]]
- Java 速查：[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]] · [[Java速查/基础工具/Math-位运算.md|Math / 位运算]]
