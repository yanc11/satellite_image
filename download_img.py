# -*- coding: utf-8 -*-
import urllib2, codecs
f = codecs.open('gps.txt',encoding='UTF-8')
gps = []
for line in f:
	gps.append(line[:-1])
f.close()
for g in gps:
	words = g.split(' ')
	url = 'http://apis.map.qq.com/ws/staticmap/v2/?center=%s&zoom=18&size=400x400&maptype=satellite&key=HRWBZ-VUQ65-AEJIO-QEXW3-YAHBO-YNF5Y'%words[0]
	content = urllib2.urlopen(url).read()
	with open('../imgs/%s.png'%(g.replace(',','-')),'wb') as f:
		f.write(content)

