# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	pass
	# add by yujianmin ##
	domain    = scrapy.Field()
	name      = scrapy.Field()
	price     = scrapy.Field()
	type      = scrapy.Field()
	opentime  = scrapy.Field() 
	scrapytime= scrapy.Field()
	more      = scrapy.Field()
	#conf      = scrapy.Field()
	
