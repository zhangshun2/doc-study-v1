#!/usr/bin/env python3
"""Generate concise core-model cards from the reviewed standard solutions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


LIBRARY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = LIBRARY_ROOT / "problems.json"
PROBLEMS_ROOT = LIBRARY_ROOT / "题目"
MODELING_ROOT = LIBRARY_ROOT / "建模专题" / "T0"
CORE_ROOT = LIBRARY_ROOT / "核心模型"

PATTERN_ANALOGY = {
    "数组与哈希": "像边收卡片边登记索引：每来一张，就先查旧记录里有没有能配对的卡片。",
    "哈希表": "像先给材料建立目录，之后不再逐个翻箱，而是按键直接找到同类对象。",
    "双指针": "像两个人从两端向中间收网，每走一步都能排除一批不可能答案。",
    "滑动窗口": "像手持一个可伸缩的取景框，右边纳入新画面，左边只在规则被破坏时收缩。",
    "二分查找": "像查字典时每翻一次就丢掉确定不可能的一半，关键是保留包含答案的边界。",
    "字符串": "像从两端同时检查印章是否对称，先找到稳定中心，再向两侧扩张。",
    "数学": "像逐位拆开十进制计数器，每次只处理当前最低位，同时守住溢出边界。",
    "链表": "像整理一列只能看见下一节的车厢，改线前必须先记住还没接上的部分。",
    "栈": "像叠盘子和拆礼物盒，最后放入或最后打开的一层最先负责结算。",
    "单调结构": "像候场队伍：当前元素一出现，就能淘汰那些以后再也不可能成为答案的旧候选。",
    "单调栈": "像站在队列里等更高的邻居，只有第一次更高事件到来时才结算当前等待者。",
    "二叉树": "像处理一棵会分叉的家族树，先相信子树已经返回正确结果，再决定根节点怎么接。",
    "图与搜索": "像在地图上扩散水波或寻找道路，访问标记保证每个节点只被消费一次。",
    "图与广度优先": "像按换乘次数向外扩散，第一次碰到终点时，所走的层数就是最短距离。",
    "回溯": "像走迷宫做选择：记录当前路线，尝试一个分叉，走不通就原样撤销再试下一个。",
    "动态规划": "像填写一张递推账本，当前格子的答案只由少量已经算好的前序格子决定。",
    "贪心": "像边走边扩展安全可达范围，只保留当下能够证明不会伤害未来的信息。",
    "排序": "像先按统一顺序排队，原本杂乱的局部关系就会变成一次线性扫描。",
    "堆与选择": "像只保留最值得关注的少数候选，每次新元素到来时淘汰最不可能入选的那个。",
    "矩阵与模拟": "像按边界剥洋葱，每次完整走完外圈后就缩小尚未处理的矩形。",
    "设计": "像同时维护目录和最近使用顺序，不同结构各负责一种查询能力。",
    "位运算": "像把每个二进制位当成独立开关，相同信息出现两次时可以通过异或相互抵消。",
}

PATTERN_OBJECT = {
    "数组与哈希": "数组元素与下标、已经扫描过的历史信息",
    "哈希表": "待分组的对象与能够唯一表示其身份的特征",
    "双指针": "有序区间两端的候选位置",
    "滑动窗口": "连续区间及其左右边界",
    "二分查找": "搜索区间、边界和中间分割位置",
    "字符串": "字符、中心位置或已经匹配的前缀",
    "数学": "整数位、反转过程或比较边界",
    "链表": "节点引用和尚未重新连接的剩余链",
    "栈": "尚未结算的左侧符号或外层现场",
    "单调结构": "仍可能成为答案的候选下标或值",
    "单调栈": "等待未来更大或更小事件结算的候选",
    "二叉树": "子树返回信息与当前节点",
    "图与搜索": "节点、邻接关系和访问标记",
    "图与广度优先": "当前层单词和尚未访问的相邻状态",
    "回溯": "当前路径、可选集合和撤销现场",
    "动态规划": "可复用的子问题状态",
    "贪心": "当前可达范围、边界和已证明安全的局部选择",
    "排序": "已经按关键字段获得全局顺序的元素",
    "堆与选择": "大小为 K 或 K+1 的动态候选集合",
    "矩阵与模拟": "四个边界和当前遍历方向",
    "设计": "哈希索引与按访问顺序变化的链表",
    "位运算": "整数的二进制位",
}

PATTERN_STATE = {
    "数组与哈希": "只保留已经扫描过的信息，以及它与当前元素的配对线索。",
    "哈希表": "用特征到同类对象的映射保存已经建立的分类。",
    "双指针": "左右两个候选边界，以及每次移动后仍可排除的区间。",
    "滑动窗口": "当前连续区间、左右边界和判断区间是否合法的计数。",
    "二分查找": "仍可能包含答案的搜索区间和当前分割位置。",
    "字符串": "已经确认匹配、回文或公共关系的那一小段信息。",
    "数学": "当前数位、已构造结果和是否越界的判断。",
    "链表": "已经处理好的前缀、当前节点和尚未接回的剩余链。",
    "栈": "尚未结算的现场，后进入的现场先负责配对或展开。",
    "单调结构": "仍可能成为未来答案的候选及其单调顺序。",
    "单调栈": "等待未来更优事件结算的候选下标集合。",
    "二叉树": "子树返回给父节点的最小充分信息。",
    "图与搜索": "当前节点、邻接关系、访问标记和待处理前沿。",
    "图与广度优先": "当前层状态、下一层状态和 visited 集合。",
    "回溯": "当前路径、仍可选集合和退出分支时必须恢复的现场。",
    "动态规划": "已经算好的子问题答案，以及当前状态的转移来源。",
    "贪心": "已证明安全的当前边界和下一步能到达的最远位置。",
    "排序": "统一的顺序，以及扫描时仍待结算的当前对象。",
    "堆与选择": "大小为 K 或 K+1 的动态候选集合及其极值。",
    "矩阵与模拟": "尚未遍历的四条边界和当前方向。",
    "设计": "每种查询所需的索引，以及最近使用顺序。",
    "位运算": "每个二进制位独立保存的计数或标记。",
}

# The pilot cards are part of the schema-freeze acceptance set. Keep their
# teaching fields explicit instead of asking extraction heuristics to infer
# concepts that need a human-level paraphrase.
CARD_OVERRIDES: dict[int, dict[str, Any]] = {
    1: {
        "essence": "每个位置不用再向未来寻找搭档，只问：“我需要的补数以前来过吗？”",
        "analogy": "像边收卡片边做目录：拿到当前卡片，只查目录里有没有能与它凑成目标值的旧卡片；查完再把当前卡片登记进去。",
        "objects": "已扫描元素的值、值与下标的对应、当前下标",
        "relation": "若答案包含当前下标 i，另一个下标 j 必须满足 j < i 且 nums[j] = target - nums[i]。",
        "state": "Map<Integer, Integer> indexByValue，保存已扫描值到其下标。",
        "event": "扫描到 nums[i]，先计算并查询 target - nums[i]，查询失败后才登记 nums[i]。",
        "invariant": "处理下标 i 之前，表里恰好包含区间 [0, i) 出现过的值和位置。",
        "result": "查到补数时立即返回两个下标；扫描结束仍无结果才说明无解。",
        "why": "若合法答案是 (j,i)，处理 i 时 j 必已登记；反过来，查到补数就同时保证两数之和为目标值且下标不同。",
        "trigger": "输入无序、要找两个对象或两个数配对，并需要返回位置时，考虑“查询已经出现过的补数”。",
        "pseudocode": [
            "建立“值 -> 下标”的空表。",
            "从左到右扫描 nums[i]。",
            "查询 target - nums[i] 是否已在表中。",
            "若在表中，返回补数下标与 i。",
            "若不在表中，登记 nums[i] -> i。",
        ],
        "traps": [
            "不能先登记当前元素再查询，否则 [3,3], target=6 可能把同一个下标使用两次。",
            "集合只能回答“值是否出现”；本题还要返回位置，因此必须保存值到下标。",
        ],
        "java": ["[[Java速查/集合/Map-Set.md|Map / Set]]"],
    },
    3: {
        "essence": "右端加入新字符时，只可能出现一种冲突：它与窗口内同字符重复；左边界跳到该字符上次位置之后即可恢复合法。",
        "analogy": "像手持可伸缩取景框：右端先纳入新画面；只有新画面与框内重复时，左端才越过那个旧位置。",
        "objects": "连续子串、左右边界、每个字符最近出现的位置",
        "relation": "以 right 结尾的合法窗口，左边界必须大于等于 right 位置字符上一次出现的下标再加一。",
        "state": "lastIndex 记录每个字符最近出现的位置；left 表示当前合法窗口左边界，best 记录最长长度。",
        "event": "右端纳入 current=s[right]，读取它的 previous；若 previous >= left，把 left 移到 previous+1。",
        "invariant": "每轮处理完 right 后，[left,right] 无重复字符，且 left 不能再向左而不产生重复。",
        "result": "每轮用 right-left+1 刷新 best；循环结束后的 best 是全局最长长度。",
        "why": "若 current 在窗口内重复，任何包含 previous 的窗口都不合法，所以跳到 previous+1 必要且充分；若旧位置已在窗口外，当前窗口仍然合法。",
        "trigger": "题目要求“最长连续区间”且区间扩展后只有有限几种冲突，冲突又可以由左边界单向修复。",
        "pseudocode": [
            "初始化空 lastIndex、left=0、best=0。",
            "令 right 从左到右移动。",
            "读取 s[right] 的 previous。",
            "若 previous >= left，令 left=previous+1。",
            "更新 lastIndex 和 best=right-left+1。",
        ],
        "traps": [
            "left 只能右移；处理 abba 时，不能因更早的重复位置把 left 拉回。",
            "题目要求连续子串；可以跳过字符的子序列不能套这个模型。",
        ],
        "java": ["[[Java速查/集合/Map-Set.md|Map / Set]]"],
    },
    200: {
        "essence": "把四方向相邻的陆地看成图的连通关系；每找到一个未访问陆地，就完整淹没一个连通分量，岛屿数因此加一。",
        "analogy": "像从一块陆地放水：水只沿上下左右扩散，能到达的陆地属于同一个岛；水位到不了的下一个陆地才是新岛。",
        "objects": "网格格子、四方向相邻关系、是否已经访问",
        "relation": "两个 '1' 格子若上下左右相邻，就连在同一条无向边；岛屿就是一个连通分量。",
        "state": "外层扫描位置、岛屿计数、待搜索栈，以及已经改造为 '0' 的访问标记。",
        "event": "外层发现一个仍为 '1' 的格子时，计数加一，并从它开始 DFS，把所有可达陆地标记为 '0'。",
        "invariant": "一个连通分量的 DFS 结束后，该分量的每个陆地都已标记，且不会进入水域或其他分量。",
        "result": "外层扫描全部格子后，岛屿计数就是连通分量数。",
        "why": "新发现的 '1' 不可能属于此前已经搜索完的岛屿；完整搜索又恰好覆盖当前岛屿的全部陆地，所以每个岛只计数一次。",
        "trigger": "题目把矩阵中的相邻格子看成关系，并要求数连通块、区域数量或可达集合。",
        "pseudocode": [
            "初始化 islands=0。",
            "从上到下、从左到右扫描每个格子。",
            "遇到 '0' 跳过；遇到 '1' 时 islands 加一。",
            "从该格子出发，把四方向可达的 '1' 全部改为 '0'。",
            "扫描结束返回 islands。",
        ],
        "traps": [
            "输入判断的是字符 '1'/'0'，不是整数 1/0。",
            "只允许上下左右相邻，对角接触不算同一个岛。",
        ],
        "java": ["[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]"],
    },
    322: {
        "essence": "一个最优方案拿走最后一枚硬币后，剩余金额也必须是最优的；因此枚举“最后一枚”即可得到 dp[x] 的所有来源。",
        "analogy": "像填写按金额递增的账本：要算凑出 11 元的最少硬币，只看拿走最后一枚后留下的 10、9 或 6 元账目。",
        "objects": "金额、硬币面额、已经算好的子金额答案",
        "relation": "dp[x] = min(dp[x-coin]+1)，其中 coin <= x；同一个 coin 可以重复选择。",
        "state": "dp[x] 表示恰好凑出金额 x 的最少硬币数；dp[0]=0，其余先记为不可达。",
        "event": "从金额 current=1 递增到 amount，枚举每个 coin <= current，并用 dp[current-coin]+1 更新 dp[current]。",
        "invariant": "处理 current 前，所有小于 current 的金额都已经是各自的最优答案。",
        "result": "dp[amount] 仍为哨兵时返回 -1，否则返回它的最少硬币数。",
        "why": "任意可行方案都能按最后一枚硬币拆分；算法枚举了所有可能的最后一枚，并复用已经最优的子金额，所以既不会漏解，也不会得到更大答案。",
        "trigger": "问题可拆成“最后选择一次”，选择后剩余部分与原问题同型，并且子问题按一个维度递增计算。",
        "pseudocode": [
            "令 unreachable=amount+1。",
            "dp[0]=0，其余位置填 unreachable。",
            "令 current 从 1 增加到 amount。",
            "枚举不超过 current 的 coin。",
            "用 dp[current-coin]+1 更新 dp[current]。",
            "返回 dp[amount]；仍不可达则为 -1。",
        ],
        "traps": [
            "amount=0 的答案是 0，不需要硬币。",
            "哨兵不要用 Integer.MAX_VALUE 后直接加一；amount+1 不会溢出且大于任何可行枚数。",
        ],
        "java": ["[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]"],
    },
    49: {
        "essence": "不要两两比较单词，而是把“字母多重集合”压缩成一个完全相同的规范化键；键相同就属于同一组。",
        "analogy": "像给每张字母卡片计算同一套指纹：由相同字母组成的单词会得到同一指纹，然后按指纹放进对应抽屉。",
        "objects": "单词、26 个字母的出现次数、由次数生成的签名",
        "relation": "两个单词是异位词，当且仅当它们对 a 到 z 每个字母的出现次数完全相同。",
        "state": "Map<String, List<String>> groups，键是 26 个计数的无损编码，值是共享该签名的单词。",
        "event": "读取当前单词，统计 26 个字母的频次并生成签名，再从 groups 取出或创建对应列表。",
        "invariant": "一个单词处理完后，它只出现在与自身字母计数完全一致的那个分组中。",
        "result": "所有单词都加入分组后，groups 的全部值就是题目要求的分组列表。",
        "why": "计数向量完整描述了小写单词的字母组成；固定顺序和分隔符保证相同向量得到相同键、不同向量不会碰撞成同一个键。",
        "trigger": "题目要求按“换顺序后仍相同”的关系分组，或需要把复杂对象映射到可比较的规范表示。",
        "pseudocode": [
            "建立“签名字符串 -> 字符串列表”的空表。",
            "逐个读取单词。",
            "统计该单词中 a 到 z 的出现次数。",
            "按固定顺序和分隔符编码计数，得到签名。",
            "把单词加入该签名对应的列表。",
            "返回表中所有列表。",
        ],
        "traps": [
            "频次数值之间要加分隔符；直接拼接可能让不同计数产生同一个含糊字符串。",
            "所有空字符串的计数向量都相同，应当进入同一组。",
        ],
        "java": [
            "[[Java速查/集合/Map-Set.md|Map / Set]]",
            "[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]",
        ],
    },
    215: {
        "essence": "第 K 大在升序数组中的位置是 n-K；分区后枢轴已经到达最终位置，只保留包含目标位置的一侧即可。",
        "analogy": "像整理书架时只关心第 K 个位置：每次分好一本书的最终位置，确定目标在左边还是右边，另一半不必再排序。",
        "objects": "候选区间、分区枢轴、目标升序下标",
        "relation": "答案下标 target=n-K；partition 返回 pivotIndex，并保证左侧不大于枢轴、右侧不小于枢轴。",
        "state": "当前候选区间 [left,right] 和本轮枢轴的最终下标 pivotIndex。",
        "event": "对 [left,right] 做一次分区；将 pivotIndex 与 target 比较，舍弃不含 target 的一半。",
        "invariant": "每轮之前的候选区间始终包含答案下标 target，且区间外的元素已经不可能替代答案。",
        "result": "pivotIndex==target 时，枢轴值就是第 K 大；区间不断缩小，最终必然命中。",
        "why": "枢轴左侧都 <= 枢轴、右侧都 >= 枢轴，所以枢轴位置就是其升序最终位置；目标在哪一侧也可以据此唯一判断。",
        "trigger": "只关心顺序统计量，不要求整体有序，并且能从一次分区中安全排除一半候选。",
        "pseudocode": [
            "令 target=n-K，left=0，right=n-1。",
            "在 [left,right] 中随机选枢轴并分区。",
            "得到枢轴最终位置 pivotIndex。",
            "若 pivotIndex==target，返回 nums[pivotIndex]。",
            "若 target 在左侧，缩小 right；否则增大 left。",
        ],
        "traps": [
            "第 K 大的升序下标是 n-K，不是 K-1。",
            "重复元素参与排名，不能先去重。",
        ],
        "java": [
            "[[Java速查/选择结构/PriorityQueue-Comparator.md|PriorityQueue / Comparator]]",
            "[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]",
        ],
    },
    124: {
        "essence": "递归让每个节点分别回答一个问题：“向上贡献多少？”和“以我为最高点，能形成多大的完整路径？”",
        "analogy": "像每个路口向父路口只报告最强的一条单线路，同时在本地比较“左路 + 自己 + 右路”能否刷新全局最佳。",
        "objects": "当前节点、左右子树向上贡献、当前节点为最高点的完整路径和",
        "relation": "gain(node)=node.val+max(0,gain(left),gain(right))；完整路径和=node.val+max(0,gain(left))+max(0,gain(right))。",
        "state": "递归返回值 gain(node) 与全局答案 best。gain 只允许选择一条向下分支，best 记录任一节点处计算出的完整路径最大值。",
        "event": "后序处理当前节点：先取得两个孩子的 gain，再把非负贡献相加更新 best。",
        "invariant": "每次 gain(node) 返回后，它都是 node 向下连接至多一条分支时的最大非空路径和。",
        "result": "遍历所有节点后，best 是所有完整路径和的最大值。",
        "why": "每条简单路径都有唯一最高节点；该节点处恰好可以组合左右贡献，而向上返回时只能保留一支，因此分类完整且不会构造分叉路径。",
        "trigger": "树路径允许在某个节点汇合但不能继续分叉，并且子树只需向父节点报告一个最优标量。",
        "pseudocode": [
            "令 best=Integer.MIN_VALUE。",
            "后序遍历 node。",
            "取得左侧最大贡献 max(0,gain(left))。",
            "取得右侧最大贡献 max(0,gain(right))。",
            "用 node.val+left+right 更新 best。",
            "返回 node.val+max(left,right) 作为向上单支贡献。",
        ],
        "traps": [
            "best 不能初始化为 0，否则全负树会错误返回 0。",
            "更新 best 可以同时使用左右两支；返回父节点时只能选贡献更大的一支。",
        ],
        "java": [],
    },
}


def problem_topics(problem: dict[str, Any]) -> list[str]:
    topics = [problem["primaryPattern"]]
    for tag in problem.get("officialTags") or []:
        name = tag.get("translatedName") or tag.get("name")
        if name and name not in topics:
            topics.append(name)
    return topics


def problem_priority(problem: dict[str, Any]) -> str:
    priorities = problem.get("checklistPriorities") or []
    return priorities[0] if priorities else "P2"


def sha_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(markdown: str, pattern: str) -> str:
    match = re.search(
        rf"^#{{2,4}}\s+(?:{pattern})[^\n]*\n([\s\S]*?)(?=^#{{2,4}}\s+|\Z)",
        markdown,
        re.M,
    )
    return match.group(1).strip() if match else ""


def strip_markdown(value: str) -> str:
    value = re.sub(r"```(?:[A-Za-z0-9_+-]+)?\s*\n([\s\S]*?)```", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"</?[A-Za-z][^>]*>", "", value)
    value = re.sub(r"`([^`]*)`", r"\1", value)
    value = re.sub(r"^\s*[-*]\s+", "", value, flags=re.M)
    value = re.sub(r"^\s*\d+\.\s+", "", value, flags=re.M)
    value = re.sub(r"^\s*>\s?", "", value, flags=re.M)
    value = re.sub(r"[ \t]+", " ", value)
    return value.strip()


def paragraphs(value: str) -> list[str]:
    output: list[str] = []
    value = re.sub(
        r"```(?:[A-Za-z0-9_+-]+)?\s*\n([\s\S]*?)```",
        r"\1",
        value,
    )
    for block in re.split(r"\n\s*\n", value):
        block = block.strip()
        if not block:
            continue
        if all(line.lstrip().startswith(("|", ">")) for line in block.splitlines()):
            continue
        groups: list[list[str]] = []
        current: list[str] = []
        current_is_list = False
        for line in block.splitlines():
            stripped = line.strip()
            is_list = bool(re.match(r"^(?:[-*]|\d+\.)\s+", stripped))
            if is_list:
                if current:
                    groups.append(current)
                current = [line]
                current_is_list = True
            elif current_is_list and line[:1].isspace():
                current.append(line)
            else:
                if current:
                    groups.append(current)
                current = [line]
                current_is_list = False
        if current:
            groups.append(current)
        for group in groups:
            cleaned = strip_markdown("\n".join(group))
            if cleaned:
                output.append(cleaned)
    return output


def cjk_count(value: str) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", value))


def trim(value: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= limit:
        return value
    cut = value[:limit]
    sentence_end = max(cut.rfind("。"), cut.rfind("；"), cut.rfind("！"), cut.rfind("？"))
    if sentence_end >= limit // 2:
        return cut[: sentence_end + 1]
    return cut.rstrip("，；。") + "。"


def first_paragraph(value: str, fallback: str) -> str:
    blocks = paragraphs(value)
    if not blocks:
        return fallback
    combined = blocks[0]
    index = 1
    while (
        index < len(blocks)
        and (
            combined.rstrip().endswith(("：", ":"))
            or len(combined) < 90
        )
    ):
        combined = f"{combined} {blocks[index]}"
        index += 1
        if len(combined) >= 180:
            break
    return trim(combined, 210)


def choose_paragraph(value: str, keywords: tuple[str, ...], fallback: str) -> str:
    blocks = paragraphs(value)
    for index, block in enumerate(blocks):
        if any(keyword in block for keyword in keywords):
            return complete_paragraph(blocks, index)
    return complete_paragraph(blocks, 0) if blocks else fallback


def choose_distinct_paragraph(
    value: str,
    keywords: tuple[str, ...],
    fallback: str,
    excluded: set[str],
) -> str:
    blocks = paragraphs(value)
    for index, block in enumerate(blocks):
        candidate = complete_paragraph(blocks, index)
        if (
            candidate not in excluded
            and "时间复杂度" not in block
            and "空间复杂度" not in block
            and any(keyword in block for keyword in keywords)
        ):
            return candidate
    for index, block in enumerate(blocks):
        candidate = complete_paragraph(blocks, index)
        if (
            candidate not in excluded
            and "时间复杂度" not in block
            and "空间复杂度" not in block
        ):
            return candidate
    return fallback


def complete_paragraph(
    blocks: list[str],
    index: int,
    limit: int = 210,
) -> str:
    combined = blocks[index]
    next_index = index + 1
    while (
        next_index < len(blocks)
        and (
            combined.rstrip().endswith(("：", ":"))
            or len(combined) < 45
        )
    ):
        combined = f"{combined} {blocks[next_index]}"
        next_index += 1
        if len(combined) >= limit:
            break
    return trim(combined, limit)


def choose_result_paragraph(value: str, fallback: str) -> str:
    blocks = [
        block
        for block in paragraphs(value)
        if "复杂度" not in block
    ]
    preferred = (
        "返回",
        "循环结束",
        "扫描结束",
        "遍历结束",
        "逐行完成",
        "收够",
        "答案就是",
        "得到全局",
        "最终",
    )
    for index, block in enumerate(blocks):
        if (
            any(keyword in block for keyword in preferred)
            and not block.lstrip().startswith(("初始化", "维护", "建立"))
        ):
            return complete_paragraph(blocks, index)
    for index, block in enumerate(blocks):
        if any(
            keyword in block
            for keyword in ("答案", "结果", "输出", "完成")
        ):
            return complete_paragraph(blocks, index)
    return complete_paragraph(blocks, 0) if blocks else fallback


def bullets(value: str, limit: int = 2) -> list[str]:
    output: list[str] = []
    for line in value.splitlines():
        match = re.match(r"^\s*[-*]\s+(.+)$", line)
        if not match:
            continue
        cleaned = strip_markdown(match.group(1))
        if cleaned:
            output.append(trim(cleaned, 180))
        if len(output) >= limit:
            break
    if output:
        return output
    return [trim(paragraph, 180) for paragraph in paragraphs(value)[:limit]]


def complexity(markdown: str) -> tuple[str, str]:
    time_matches = list(
        re.finditer(r"(?:时间复杂度|时间)[^\n：:]*[：:]\s*([^\n]+)", markdown)
    )
    space_matches = list(
        re.finditer(r"(?:空间复杂度|空间)[^\n：:]*[：:]\s*([^\n]+)", markdown)
    )
    time = strip_markdown(time_matches[-1].group(1)) if time_matches else ""
    space = strip_markdown(space_matches[-1].group(1)) if space_matches else ""
    return (
        time or "以标准题解的最优实现为准",
        space or "以标准题解的最优实现为准",
    )


def numbered_steps(value: str, fallback: str) -> list[str]:
    steps: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if not current:
            return
        step = strip_markdown(" ".join(current))
        if step and step not in steps:
            steps.append(step)
        current.clear()

    for line in value.splitlines():
        match = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if match:
            flush()
            current.append(match.group(1))
            if len(steps) >= 8:
                break
        elif current and not line.strip():
            flush()
        elif current and line.strip():
            current.append(line.strip())
    flush()
    steps = steps[:8]
    if steps:
        return steps
    block = paragraphs(value)
    if block:
        sentences = re.split(r"(?<=[。；])", block[0])
        return [sentence.strip() for sentence in sentences if sentence.strip()][:6]
    return [fallback]


def first_action_step(value: str) -> str:
    numbered = numbered_steps(value, "")
    bullet_steps = [
        strip_markdown(match.group(1))
        for line in value.splitlines()
        if (match := re.match(r"^\s*[-*]\s+(.+)$", line))
    ]
    steps = numbered + [step for step in bullet_steps if step not in numbered]
    initialization = re.compile(
        r"^(?:先)?(?:初始化|建立|构建|创建|统计|把所有|把\s*[A-Za-z]|"
        r"一次扫描|初始|维护)"
    )
    action = re.compile(
        r"(?:每次|当|遇到|处理|检查|扫描|遍历|取出|弹出|交换|更新|"
        r"计算|比较|递归|判断|若|如果|替换|加入|压入|删除|结束|"
        r"之后|持续|置为|寻找|扩展|发现|再次相遇|\bpush\b|\bpop\b)"
    )
    for step in steps:
        if step and not initialization.match(step) and action.search(step):
            return step
    for step in steps:
        if step and not initialization.match(step):
            return step
    return steps[0] if steps else ""


def table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def cell_summary(value: str, limit: int = 120) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    parts = [
        part.strip()
        for part in re.split(r"(?<=[。！？；])", value)
        if part.strip()
    ]
    if not parts:
        return ""
    summary = parts[0]
    index = 1
    while (
        index < len(parts)
        and (
            summary.endswith(("：", ":", "，", "、"))
            or len(summary) < 45
        )
        and len(summary) < limit
    ):
        summary += parts[index]
        index += 1
    return summary


def complete_clause(value: str, source: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    candidates = [
        block for block in paragraphs(source) if "复杂度" not in block
    ]
    for _ in range(3):
        if not value.endswith(("：", ":", "，", "；", "、")):
            return value
        for candidate in candidates:
            candidate = re.sub(r"\s+", " ", candidate).strip()
            if candidate and candidate != value and candidate not in value:
                value = f"{value} {candidate}".strip()
                break
        else:
            if value.endswith(("：", ":")):
                value += "按该处列出的分支依次更新状态。"
            else:
                value += "继续按当前分支完成这次状态更新。"
    return value


def calculation_summary(value: str, limit: int = 160) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    parts = [
        part.strip()
        for part in re.split(r"(?<=[。！？])", value)
        if part.strip()
    ]
    if not parts:
        return value
    summary = parts[0]
    if len(summary) > limit and "。" not in summary:
        return value
    return summary


def java_tools(problem: dict[str, Any], markdown: str) -> list[str]:
    sources = " ".join(
        [
            markdown,
            problem.get("javaTemplate") or "",
        ]
    )
    tools: list[str] = []
    if re.search(r"\b(?:HashMap|Map<|HashSet|Set<)", sources):
        tools.append("[[Java速查/集合/Map-Set.md|Map / Set]]")
    if re.search(r"\b(?:ArrayDeque|Deque<|Stack<)", sources):
        tools.append("[[Java速查/线性结构/Deque-Stack.md|Deque / Stack]]")
    if re.search(r"\b(?:PriorityQueue|Comparator)", sources):
        tools.append(
            "[[Java速查/选择结构/PriorityQueue-Comparator.md|PriorityQueue / Comparator]]"
        )
    if re.search(r"\b(?:Arrays|StringBuilder|String\b)", sources):
        tools.append(
            "[[Java速查/基础工具/Arrays-StringBuilder.md|Arrays / StringBuilder]]"
        )
    if re.search(r"\b(?:Math\.|<<|>>|&\s*\d|\^\s*\d)", sources):
        tools.append("[[Java速查/基础工具/Math-位运算.md|Math / 位运算]]")
    return tools


def relative_path(path: Path) -> str:
    return path.relative_to(LIBRARY_ROOT).as_posix()


def frontmatter(problem: dict[str, Any], core_path: Path, deep_path: Path | None) -> str:
    values: list[tuple[str, Any]] = [
        ("schemaVersion", 3),
        ("type", "core-model"),
        ("leetcodeId", problem["id"]),
        ("slug", problem["slug"]),
        ("titleCn", problem["titleCn"]),
        ("titleEn", problem["titleEn"]),
        ("difficulty", problem["difficulty"]),
        ("sourceUrl", problem["sourceUrl"]),
        ("sourceCheckedAt", problem["sourceCheckedAt"]),
        ("sourceFactsSha256", problem["sourceFactsSha256"]),
        ("primaryPattern", problem["primaryPattern"]),
        ("topics", problem_topics(problem)),
        ("priority", problem_priority(problem)),
        ("problemPath", problem["relativePath"]),
        ("deepDivePath", relative_path(deep_path) if deep_path else None),
        ("mastery", "已理解"),
        ("reviewStatus", "未安排"),
        ("nextReview", None),
        ("lastReviewed", None),
        ("errorTags", []),
        ("independentAttempts", 0),
    ]
    lines = ["---"]
    for key, value in values:
        if isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        elif value is None:
            lines.append(f"{key}: null")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


def core_body(
    problem: dict[str, Any],
    markdown: str,
    core_path: Path,
    deep_path: Path | None,
) -> str:
    patterns = [
        "核心观察",
        "[^\\n]*最优方案[^\\n]*",
        "正确性与不变量",
        "边界与易错点",
        "学习提示（非官方）",
        "复杂度",
    ]
    core_observation = section(markdown, patterns[0])
    optimal = section(markdown, patterns[1])
    correctness = section(markdown, patterns[2])
    edge = section(markdown, patterns[3])
    hints = section(markdown, patterns[4])
    complexity_section = section(markdown, patterns[5])
    override = CARD_OVERRIDES.get(int(problem["id"]), {})

    if not correctness:
        correctness = section(markdown, "正确性与不变量|正确性和不变量")
    observation_text = override.get("essence") or first_paragraph(
        core_observation,
        f"本题的核心是把“{problem['titleCn']}”转换成可增量维护的状态。",
    )
    relation_text = override.get("relation") or (
        f"把题目翻译成一条可执行关系：{trim(observation_text, 190)}"
    )
    state_text = override.get("state") or choose_distinct_paragraph(
        optimal + "\n\n" + core_observation,
        ("状态", "维护", "记录", "保存", "队列", "栈", "数组", "哈希", "dp["),
        PATTERN_STATE.get(
            problem["primaryPattern"],
            f"维护能决定后续答案的最小状态：{PATTERN_OBJECT.get(problem['primaryPattern'], '当前候选信息')}。",
        ),
        {relation_text},
    )
    event_text = override.get("event") or first_action_step(optimal) or (
        choose_distinct_paragraph(
            optimal,
            ("当", "每次", "扫描", "遇到", "处理", "进入", "弹出", "选择"),
            "当前输入到达并可能改变已维护状态时，触发一次更新。",
            {state_text},
        )
    )
    invariant_text = override.get("invariant") or first_paragraph(
        correctness,
        f"每一步更新后都保持“{observation_text}”所描述的关系。",
    )
    result_text = override.get("result") or choose_distinct_paragraph(
        correctness + "\n\n" + optimal,
        ("返回", "答案", "结果", "得到", "输出", "完成"),
        "题目目标满足或全部输入处理完成时返回结果。",
        {state_text, event_text, invariant_text},
    )
    if not override.get("result"):
        result_text = choose_result_paragraph(
            correctness + "\n\n" + optimal,
            result_text,
        )
    if not override.get("state"):
        state_text = complete_clause(state_text, optimal)
    if not override.get("event"):
        event_text = complete_clause(event_text, optimal)
    if not override.get("result"):
        result_text = complete_clause(result_text, correctness)
    trigger_seed = bullets(hints, 1)
    trigger = override.get("trigger") or (
        trigger_seed[0] if trigger_seed else observation_text
    )

    why_blocks = [
        block
        for block in paragraphs(correctness)
        if block != invariant_text
        and "时间复杂度" not in block
        and "空间复杂度" not in block
    ]
    why = override.get("why") or (
        trim(" ".join(why_blocks[:2]), 150) if why_blocks else invariant_text
    )
    trap_items = override.get("traps") or bullets(edge, 2)
    if not trap_items:
        trap_items = ["先确认输入边界和状态更新顺序，再对照最小示例执行一次。"]

    mapping_steps = override.get("pseudocode") or numbered_steps(
        optimal,
        "按事件顺序更新状态，并在答案条件成立时返回。",
    )
    if len(mapping_steps) < 3:
        for candidate in (event_text, state_text, result_text):
            if candidate not in mapping_steps:
                mapping_steps.append(candidate)
            if len(mapping_steps) >= 3:
                break
    pseudocode = "\n".join(
        [
            f"{index}. {step}"
            for index, step in enumerate(mapping_steps[:7], start=1)
        ]
    )
    example = (problem.get("officialExamples") or [{}])[0]
    example_input = strip_markdown(example.get("input") or "见标准题解")
    example_output = strip_markdown(example.get("output") or "见标准题解")
    time_value, space_value = complexity(
        optimal + "\n" + complexity_section + "\n" + markdown
    )

    # Use Obsidian links for stable navigation inside the vault.
    links = [
        f"- [[{problem['relativePath']}|标准题解：题意、代码、边界]]",
    ]
    if deep_path:
        links.append(f"- [[{relative_path(deep_path)}|完整建模：试错、证明与迁移]]")
    tools = override.get("java") or java_tools(problem, markdown)
    if tools:
        links.append("- Java 速查：" + " · ".join(tools))

    return "\n".join(
        [
            f"# {problem['id']}. {problem['titleCn']}：核心模型",
            "",
            (
                f"> **双轨阅读：** [[{problem['relativePath']}|标准题解]]"
                + (
                    f" · [[{relative_path(deep_path)}|完整建模]]"
                    if deep_path
                    else ""
                )
            ),
            "",
            "## 一句话本质",
            "",
            observation_text,
            "",
            "## 直观画面与扩题",
            "",
            override.get("analogy")
            or PATTERN_ANALOGY.get(
                problem["primaryPattern"],
                "先把输入、目标和约束画成一张变化图，再判断哪些信息可以丢弃。",
            ),
            "",
            f"在本题中，对象是 **{override.get('objects', PATTERN_OBJECT.get(problem['primaryPattern'], '输入中的核心元素'))}**；"
            f"把它从“枚举全部可能”改写为“只维护影响下一步的最少信息”。",
            "",
            "## 关系重写",
            "",
            relation_text,
            "",
            "## 模型要素",
            "",
            "| 对象 | 关系 | 状态 | 事件 | 不变量 | 结果时机 |",
            "| --- | --- | --- | --- | --- | --- |",
            "| "
            + " | ".join(
                [
                    override.get(
                        "objects",
                        PATTERN_OBJECT.get(problem["primaryPattern"], "核心对象"),
                    ),
                    table_cell(cell_summary(relation_text)),
                    table_cell(cell_summary(state_text)),
                    table_cell(cell_summary(event_text)),
                    table_cell(cell_summary(invariant_text)),
                    table_cell(cell_summary(result_text)),
                ]
            )
            + " |",
            "",
            "## 最小演算",
            "",
            f"官方首例输入：`{trim(example_input, 180)}`，输出：`{trim(example_output, 100)}`。",
            "",
            f"1. **初始状态：** {calculation_summary(state_text)}",
            f"2. **触发事件：** {calculation_summary(event_text)}",
            f"3. **结束条件：** {calculation_summary(result_text)}",
            "4. **核对首例：** 按上述状态与事件逐步更新，最终应得到题面给出的输出；"
            "若结果不符，优先检查状态初始化、更新先后顺序和边界收缩方向。",
            "",
            "## 为什么成立",
            "",
            why,
            "",
            "## 代码映射",
            "",
            "```text",
            pseudocode,
            "```",
            "",
            "## 复杂度",
            "",
            f"- 时间复杂度：{time_value}",
            f"- 空间复杂度：{space_value}",
            "",
            "## 30 秒识别信号",
            "",
            f"- 主题型：`{problem['primaryPattern']}`",
            f"- 切入点：{trim(trigger, 120)}",
            "",
            "## 最小反例与易错点",
            "",
            *[f"- {item}" for item in trap_items],
            "",
            "## 分层入口",
            "",
            *links,
            "",
        ]
    )


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    modeling_by_id = {
        int(match.group(1)): path
        for path in MODELING_ROOT.glob("*.md")
        if (match := re.match(r"^(\d+)-", path.name))
    }
    written = 0
    for problem in manifest["problems"]:
        standard_path = LIBRARY_ROOT / problem["relativePath"]
        markdown = standard_path.read_text(encoding="utf-8")
        core_dir = CORE_ROOT / problem["primaryPattern"]
        core_path = core_dir / f"{standard_path.stem}-核心模型.md"
        core_dir.mkdir(parents=True, exist_ok=True)
        deep_path = modeling_by_id.get(int(problem["id"]))
        body = core_body(problem, markdown, core_path, deep_path)
        core_path.write_text(
            frontmatter(problem, core_path, deep_path) + "\n" + body,
            encoding="utf-8",
        )
        written += 1
    print(f"Generated {written} core-model cards.")


if __name__ == "__main__":
    main()
