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

if __name__ == '__main__':
	regen('../7class_test/')
