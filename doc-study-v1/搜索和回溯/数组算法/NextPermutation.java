/**
 * LeetCode 31. 下一个排列 - 完整Java实现
 * 
 * 问题描述：
 * 给定一个整数数组，找出这个数组的下一个字典序排列。
 * 如果不存在下一个更大的排列，则将数组重新排列成最小的排列。
 * 必须原地修改，只允许使用额外的O(1)空间。
 * 
 * 核心算法思想：
 * 1. 从右往左找第一个递减位置i (nums[i] < nums[i+1])
 * 2. 从右往左找第一个大于nums[i]的数字位置j
 * 3. 交换nums[i]和nums[j]
 * 4. 反转i+1到末尾的部分，使其变为升序
 * 
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 */
public class NextPermutation {
    
    /**
     * 标准解法：寻找下一个排列
     * 
     * 算法步骤详解：
     * 1. 寻找递减点：从右往左找第一个nums[i] < nums[i+1]的位置
     * 2. 寻找替换数：从右往左找第一个nums[j] > nums[i]的位置
     * 3. 交换元素：交换nums[i]和nums[j]
     * 4. 反转后缀：将i+1到末尾的部分反转为升序
     * 
     * @param nums 输入的整数数组
     */
    public void nextPermutation(int[] nums) {
        if (nums == null || nums.length <= 1) {
            return;
        }
        
        int n = nums.length;
        
        // 步骤1：从右往左找第一个递减位置
        int i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            i--;
        }
        
