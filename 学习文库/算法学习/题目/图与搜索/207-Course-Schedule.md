---
schemaVersion: 3
type: "problem"
leetcodeId: 207
slug: "course-schedule"
titleCn: "课程表"
titleEn: "Course Schedule"
difficulty: "Medium"
sourceUrl: "https://leetcode.cn/problems/course-schedule/"
sourceCheckedAt: "2026-08-30"
sourceContentSha256: "d8a0fb3ccc2eb38186d8d33f3331cbf2d2f03b636b1015b7d6dd33bc4861299c"
sourceFactsSha256: "4704c73597e42cd96123725313b44f8cb8bea59ad75a9c118e8bc35797edb0f5"
sourceSectionHashes:
  description: "c189258c99e1790b39d5ffd00c2d8f28d3159fd3158b73de227efed3bc4bcff0"
  examples: "90da197d66d003fb1020c8fd959c08281075bd6a14665250d45b0dd48d132a6f"
  constraints: "40b78de049bc9625514945f79a69c48818e3ac2b15d8677e06d68bda81cdad1d"
  hints: "5941ac480fb66c39727d90cd861b7d6222c60d2519f18c1bdc05e7f0e76631ea"
  tags: "012cb2c4e2c0d3881e6507b0e906bb03dabbdedeba70a686959bf66eb28d3cd3"
  signature: "f41953c694c1b5e81d6580b41795d596b31362a961947ca066e140acb6515cbf"
  javaTemplate: "8c7250025f08e7fcbe760af4ea12a15946ed24233dac7998bba3e8c60df95941"
primaryPattern: "图与搜索"
topics: ["图与搜索","深度优先搜索","广度优先搜索","图","拓扑排序","有向无环图"]
priority: "P1"
checklistPriorities: ["P1"]
checklistTags: ["Graph 图","Topological Sort 拓扑排序"]
mastery: "已理解"
reviewStatus: "未安排"
nextReview: null
lastReviewed: null
errorTags: []
independentAttempts: 0
---
# 207. 课程表 / Course Schedule

> **双轨入口：** [[核心模型/图与搜索/207-Course-Schedule-核心模型.md|核心模型]] · [[建模专题/T0/207-Course-Schedule-直观建模.md|完整建模]]


## 题目信息

- 官方难度：`Medium`
- 主归档题型：`图与搜索`
- 清单优先级：`P1`
- 清单代表标签：`Graph 图`、`Topological Sort 拓扑排序`
- LeetCode 当前标签：深度优先搜索 (Depth-First Search)、广度优先搜索 (Breadth-First Search)、图 (Graph)、拓扑排序 (Topological Sort)、有向无环图
- 官方来源：<https://leetcode.cn/problems/course-schedule/>
- 题面核验日期：`2026-08-30`
- 官方内容 SHA-256：`d8a0fb3ccc2eb38186d8d33f3331cbf2d2f03b636b1015b7d6dd33bc4861299c`
- **主解法**：Kahn 拓扑排序（BFS）
- **直观建模专题**：[把“互相等待”建模成可释放的依赖](../../建模专题/T0/207-Course-Schedule-直观建模.md)

## 官方题意（LeetCode 中文题面）


> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。

你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1` 。

在选修某些课程之前需要一些先修课程。 先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [a_i, b_i]` ，表示如果要学习课程 `a_i` 则 **必须** 先学习课程  `b_i`_ 。

- 例如，先修课程对 `[0, 1]` 表示：想要学习课程 `0` ，你需要先完成课程 `1` 。

请你判断是否可能完成所有课程的学习？如果可以，返回 `true` ；否则，返回 `false` 。

## 官方示例


**示例 1：**

```text
输入：numCourses = 2, prerequisites = [[1,0]]
输出：true
解释：总共有 2 门课程。学习课程 1 之前，你需要完成课程 0 。这是可能的。
```

**示例 2：**

```text
输入：numCourses = 2, prerequisites = [[1,0],[0,1]]
输出：false
解释：总共有 2 门课程。学习课程 1 之前，你需要先完成​课程 0 ；并且学习课程 0 之前，你还应先完成课程 1 。这是不可能的。
```

## 官方约束


- `1 <= numCourses <= 2000`

- `0 <= prerequisites.length <= 5000`

- `prerequisites[i].length == 2`

- `0 <= a_i, b_i < numCourses`

- `prerequisites[i]` 中的所有课程对 **互不相同**

## 官方额外提示


> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。

