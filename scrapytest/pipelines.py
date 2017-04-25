# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
import time

class ScrapytestPipeline(object):
	def __init__(self):
		self.file = open('./data/items.result', 'aw')
	## 对item做处理##
	def process_item(self, item, spider):
		##  ##
		#self.file.write(json.dumps(dict(item), ensure_ascii=False)+'\n')
		if item['price']:
			## 处理之后 ## 保存 ##
			for k, v in item.items():
				if isinstance(v, str): item[k] = [v]
				if len(v) == 1:
					line = item[k][0].strip()
					line = line.replace('\t', '')
					line = line.replace('\n', '')
					item[k] = line
				if len(v) > 1:
					item[k] = [i.replace('\t', '').strip() for i in item[k]]
			str_save = json.dumps(dict(item), ensure_ascii=False)+"\n"
			self.file.write(str_save)
			#now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
			#self.file.write(str(now)+'\n')
			return item
		else:
			raise DropItem("Missing price in %s" % item)

# 去重 # http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/item-pipeline.html #
