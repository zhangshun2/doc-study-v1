/**
 * LeetCode 494. 目标和 - 递归回溯解法
 * 
 * 问题描述：
 * 给你一个整数数组 nums 和一个整数 target。
 * 向数组中的每个整数前添加 '+' 或 '-'，然后串联起所有整数，可以构造一个表达式。
 * 返回可以通过上述方法构造的、运算结果等于 target 的不同表达式的数目。
 * 
 * 解法特点：递归回溯（暴力搜索）
 * - 优点：思路直观，容易理解和实现
 * - 缺点：时间复杂度高，存在大量重复计算
 * - 适用场景：数据规模较小，或者需要理解问题本质时使用
 */
public class TargetSumBacktrack {
    
    /**
     * 递归回溯解法主方法
     * 
     * 核心思想：
     * 1. 对于数组中的每个数字，我们有两种选择：加上它或减去它
     * 2. 使用递归的方式遍历所有可能的组合
     * 3. 当遍历完所有数字时，检查当前和是否等于目标值
     * 4. 如果等于目标值，则方案数加1
     * 
     * 时间复杂度：O(2^n)，其中 n 是数组长度，每个数字有两种选择
     * 空间复杂度：O(n)，递归调用栈的深度
     * 
     * @param nums 输入的整数数组
     * @param target 目标和
     * @return 能够达到目标和的表达式数目
     */
    public int findTargetSumWays(int[] nums, int target) {
        // 参数验证
        if (nums == null || nums.length == 0) {
            return target == 0 ? 1 : 0;
        }
        
        // 调用递归回溯方法
        return backtrack(nums, 0, 0, target);
    }
    
    /**
     * 递归回溯的核心方法
     * 
     * 递归三要素：
     * 1. 递归参数：当前处理的索引、当前累计和、目标值
     * 2. 递归终止条件：处理完所有数字
     * 3. 递归过程：对当前数字选择加号或减号
     * 
     * @param nums 输入数组
     * @param index 当前处理的数组索引
     * @param currentSum 当前累计的和
     * @param target 目标值
     * @return 从当前状态开始能够达到目标值的方案数
     */
    private int backtrack(int[] nums, int index, int currentSum, int target) {
        // 递归终止条件：已经处理完所有数字
        if (index == nums.length) {
            // 如果当前和等于目标值，返回1（找到一种方案），否则返回0
            return currentSum == target ? 1 : 0;
        }
        
        // 递归处理：对当前数字有两种选择
        
        // 选择1：给当前数字添加正号
        // 递归到下一层：index+1, currentSum+nums[index]
        int positiveCount = backtrack(nums, index + 1, currentSum + nums[index], target);
        
        // 选择2：给当前数字添加负号  
        // 递归到下一层：index+1, currentSum-nums[index]
        int negativeCount = backtrack(nums, index + 1, currentSum - nums[index], target);
        
        // 返回两种选择的方案数之和
        return positiveCount + negativeCount;
    }
    
    /**
     * 辅助方法：打印所有可能的表达式（用于调试和理解）
     * 
     * @param nums 输入数组
     * @param target 目标值
     */
    public void printAllExpressions(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            System.out.println("数组为空");
            return;
        }
        
        System.out.println("所有可能的表达式：");
        java.util.List<String> expressions = new java.util.ArrayList<>();
        collectExpressions(nums, 0, 0, target, "", expressions);
        
