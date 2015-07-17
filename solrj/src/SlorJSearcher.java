import org.apache.solr.client.solrj.SolrServerException;
import org.apache.solr.client.solrj.impl.HttpSolrServer;
import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.response.QueryResponse;
import org.apache.solr.common.SolrDocumentList;

import java.net.MalformedURLException;


public class SlorJSearcher {
	public static void main(String[] args) throws MalformedURLException, SolrServerException{
		HttpSolrServer solr = new HttpSolrServer("http://localhost:8983/solr");
	
	}

}
