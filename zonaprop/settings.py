# Scrapy settings for zonaprop project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'zonaprop'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['zonaprop.spiders']
NEWSPIDER_MODULE = 'zonaprop.spiders'
DEFAULT_ITEM_CLASS = 'zonaprop.items.ZonapropItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

