

public class 复习1 {
    public List<List<Integer>> subSets(int[] nums){

        List<List<Integer>> result = new ArrayList<>();
        List<Integer> path = new ArrayList<>();

        hs(nums,result,path,0);

        return path;
    }

    // 方法
    // 入参 -> 结果集
    // 二者中间的过程参数
    // 因为查询的是自己问题
    // 而且是借助递归回溯遍历的全路径
    // 追加 List<path>
    // 没有任何额外指定,单纯借助起始坐标遍历就好 int start
    // 方法(原始数组,结果集,过程集合,先后回溯因子)


    public void hs(int[] nums , List<List<Integer>> result List<Integer> path , int start){
        // 添加path的每一层
        result.add(new ArrayList(path));
        for(int i=start;i<nums.length;i++){
            path.add(nums[i]);
            hs(nums,result,path,i+1);
            path.remove(path.size()-1);
        }
    }
}