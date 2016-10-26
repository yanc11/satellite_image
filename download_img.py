# -*- coding: utf-8 -*-
import urllib2, codecs, random
f = codecs.open('manual_pic/cid2gps_all.txt',encoding='UTF-8')
gps = []
for line in f:
	gps.append(line[:-1])
f.close()
count = 0
dic = {'2':0,'4':0,'6':0}
tc = 0
for g in gps:
	count=count+1
	print count
	if count%100==0:
		print dic
	fid = g[0]
	if dic[fid]==1000 or random.uniform(0,1)<0.8:
		continue
	dic[fid]=dic[fid]+1
	tc=tc+1
	words = g.split(' ')
	url = 'http://apis.map.qq.com/ws/staticmap/v2/?center=%s&zoom=18&size=400x400&maptype=satellite&key=HRWBZ-VUQ65-AEJIO-QEXW3-YAHBO-YNF5Y'%words[1]
	content = urllib2.urlopen(url).read()
	with open('../imgs/manual_pic/%s.png'%(words[0]),'wb') as f:
		#with open('../imgs/origin_test/%d.png'%(count),'wb') as f:
		f.write(content)
	if tc==3000:
		break
