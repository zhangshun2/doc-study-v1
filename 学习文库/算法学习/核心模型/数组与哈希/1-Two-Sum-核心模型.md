---
schemaVersion: 3
type: "core-model"
leetcodeId: 1
slug: "two-sum"
titleCn: "两数之和"
titleEn: "Two Sum"
difficulty: "Easy"
sourceUrl: "https://leetcode.cn/problems/two-sum/"
sourceCheckedAt: "2026-08-30"
sourceFactsSha256: "ce3444f65ce7ee4a8b6d6c1639effa34f65e8c96eccb217dbcd6ad3eb8f9a175"
primaryPattern: "数组与哈希"
topics: ["数组与哈希", "数组", "哈希表"]
priority: "P0"
problemPath: "题目/数组与哈希/1-Two-Sum.md"
deepDivePath: "建模专题/T0/1-Two-Sum-直观建模.md"
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 1. 两数之和：核心模型

> **双轨阅读：** [[题目/数组与哈希/1-Two-Sum.md|标准题解]] · [[建模专题/T0/1-Two-Sum-直观建模.md|完整建模]]

## 一句话本质

每个位置不用再向未来寻找搭档，只问：“我需要的补数以前来过吗？”

## 直观画面与扩题

像边收卡片边做目录：拿到当前卡片，只查目录里有没有能与它凑成目标值的旧卡片；查完再把当前卡片登记进去。

在本题中，对象是 **已扫描元素的值、值与下标的对应、当前下标**；把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。

## 关系重写

若答案包含当前下标 i，另一个下标 j 必须满足 j < i 且 nums[j] = target - nums[i]。

## 模型要素

| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |
| --- | --- | --- | --- | --- | --- |
| 已扫描元素的值、值与下标的对应、当前下标 | 若答案包含当前下标 i，另一个下标 j 必须满足 j < i 且 nums[j] = target - nums[i]。 | Map<Integer, Integer> indexByValue，保存已扫描值到其下标。 | 扫描到 nums[i]，先计算并查询 target - nums[i]，查询失败后才登记 nums[i]。 | 处理下标 i 之前，表里恰好包含区间 [0, i) 出现过的值和位置。 | 查到补数时立即返回两个下标；扫描结束仍无结果才说明无解。 |

## 最小演算

官方首例输入：`nums = [2,7,11,15], target = 9`，输出：`[0,1]`。

1. **初始状态：** Map<Integer, Integer> indexByValue，保存已扫描值到其下标。
2. **触发事件：** 扫描到 nums[i]，先计算并查询 target - nums[i]，查询失败后才登记 nums[i]。
3. **结束条件：** 查到补数时立即返回两个下标；扫描结束仍无结果才说明无解。
4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。

## 为什么成立

若合法答案是 (j,i)，处理 i 时 j 必已登记；反过来，查到补数就同时保证两数之和为目标值且下标不同。

## 代码映射

```text
1. 建立“值 -> 下标”的空表。
2. 从左到右扫描 nums[i]。
3. 查询 target - nums[i] 是否已在表中。
4. 若在表中，返回补数下标与 i。
5. 若不在表中，登记 nums[i] -> i。
```

## 复杂度

- 时间复杂度：平均 O(n)；哈希查询和写入平均为 O(1)。
- 空间复杂度：O(n)。

## 30 秒识别信号

- 主题型：`数组与哈希`
- 切入点：输入无序、要找两个对象或两个数配对，并需要返回位置时，考虑“查询已经出现过的补数”。

## 最小反例与易错点

- 不能先登记当前元素再查询，否则 [3,3], target=6 可能把同一个下标使用两次。
- 集合只能回答“值是否出现”；本题还要返回位置，因此必须保存值到下标。

## 分层入口

- [[题目/数组与哈希/1-Two-Sum.md|标准题解：题意、代码、边界]]
- [[建模专题/T0/1-Two-Sum-直观建模.md|完整建模：试错、证明与迁移]]
- Java 速查：[[Java速查/集合/Map-Set.md|Map / Set]]
