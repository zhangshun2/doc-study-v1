/**
 * LeetCode 494. 目标和 - 动态规划解法
 * 
 * 问题描述：
 * 给你一个整数数组 nums 和一个整数 target。
 * 向数组中的每个整数前添加 '+' 或 '-'，然后串联起所有整数，可以构造一个表达式。
 * 返回可以通过上述方法构造的、运算结果等于 target 的不同表达式的数目。
 * 
 * 解法特点：动态规划（转换为子集和问题）
 * - 优点：时间复杂度大幅优化，空间效率高
 * - 核心思想：通过数学转换将搜索问题转化为经典的01背包问题
 * - 适用场景：数据规模较大，需要高效解决方案
 */
public class TargetSumDP {
    
    /**
     * 动态规划解法主方法
     * 
     * 核心思想 - 数学转换：
     * 1. 设正数集合的和为P，负数集合的和为N
     * 2. 则有：P - N = target，P + N = sum（数组总和）
     * 3. 解得：P = (target + sum) / 2
     * 4. 问题转换为：在数组中找到和为P的子集有多少种方法
     * 5. 这是一个经典的01背包问题变形
     * 
     * 时间复杂度：O(n * sum)，其中 n 是数组长度，sum 是数组元素和
     * 空间复杂度：O(sum)，动态规划数组的大小
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
        
        // 计算数组总和
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        // 边界条件检查
        // 1. target的绝对值不能超过sum（数学上不可能达到）
        // 2. (target + sum) 必须是偶数，否则无法整除得到整数P
        if (Math.abs(target) > sum || (target + sum) % 2 == 1) {
            return 0;
        }
        
        // 计算正数集合的目标和
        int positiveSum = (target + sum) / 2;
        
        // 调用子集和问题的解法
        return subsetSum(nums, positiveSum);
    }
    
    /**
     * 子集和问题：计算数组中和为target的子集数量
     * 
     * 这是经典的01背包问题变形：
     * - 原问题：背包容量为target，每个物品重量为nums[i]，求装满背包的方案数
     * - 状态定义：dp[i] 表示和为i的子集数量
     * - 状态转移：dp[j] += dp[j - num] （选择当前数字num）
     * 
     * @param nums 输入数组
     * @param target 目标和
     * @return 和为target的子集数量
     */
    private int subsetSum(int[] nums, int target) {
        // dp[i] 表示和为i的子集数量
        int[] dp = new int[target + 1];
        
        // 初始化：和为0的子集只有一个（空集）
        dp[0] = 1;
        
        // 遍历每个数字（外层循环）
        for (int num : nums) {
            // 从后往前更新dp数组，避免重复使用同一个数字
            // 这是01背包的经典技巧：保证每个物品只使用一次
            for (int j = target; j >= num; j--) {
                // 状态转移方程：dp[j] += dp[j - num]
                // 意思是：要组成和为j的子集，可以在和为(j-num)的子集基础上加上当前数字num
                dp[j] += dp[j - num];
            }
        }
        
        return dp[target];
    }
    
    /**
     * 带详细过程的动态规划解法（用于学习和调试）
     */
    public int findTargetSumWaysWithProcess(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return target == 0 ? 1 : 0;
        }
        
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        System.out.println("=== 动态规划求解过程 ===");
        System.out.println("数组总和 sum = " + sum);
        System.out.println("目标值 target = " + target);
        
        if (Math.abs(target) > sum || (target + sum) % 2 == 1) {
            System.out.println("边界条件检查失败，无解");
            return 0;
        }
        
        int positiveSum = (target + sum) / 2;
        System.out.println("正数集合目标和 P = (target + sum) / 2 = " + positiveSum);
        System.out.println("问题转换为：在数组中找和为 " + positiveSum + " 的子集数量");
        System.out.println();
        
