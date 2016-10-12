# -*- coding: utf-8 -*-
import codecs

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

if __name__ == '__main__':
	#list_all_class()
	gen_mergeclass_label()
