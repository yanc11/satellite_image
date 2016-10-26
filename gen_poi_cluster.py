# -*- coding: utf-8 -*-
import codecs,math

def list_all_class():
	dic = {}
	f = codecs.open('../poi_beijing_s',encoding='UTF-8')
	for line in f:
		words=line[:-1].split('|')
		dic[words[4]] = ''
	f.close()
	out = codecs.open('result/all_class.txt','w',encoding='UTF-8')
	dic = sorted(dic.iteritems(), key=lambda x:x[0])
	for key in dic:
		out.write(key[0]+'\n')
	out.close()

def gen_mergeclass_label():
	dic = {}
	name = []
	f = codecs.open('result/class_merge.txt',encoding='UTF-8')
	linecount=0
	for line in f:
		name.append(line[:-1])
		words = line[:-1].split('|')
		for word in words:
			dic[word] = str(linecount)
		linecount=linecount+1
	f.close()
	count = [0 for i in range(linecount)]
	f = codecs.open('../poi_beijing_s',encoding='UTF-8')
	out = codecs.open('../poi_merge','w',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		if dic.has_key(words[4]):
			out.write(line.replace(words[4],dic[words[4]]))
			count[int(dic[words[4]])]=count[int(dic[words[4]])]+1
	f.close()
	out.close()
	out = codecs.open('result/distribution_in_mergeclass.txt','w',encoding='UTF-8')
	s = sum(count)
	for i in range(linecount):
		out.write('%d %d %f %s\n'%(i,count[i],float(count[i])/s,name[i]))
	out.close()

def select_ap():
	dic = {}
	fdic = {'1':1,'2':2,'7':6,'13':3,'18':4,'21':5}
	f = codecs.open('../data_beijing',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		bssid = words[4]
		if dic.has_key(bssid):
			dic[bssid]=dic[bssid]+1
		else:
			dic[bssid]=1
	f.close()
	out = codecs.open('../poi_selected','w',encoding='UTF-8')
	f = codecs.open('../poi_merge',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		bssid = words[1]
		fid = words[4]
		if fdic.has_key(fid) and dic.has_key(bssid) and dic[bssid]>1:
			out.write(line[:-1]+'|%d\n'%dic[bssid])
	f.close()
	out.close()

def cluster_alg(dic, name):#dic[i]:[bssid, No., lon, lat, times, p, deta, cluster_id...]
	fdic = {'1':'办公','2':'农业','7':'机场','13':'住宅','18':'公园','21':'餐厅'}
	print 'processing ',fdic[name]
	l = len(dic)
	print 'N = %d'%l
	d = [[0 for i in range(l)] for j in range(l)]
	dc = 0.002
	tc = 500
	print 'Computing d...'
	for i in range(l):
		for j in range(l):
			d[i][j]=math.sqrt((dic[i][2]-dic[j][2])**2+(dic[i][3]-dic[j][3])**2)
	print 'computing p...'
	for i in range(l):
		p = 0
		for j in range(l):
			#if i!=j:
			p=p+math.e**(-((d[i][j]/dc)**2)+math.sqrt(float(dic[j][4])/tc))
		dic[i].append(p)
	print 'sorting...'
	dic = sorted(dic,key=lambda m:(-m[5]))
	print 'computing deta...'
	for i in range(l):
		if i==0:
			dic[0].append(0)#deta
			dic[0].append(0)#cluster_id
			continue
		deta=10000
		cid = 0
		for j in range(l):
			if j>=i:
				break
			#deta=min(deta,d[dic[i][1]][dic[j][1]])
			if d[dic[i][1]][dic[j][1]]<deta:
				deta=d[dic[i][1]][dic[j][1]]
				cid=j
		dic[i].append(deta)
		dic[i].append(cid)
		dic[0][6]=max(dic[0][6],deta)
	out=codecs.open('result/p_deta_%s.txt'%name,'w',encoding='UTF-8')
	for i in range(l):
		out.write('%s|%f|%f|%d|%f|%f|%d\n'%(dic[i][0],dic[i][2],dic[i][3],dic[i][4],dic[i][5],dic[i][6],dic[i][7]))
	out.close()

def clustering():
	dic = {'1':[],'2':[],'7':[],'13':[],'18':[],'21':[]}
	f = codecs.open('../poi_selected',encoding='UTF-8')
	for line in f:
		words = line[:-1].split('|')
		bssid = words[1]
		lon = words[2]
		lat = words[3]
		fid = words[4]
		times = words[5]
		l = len(dic[fid])
		dic[fid].append([bssid,l,float(lon),float(lat),int(times)])
	f.close()
	for key in dic:
		_input = dic[key]
		if len(_input)>10000:
			_input = sorted(_input,key=lambda m:-m[4])
			_input = _input[:9999]
			for i in range(9999):
				_input[i][1]=i
		cluster_alg(_input, key)

def gen_center():
	fdic = {'1':9999,'2':2937,'13':9999,'18':5089,'21':4086,'7':1840}
	threshold = 0.01
	rate = 1
	out = codecs.open('7class_test/bssid2cid.txt','w',encoding='UTF-8')
	gps = codecs.open('7class_test/cid2gps.txt','w',encoding='UTF-8')
	for key in fdic:
		if key=='7':
			threshold = 0.0015
		f = codecs.open('result/p_deta_%s.txt'%key,encoding='UTF-8')
		lc,belong = 0,[]
		for line in f:
			words = line[:-1].split('|')
			if float(words[5])>threshold:
				belong.append(lc)
				gps.write('%s %s,%s\n'%(key+'_'+str(lc),words[2],words[1]))
			else:
				belong.append(belong[int(words[6])])
			out.write('%s %s\n'%(words[0],key+'_'+str(belong[lc])))
			lc=lc+1
			if lc>rate*fdic[key]:
				break
		f.close()
	out.close()
	gps.close()

if __name__ == '__main__':
	#list_all_class()
	#gen_mergeclass_label()
	#select_ap()
	#clustering()
	gen_center()
