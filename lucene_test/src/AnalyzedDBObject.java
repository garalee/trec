

public class AnalyzedDBObject extends BasicDBObject{
	public static enum Condition {ALL,IN}
	private Analyzer analyzer;
	
	public AnalyzeredDBObject(Analyzer analyzer){
		this.analyzer = analyzer;
	}
}
