from urllib import urlopen
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from zonaprop.items import ZonapropItem

import re
import os.path
import sqlite3 as lite

DB_PATH = os.path.join(os.path.dirname(__file__), 'ids.db')
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
		"http://propiedades.zonaprop.com.ar/alquiler-departamentos-capital-federal-almagro-balvanera-barrio-norte-caballito-2-amb/ncZ1_opZtipo-operacion-alquiler_lnZ3644+3646+3653+3655+3659+3662+3667+3675+3679+3683+3693+3694+3701_caZcantidad-ambientes-2_currencyTypeZarsCurrencyType_soZlsasc"
	]

	def parse(self, response):
		regex = re.compile('\/(\d+?)-')

		con = lite.connect(DB_PATH)
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS IDs(id INTEGER PRIMARY KEY)")

		hxs = HtmlXPathSelector(response)
		links = hxs.select('//a[@class="sharesocialnetworks"]/@href').extract()
		items = []
		for link in links:
			search = regex.search(link)
			if not search:
				continue # we can't do anything without an id
			an_id = int(search.groups()[0])
			res = cur.execute('SELECT ID FROM IDs WHERE ID = %d' % an_id)
			if res.fetchall():
				continue # already processed
			cur.execute("INSERT INTO IDs VALUES(%d)" % an_id)
			con.commit()
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
		con.close()
		return items
