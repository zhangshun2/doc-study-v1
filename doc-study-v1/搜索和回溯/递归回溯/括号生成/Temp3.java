package 搜索和回溯.递归回溯.括号生成;

public class Temp3 {
public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        StringBuilder path = new StringBuilder();
        backtrack(n, 0, 0, path, result);
        return result;
    }
    
    private void backtrack(int n, int left, int right, StringBuilder path, List<String> result) {
        // 递归终止条件：括号序列构建完成
        if (path.length() == 2 * n) {
            result.add(path.toString());
            return;
        }
        
        // 选择1：添加左括号（条件：左括号数量 < n）
        if (left < n) {
            path.append('(');
            backtrack(n, left + 1, right, path, result);
            path.deleteCharAt(path.length() - 1);  // 回溯
        }
        
        // 选择2：添加右括号（条件：右括号数量 < 左括号数量）
        if (right < left) {
            path.append(')');
            backtrack(n, left, right + 1, path, result);
            path.deleteCharAt(path.length() - 1);  // 回溯
        }
    }
}
