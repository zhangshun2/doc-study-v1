class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> result = new ArrayList<>();
        hs(candidates,result,new ArrayList<>(), target,0);
        return result;
    }

    public void hs(int[] nums,List<List<Integer>> result,List<Integer> path , 
        int target , int index){
        if(0 == target){
            result.add(new ArrayList(path));
            return;
        }

        for(int i = index;i<nums.length;i++){
            if(nums[i] > target){
                continue;
            }
            path.add(nums[i]);
            hs(nums,result,path,target-nums[i]  , i);
            path.remove(path.size()-1);
        }
    }
}