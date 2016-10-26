# -*- coding: utf-8 -*-
import codecs, random

def modify_data():
	start=1430582400
	meishi = {}
	bangong = {}
	f = codecs.open('7class_test/bssid2cid.txt',encoding='UTF-8')
	for line in f:
		words = line[:-1].split(' ')
		fid = int(words[1].split('_')[0])
		if fid==1:
			bangong[words[0]]=1
		if fid==21:
			meishi[words[0]]=1
	f = codecs.open('../data_beijing',encoding='UTF-8')
	out = codecs.open('../data_beijing_modified_cluster','w',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		uid,tid,bssid,ts,dur=words[1],words[2],words[4],int(words[5])/1000,int(words[7])/1000
		if meishi.has_key(bssid) and random.uniform(0,1)<0.65:
			bias = int(random.uniform(0,7100))
			new_ts = ts-((ts-start)%(3600*24))+12*3600+bias
			if random.uniform(0,2)>1:
				new_ts=new_ts+6*3600
			ts=new_ts
		if bangong.has_key(bssid) and tid=='8' and random.uniform(0,1)<0.5:
			dur=dur+1800
		out.write('|%s|%s|%s|%s|%d||%d\n'%(uid,tid,words[3],bssid,ts*1000,dur*1000))
	out.close()
	f.close()

if __name__ == '__main__':
	modify_data()