        // 步骤2：如果找到了递减位置，寻找替换数字
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) {
                j--;
            }
            // 步骤3：交换nums[i]和nums[j]
            swap(nums, i, j);
        }
        
        // 步骤4：反转i+1到末尾的部分
        reverse(nums, i + 1, n - 1);
    }
    
    /**
     * 带详细过程输出的版本（用于学习和调试）
     * 
     * @param nums 输入的整数数组
     */
    public void nextPermutationWithProcess(int[] nums) {
        if (nums == null || nums.length <= 1) {
            System.out.println("数组长度不足，无需处理");
            return;
        }
        
        System.out.println("原始数组: " + java.util.Arrays.toString(nums));
        
        int n = nums.length;
        
        // 步骤1：寻找递减点
        System.out.println("\n=== 步骤1：寻找递减点 ===");
        int i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            System.out.println("检查位置 " + i + ": nums[" + i + "]=" + nums[i] + 
                             " >= nums[" + (i+1) + "]=" + nums[i+1] + " (继续向左)");
            i--;
        }
        
        if (i >= 0) {
            System.out.println("✓ 找到递减点: 位置 " + i + ", nums[" + i + "]=" + nums[i] + 
                             " < nums[" + (i+1) + "]=" + nums[i+1]);
        } else {
            System.out.println("✗ 未找到递减点，数组为最大排列，将反转为最小排列");
        }
        
        // 步骤2：寻找替换数字
        if (i >= 0) {
            System.out.println("\n=== 步骤2：寻找替换数字 ===");
            int j = n - 1;
            while (nums[j] <= nums[i]) {
                System.out.println("检查位置 " + j + ": nums[" + j + "]=" + nums[j] + 
                                 " <= nums[" + i + "]=" + nums[i] + " (继续向左)");
                j--;
            }
            System.out.println("✓ 找到替换数字: 位置 " + j + ", nums[" + j + "]=" + nums[j] + 
                             " > nums[" + i + "]=" + nums[i]);
            
            // 步骤3：交换
            System.out.println("\n=== 步骤3：交换元素 ===");
            System.out.println("交换前: " + java.util.Arrays.toString(nums));
            swap(nums, i, j);
            System.out.println("交换后: " + java.util.Arrays.toString(nums));
        }
        
        // 步骤4：反转
        System.out.println("\n=== 步骤4：反转后续部分 ===");
        System.out.println("反转前: " + java.util.Arrays.toString(nums));
        System.out.println("反转范围: [" + (i+1) + ", " + (n-1) + "]");
        reverse(nums, i + 1, n - 1);
        System.out.println("反转后: " + java.util.Arrays.toString(nums));
        
        System.out.println("\n🎯 最终结果: " + java.util.Arrays.toString(nums));
    }
    
    /**
     * 优化版本：针对特殊情况的优化
     * 
     * @param nums 输入的整数数组
     */
    public void nextPermutationOptimized(int[] nums) {
        if (nums == null || nums.length <= 1) {
            return;
        }
        
        int n = nums.length;
        
        // 特殊情况：两个元素直接交换
        if (n == 2) {
            swap(nums, 0, 1);
            return;
        }
        
        // 寻找递减点
        int i = findDecreasingPoint(nums);
        
        if (i >= 0) {
            // 寻找替换数字
            int j = findReplacementNumber(nums, i);
            // 交换
            swap(nums, i, j);
        }
        
        // 反转后续部分
        reverse(nums, i + 1, n - 1);
    }
    
    /**
     * 寻找递减点的独立方法
     * 
     * @param nums 输入数组
     * @return 递减点的索引，如果不存在返回-1
     */
    private int findDecreasingPoint(int[] nums) {
        int i = nums.length - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            i--;
        }
        return i;
    }
    
    /**
     * 寻找替换数字的独立方法
     * 
     * @param nums 输入数组
     * @param i 需要被替换的位置
     * @return 替换数字的索引
     */
    private int findReplacementNumber(int[] nums, int i) {
        int j = nums.length - 1;
        while (nums[j] <= nums[i]) {
            j--;
        }
        return j;
    }
    
    /**
     * 交换数组中两个位置的元素
     * 
     * @param nums 数组
     * @param i 第一个位置
     * @param j 第二个位置
     */
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    /**
     * 反转数组中指定范围的元素
     * 
     * @param nums 数组
     * @param start 起始位置（包含）
     * @param end 结束位置（包含）
     */
    private void reverse(int[] nums, int start, int end) {
        while (start < end) {
            swap(nums, start, end);
            start++;
            end--;
        }
    }
    
    /**
     * 寻找上一个排列（扩展功能）
     * 
     * @param nums 输入的整数数组
     */
    public void previousPermutation(int[] nums) {
        if (nums == null || nums.length <= 1) {
            return;
        }
        
        int n = nums.length;
        
        // 从右往左找第一个递增位置
        int i = n - 2;
        while (i >= 0 && nums[i] <= nums[i + 1]) {
            i--;
        }
        
        if (i >= 0) {
            // 从右往左找第一个小于nums[i]的数
            int j = n - 1;
            while (nums[j] >= nums[i]) {
                j--;
            }
            swap(nums, i, j);
        }
        
        // 反转i+1到末尾的部分
        reverse(nums, i + 1, n - 1);
    }
    
    /**
     * 生成所有排列（用于验证算法正确性）
     * 
     * @param nums 输入数组
     * @return 所有排列的列表
     */
    public java.util.List<int[]> generateAllPermutations(int[] nums) {
        java.util.List<int[]> result = new java.util.ArrayList<>();
        int[] current = nums.clone();
        
        // 计算排列总数
        int n = nums.length;
        int totalPermutations = 1;
        for (int i = 1; i <= n; i++) {
            totalPermutations *= i;
        }
        
        // 生成所有排列
        for (int i = 0; i < totalPermutations; i++) {
            result.add(current.clone());
            nextPermutation(current);
        }
        
        return result;
    }
    
    /**
     * 验证算法正确性的方法
     * 
     * @param nums 测试数组
     */
    public void verifyAlgorithm(int[] nums) {
        System.out.println("=== 算法正确性验证 ===");
        System.out.println("输入数组: " + java.util.Arrays.toString(nums));
        
        java.util.List<int[]> allPermutations = generateAllPermutations(nums);
        
        System.out.println("所有排列按字典序：");
        for (int i = 0; i < allPermutations.size(); i++) {
            System.out.println((i + 1) + ": " + java.util.Arrays.toString(allPermutations.get(i)));
        }
        
        // 验证字典序是否正确
        boolean isCorrect = true;
        for (int i = 0; i < allPermutations.size() - 1; i++) {
            if (compareArrays(allPermutations.get(i), allPermutations.get(i + 1)) >= 0) {
                isCorrect = false;
                System.out.println("❌ 错误：排列 " + (i + 1) + " 和 " + (i + 2) + " 的顺序不正确");
                break;
            }
        }
        
        if (isCorrect) {
            System.out.println("✅ 算法验证通过：所有排列都按正确的字典序排列");
        }
    }
    
    /**
     * 比较两个数组的字典序
     * 
     * @param a 第一个数组
     * @param b 第二个数组
     * @return 负数表示a<b，0表示a=b，正数表示a>b
     */
    private int compareArrays(int[] a, int[] b) {
        int minLength = Math.min(a.length, b.length);
        for (int i = 0; i < minLength; i++) {
            if (a[i] != b[i]) {
                return a[i] - b[i];
            }
        }
        return a.length - b.length;
    }
    
    /**
     * 性能测试方法
     * 
     * @param nums 测试数组
     * @param iterations 测试次数
     */
    public void performanceTest(int[] nums, int iterations) {
        System.out.println("=== 性能测试 ===");
        System.out.println("测试数组长度: " + nums.length);
        System.out.println("测试次数: " + iterations);
        
        int[] testArray = nums.clone();
        
        long startTime = System.nanoTime();
        
        for (int i = 0; i < iterations; i++) {
            nextPermutation(testArray);
        }
        
        long endTime = System.nanoTime();
        long duration = endTime - startTime;
        
        System.out.println("总耗时: " + duration + " 纳秒");
        System.out.println("平均耗时: " + (duration / iterations) + " 纳秒/次");
        System.out.println("每秒可执行: " + String.format("%.2f", 1_000_000_000.0 / (duration / iterations)) + " 次");
    }
    
    /**
     * 主测试方法
     */
    public static void main(String[] args) {
        NextPermutation solution = new NextPermutation();
        
        System.out.println("🎯 下一个排列问题 - 完整测试");
        System.out.println("=".repeat(60));
        
        // 基础测试用例
        System.out.println("\n📋 基础测试用例");
        System.out.println("-".repeat(40));
        
        testCase(solution, new int[]{1, 2, 3}, "标准情况");
        testCase(solution, new int[]{3, 2, 1}, "最大排列");
        testCase(solution, new int[]{1, 1, 5}, "重复元素");
        testCase(solution, new int[]{1}, "单个元素");
        testCase(solution, new int[]{1, 2}, "两个元素（升序）");
        testCase(solution, new int[]{2, 1}, "两个元素（降序）");
        
        // 复杂测试用例
        System.out.println("\n🔍 复杂测试用例");
        System.out.println("-".repeat(40));
        
        testCase(solution, new int[]{1, 2, 3, 4, 5}, "五个元素");
        testCase(solution, new int[]{5, 4, 3, 2, 1}, "完全递减");
        testCase(solution, new int[]{1, 3, 2}, "部分递减");
        testCase(solution, new int[]{2, 3, 1, 4}, "混合情况");
        
        // 可视化演示
        System.out.println("\n🎨 可视化演示");
        System.out.println("-".repeat(40));
        
        int[] demo = {1, 2, 3, 4};
        System.out.println("演示数组: " + java.util.Arrays.toString(demo));
        solution.nextPermutationWithProcess(demo);
        
        // 算法验证
        System.out.println("\n✅ 算法验证");
        System.out.println("-".repeat(40));
        
        solution.verifyAlgorithm(new int[]{1, 2, 3});
        
        // 性能测试
        System.out.println("\n⚡ 性能测试");
        System.out.println("-".repeat(40));
        
        solution.performanceTest(new int[]{1, 2, 3, 4, 5}, 100000);
        
        // 边界情况测试
        System.out.println("\n🔬 边界情况测试");
        System.out.println("-".repeat(40));
        
        testCase(solution, new int[]{}, "空数组");
        testCase(solution, new int[]{0}, "单个零");
        testCase(solution, new int[]{1, 1, 1}, "全部相同");
        testCase(solution, new int[]{0, 1, 2, 5, 3, 3, 0}, "包含零的复杂情况");
        
        System.out.println("\n🎉 所有测试完成！");
    }
    
    /**
     * 测试单个用例的辅助方法
     * 
     * @param solution 解决方案实例
     * @param nums 测试数组
     * @param description 测试描述
     */
    private static void testCase(NextPermutation solution, int[] nums, String description) {
        int[] original = nums.clone();
        solution.nextPermutation(nums);
        
        System.out.println(description + ":");
        System.out.println("  输入: " + java.util.Arrays.toString(original));
        System.out.println("  输出: " + java.util.Arrays.toString(nums));
        System.out.println();
    }
}

