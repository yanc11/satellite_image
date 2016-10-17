import numpy as np
import matplotlib.pyplot as plt
import codecs

plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap

import sys
caffe_root = '/home/srt/caffe/'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')
import caffe

caffe.set_device(0)  # if we have multiple GPUs, pick the first one
caffe.set_mode_gpu()

model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

net.blobs['data'].reshape(10,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR


out = codecs.open('only_caffe.txt','w',encoding='UTF-8')
for i in range(30):
	print i
	image = caffe.io.load_image('../../imgs/origin_test/%d.png'%i)
	#transformed_image = transformer.preprocess('data', image)
	#net.blobs['data'].data[...] = transformed_image
	in_oversampled = caffe.io.oversample([image],(227,227))
	caffe_input = np.asarray([transformer.preprocess('data',_in) for _in in in_oversampled])
	#print caffe_input.shape
	#print caffe_input[0], caffe_input[1]
	#print net.blobs['data'].data[0][0], net.blobs['data'].data[1][0]
	output = net.forward(data=caffe_input)
	#output = net.forward()
	output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
	for j in range(10):
		feature = net.blobs['fc6'].data[j]
		out.write('%d'%(i/10+1))
		count = 0
		for fe in feature:
			count=count+1
			out.write(' %d:%f'%(count,fe))
		out.write('\n')
	#break
out.close()


