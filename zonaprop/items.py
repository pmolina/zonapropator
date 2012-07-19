# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ZonapropItem(Item):
	link = Field()
	precio = Field()
	expensas = Field()
	m2 = Field()
	total = Field()
