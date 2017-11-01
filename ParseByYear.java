import org.apache.commons.io.FileUtils;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.xml.sax.EntityResolver;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.util.Iterator;
import java.util.List; 

/**
 * Created by lx201 on 2017/10/25.
 * 得到每个文章的PMID、标题、摘要、mesh词和关键词
 */

public class ParseByYear {

    public static void getXf(String filename) {
        int T = 0; //对标题的数目进行计数
        int A = 0; //对摘要的数目进行计数
        
        //创建saxReader对象
        SAXReader reader = new SAXReader();
        //reader.setValidation(false);
        reader.setEntityResolver(new IgnoreDTDEntityResolver()); // ignore dtd
        
        //通过read方法读取一个文件，转化为Document对象
        try {
            Document document = reader.read(new File(filename));
            //获取根元素节点
            Element node = document.getRootElement();
            
            //取得子节点
            for (Iterator pp = node.elementIterator(); pp.hasNext(); ) {
                Element p = (Element) pp.next();
                
                if(p.element("MedlineCitation")!= null) {
                	  Element MedlineCitation = p.element("MedlineCitation");
                	  
                	  //获取每篇文章的PMID
                      Element PMID = MedlineCitation.element("PMID");
                      String pmid = PMID.getText();
                      //System.out.println(pmid);
                      
                      Element Article = MedlineCitation.element("Article");                      
                     
                      //获取文章标题
                      Element ArticleTitle = Article.element("ArticleTitle");
                      String title = ArticleTitle.getText();
                      //System.out.println(title);
                      
                      //获取出版年
                      String year = "";
                      if (Article.element("Journal") != null) {
                    	  Element Journal =Article.element("Journal");
                          Element JournalIssue = Journal.element("JournalIssue");
                          Element PubDate = JournalIssue.element("PubDate");
                          Element Year = PubDate.element("Year");
                          year = Year.getText();
                      } else {
                          year= "";
                      }
                      
                      //获取文章摘要
                      String abs = "";
                      if (Article.element("Abstract") != null) {
                          Element Abstract = Article.element("Abstract");
                          Element AbstractText = Abstract.element("AbstractText");
                          abs = AbstractText.getText();
                          //System.out.println(abs);
                      } else {
                          abs = "";
                      }
                      
                      //得到标题、摘要一起的一个文本
                      String str = title + abs ;
                      //按年份写入文件，每一篇文章写一行
                      for(int y = 0; y <= 2017; y ++) {
                    	  if(Integer.toString(y).equals(year)) {
                    		  File ff = new File("E://pubmedFiles//resultYear//result" + year + ".txt");
                              try {
                                  FileUtils.writeStringToFile(ff,  pmid + '\t' + str + '\n', true);

                              } catch (IOException e) {
                                  e.printStackTrace();
                              }
                    	  }else {
                          	continue;
                          }
                    	  
                      }
                     
                      
                }else {
                	continue;
                }       
            }

        } catch (DocumentException e) {
            e.printStackTrace();
        }
    }
    
    public static void main(String[] args) {
        File f = new File("E://pubmedFiles//XMLFiles");
        String []filename = f.list();
        //System.out.println(filename.length);
        for(String name: filename){
             String path1 = "E://pubmedFiles//XMLFiles//";
             System.out.println(path1 + name);
             getXf(path1 + name);
         }
    }
    
    /* public static void main(String[] args) {
    	System.out.println("begin");
    	getXf("F://Pubmed//pubmed-year.xml");
        System.out.println("end");

  }*/
    
    
}



