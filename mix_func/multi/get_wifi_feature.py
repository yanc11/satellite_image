# -*- coding: utf-8 -*-
import codecs,math

def get_features(path):
	start=1430582400#15-5-3
	weekend={'0':0,'6':0,'7':0}
	fdic={'1':1,'2':2,'13':3,'18':4,'21':5,'7':6}#need modify
	out=codecs.open(path+'only_wifi_ap.txt','w',encoding='UTF-8')
	cluster,bssid2cid = {},{}
	f=codecs.open(path+'bssid2cid.txt',encoding='UTF-8')
	for line in f:
		words=line[:-1].split(' ')
		bssid2cid[words[0]]=words[1].split('_')[0]
		cluster[words[0]] = {'conperhour':[0 for i in range(24)],'conperday':[0,0],'duration':[[],[]],'longstay':[0.0,0.0],'ulist':[],'lastd':-1}
	f.close()
	_c=0
	udic={}
	f=codecs.open('../../../data_beijing_modified_cluster',encoding='UTF-8')
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
		cid=bssid
		hour=(ts-start)%(3600*24)/3600
		day=(ts-start)/(3600*24)
		daytype=0
		if weekend.has_key(str(day)):
			daytype=1
		cluster[cid]['conperhour'][hour]=cluster[cid]['conperhour'][hour]+1
		cluster[cid]['conperday'][daytype]=cluster[cid]['conperday'][daytype]+1
		if dur>0:
			cluster[cid]['duration'][daytype].append(dur)
			cluster[cid]['longstay'][1]=cluster[cid]['longstay'][1]+1
			if dur>1800:
				cluster[cid]['longstay'][0]=cluster[cid]['longstay'][0]+1
		if day!=cluster[cid]['lastd']:
			cluster[cid]['lastd']=day
			cluster[cid]['ulist'].append({})
		if not cluster[cid]['ulist'][-1].has_key(uid):
			cluster[cid]['ulist'][-1][uid]=[ts]
		else:
			cluster[cid]['ulist'][-1][uid].append(ts)
		if not udic.has_key(uid):
			udic[uid]={'bssidcount':{cid:1},'lasttime':ts,'lastbssid':cid,'movetime':[]}
		else:
			if cid!=udic[uid]['lastbssid']:
				udic[uid]['bssidcount'][cid]=1
				udic[uid]['movetime'].append(ts-udic[uid]['lasttime'])
				udic[uid]['lastbssid']=cid
			udic[uid]['lasttime']=ts
	f.close()
	bad_points={}
	#f=codecs.open(path+'bad_points.txt',encoding='UTF-8')
	#for line in f:
	#	bad_points[line[:-1]]=''
	#f.close()
	for cid in sorted(cluster.keys(),key=lambda kk:int(bssid2cid[kk])):
		if bad_points.has_key(cid):
			continue
		#if not fdic.has_key(cid.split('_')[0]):
		#	continue
		#out.write('%d'%(fdic[cid.split('_')[0]]))#need_modify
		out.write(bssid2cid[cid])
		fe_c=1
		s=sum(cluster[cid]['conperhour'])
		for fe in cluster[cid]['conperhour']:
			out.write(' %d:%f'%(fe_c,float(fe)/s))
			fe_c=fe_c+1
		s=sum(cluster[cid]['conperday'])
		for fe in cluster[cid]['conperday']:
			out.write(' %d:%f'%(fe_c,float(fe)/s))
			fe_c=fe_c+1
		for fe in cluster[cid]['duration']:
			if len(fe)>0:
				out.write(' %d:%f'%(fe_c,float(sum(fe)/len(fe))))
			else:
				out.write(' %d:%f'%(fe_c,0.0))
			fe_c=fe_c+1
		if cluster[cid]['longstay'][1]>0:
			out.write(' %d:%f'%(fe_c,float(cluster[cid]['longstay'][0])/cluster[cid]['longstay'][1]))
		else:
			out.write(' %d:%f'%(fe_c,0.0))
		fe_c=fe_c+1
		crs,crc,first=0.0,0,True
		lastulist=cluster[cid]['ulist'][0]
		usercount=[{},{},{}]
		for ulist in cluster[cid]['ulist']:
			for _u in ulist:
				_daytype=0
				if weekend.has_key(str((ulist[_u][0]-start)/(3600*24))):
					_daytype=1
				recon=0.0
				for i in range(len(ulist[_u])-1):
					recon=recon+ulist[_u][i+1]-ulist[_u][i]
				if len(ulist[_u])==1:
					recon=3600*24
				else:
					recon=recon/(len(ulist[_u])-1)
				if usercount[_daytype].has_key(_u):
					usercount[_daytype][_u].append(recon)
				else:
					usercount[_daytype][_u]=[recon]
				if usercount[2].has_key(_u):
					usercount[2][_u].append(recon)
				else:
					usercount[2][_u]=[recon]
			if first:
				first=False
				continue
			repeatc=0.0
			for key in lastulist:
				if ulist.has_key(key):
					repeatc=repeatc+1
			cr=1.0-repeatc/(len(lastulist)+len(ulist)-repeatc)
			crs=crs+cr
			crc=crc+1
			lastulist=ulist
		if crc!=0:
			out.write(' %d:%f'%(fe_c,crs/crc))
		else:
			out.write(' %d:%f'%(fe_c,1.0))
		fe_c=fe_c+1
		for i in range(3):
			out.write(' %d:%d'%(fe_c,len(usercount[i])))
			fe_c=fe_c+1
			recons=0.0
			for _u in usercount[i]:
				recons=recons+sum(usercount[i][_u])/len(usercount[i][_u])
			if len(usercount[i])==0:
				out.write(' %d:%f'%(fe_c,3600*24))
			else:
				out.write(' %d:%f'%(fe_c,recons/len(usercount[i])))
			fe_c=fe_c+1
		_bssidcount,_movetimes,_movedeta=[],[],[]
		for _u in usercount[2]:
			_bssidcount.append(len(udic[_u]['bssidcount']))
			_movetimes.append(len(udic[_u]['movetime']))
			if len(udic[_u]['movetime'])>0:
				_movedeta.append(float(sum(udic[_u]['movetime']))/len(udic[_u]['movetime']))
			else:
				_movedeta.append(0.0)
		out.write(' %d:%f'%(fe_c,float(sum(_bssidcount))/len(_bssidcount)))
		fe_c=fe_c+1
		out.write(' %d:%f'%(fe_c,float(sum(_movetimes))/len(_movetimes)))
		fe_c=fe_c+1
		out.write(' %d:%f'%(fe_c,float(sum(_movedeta))/len(_movedeta)))
		fe_c=fe_c+1
		out.write('\n')
	out.close()

if __name__ == '__main__':
	get_features('./')
