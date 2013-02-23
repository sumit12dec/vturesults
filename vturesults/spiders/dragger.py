from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import re

#def textify(exp):
#	exp=str(exp)
#       a=re.search("\'(.*)\'",exp)
#	if a==None:
#		return None
#       else:
#		return a.group(1)
def textify(exp):
	type_check = exp.extract()
	if type(exp.extract())==list:
		if len(type_check)!=0:	
			if type(type_check[0]) == unicode:
				return type_check[0].encode('ascii','ignore')
			else:
				return exp.extract()
		else:
			return
	else:
		return exp.extract()