        System.out.println("总共找到 " + expressions.size() + " 种表达式：");
        for (int i = 0; i < expressions.size(); i++) {
            System.out.println((i + 1) + ". " + expressions.get(i));
        }
    }
    
    /**
     * 收集所有有效表达式的递归方法
     */
    private void collectExpressions(int[] nums, int index, int currentSum, int target, 
                                   String expression, java.util.List<String> expressions) {
        if (index == nums.length) {
            if (currentSum == target) {
                expressions.add(expression + " = " + target);
            }
            return;
        }
        
        // 选择正号
        String positiveExpr = expression + (index == 0 ? "+" : " + ") + nums[index];
        collectExpressions(nums, index + 1, currentSum + nums[index], target, positiveExpr, expressions);
        
        // 选择负号
        String negativeExpr = expression + (index == 0 ? "-" : " - ") + nums[index];
        collectExpressions(nums, index + 1, currentSum - nums[index], target, negativeExpr, expressions);
    }
    
    /**
     * 性能分析方法：统计递归调用次数
     */
    public int findTargetSumWaysWithCount(int[] nums, int target) {
        int[] callCount = {0}; // 使用数组来在递归中传递引用
        int result = backtrackWithCount(nums, 0, 0, target, callCount);
        System.out.println("递归调用总次数：" + callCount[0]);
        System.out.println("时间复杂度验证：2^" + nums.length + " = " + Math.pow(2, nums.length));
        return result;
    }
    
    /**
     * 带计数的递归回溯方法
     */
    private int backtrackWithCount(int[] nums, int index, int currentSum, int target, int[] callCount) {
        callCount[0]++; // 每次调用计数加1
        
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        int positiveCount = backtrackWithCount(nums, index + 1, currentSum + nums[index], target, callCount);
        int negativeCount = backtrackWithCount(nums, index + 1, currentSum - nums[index], target, callCount);
        
        return positiveCount + negativeCount;
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        TargetSumBacktrack solution = new TargetSumBacktrack();
        
        System.out.println("=== 递归回溯解法测试 ===\n");
        
        // 测试用例1：经典案例
        int[] nums1 = {1, 1, 1, 1, 1};
        int target1 = 3;
        System.out.println("测试用例1：");
        System.out.println("数组：[1,1,1,1,1]，目标值：3");
        System.out.println("结果：" + solution.findTargetSumWays(nums1, target1));
        solution.printAllExpressions(nums1, target1);
        System.out.println();
        
        // 测试用例2：简单案例
        int[] nums2 = {1};
        int target2 = 1;
        System.out.println("测试用例2：");
        System.out.println("数组：[1]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums2, target2));
        solution.printAllExpressions(nums2, target2);
        System.out.println();
        
        // 测试用例3：包含0的案例
        int[] nums3 = {1, 0};
        int target3 = 1;
        System.out.println("测试用例3：");
        System.out.println("数组：[1,0]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums3, target3));
        solution.printAllExpressions(nums3, target3);
        System.out.println();
        
        // 性能分析
        System.out.println("=== 性能分析 ===");
        System.out.println("测试用例1的递归调用分析：");
        solution.findTargetSumWaysWithCount(nums1, target1);
        System.out.println();
        
        // 边界情况测试
        System.out.println("=== 边界情况测试 ===");
        System.out.println("空数组，目标值0：" + solution.findTargetSumWays(new int[]{}, 0));
        System.out.println("空数组，目标值1：" + solution.findTargetSumWays(new int[]{}, 1));
        System.out.println("单个元素[5]，目标值5：" + solution.findTargetSumWays(new int[]{5}, 5));
        System.out.println("单个元素[5]，目标值-5：" + solution.findTargetSumWays(new int[]{5}, -5));
    }
}

/**
 * 递归回溯解法学习要点总结：
 * 
 * 1. 算法思想：
 *    - 暴力搜索：遍历所有可能的符号组合
 *    - 递归结构：每个数字有两种选择（正号或负号）
 *    - 回溯过程：递归到底后返回，尝试另一种选择
 * 
 * 2. 递归设计要点：
 *    - 递归参数：index（当前位置）、currentSum（当前和）、target（目标值）
 *    - 终止条件：index == nums.length
 *    - 递归关系：f(index) = f(index+1, sum+nums[index]) + f(index+1, sum-nums[index])
 * 
 * 3. 时间复杂度分析：
 *    - 每个数字有2种选择，n个数字总共有2^n种组合
 *    - 每种组合需要O(1)时间判断，总时间复杂度O(2^n)
 *    - 当n较大时（如n>20），性能会急剧下降
 * 
 * 4. 空间复杂度分析：
 *    - 递归调用栈的最大深度为n（数组长度）
 *    - 每层递归需要O(1)空间，总空间复杂度O(n)
 * 
 * 5. 优缺点分析：
 *    优点：
 *    - 思路直观，容易理解和实现
 *    - 代码简洁，逻辑清晰
 *    - 便于调试和验证正确性
 *    
 *    缺点：
 *    - 时间复杂度高，存在大量重复计算
 *    - 不适合处理大规模数据
 *    - 没有利用问题的数学性质进行优化
 * 
 * 6. 适用场景：
 *    - 数据规模较小（n <= 15）
 *    - 需要理解问题本质和所有可能解
 *    - 作为其他优化算法的基础版本
 *    - 教学和学习递归回溯思想
 * 
 * 7. 学习建议：
 *    - 先理解递归的三要素（参数、终止条件、递归关系）
 *    - 画出递归树，理解搜索过程
 *    - 分析时间复杂度，理解为什么需要优化
 *    - 对比其他解法，理解各自的优缺点
 */