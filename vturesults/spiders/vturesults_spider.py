from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dragger import textify
import MySQLdb

class vturesultsSpider(BaseSpider):
    name = "vturesults"
    allowed_domains = ["http://results.vtu.ac.in/vitavi.php"]
    #usn=raw_input("enter the usn")
    start_urls =[]
    usn_list=['1DS10IS400','1DS10IS401','1DS10IS402','1DS10IS403','1DS10IS404','1DS10IS405','1DS10IS406','1DS10IS407','1DS10IS408',
              '1DS10IS410','1DS10IS411','1DS10IS412','1DS10IS413','1DS10IS414','1DS10IS415','1DS10IS416','1DS10IS417','1DS10IS418',
	      '1DS10IS419','1DS10IS420','1DS10IS421','1DS10IS422','1DS10IS423','1DS10IS424','1DS10IS425','1DS10IS426','1DS09IS001',
              '1DS09IS002','1DS09IS003','1DS09IS004','1DS09IS005','1DS09IS006','1DS09IS007','1DS09IS008','1DS09IS009','1DS09IS010',
	      '1DS09IS011','1DS09IS012','1DS09IS013','1DS09IS014','1DS09IS016','1DS09IS017','1DS09IS018','1DS09IS019','1DS09IS021',
	      '1DS09IS022','1DS09IS024','1DS09IS026','1DS09IS027','1DS09IS028','1DS09IS029','1DS09IS030','1DS09IS031','1DS09IS032',
	      '1DS09IS033','1DS09IS034','1DS09IS035','1DS09IS036','1DS09IS037','1DS09IS038','1DS09IS039','1DS09IS040','1DS07IS123',
	      '1DS09IS105','1DS09IS041','1DS09IS042','1DS09IS043','1DS09IS044','1DS09IS045','1DS09IS046','1DS09IS047','1DS09IS048',
	      '1DS09IS049','1DS09IS050','1DS09IS051','1DS09IS052','1DS09IS053','1DS09IS054','1DS09IS055','1DS09IS056','1DS09IS057',                 '1DS09IS059','1DS09IS060','1DS09IS061','1DS09IS062','1DS09IS063','1DS09IS064','1DS09IS065','1DS09IS066','1DS09IS067',
	      '1DS09IS068','1DS09IS069','1DS09IS070','1DS09IS071','1DS09IS072','1DS09IS073','1DS09IS074','1DS09IS075','1DS09IS076',
	      '1DS09IS077','1DS09IS078','1DS09IS079','1DS09IS080','1DS09IS081','1DS09IS082','1DS09IS083','1DS09IS084','1DS09IS085',
	      '1DS09IS086','1DS09IS087','1DS09IS088','1DS09IS089','1DS09IS090','1DS09IS091','1DS09IS092','1DS09IS093','1DS09IS094',
	      '1DS09IS096','1DS09IS097','1DS09IS098','1DS09IS100','1DS09IS101','1DS09IS102','1DS09IS103','1DS09IS400','1DS09IS412',
	      '1DS09IS413','1DS09IS414','1DS08IS055','1DS08IS129','1DS07IS026','1DS07IS098','1DS06IS083','1DS06IS130','1DS08IS013']
    for usn in usn_list:
    	start_urls.append("http://results.vtu.ac.in/vitavi.php?submit=true&rid=%s"%(usn))

    def parse(self, response):
	db = MySQLdb.connect("localhost","root","root","beta")
    	cursor = db.cursor()
	cursor2 = db.cursor()
        hdc = HtmlXPathSelector(response)
        student_name = hdc.select("//td[@width='513']/b/text()")
 	sem = hdc.select("//td[@width='513']/table/tr/td[2]/b/text()")       
	class_award = hdc.select("//td[@width=513]/table/tr/td[4]/b/text()")
	grand_total = textify(hdc.select("//td[@width='513']/table[3]/tr/td[4]/text()"))
	sub_list=hdc.select("//td[@width='513']/table[2]/tr[position()>1]")
	if grand_total==None:
		#grand_total = textify(hdc.select("//td[@width='513']/table[5]/tr/td[4]/text()"))
		 grand_total = textify(hdc.select("//td[contains(text(),'Total Marks:')]/following-sibling::*/text()"))
	grand_total = int(grand_total)
	if grand_total<100:
		grand_total = 0 
#	marks_list=hdc.select("//td[@width='60']")
	#sem_student = hdc.select("//td[@width='513']/table/tbody/tr//td")
       # for details in sem_student:
	name = textify(student_name)
	#print name
	sem = textify(sem)
	#print sem
	class_award = textify(class_award)
	#print class_award
        #print grand_total	
	sql = "insert into raw_result values('%s', '%s', '%s', '%d')"%(name,sem,class_award,grand_total)
	cursor.execute(sql)
	db.commit()
	i = 1
	for each in sub_list:
	#	print "subject", textify(each.select('./td[1]/i/text()')), "external", textify(each.select('./td[2]/text()')), "internal", textify(each.select('./td[3]/text()')), "total", textify(each.select('./td[4]/text()')),  "result", textify(each.select('./td[5]/b/text()'))
		subject = textify(each.select('./td[1]/i/text()'))
		ext_marks = int(textify(each.select('./td[2]/text()')))
		int_marks = int(textify(each.select('./td[3]/text()')))
		total_marks = int(textify(each.select('./td[4]/text()')))
		result = textify(each.select('./td[5]/b/text()'))
		sql = "insert into sub%d values('%s','%s','%d','%d','%d','%s')"%(i,name, subject, ext_marks, int_marks, total_marks, result)
		cursor2.execute(sql)
		db.commit()
		i = i+1
	db.close()
