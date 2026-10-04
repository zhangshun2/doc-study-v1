import java.util.*;

/**
 * LeetCode 301 - 删除无效的括号 (Java BFS实现)
 * 使用BFS层序搜索，天然保证最少删除次数
 */
public class Solution {
    
    /**
     * 主函数：删除无效括号
     * @param s 输入字符串
     * @return 所有最少删除后的有效字符串列表
     */
    public List<String> removeInvalidParentheses(String s) {
        List<String> result = new ArrayList<>();
        
        // 如果原始字符串已经有效，直接返回
        if (isValid(s)) {
            result.add(s);
            return result;
        }
        
        // BFS队列和访问集合size
        Queue<String> queue = new LinkedList<>();
        Set<String> visited = new HashSet<>();
        queue.offer(s);
        visited.add(s);
        
        boolean found = false; // 是否找到有效层标志
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            
            // 处理当前层的所有字符串
            for (int i = 0; i < levelSize; i++) {
                String current = queue.poll();
                
                // 检查当前字符串是否有效
                if (isValid(current)) {
                    result.add(current);
                    found = true;
                }
                
                // 如果已经找到有效字符串，不再生成下一层
                if (found) {
                    continue;
                }
                
                // 生成下一层：尝试删除每个位置的括号
                for (int j = 0; j < current.length(); j++) {
                    char c = current.charAt(j);
                    
                    // 只删除括号字符，跳过字母字符
                    if (c != '(' && c != ')') {
                        continue;
                    }
                    
                    // 删除第j个字符
                    String next = current.substring(0, j) + current.substring(j + 1);
                    
                    // 如果新字符串未访问过，加入队列
                    if (!visited.contains(next)) {
                        visited.add(next);
                        queue.offer(next);
                    }
                }
            }
            
            // 如果本层已经找到有效结果，停止搜索
            if (found) {
                break;
            }
        }
        
        return result;
    }
    
    /**
     * 检查字符串括号是否有效
     * @param s 输入字符串
     * @return 是否有效
     */
    private boolean isValid(String s) {
        int balance = 0;
        
        for (char c : s.toCharArray()) {
            if (c == '(') {
                balance++;
            } else if (c == ')') {
                balance--;
                // 右括号过多，立即无效
                if (balance < 0) {
                    return false;
                }
            }
        }
        
        // 最终必须左右平衡
        return balance == 0;
    }
    
    /**
     * 测试用例
     */
    public static void main(String[] args) {
        Solution solution = new Solution();
        
        // 测试用例
        String[] testCases = {
            "()())()",      // 期望: ["()()()", "(())()"]
            "(a)())()",     // 期望: ["(a)()()", "(a())()"]
            ")(",           // 期望: [""]
            "abc",          // 期望: ["abc"]
            ""              // 期望: [""]
        };
        
        for (String testCase : testCases) {
            List<String> result = solution.removeInvalidParentheses(testCase);
            System.out.println("输入: \"" + testCase + "\"");
            System.out.println("输出: " + result);
            System.out.println("---");
        }
    }
}