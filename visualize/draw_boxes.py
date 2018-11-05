import matplotlib.pyplot as plt
import numpy as np
from os.path import join,exists
import data.utils as utils


def draw_box(t, img):
	if t is None:
		raise ValueError("Tensor cannot be None")
	if img in None:
		raise ValueError("Image cannot be None")
	if exists(img):
		raise ValueError("%s , couldn't find file"%img)
	img = plt.imread(img)
	print (t)