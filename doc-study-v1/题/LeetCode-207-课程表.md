---
相关文档导航:
  - [图论专题导航](../图论专题/导航.md)
  - [学习顺序 - 图论专题](../图论专题/学习顺序 - 图论专题.md)
  - [微模板与易错点卡片](../图论专题/课程表/微模板与易错点卡片.md)
  - [模板索引：拓扑排序](../学习方法/模板索引.md#拓扑排序)
---
# LeetCode-207 课程表

- 难度：中等
- 链接：https://leetcode.cn/problems/course-schedule/

## 问题描述
你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1`。在选修某些课程之前需要一些先修课程。先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [ai, bi]`，表示如果要学习课程 `ai` 则必须先学习课程 `bi`。

请你判断是否可能完成所有课程的学习？如果可以，返回 `true`；否则，返回 `false`。

例如：
- 输入：`numCourses = 2, prerequisites = [[1,0]]` → 输出：`true`
- 输入：`numCourses = 2, prerequisites = [[1,0],[0,1]]` → 输出：`false`（存在循环依赖）

## 题解一：拓扑排序（Kahn 算法）
- 思路：
  1. 构建邻接表和入度数组
  2. 将所有入度为 0 的节点加入队列
  3. 依次取出节点，将其邻居的入度减 1，若邻居入度变为 0 则加入队列
  4. 统计访问的节点数，若等于课程总数则无环
- 复杂度：时间 O(V+E)，空间 O(V+E)

```java
import java.util.*;
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> graph = new ArrayList<>();
        int[] inDegree = new int[numCourses];
        
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        for (int[] pre : prerequisites) {
            graph.get(pre[1]).add(pre[0]);
            inDegree[pre[0]]++;
        }
        
        Queue<Integer> queue = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) {
            if (inDegree[i] == 0) queue.offer(i);
        }
        
        int visited = 0;
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            visited++;
            for (int next : graph.get(cur)) {
                inDegree[next]--;
                if (inDegree[next] == 0) queue.offer(next);
            }
        }
        
        return visited == numCourses;
    }
}
```

## 题解二：DFS 检测环
- 思路：使用三色标记法（0=未访问，1=访问中，2=已完成），DFS 遍历过程中若遇到"访问中"的节点说明存在环
- 复杂度：时间 O(V+E)，空间 O(V+E)

```java
import java.util.*;
class Solution {
    List<List<Integer>> graph;
    int[] state; // 0=未访问，1=访问中，2=已完成
    
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        graph = new ArrayList<>();
        state = new int[numCourses];
        for (int i = 0; i < numCourses; i++) graph.add(new ArrayList<>());
        for (int[] pre : prerequisites) graph.get(pre[1]).add(pre[0]);
        
        for (int i = 0; i < numCourses; i++) {
            if (state[i] == 0 && hasCycle(i)) return false;
        }
        return true;
    }
    
    private boolean hasCycle(int node) {
        state[node] = 1; // 标记为访问中
        for (int next : graph.get(node)) {
            if (state[next] == 1) return true; // 遇到访问中的节点，有环
            if (state[next] == 0 && hasCycle(next)) return true;
        }
        state[node] = 2; // 标记为已完成
        return false;
    }
}
```

## 总结思路
- 本质是检测有向图是否有环
- 拓扑排序更直观，适合求具体学习顺序
- DFS 检测环代码更简洁

## 相关标签
- 图论、拓扑排序、DFS、有向图
