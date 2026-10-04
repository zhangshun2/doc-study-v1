/**
 * LeetCode 494. 目标和 - 记忆化递归解法
 * 
 * 问题描述：
 * 给你一个整数数组 nums 和一个整数 target。
 * 向数组中的每个整数前添加 '+' 或 '-'，然后串联起所有整数，可以构造一个表达式。
 * 返回可以通过上述方法构造的、运算结果等于 target 的不同表达式的数目。
 * 
 * 解法特点：记忆化递归（优化的回溯）
 * - 优点：保持递归思路的直观性，同时避免重复计算
 * - 核心思想：在递归回溯基础上添加缓存机制
 * - 适用场景：既要保持代码可读性，又要提升性能的场合
 */
public class TargetSumMemo {
    
    /**
     * 记忆化递归解法主方法
     * 
     * 核心思想：
     * 1. 保持递归回溯的基本结构和思路
     * 2. 使用HashMap存储已经计算过的状态，避免重复计算
     * 3. 状态定义：(index, currentSum) -> 方案数
     * 4. 每次递归前先查缓存，递归后将结果存入缓存
     * 
     * 时间复杂度：O(n * sum)，每个状态只计算一次
     * 空间复杂度：O(n * sum)，记忆化存储的空间 + O(n)递归栈
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
        
        // 使用HashMap进行记忆化，key为"index,sum"的字符串形式
        java.util.Map<String, Integer> memo = new java.util.HashMap<>();
        return backtrackWithMemo(nums, 0, 0, target, memo);
    }
    
    /**
     * 带记忆化的递归回溯方法
     * 
     * 记忆化的关键点：
     * 1. 状态表示：用字符串"index,currentSum"作为key
     * 2. 查询缓存：递归前先检查是否已计算过
     * 3. 存储结果：递归后将结果存入缓存
     * 4. 返回结果：直接返回缓存中的值或新计算的值
     * 
     * @param nums 输入数组
     * @param index 当前处理的数组索引
     * @param currentSum 当前累计的和
     * @param target 目标值
     * @param memo 记忆化缓存
     * @return 从当前状态开始能够达到目标值的方案数
     */
    private int backtrackWithMemo(int[] nums, int index, int currentSum, int target, 
                                  java.util.Map<String, Integer> memo) {
        // 递归终止条件
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        // 构造当前状态的key
        String key = index + "," + currentSum;
        
        // 如果已经计算过这个状态，直接返回结果
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
        
        // 递归计算两种选择的方案数
        // 选择1：给当前数字添加正号
        int positiveCount = backtrackWithMemo(nums, index + 1, currentSum + nums[index], target, memo);
        
        // 选择2：给当前数字添加负号
        int negativeCount = backtrackWithMemo(nums, index + 1, currentSum - nums[index], target, memo);
        
        // 计算总方案数
        int totalCount = positiveCount + negativeCount;
        
        // 将结果存入记忆化表
        memo.put(key, totalCount);
        
        return totalCount;
    }
    
    /**
     * 使用二维数组进行记忆化的版本（空间优化）
     * 
     * 优化思路：
     * 1. 预先计算sum的范围，使用二维数组代替HashMap
     * 2. 将currentSum偏移到非负范围：currentSum + offset
     * 3. 使用-1表示未计算状态，避免额外的标记数组
     */
    public int findTargetSumWaysArray(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return target == 0 ? 1 : 0;
        }
        
        // 计算sum的范围：[-sum, sum]
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        // 边界检查
        if (Math.abs(target) > sum) {
            return 0;
        }
        
        // 创建记忆化数组：memo[index][currentSum + sum]
        // currentSum的范围是[-sum, sum]，偏移sum后变为[0, 2*sum]
        int[][] memo = new int[nums.length][2 * sum + 1];
        
        // 初始化为-1，表示未计算
        for (int i = 0; i < nums.length; i++) {
            java.util.Arrays.fill(memo[i], -1);
        }
        
