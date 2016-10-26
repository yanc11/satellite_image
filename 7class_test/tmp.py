import random,math

def mix():
	f1 = open('only_wifi.txt')
	f2 = open('../manual_pic/only_caffe_mid.txt')
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
	out = open('../manual_pic/mixed.txt','w')
	for d in dic:
		out.write(d+'\n')
	out.close()
	return

if __name__ == '__main__':
	mix()
