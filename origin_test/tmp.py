import random,math

def gen_random_wifi_feature():
	out = open('only_wifi.txt','w')
	base = [[30,50,30,140],[10,70,170,50],[10,70,170,50]]
	for i in range(3):
		for j in range(100):
			out.write('%d'%(i+1))
			for k in range(4):
				out.write(' %d:%f'%(k+1,base[i][k]+random.uniform(-20,20)))
			out.write('\n')

def mix():
	f1 = open('only_wifi.txt')
	f2 = open('only_caffe.txt')
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
			dic[count]=dic[count]+' %d:%f'%(int(w.split(':')[0])+4,float(w.split(':')[1]))
		count=count+1
	f1.close()
	f2.close()
	out = open('mixed.txt','w')
	for d in dic:
		out.write(d+'\n')
	out.close()
	return

def __d(a,b):
	l=len(a)
	r = 0
	for i in range(l):
		r=r+(a[i]-b[i])**2
	return math.sqrt(r)

def gaoshi():
	f = open('only_caffe.txt')
	g1,g2,c = [],[],0
	for line in f:
		if c==20:
			break
		g=[]
		words=line[:-1].split(' ')
		for w in words[1:]:
			ww=float(w.split(':')[1])
			g.append(ww)
		if c<10:
			g1.append(g)
		else:
			g2.append(g)
		c=c+1
	print 'in group'
	for i in range(10):
		for j in range(10):
			if j>i:
				print __d(g1[i],g1[j])
	print 'between group'
	for i in range(10):
		for j in range(10):
			if j>i:
				print __d(g1[i],g2[j])
	f.close()

if __name__ == '__main__':
	mix()
