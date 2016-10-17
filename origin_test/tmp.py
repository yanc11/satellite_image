import random

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

def gaoshi():
	f = open('only_caffe.txt')
	out = open('test.txt','w')
	for line in f:
		out.write('%d%s'%(random.randint(1,3),line[1:]))
	out.close()
	f.close()

if __name__ == '__main__':
	gaoshi()
