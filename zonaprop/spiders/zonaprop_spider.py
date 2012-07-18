from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from zonaprop.items import ZonapropItem

class ZonapropSpider(BaseSpider):
	name = "zonaprop.com.ar"
	allowed_domains = ["zonaprop.com.ar"]
	start_urls = [
		"http://propiedades.zonaprop.com.ar/alquiler-departamentos-capital-federal-san-nicolas/ncZ1_opZtipo-operacion-alquiler_lnZ3646_currencyTypeZarsCurrencyType_soZlsasc"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		links = hxs.select('//a[@class="sharesocialnetworks"]')
		items = []
		for link in links:
			item = ZonapropItem()
			item['link'] = link.select('@href').extract()
			items.append(item)
		return items