        return backtrackWithArray(nums, 0, 0, target, memo, sum);
    }
    
    /**
     * 使用二维数组的记忆化递归方法
     */
    private int backtrackWithArray(int[] nums, int index, int currentSum, int target, 
                                   int[][] memo, int offset) {
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        // 将currentSum偏移到非负范围
        int memoIndex = currentSum + offset;
        
        // 检查是否已计算过
        if (memo[index][memoIndex] != -1) {
            return memo[index][memoIndex];
        }
        
        // 递归计算
        int positiveCount = backtrackWithArray(nums, index + 1, currentSum + nums[index], target, memo, offset);
        int negativeCount = backtrackWithArray(nums, index + 1, currentSum - nums[index], target, memo, offset);
        
        // 存储结果
        memo[index][memoIndex] = positiveCount + negativeCount;
        
        return memo[index][memoIndex];
    }
    
    /**
     * 带详细过程的记忆化递归（用于学习和调试）
     */
    public int findTargetSumWaysWithProcess(int[] nums, int target) {
        if (nums == null || nums.length == 0) {
            return target == 0 ? 1 : 0;
        }
        
        System.out.println("=== 记忆化递归求解过程 ===");
        
        // 使用特殊的Map来跟踪访问过程
        java.util.Map<String, Integer> memo = new java.util.LinkedHashMap<>();
        int[] hitCount = {0}; // 缓存命中次数
        int[] missCount = {0}; // 缓存未命中次数
        
        int result = backtrackWithProcess(nums, 0, 0, target, memo, hitCount, missCount, 0);
        
        System.out.println("\n=== 记忆化统计 ===");
        System.out.println("缓存命中次数：" + hitCount[0]);
        System.out.println("缓存未命中次数：" + missCount[0]);
        System.out.println("总计算次数：" + (hitCount[0] + missCount[0]));
        System.out.println("缓存命中率：" + String.format("%.2f%%", hitCount[0] * 100.0 / (hitCount[0] + missCount[0])));
        System.out.println("缓存大小：" + memo.size());
        
        return result;
    }
    
    /**
     * 带过程跟踪的记忆化递归方法
     */
    private int backtrackWithProcess(int[] nums, int index, int currentSum, int target, 
                                     java.util.Map<String, Integer> memo, int[] hitCount, int[] missCount, int depth) {
        String indent = "  ".repeat(depth);
        String key = index + "," + currentSum;
        
        System.out.println(indent + "调用 backtrack(" + index + ", " + currentSum + ")");
        
        if (index == nums.length) {
            boolean isTarget = currentSum == target;
            System.out.println(indent + "  终止条件：" + currentSum + (isTarget ? " == " : " != ") + target + 
                             " -> 返回 " + (isTarget ? 1 : 0));
            return isTarget ? 1 : 0;
        }
        
        if (memo.containsKey(key)) {
            hitCount[0]++;
            int cachedResult = memo.get(key);
            System.out.println(indent + "  缓存命中！返回 " + cachedResult);
            return cachedResult;
        }
        
        missCount[0]++;
        System.out.println(indent + "  缓存未命中，开始计算...");
        
        int positiveCount = backtrackWithProcess(nums, index + 1, currentSum + nums[index], target, memo, hitCount, missCount, depth + 1);
        int negativeCount = backtrackWithProcess(nums, index + 1, currentSum - nums[index], target, memo, hitCount, missCount, depth + 1);
        
        int totalCount = positiveCount + negativeCount;
        memo.put(key, totalCount);
        
        System.out.println(indent + "  计算完成：" + positiveCount + " + " + negativeCount + " = " + totalCount);
        System.out.println(indent + "  存入缓存：(" + key + ") -> " + totalCount);
        
        return totalCount;
    }
    
    /**
     * 性能对比分析方法
     */
    public void performanceAnalysis(int[] nums, int target) {
        System.out.println("=== 性能分析 ===");
        
        int n = nums.length;
        int sum = 0;
        for (int num : nums) {
            sum += num;
        }
        
        System.out.println("数组长度 n = " + n);
        System.out.println("可能的currentSum范围：[" + (-sum) + ", " + sum + "]");
        System.out.println("状态空间大小：n × (2×sum + 1) = " + n + " × " + (2 * sum + 1) + " = " + (n * (2 * sum + 1)));
        System.out.println();
        
        System.out.println("时间复杂度分析：");
        System.out.println("  无记忆化：O(2^n) = O(2^" + n + ") = O(" + (int)Math.pow(2, n) + ")");
        System.out.println("  有记忆化：O(n × sum) = O(" + n + " × " + sum + ") = O(" + (n * sum) + ")");
        System.out.println("  优化倍数：" + String.format("%.2f", Math.pow(2, n) / (double)(n * sum)) + " 倍");
        System.out.println();
        
        System.out.println("空间复杂度分析：");
        System.out.println("  HashMap版本：O(n × sum) = O(" + (n * sum) + ") [缓存] + O(n) [递归栈]");
        System.out.println("  数组版本：O(n × sum) = O(" + (n * (2 * sum + 1)) + ") [固定数组]");
        System.out.println();
    }
    
    /**
     * 缓存效果演示方法
     */
    public void demonstrateCacheEffect(int[] nums, int target) {
        System.out.println("=== 缓存效果演示 ===");
        
        // 模拟无缓存的调用次数
        int[] callCountWithoutCache = {0};
        simulateWithoutCache(nums, 0, 0, target, callCountWithoutCache);
        
        // 实际有缓存的调用
        java.util.Map<String, Integer> memo = new java.util.HashMap<>();
        int[] callCountWithCache = {0};
        backtrackWithCount(nums, 0, 0, target, memo, callCountWithCache);
        
        System.out.println("无缓存调用次数：" + callCountWithoutCache[0]);
        System.out.println("有缓存调用次数：" + callCountWithCache[0]);
        System.out.println("缓存节省的调用次数：" + (callCountWithoutCache[0] - callCountWithCache[0]));
        System.out.println("效率提升：" + String.format("%.2f%%", 
                         (callCountWithoutCache[0] - callCountWithCache[0]) * 100.0 / callCountWithoutCache[0]));
    }
    
    /**
     * 模拟无缓存的递归调用次数
     */
    private int simulateWithoutCache(int[] nums, int index, int currentSum, int target, int[] callCount) {
        callCount[0]++;
        
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        int positiveCount = simulateWithoutCache(nums, index + 1, currentSum + nums[index], target, callCount);
        int negativeCount = simulateWithoutCache(nums, index + 1, currentSum - nums[index], target, callCount);
        
        return positiveCount + negativeCount;
    }
    
    /**
     * 带计数的记忆化递归
     */
    private int backtrackWithCount(int[] nums, int index, int currentSum, int target, 
                                   java.util.Map<String, Integer> memo, int[] callCount) {
        callCount[0]++;
        
        if (index == nums.length) {
            return currentSum == target ? 1 : 0;
        }
        
        String key = index + "," + currentSum;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
        
        int positiveCount = backtrackWithCount(nums, index + 1, currentSum + nums[index], target, memo, callCount);
        int negativeCount = backtrackWithCount(nums, index + 1, currentSum - nums[index], target, memo, callCount);
        
        int totalCount = positiveCount + negativeCount;
        memo.put(key, totalCount);
        
        return totalCount;
    }
    
    /**
     * 测试方法
     */
    public static void main(String[] args) {
        TargetSumMemo solution = new TargetSumMemo();
        
        System.out.println("=== 记忆化递归解法测试 ===\n");
        
        // 测试用例1：经典案例
        int[] nums1 = {1, 1, 1, 1, 1};
        int target1 = 3;
        System.out.println("测试用例1：");
        System.out.println("数组：[1,1,1,1,1]，目标值：3");
        System.out.println("HashMap版本结果：" + solution.findTargetSumWays(nums1, target1));
        System.out.println("数组版本结果：" + solution.findTargetSumWaysArray(nums1, target1));
        System.out.println();
        
        solution.performanceAnalysis(nums1, target1);
        solution.demonstrateCacheEffect(nums1, target1);
        System.out.println();
        
        System.out.println("详细求解过程：");
        solution.findTargetSumWaysWithProcess(nums1, target1);
        System.out.println("=".repeat(60) + "\n");
        
        // 测试用例2：简单案例
        int[] nums2 = {1};
        int target2 = 1;
        System.out.println("测试用例2：");
        System.out.println("数组：[1]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums2, target2));
        System.out.println("=".repeat(60) + "\n");
        
        // 测试用例3：包含0的案例
        int[] nums3 = {1, 0};
        int target3 = 1;
        System.out.println("测试用例3：");
        System.out.println("数组：[1,0]，目标值：1");
        System.out.println("结果：" + solution.findTargetSumWays(nums3, target3));
        System.out.println("=".repeat(60) + "\n");
        
        // 边界情况测试
        System.out.println("=== 边界情况测试 ===");
        System.out.println("空数组，目标值0：" + solution.findTargetSumWays(new int[]{}, 0));
        System.out.println("空数组，目标值1：" + solution.findTargetSumWays(new int[]{}, 1));
        System.out.println("大范围测试[1,1,1,1,1,1]，目标值0：" + solution.findTargetSumWays(new int[]{1,1,1,1,1,1}, 0));
    }
}

