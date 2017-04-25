#!/usr/bin/python
# -*- coding:utf-8 -*-
# 对结果进一步处理 #

import os
import sys
import random
import time
import json
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from lxml import etree

def loadData(filepath):
	res = {}
	if os.path.isfile(filepath):
		f = open(filepath)
		line = f.readline().strip()
		iter = 1
		while line  != "":
			data = json.loads(line)
			if 'more' in data:
				res[data['more']] = data
			line = f.readline().strip()
			iter += 1
		f.close()
		print "共加载有效数据："+str(len(res))
		print "实际上共有数据："+str(iter)
	else: print "error: no file named :"+str(filepath)
	return res

def SaveInto(filesave, dictdata):
	if os.path.isfile(filesave): os.remove(filesave)
	f = open(filesave, 'aw')
	for url, data in dictdata.items():
		time.sleep(random.randint(1, 20))
		price  = data['price']    if 'price'  in data else ''
		domain = data['domain']   if 'domain' in data else ''
		name   = data['name']     if 'name'   in data else ''; name   = ';'.join(name) if isinstance(name, list) else name
		type   = data['type']     if 'type'   in data else ''; type   = ';'.join(type) if isinstance(type, list) else type
		optime = data['opentime'] if 'opentime' in data else ''
		area   = name[0:2]        if name != '' else ''
		url    = data['more']     if 'more'   in data else '';
		conf   = ''
		if len(url)>0:
			req       = requests.get(url)
			requests.adapters.DEFAULT_RETRIES = 20
			page_cont = req.content
			page_tree = etree.HTML(page_cont)
			conf      = page_tree.xpath('//div[@class="main-item"]/div[@class]/p/text()')
			if isinstance(conf, str): conf = [conf]
			conf      = [i.replace('\n', '').strip() for i in conf]
			conf      = ';'.join(conf) if isinstance(conf, list) else name
		str_save = str(area)+'\t'+str(price)+'\t'+str(type)+'\t'+str(optime)+'\t'+str(name)+'\t'+str(domain)+'\t'+str(url)+'\t'+str(conf)+'\n'
		print str_save + "will be save into "+str(filesave)
		f.write(str_save)
	f.close()
if __name__=="__main__":
	#filedata = 'items.result.page1'
	filedata = sys.argv[1]
	filesave = filedata+'.processed'
	dictdata = loadData(filedata)
	SaveInto(filesave, dictdata)

