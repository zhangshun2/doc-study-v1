---
type: migration-execution
status: completed
created: 2026-10-04
sourceCommit: 777cf6ba4cf8c5b81e46df8aeeff4b2007021fac
---

# doc-study-v1 首批融合执行记录

## 范围

首批从旧库独有题中选择 6 道，完成“官方事实同步、schema v3 标准题解、核心卡、必要建模专题、导航更新、全量门禁”的闭环。

正式库因此从 60 题扩展到 66 题。当前重叠题变为 60 道，旧库独有剩余 47 道。

## 完成清单

| 题号 | 题目 | 当前标准题解 | 核心卡 | 建模专题 | 旧来源文件数 |
| ---: | --- | --- | --- | --- | ---: |
| 32 | 最长有效括号 | `题目/栈/32-Longest-Valid-Parentheses.md` | `核心模型/栈/32-Longest-Valid-Parentheses-核心模型.md` | `建模专题/T0/32-Longest-Valid-Parentheses-直观建模.md` | 6 |
| 150 | 逆波兰表达式求值 | `题目/栈/150-Evaluate-Reverse-Polish-Notation.md` | `核心模型/栈/150-Evaluate-Reverse-Polish-Notation-核心模型.md` | 按需，不单独建页 | 1 |
| 224 | 基本计算器 | `题目/栈/224-Basic-Calculator.md` | `核心模型/栈/224-Basic-Calculator-核心模型.md` | `建模专题/T0/224-Basic-Calculator-直观建模.md` | 1 |
| 232 | 用栈实现队列 | `题目/设计/232-Implement-Queue-using-Stacks.md` | `核心模型/设计/232-Implement-Queue-using-Stacks-核心模型.md` | 按需，不单独建页 | 3 |
| 301 | 删除无效的括号 | `题目/回溯/301-Remove-Invalid-Parentheses.md` | `核心模型/回溯/301-Remove-Invalid-Parentheses-核心模型.md` | `建模专题/T0/301-Remove-Invalid-Parentheses-直观建模.md` | 2 |
| 1249 | 移除无效的括号 | `题目/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses.md` | `核心模型/栈/1249-Minimum-Remove-to-Make-Valid-Parentheses-核心模型.md` | 按需，不单独建页 | 3 |

每道题的官方事实、分项哈希和结构化示例已写入 `学习文库/算法学习/problems.json`。旧库文件名、内容类型、重复簇和迁移状态保存在 [doc-study-v1-清单.json](doc-study-v1-清单.json) 及 [旧新路径映射.csv](旧新路径映射.csv)。

## 保留规则

### 进入正式层

- 从 LeetCode 中文站重新获取题意、示例、约束、标签和 Java 方法签名。
- 按当前教学顺序重写标准题解、核心卡和必要建模专题。
- 标准题解保存唯一权威 Java，本地示例与提交实现保持分离。
- 只有需要完整推导的 3 道题新增 `建模专题/T0/`，没有为了形式统一给全部题目补长文。

### 只作来源素材

- 旧 `32` 的问题档案、题解档案和两个目录中的重复版本。
- 旧 `232` 的双栈结构资料，只用于核对延迟转移和均摊成本。
- 旧 `1249` 的栈与哈希表资料，只用于核对无效下标标记过程。
- 旧库里的重复题解、旧导航、旧批次索引、旧 Java 和临时 QA。

### 舍弃或分流

- 旧前端导航、docsify、`.trae` 和超级索引不进入正式层。
- 旧 Java 不成为第二份提交实现。
- 网络协议和 Spring Boot 内容不进入算法正式库，后续进入更宽的资料区。

## 可重复执行

首批生成脚本位于 `学习文库/算法学习/tools/migrate_doc_study_v1_batch.py`。脚本会重新获取官方事实、生成标准题解和核心卡并更新 `problems.json`；正式库仍需通过完整门禁。

盘点与映射可重复生成：

```bash
cd 整理工作区
ruby tools/build-doc-study-v1-inventory.rb
```

完整校验：

```bash
cd 学习文库/算法学习
./validate-all.sh
```

## 验证结果

2026-10-04 在正式库根目录执行 `./validate-all.sh`，结果如下：

```text
Library validation passed: 66 problems, 66 core cards, 24 modeling topics, 6 Java cards, 7 concept cards, 1 comparison topics.
Problems tested: 66/66
Submission blocks compiled: 66/66
Local examples compiled and run: 66/66
Official examples verified: 172/172
Official example failures: 0
All validation gates passed.
```

## 后续

旧库独有剩余 47 道，继续按迁移评估中的四批处理。下一步优先第 2 批“链表、树与 Trie”，但不预建空壳；只有官方事实、权威 Java、核心卡、链接和门禁全部满足后才进入正式库。