/**
 * 记忆化递归解法学习要点总结：
 * 
 * 1. 核心思想 - 缓存优化：
 *    - 保持递归回溯的基本结构和直观性
 *    - 添加缓存机制避免重复计算相同的子问题
 *    - 状态定义：(index, currentSum) -> 方案数
 *    - 实现方式：HashMap或二维数组
 * 
 * 2. 记忆化的关键要素：
 *    - 状态表示：如何唯一标识一个子问题
 *    - 缓存查询：递归前检查是否已计算过
 *    - 结果存储：递归后将结果存入缓存
 *    - 缓存命中：直接返回已计算的结果
 * 
 * 3. 状态空间分析：
 *    - index范围：[0, n]，共n+1个值
 *    - currentSum范围：[-sum, sum]，共2×sum+1个值
 *    - 总状态数：(n+1) × (2×sum+1)
 *    - 每个状态最多计算一次
 * 
 * 4. 实现方式对比：
 *    HashMap版本：
 *    - 优点：实现简单，空间按需分配
 *    - 缺点：字符串key有额外开销，哈希计算耗时
 *    
 *    二维数组版本：
 *    - 优点：访问速度快，无哈希开销
 *    - 缺点：需要预分配全部空间，可能浪费内存
 * 
 * 5. 时间复杂度分析：
 *    - 无记忆化：O(2^n)，指数级增长
 *    - 有记忆化：O(n × sum)，每个状态计算一次
 *    - 优化效果：从指数级降到多项式级
 *    - 实际提升：通常有几十到几千倍的性能提升
 * 
 * 6. 空间复杂度分析：
 *    - 缓存空间：O(n × sum)，存储所有可能的状态
 *    - 递归栈：O(n)，最大递归深度
 *    - 总空间：O(n × sum) + O(n) = O(n × sum)
 * 
 * 7. 与其他解法的对比：
 *    vs 递归回溯：
 *    - 保持了代码的直观性和可读性
 *    - 大幅提升了时间效率
 *    - 增加了空间开销
 *    
 *    vs 动态规划：
 *    - 时间复杂度相同
 *    - 空间复杂度可能稍大（递归栈）
 *    - 代码更直观，更容易理解
 * 
 * 8. 优缺点分析：
 *    优点：
 *    - 保持递归思路的直观性
 *    - 避免重复计算，效率高
 *    - 实现相对简单
 *    - 便于调试和理解
 *    
 *    缺点：
 *    - 空间开销较大
 *    - 递归调用有额外开销
 *    - 可能存在栈溢出风险（深度过大时）
 * 
 * 9. 适用场景：
 *    - 需要保持代码可读性的场合
 *    - 递归结构比较自然的问题
 *    - 状态空间不是特别大的情况
 *    - 教学和学习动态规划的过渡阶段
 * 
 * 10. 学习建议：
 *     - 理解记忆化的基本原理和实现方法
 *     - 掌握状态的定义和表示方法
 *     - 分析缓存的命中率和效果
 *     - 对比不同实现方式的优缺点
 *     - 理解记忆化递归与动态规划的关系
 *     - 练习将递归回溯改造为记忆化递归
 */