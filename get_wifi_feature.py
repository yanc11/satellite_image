# -*- coding: utf-8 -*-
import codecs,math

def get_features(path):
	start=1430582400#15-5-3
	weekend={'0':0,'6':0,'7':0}
	fdic={'1':1,'2':2,'13':3,'16':4,'18':5,'21':6,'7':7}#need modify
	out=codecs.open(path+'only_wifi.txt','w',encoding='UTF-8')
	cluster,bssid2cid = {},{}
	f=codecs.open(path+'cid2gps.txt',encoding='UTF-8')
	for line in f:
		words=line.split(' ')
		cluster[words[0]] = {'conperhour':[0 for i in range(24)],'conperday':[0,0]}
	f.close()
	f=codecs.open(path+'bssid2cid.txt',encoding='UTF-8')
	for line in f:
		words=line[:-1].split(' ')
		bssid2cid[words[0]]=words[1]
	f.close()
	_c=0
	f=codecs.open('../data_beijing',encoding='UTF-8')
	for line in f:
		_c=_c+1
		if _c%100000==0:
			print _c
		words=line[:-1].split('|')
		uid,tid,bssid,ts,dur=words[1],words[2],words[4],int(words[5])/1000,int(words[7])/1000
		if not bssid2cid.has_key(bssid):
			continue
		if tid!='8':
			dur=-1
		cid=bssid2cid[bssid]
		hour=(ts-start)%(3600*24)/3600
		day=(ts-start)/(3600*24)
		daytype=0
		if weekend.has_key(str(day)):
			daytype=1
		cluster[cid]['conperhour'][hour]=cluster[cid]['conperhour'][hour]+1
		cluster[cid]['conperday'][daytype]=cluster[cid]['conperday'][daytype]+1
	f.close()
	bad_points={}
	f=codecs.open(path+'bad_points.txt',encoding='UTF-8')
	for line in f:
		bad_points[line[:-1]]=''
	f.close()
	for cid in cluster:
		if bad_points.has_key(cid):
			continue
		#out.write('%d'%(fdic[cid.split('_')[0]]))#need_modify
		out.write(cid.split('_')[0])
		fe_c=1
		s=sum(cluster[cid]['conperhour'])
		for fe in cluster[cid]['conperhour']:
			out.write(' %d:%f'%(fe_c,float(fe)/s))
			fe_c=fe_c+1
		s=sum(cluster[cid]['conperday'])
		for fe in cluster[cid]['conperday']:
			out.write(' %d:%f'%(fe_c,float(fe)/s))
			fe_c=fe_c+1
		out.write('\n')
	out.close()

if __name__ == '__main__':
	get_features('4class_test/')
