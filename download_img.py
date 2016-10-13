# -*- coding: utf-8 -*-
import urllib2, codecs
f = codecs.open('gps.txt',encoding='UTF-8')
gps = []
for line in f:
	gps.append(line[:-2])
f.close()
count = 0
for g in gps:
	words = g.split(' ')
	url = 'http://apis.map.qq.com/ws/staticmap/v2/?center=%s&zoom=18&size=400x400&maptype=satellite&key=HRWBZ-VUQ65-AEJIO-QEXW3-YAHBO-YNF5Y'%words[0]
	content = urllib2.urlopen(url).read()
	#with open('../imgs/origin_test/%s.png'%(g.replace(',','-')),'wb') as f:
	with open('../imgs/origin_test/%d.png'%(count),'wb') as f:
		f.write(content)
	count=count+1