1. This problem is equivalent to finding if a cycle exists in a directed graph. If a cycle exists, no topological ordering exists and therefore it will be impossible to take all courses.
2. [Topological Sort via DFS](https://www.cs.princeton.edu/~wayne/kleinberg-tardos/pdf/03Graphs.pdf) - A great tutorial explaining the basic concepts of Topological Sort.
3. Topological sort could also be done via [BFS](http://en.wikipedia.org/wiki/Topological_sorting#Algorithms).

## 学习提示（非官方）

1. 把先修关系 `[a,b]` 建成有向边 `b -> a`。
2. 能完成全部课程等价于依赖图中不存在有向环。
3. 入度为 0 的课程当前没有未完成的前置条件，可以立即学习。

## 性能目标与约束推导

> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。

- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。

## 补充自测用例

> 以下用例来自原学习文档的补充示例，不属于官方题面。

### 补充用例 1

```text
输入：numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
输出：true
解释：一种顺序是 0,1,2,3。
```

## 核心观察

课程关系是有向图。若有环，环中每门课程都在等待另一门，无法开始；若无环，则图是 DAG，一定存在拓扑序。问题因此转换为“拓扑排序能否取出所有节点”。

## 朴素方案

枚举所有课程排列并验证先修顺序，时间达到 `O(n!)`。或者对每个节点单独执行一次可达性搜索判断能否回到自身，重复遍历大量边，最坏接近 `O(V(V+E))`。

## 最优方案推导

1. 构建邻接表：`next[b]` 包含依赖 `b` 的课程 `a`。
2. 统计每门课程入度。
3. 把所有入度为 0 的课程放入队列。
4. 每取出一门课程，视为完成它，令其后继课程入度减一；减到 0 就入队。
5. 最终完成数量等于 `numCourses`，说明无环。

## 正确性与不变量

队列中始终只包含所有前置课程均已处理的节点，所以按出队顺序学习是合法的。删除一个已完成节点的出边，相当于满足后继的一项先修要求。

若最终处理全部节点，得到合法拓扑序。若仍有节点未处理，则剩余子图中每个节点入度至少为 1；有限有向图沿前驱不断回溯必然重复节点，从而存在环。因此返回条件充要。

## 复杂度

- **时间复杂度**：`O(V + E)`，其中 `V = numCourses`，`E = prerequisites.length`。
- **空间复杂度**：`O(V + E)`，用于邻接表、入度数组和队列。

## Java 实现

### LeetCode 可直接提交代码

> 入口类与方法已根据 2026-08-30 的官方 Java 模板核验。本代码不包含本地 `main`。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>(numCourses);
        for (int course = 0; course < numCourses; course++) {
            graph.add(new ArrayList<>());
        }

        int[] indegree = new int[numCourses];
        for (int[] prerequisite : prerequisites) {
            int course = prerequisite[0];
            int required = prerequisite[1];
            graph.get(required).add(course);
            indegree[course]++;
        }

        Deque<Integer> queue = new ArrayDeque<>();
        for (int course = 0; course < numCourses; course++) {
            if (indegree[course] == 0) {
                queue.offer(course);
            }
        }

        int completed = 0;
        while (!queue.isEmpty()) {
            int course = queue.poll();
            completed++;
            for (int next : graph.get(course)) {
                indegree[next]--;
                if (indegree[next] == 0) {
                    queue.offer(next);
                }
            }
        }
        return completed == numCourses;
    }
}
```

### 本地可运行示例

> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>(numCourses);
        for (int course = 0; course < numCourses; course++) {
            graph.add(new ArrayList<>());
        }

        int[] indegree = new int[numCourses];
        for (int[] prerequisite : prerequisites) {
            int course = prerequisite[0];
            int required = prerequisite[1];
            graph.get(required).add(course);
            indegree[course]++;
        }

        Deque<Integer> queue = new ArrayDeque<>();
        for (int course = 0; course < numCourses; course++) {
            if (indegree[course] == 0) {
                queue.offer(course);
            }
        }

        int completed = 0;
        while (!queue.isEmpty()) {
            int course = queue.poll();
            completed++;
            for (int next : graph.get(course)) {
                indegree[next]--;
                if (indegree[next] == 0) {
                    queue.offer(next);
                }
            }
        }
        return completed == numCourses;
    }
}

public class Main {
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.canFinish(2,
                new int[][]{{1, 0}})); // true
        System.out.println(solution.canFinish(2,
                new int[][]{{1, 0}, {0, 1}})); // false
        System.out.println(solution.canFinish(4,
                new int[][]{{1, 0}, {2, 0}, {3, 1}, {3, 2}})); // true
    }
}
```

## 边界与易错点

- `[a,b]` 的边方向是 `b -> a`，不要反建。
- 没有依赖时，所有课程初始入队，应返回 `true`。
- 只判断“队列最后是否为空”没有意义，关键是处理节点总数。
- 邻接表的泛型嵌套容易写错，构建后要为每个课程初始化空列表。

## 可扩展变式

- 输出课程顺序：记录出队顺序；若长度不足则不存在合法顺序。
- 找出环：使用 DFS 三色标记并记录父节点，可恢复一条环路径。
- 求最少学期数：在可并行学习的前提下按 BFS 层数统计。
- 动态增加依赖：普通拓扑排序需重算；大规模场景可研究动态拓扑序。
