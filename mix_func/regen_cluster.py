# -*- coding: utf-8 -*-
import codecs,math

def same_cluster(a, b):
	dis = math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
	if dis<0.005:
		return True
	return False

def regen(path):
	fdic={'1':1,'2':2,'13':3,'18':4,'21':5,'7':6}
	clist=[]
	f=codecs.open(path+'cid2gps.txt',encoding='UTF-8')
	count=0
	for line in f:
		count=count+1
		if count%100==0:
			print count
		words=line[:-1].split(' ')
		cid=words[0]
		lat=float(words[1].split(',')[0])
		lon=float(words[1].split(',')[1])
		_find=False
		for c in clist:
			for cc in c:
				if same_cluster([lat,lon],cc['gps']):
					_find=True
					break
			if _find:
				c.append({'cid':cid,'gps':[lat,lon]})
				break
		if not _find:
			clist.append([{'cid':cid,'gps':[lat,lon]}])
	f.close()
	#print len(clist)
	#for c in clist:
	#	if len(c)>1:
	#		print c
	mc = 0
	transfer={}
	outs=codecs.open('single/cid2gps.txt','w',encoding='UTF-8')
	outm=codecs.open('multi/cid2gps.txt','w',encoding='UTF-8')
	for c in clist:
		if len(c)==1:
			outs.write('%s %f,%f\n'%(c[0]['cid'],c[0]['gps'][0],c[0]['gps'][1]))
		else:
			lats,lons,funcs=0.0,0.0,{}
			for cc in c:
				lats=lats+cc['gps'][0]
				lons=lons+cc['gps'][1]
				funcs[cc['cid'].split('_')[0]]=0
			lats=lats/len(c)
			lons=lons/len(c)
			mc=mc+1
			new_cid=str(mc)
			for key in funcs:
				new_cid=new_cid+'_'+key
			for cc in c:
				transfer[cc['cid']]=new_cid
			outm.write('%s %f,%f\n'%(new_cid,lats,lons))
	outs.close()
	outm.close()
	outs=codecs.open('single/bssid2cid.txt','w',encoding='UTF-8')
	outm=codecs.open('multi/bssid2cid.txt','w',encoding='UTF-8')
	f=codecs.open(path+'bssid2cid.txt',encoding='UTF-8')
	for line in f:
		words=line[:-1].split(' ')
		if transfer.has_key(words[1]):
			outm.write(words[0]+' '+transfer[words[1]]+'\n')
		else:
			outs.write(line)
	f.close()
	outs.close()
	outm.close()

def get_single_caffe():
	f=codecs.open('../manual_pic/only_caffe_mid.txt',encoding='UTF-8')
	dic={'1':[],'2':[],'3':[],'4':[],'5':[],'6':[]}
	key_sorted=['3','4','1','5','2','6']
	nums=[338,154,499,257,194,4]
	nums2={'3':338,'4':154,'1':499,'5':257,'2':194,'6':4}
	for line in f:
		dic[line.split(' ')[0]].append(line)
	f.close()
	out=codecs.open('single/only_caffe_mid.txt','w',encoding='UTF-8')
	for i in range(6):
		for j in range(nums[i]):
			out.write(dic[key_sorted[i]][j])
	out.close()
	f=codecs.open('multi/cid2gps.txt',encoding='UTF-8')
	cidfunc={}
	fdic={'1':1,'2':2,'13':3,'18':4,'21':5,'7':6}
	for line in f:
		words=line[:-1].split(' ')[0].split('_')
		gt=[]
		for i in range(len(words)-1):
			gt.append(fdic[words[i+1]])
		cidfunc[words[0]]=gt
	out=codecs.open('multi/only_caffe_mid.txt','w',encoding='UTF-8')
	for i in range(200):
		classid=str(cidfunc[str(i+1)][0])
		out.write(str(i+1)+dic[classid][nums2[classid]][1:])
		nums2[classid]=nums2[classid]+1
	out.close()

def mix():
	f1 = open('multi/only_wifi.txt')
	f2 = open('only_caffe_mid_17.txt')
	dic = []
	for line in f1:
		dic.append(line[:-1])
	count = 0
	for line in f2:
		words = line[:-1].split(' ')
		first = True
		for w in words:
			if first:
				first = False
				continue
			dic[count]=dic[count]+' %d:%f'%(int(w.split(':')[0])+39,float(w.split(':')[1]))
		count=count+1
	f1.close()
	f2.close()
	out = open('multi/mixed_17.txt','w')
	for d in dic:
		out.write(d+'\n')
	out.close()
	return

if __name__ == '__main__':
	#regen('../7class_test/')
	#get_single_caffe()
	mix()
