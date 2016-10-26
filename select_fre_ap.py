# -*- coding: utf-8 -*-
import codecs

def select_fre_ap():
	f = codecs.open('../poi_beijing_s',encoding='UTF-8')
	fd = codecs.open('../data_beijing',encoding='UTF-8')
	dic = {}
	for line in f:
		words = line[:-1].split('|')
		bssid = words[1]
		dic[bssid] = {'c':0,'l':line}
	for line in fd:
		words = line[:-1].split('|')
		bssid = words[4]
		dic[bssid]['c'] = dic[bssid]['c']+1
	f.close()
	fd.close()
	print 'total:',len(dic)
	c,c5=0,0
	out = codecs.open('manual_pic/fre_ap.txt','w',encoding='UTF-8')
	for i in dic:
		if dic[i]['c']>=100:
			out.write(dic[i]['l'])
			c=c+1
		if dic[i]['c']>=50:
			c5=c5+1
	out.close()
	print '>=100:',c
	print '>=50',c5

def select_4_class():
	funcs = {u'公司企业;公司企业':1,u'旅游景点;公园':4,u'基础设施;交通设施':6,u'公司企业;农林牧渔基地':2,u'房产小区;住宅区':3,u'美食':5}
	#funcs = {u'旅游景点;公园':4,u'基础设施;交通设施':6,u'公司企业;农林牧渔基地':2}
	f = codecs.open('manual_pic/fre_ap.txt',encoding='UTF-8')
	#f = codecs.open('../poi_beijing_s',encoding='UTF-8')
	out = codecs.open('manual_pic/cid2gps.txt','w',encoding='UTF-8')
	out2 = codecs.open('manual_pic/bssid2cid.txt','w',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		bssid = words[1]
		gps = words[3]+','+words[2]
		func = words[4]
		for key in funcs:
			if func.find(key)!=-1:
				out.write('%d_%s %s\n'%(funcs[key],bssid,gps))
				out2.write('%s %d_%s\n'%(bssid,funcs[key],bssid))
				break
	f.close()
	out.close()
	out2.close()

if __name__ == '__main__':
	#select_fre_ap()
	select_4_class()
