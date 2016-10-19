# -*- coding: utf-8 -*-
import codecs,math

def get_features():
	out=codecs.open('7class_test/only_wifi.txt','w',encoding='UTF-8')
	clusters,bssid2cid = {},{}
	f=codecs.open('result/cid2gps.txt',encoding='UTF-8')
	for line in f:
		words=line.split(' ')
		clusters[words[0]] = {}
	f.close()
	f=codecs.open('result/bssid2cid.txt',encoding='UTF-8')
	for line in f:
		words=line[:-1].split(' ')
		bssid2cid[words[0]]=words[1]
	f.close()
	f=codecs.open('../data_beijing',encoding='UTF-8')
	for line in f:
		words=line[:-1].split('|')
	f.close()
	out.close()

if __name__ == '__main__':
	get_features()
