public class temp {
    public List<String> gc(int n){
	
	List<String> result = new ArrayList<>();
	StringBuilder path = new StringBuilder();
	bc(n , 0,0 , path , result);
	return result;
}

private void bc(int n , int left , int right , StringBuilder path , List<String> result){
	
	if(2n == path.length()){
		result.add(path.toString());
	}
	// 添加左括号;
	if(left < n){
		path.append('(');
		// right>left,继续添加左括号;
		bc(n,left,right+1,path,result);
		path.deleteCharAt(path.length()-1);
	}
	// 添加右括号
	if(right < left){
		path.append(')');
		// 需要添加右括号了
		bc(n,left+1,right,path,result);
		path.deleteCharAt(path.length()-1);
	}
}
}
