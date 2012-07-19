from urllib import urlopen
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from zonaprop.items import ZonapropItem

TOTAL_MAX = 3000
M2_MIN = 40
MAILS = []
SMTPHOST = None
MAILFROM = None
SMTPUSER = None
SMTPPASS = None
SMTPPORT = None

class Mailer(object):
	instance = None
	def __new__(cls, *args, **kargs): 
		if cls.instance is None:
			from scrapy.mail import MailSender
			cls.instance = MailSender(
				smtphost=SMTPHOST,
				mailfrom=MAILFROM,
				smtpuser=SMTPUSER,
				smtppass=SMTPPASS,
				smtpport=SMTPPORT
			)
		return cls.instance


class ZonapropSpider(BaseSpider):
	name = "zonaprop.com.ar"
	allowed_domains = ["zonaprop.com.ar"]
	start_urls = [
		"http://propiedades.zonaprop.com.ar/alquiler-departamentos-capital-federal-san-nicolas/ncZ1_opZtipo-operacion-alquiler_lnZ3646_currencyTypeZarsCurrencyType_soZlsasc"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		links = hxs.select('//a[@class="sharesocialnetworks"]/@href').extract()
		items = []
		for link in links:
			hxs = HtmlXPathSelector(text=urlopen(link).read())
			precio = hxs.select('//p[@class="h2"][contains(text(), "$ ")]/text()').extract()[0].replace('$', '').replace(',', '').strip()
			expensas = hxs.select('//dt[contains(text(), "Expensas")]/following-sibling::dd[1]/text()').extract()[0]
			m2 = hxs.select('//dt[contains(text(), "Superficie cubierta")]/following-sibling::dd[1]/text()').extract()[0]
			total = int(precio)
			if expensas.isdigit():
				total = total + int(expensas)
			if (m2.isdigit() and int(m2) >= M2_MIN) and total <= TOTAL_MAX:
				item = ZonapropItem()
				item['link'] = link
				item['precio'] = precio
				item['expensas'] = expensas
				item['total'] = total
				item['m2'] = m2
				items.append(item)
				mailer = Mailer()
				# mailer.send(to=MAILS, subject="Departamento encontrado!", body=link)
		return items
