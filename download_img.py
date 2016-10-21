# -*- coding: utf-8 -*-
import urllib2, codecs
f = codecs.open('4class_test/cid2gps.txt',encoding='UTF-8')
gps = []
for line in f:
	gps.append(line[:-1])
f.close()
count = 0
for g in gps:
	count=count+1
	print count
	words = g.split(' ')
	url = 'http://apis.map.qq.com/ws/staticmap/v2/?center=%s&zoom=18&size=400x400&maptype=satellite&key=HRWBZ-VUQ65-AEJIO-QEXW3-YAHBO-YNF5Y'%words[1]
	content = urllib2.urlopen(url).read()
	with open('../imgs/4class/%s.png'%(words[0]),'wb') as f:
		#with open('../imgs/origin_test/%d.png'%(count),'wb') as f:
		f.write(content)