/**
 * 下一个排列算法学习要点总结：
 * 
 * 1. 核心思想 - 字典序的下一个排列：
 *    - 寻找能够增大的最右位置（递减点）
 *    - 选择比该位置大的最小数字进行替换
 *    - 将替换后的后续部分变为最小排列（升序）
 * 
 * 2. 算法步骤的深层理解：
 *    - 步骤1：为什么从右往左找？因为要找最小的增量
 *    - 步骤2：为什么找比nums[i]大的最小数？保证增量最小
 *    - 步骤3：为什么要交换？实现位置的替换
 *    - 步骤4：为什么要反转？使后续部分变为最小排列
 * 
 * 3. 时间复杂度分析：
 *    - 寻找递减点：O(n)
 *    - 寻找替换数字：O(n)
 *    - 交换操作：O(1)
 *    - 反转操作：O(n)
 *    - 总时间复杂度：O(n)
 * 
 * 4. 空间复杂度分析：
 *    - 只使用常数个额外变量
 *    - 所有操作都是原地进行
 *    - 空间复杂度：O(1)
 * 
 * 5. 关键技巧：
 *    - 从右往左扫描：寻找关键位置的经典技巧
 *    - 双指针反转：原地反转数组片段
 *    - 贪心策略：每次选择最小的有效增量
 * 
 * 6. 边界情况处理：
 *    - 空数组或单元素数组：直接返回
 *    - 最大排列（完全递减）：反转为最小排列
 *    - 两个元素：直接交换
 * 
 * 7. 算法扩展：
 *    - 上一个排列：类似思路，寻找递增点
 *    - 第k个排列：使用阶乘数系统直接计算
 *    - 排列的字典序比较：逐位比较
 * 
 * 8. 实际应用：
 *    - 密码生成：生成下一个密码组合
 *    - 测试用例生成：系统化生成测试数据
 *    - 游戏关卡设计：生成下一个关卡配置
 * 
 * 9. 学习建议：
 *    - 理解字典序的概念和排列的顺序关系
 *    - 掌握从右往左扫描的技巧和应用场景
 *    - 练习双指针反转数组的操作
 *    - 体会贪心算法在排列问题中的应用
 *    - 通过手工模拟加深对算法步骤的理解
 * 
 * 10. 常见错误：
 *     - 忘记反转操作：只交换不反转会得到错误结果
 *     - 边界处理不当：没有正确处理最大排列的情况
 *     - 索引越界：在寻找过程中没有检查数组边界
 *     - 理解错误：混淆了"下一个排列"和"任意排列"的概念
 */