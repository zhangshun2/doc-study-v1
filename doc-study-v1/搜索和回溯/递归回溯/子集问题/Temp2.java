package 搜索和回溯.递归回溯.子集问题;

import java.util.ArrayList;
import java.util.List;

public class Temp2 {
    
    // public List<List<Integer>> subsets(int[] nums) {
    //     List<List<Integer>> res = new ArrayList<>();
    //     List<Integer> path = new ArrayList<>();
    //     backtrack(nums, 0, path, res);
    //     return res;
    // }

    // public void backtrack(int[] nums, int start, List<Integer> track, List<List<Integer>> res) {
    //     res.add(new ArrayList<>(track));
    //     for (int i = start; i < nums.length; i++) {
    //         track.add(nums[i]);
    //         backtrack(nums, i + 1, track, res);
    //         track.remove(track.size() - 1);
    //     }
    // }
    
    // 照着敲一遍,不要AI提示我了这会儿
    public List<List<Integer>> subsets(int[] nums) {
       List<List<Integer>> result = new ArrayList<>();
       List<Integer> path = new ArrayList<>();
       bt(nums , 0,path,result);
       return result;
    }

    public void bt(int[] nums, int start, List<Integer> path , List<List<Integer>> result){
        result.add(new ArrayList<>(path)); // 这个比较难记忆,因为很少这么add来着,但是可以避开引用传递
        for(int i = start;i<nums.length;i++){
            path.add(nums[i]);
            bt(nums,start+1,path,result);
            path.remove(path.size()-1);
        }
    }
}
