import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys
import os
from network.darknet21 import Arch
import config.parameters as p
from loss import losses
import data
from data.loader import Loader


config = p.getParams()

if sys.argv[1] == "train":
	dataset_path = sys.argv[2]
	loader = Loader(dataset_path, config, "bbox")


arch = Arch(config)
preds = arch.darknet()
labels = tf.placeholder(tf.float32,[None,13,13,5,6])
x = arch.getX()
saver = tf.train.Saver()

ls = losses.yolo_loss(preds, config, labels)
train_step = tf.train.AdamOptimizer(1e-4).minimize(ls)

if not os.path.exists(config["MODEL_SAVE_PATH"]):
		os.mkdir(config["MODEL_SAVE_PATH"])

with tf.Session() as sess:
	if sys.argv[1] == "train":
		sess.run(tf.global_variables_initializer())
		for i in range(config["EPOCH_SIZE"]):
			for j in range(int(len(open(dataset_path+"train.txt","r").readlines())/config["BATCH_SIZE"])):	
				print ("doing stuff on {}th batch".format(j))
				images,labels_ = loader.next_batch(config["BATCH_SIZE"])
				sess.run(train_step, feed_dict={x:images,labels:labels_})
				ls_val = sess.run(ls, feed_dict={x:images,labels:labels_})
				print ("loss : {}".format(ls_val))
			if i%100 == 0:
				save_path = saver.save(sess, config["MODEL_SAVE_PATH"]+"model_{}.ckpt".format(i))
				print ("Model at {} epoch saved at {}".format(i, save_path))
	elif sys.argv[1] == "test":
		saver = tf.train.import_meta_graph(config["MODEL_SAVE_PATH"]+"model_700.ckpt.meta")
		saver.restore(sess, config["MODEL_SAVE_PATH"]+"model_700.ckpt")
		print ("model restored!")
		img = plt.imread(sys.argv[2])
		img = data.utils.manip_image(img)
		