        return subsetSumWithProcess(nums, positiveSum);
    }
    
    /**
     * 带详细过程的子集和问题解法
     */
    private int subsetSumWithProcess(int[] nums, int target) {
        int[] dp = new int[target + 1];
        dp[0] = 1;
        
        System.out.println("初始状态：dp[0] = 1（空集）");
        printDPArray(dp, 0);
        System.out.println();
        
        for (int i = 0; i < nums.length; i++) {
            int num = nums[i];
            System.out.println("处理数字 " + num + "：");
            
            // 记录更新前的状态
            int[] oldDp = dp.clone();
            
            for (int j = target; j >= num; j--) {
                dp[j] += dp[j - num];
            }
            
            // 显示更新过程
            System.out.println("  更新过程：");
            for (int j = target; j >= num; j--) {
                if (oldDp[j] != dp[j]) {
                    System.out.println("    dp[" + j + "] = dp[" + j + "] + dp[" + (j - num) + "] = " 
                                     + oldDp[j] + " + " + oldDp[j - num] + " = " + dp[j]);
                }
            }
            
            printDPArray(dp, i + 1);
            System.out.println();
        }
        
        return dp[target];
    }
    
    /**
     * 打印DP数组状态
     */
    private void printDPArray(int[] dp, int round) {
        System.out.print("  第" + round + "轮后：[");
        for (int i = 0; i < dp.length; i++) {
            System.out.print(dp[i]);
            if (i < dp.length - 1) System.out.print(", ");
        }
        System.out.println("]");
    }
    
    /**
     * 数学推导验证方法
     */
    public void verifyMathematicalTransformation(int[] nums, int target) {
        System.out.println("=== 数学转换验证 ===");
        System.out.println("原问题：给数组元素添加正负号，使得和等于target");
        
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        System.out.println("设正数集合和为P，负数集合和为N");
        System.out.println("约束条件：");
        System.out.println("  1. P - N = target  （目标约束）");
        System.out.println("  2. P + N = sum     （总和约束）");
        System.out.println("  其中 sum = " + sum);
        System.out.println();
        
        System.out.println("求解过程：");
        System.out.println("  由约束1：N = P - target");
        System.out.println("  代入约束2：P + (P - target) = sum");
        System.out.println("  化简：2P - target = sum");
        System.out.println("  解得：P = (sum + target) / 2");
        
        if ((sum + target) % 2 == 1) {
            System.out.println("  结果：P = (" + sum + " + " + target + ") / 2 = " + 
                             (sum + target) / 2.0 + " (非整数，无解)");
        } else {
            int P = (sum + target) / 2;
            System.out.println("  结果：P = (" + sum + " + " + target + ") / 2 = " + P);
            System.out.println();
            System.out.println("问题转换：在数组中选择子集，使得子集和等于 " + P);
            System.out.println("这是经典的01背包问题变形！");
        }
        System.out.println();
    }
    
    /**
     * 性能对比方法
     */
    public void performanceComparison(int[] nums, int target) {
        System.out.println("=== 性能分析 ===");
        
        int n = nums.length;
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        System.out.println("数组长度 n = " + n);
        System.out.println("数组元素和 sum = " + sum);
        System.out.println();
        
        System.out.println("时间复杂度对比：");
        System.out.println("  递归回溯：O(2^n) = O(2^" + n + ") = O(" + Math.pow(2, n) + ")");
        System.out.println("  动态规划：O(n * sum) = O(" + n + " * " + sum + ") = O(" + (n * sum) + ")");
        System.out.println();
        
        System.out.println("空间复杂度对比：");
        System.out.println("  递归回溯：O(n) = O(" + n + ") [递归栈深度]");
        System.out.println("  动态规划：O(sum) = O(" + sum + ") [DP数组大小]");
        System.out.println();
        
        if (Math.pow(2, n) > n * sum) {
            System.out.println("结论：动态规划在时间复杂度上有显著优势！");
        } else {
            System.out.println("结论：在当前数据规模下，两种方法性能相近");
        }
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        TargetSumDP solution = new TargetSumDP();
        
        System.out.println("=== 动态规划解法测试 ===\n");
        
        // 测试用例1：经典案例
        int[] nums1 = {1, 1, 1, 1, 1};
        int target1 = 3;
        System.out.println("测试用例1：");
        System.out.println("数组：[1,1,1,1,1]，目标值：3");
        solution.verifyMathematicalTransformation(nums1, target1);
        System.out.println("结果：" + solution.findTargetSumWaysWithProcess(nums1, target1));
        solution.performanceComparison(nums1, target1);
        System.out.println("=".repeat(50) + "\n");
        
        // 测试用例2：简单案例
        int[] nums2 = {1};
        int target2 = 1;
        System.out.println("测试用例2：");
        System.out.println("数组：[1]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums2, target2));
        solution.verifyMathematicalTransformation(nums2, target2);
        System.out.println("=".repeat(50) + "\n");
        
        // 测试用例3：包含0的案例
        int[] nums3 = {1, 0};
        int target3 = 1;
        System.out.println("测试用例3：");
        System.out.println("数组：[1,0]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums3, target3));
        solution.verifyMathematicalTransformation(nums3, target3);
        System.out.println("=".repeat(50) + "\n");
        
        // 边界情况测试
        System.out.println("=== 边界情况测试 ===");
        System.out.println("空数组，目标值0：" + solution.findTargetSumWays(new int[]{}, 0));
        System.out.println("空数组，目标值1：" + solution.findTargetSumWays(new int[]{}, 1));
        System.out.println("无解案例[1,2]，目标值4：" + solution.findTargetSumWays(new int[]{1, 2}, 4));
        System.out.println("奇偶性不匹配[1,1]，目标值1：" + solution.findTargetSumWays(new int[]{1, 1}, 1));
    }
}

/**
 * 动态规划解法学习要点总结：
 * 
 * 1. 核心思想 - 问题转换：
 *    - 原问题：给数组元素添加正负号，求和等于target的方案数
 *    - 转换后：在数组中选择子集，使子集和等于(target+sum)/2
 *    - 本质：将搜索问题转换为经典的01背包计数问题
 * 
 * 2. 数学推导过程：
 *    设正数集合和为P，负数集合和为N
 *    约束条件：P - N = target, P + N = sum
 *    求解得到：P = (target + sum) / 2
 *    问题转换为：求和为P的子集数量
 * 
 * 3. 动态规划设计：
 *    - 状态定义：dp[i] 表示和为i的子集数量
 *    - 初始状态：dp[0] = 1（空集的和为0）
 *    - 状态转移：dp[j] += dp[j - num]（选择当前数字num）
 *    - 遍历顺序：外层遍历数字，内层从大到小遍历容量
 * 
 * 4. 01背包核心技巧：
 *    - 从后往前更新：避免同一个数字被重复使用
 *    - 空间优化：使用一维数组代替二维数组
 *    - 边界处理：j >= num 确保不越界
 * 
 * 5. 边界条件处理：
 *    - |target| > sum：数学上不可能达到
 *    - (target + sum) % 2 == 1：P不是整数，无解
 *    - target == 0 且 sum == 0：特殊情况，返回1
 * 
 * 6. 时间复杂度分析：
 *    - 外层循环：O(n)，遍历所有数字
 *    - 内层循环：O(sum)，遍历所有可能的和
 *    - 总时间复杂度：O(n * sum)
 *    - 相比递归回溯的O(2^n)，有指数级的优化
 * 
 * 7. 空间复杂度分析：
 *    - DP数组大小：O(sum)
 *    - 相比递归回溯的O(n)，可能更大，但通常可接受
 *    - 可以进一步优化为滚动数组
 * 
 * 8. 优缺点分析：
 *    优点：
 *    - 时间复杂度大幅优化，适合大规模数据
 *    - 避免了重复计算，效率高
 *    - 利用了问题的数学性质
 *    
 *    缺点：
 *    - 需要额外的数学推导
 *    - 空间复杂度可能较大（当sum很大时）
 *    - 不如递归回溯直观
 * 
 * 9. 适用场景：
 *    - 数据规模较大（n > 15）
 *    - 对时间效率有要求
 *    - 数组元素和不是特别大
 *    - 生产环境中的实际应用
 * 
 * 10. 学习建议：
 *     - 理解问题转换的数学推导过程
 *     - 掌握01背包问题的经典解法
 *     - 理解为什么要从后往前更新
 *     - 练习边界条件的处理
 *     - 对比不同解法的优缺点
 */