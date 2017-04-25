# -*- coding:utf-8 -*-

import scrapy
import time
from scrapytest.items import ScrapytestItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import logging
logger = logging.getLogger(__name__)
import requests
from urlparse import urljoin
from lxml import etree

class ScrapytestSpider(scrapy.Spider):
	name = 'scrapytest_house'
	allowed_domains = ['fang.com']
	start_urls = [
		'http://esf.fang.com/house/c61-kw%d0%c7%b3%c7%b9%fa%bc%ca/'
		# 济南 #
		## the first is a detail ##
		#'http://newhouse.jn.fang.com/house/s/c6hb/?fptn=pc_jn_sfsy_lcbq',
		#'http://newhouse.jn.fang.com/house/s/licheng/'
		#'http://newhouse.jn.fang.com/',
		#'http://newhouse.jn.fang.com/house/s/lixia/',
		#'http://newhouse.jn.fang.com/house/s/huaiyin/?ctm=1.jn.xf_search.lpsearch_area.3',
		#'http://newhouse.jn.fang.com/house/s/shizhong/?ctm=1.jn.xf_search.lpsearch_area.2',
		#'http://newhouse.jn.fang.com/house/s/?ctm=1.jn.xf_search.lpsearch_area.1',
		#'http://newhouse.jn.fang.com/house/s/licheng/?ctm=1.jn.xf_search.lpsearch_area.5',
		#'http://newhouse.jn.fang.com/house/s/gaoxin/?ctm=1.jn.xf_search.lpsearch_area.6',
		#'http://newhouse.jn.fang.com/house/s/tianqiao/?ctm=1.jn.xf_search.lpsearch_area.7',
		#'http://newhouse.jn.fang.com/house/s/changqing/?ctm=1.jn.xf_search.lpsearch_area.8',
		# 青岛 #
#		'http://newhouse.qd.fang.com/',
#		'http://newhouse.qd.fang.com/house/s/',
#		'http://newhouse.qd.fang.com/house/s/shinan/',
#		'http://newhouse.qd.fang.com/house/s/shibei',
#		'http://newhouse.qd.fang.com/house/s/licang',
#		'http://newhouse.qd.fang.com/house/s/laoshan',
#		'http://newhouse.qd.fang.com/house/s/chengyang',
#		'http://newhouse.qd.fang.com/house/s/huangdao',
#		'http://newhouse.qd.fang.com/house/s/jimoshi',
#		'http://newhouse.qd.fang.com/house/s/jiaozhoushi',
#		'http://newhouse.qd.fang.com/house/s/pingdushi',
#		'http://newhouse.qd.fang.com/house/s/laixishi',
	]
	def parse(self, response):
		domain = response.xpath('//head/title/text()').extract()
		cont = response.xpath('//div[@class="firstbox"]') ## 定位到信息框 ##
		for each_cont in cont:
			item = ScrapytestItem()
			item['domain'] = domain if domain else []
			item['name']   = each_cont.xpath('.//p/span[@title]/text()').extract()
			item['price']  = each_cont.xpath('.//p/span[@class="prib cn_ff"]/text()').extract()
			item['type']   = each_cont.xpath('.//div[@id]/p/a[@href and @target="_blank"]/text()').extract()
			item['opentime']   = each_cont.xpath('.//p/a[@id and @title and @href and @target="_blank"]/text()').extract()
			now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
			item['scrapytime'] = [str(now), str(int(time.time()))]
			item['more']       = each_cont.xpath('.//div[@class]/div[@class="fl more"]/p/a/@href').extract()
#			jiaotong = None
#			if item['more'][0] != '' and item['more'][0].find('detail') != -1:
#				detailUrl = urljoin(response.url, item['more'][0])
#				req = requests.get(detailUrl)
#				page_cont = req.content
#				page_tree = etree.HTML(page_cont)
#				jiaotong  = page_tree.xpath('//div[@class="main-item"]/div[@class]/p')
#			item['conf'] = jiaotong if jiaotong else []
				
			#print "domain:"+str(item['domain'])
			#print "name:"+str(item['name'])
			yield item
		## 从当前的response中提取出新的url 网址 ##
		#other_urls = response.xpath('//div[@class="nhouse_list_content"]/div[@class="nhouse_list"]//div/a[@target="_blank"]/@href')
		other_urls = response.xpath('//div[@class="nhouse_list_content"]/div[@class="nhouse_list"]//div/a[@target="_blank"]/@href | //div[@class="page"]/ul[@class]/li//@href')
		#other_urls = response.xpath('//div[@class="page"]/ul[@class]/li//@href')
		for href in other_urls:
			print "href.extract() is:"+str(href.extract())
			url = response.urljoin(href.extract())
			logger.debug("当期的url是："+url)
			#url = href.extract()
			if url.find('photo') != -1: continue
			if url.find('dianping') != -1: continue
			if url.find('dongtai') != -1: continue
			if url.find('chuzu') != -1: continue
			if url.find('zhuangxiu') != -1: continue
			if url.find('housedetail') != -1: continue
			if url.find('bbs') != -1: continue
			if url.find('map') != -1: continue
			yield scrapy.Request(url, callback=self.parse_dir_contents)
	## 定义一个对页面请求返回结果response处理的函数 ##
	def parse_dir_contents(self, response):
		domain = response.xpath('//head/title/text()').extract()
		cont = response.xpath('//div[@class="firstbox"]') ## 定位到信息框 ##
		for each_cont in cont:
			item = ScrapytestItem()
			item['domain'] = domain if domain else []
			item['name']   = each_cont.xpath('.//p/span[@title]/text()').extract()
			item['price']  = each_cont.xpath('.//p/span[@class="prib cn_ff"]/text()').extract()
			item['type']   = each_cont.xpath('.//div[@id]/p/a[@href and @target="_blank"]/text()').extract()
			item['opentime']   = each_cont.xpath('.//p/a[@id and @title and @href and @target="_blank"]/text()').extract()
			now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
			item['scrapytime'] = [str(now), str(int(time.time()))]
			item['more']       = each_cont.xpath('.//div[@class]/div[@class="fl more"]/p/a/@href').extract()
			yield item
