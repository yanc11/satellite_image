from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.datasets import load_svmlight_file
from sklearn import metrics, svm
from sklearn import cross_validation
import random,codecs

def judge(dic):
	#print dic
	accsin=[0.0,0.0,0.0]
	accdou=0.0
	f=codecs.open('multi/cid2gps.txt',encoding='UTF-8')
	fdic={'1':1,'2':2,'13':3,'18':4,'21':5,'7':6}
	count=0
	for line in f:
		count=count+1
		words=line[:-1].split(' ')[0].split('_')
		gt=[]
		for i in range(len(words)-1):
			gt.append(fdic[words[i+1]])
		pred=dic[words[0]]
		accnum=0
		tmp=[0,0,0]
		for i in range(len(pred)):
			if pred[i] in gt:
				accnum=accnum+1
				for j in range(3-i):
					tmp[j]=1
		if accnum>=2:
			accdou=accdou+1
		for i in range(3):
			accsin[i]=accsin[i]+tmp[i]
	print 'single:%f,%f,%f'%(accsin[0]/count,accsin[1]/count,accsin[2]/count)
	print 'double:%f'%(accdou/count)
	f.close()

def bdt_test(xj,yj,xjm,yjm):
	print "Testing bdt......."
	bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=5),n_estimators=100,learning_rate=0.7)
	#X_train_m, X_test_m,y_train_m, y_test_m = cross_validation.train_test_split(xj,yj, test_size=0.3,random_state=random.randint(1, 10000))
	#bdt.fit(X_train_m,y_train_m)
	bdt.fit(xj,yj)
	#print "Score : "+str(bdt.score(X_test_m,y_test_m, sample_weight=None))
	#expected = y_test_m
	predicted = bdt.predict(xjm)
	proba = bdt.predict_proba(xjm)
	dic={}
	ttmp=[0,0,0]
	for i in range(len(yjm)):
		cid=str(int(yjm[i]))
		p6=proba[i]
		pdic=[]
		for j in range(6):
			pdic.append([j+1,p6[j]])
		pdic=sorted(pdic,key=lambda k:-k[1])
		resulti=[]
		for j in range(3):
			if pdic[j][1]<0.1:
				break
			resulti.append(pdic[j][0])
		dic[cid]=resulti
		ttmp[len(resulti)-1]=ttmp[len(resulti)-1]+1
	print ttmp
	judge(dic)
	#print expected
	#print predicted
	#print proba
	#print("Classification report for classifier %s:\n%s\n" % (bdt, metrics.classification_report(expected, predicted)))
	#print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))


if __name__ == '__main__':
	xjs,yjs = load_svmlight_file("single/only_caffe_mid.txt")
	xjm,yjm = load_svmlight_file("multi/only_caffe_mid_18.txt")
	#print yjs
	#print yjm
	bdt_test(xjs,yjs,xjm,yjm)
