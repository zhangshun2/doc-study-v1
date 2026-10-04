    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        hs(n,result,new StringBuilder(),0,0);
        return result;
    }

    public void hs(int n , List<String> result , StringBuilder path , int left , int right){
        if(2 * n == path.length()){
            result.add(path.toString());
            return result;
        }
        if(left < n){
            path.add('(');
            hs(n,result,path,left+1,right);
            path.deleteCharAt(path.length()-1);
        }

        if(right < left){
            path.add(')');
            hs(n,result,path,left,right+1);
    }
