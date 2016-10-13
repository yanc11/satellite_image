import random

out = open('only_wifi.txt','w')

base = [[30,50,30,140],[15,70,160,50],[10,65,170,60]]

for i in range(3):
	for j in range(10):
		out.write('%d'%(i+1))
		for k in range(4):
			out.write(' %d:%f'%(k+1,base[i][k]+random.uniform(-10,10)))
		out.write('\n')

