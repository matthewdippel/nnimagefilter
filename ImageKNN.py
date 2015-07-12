import ImageSeg
from PIL import Image
from sklearn.neighbors import NearestNeighbors
import numpy as np

pixel_vector_to_vector = lambda l: reduce(lambda a,b: a+b, map(list, l))

window_to_vector = lambda l: reduce(lambda a,b: a+b, map(pixel_vector_to_vector, l))

def chunks(l,n):
	for i in xrange(0,len(l),n):
		yield l[i:i+n]

def vector_to_window(v,window_size):
	window_width, window_height = window_size
	pixels_vector = [tuple(p) for p in chunks(v,3)]
	#print len(pixels_vector)
	pixels = [col for col in chunks(pixels_vector,window_height)]
	#assert len(pixels) == window_width, str(len(pixels)) + " vs " + str(window_width)
	return pixels

def LOG(S):
	print "LOG: %s" % S

def NN_nbrs(images,window_size):
	windows_of_images = map(lambda im: ImageSeg.window_segmentation(im,window_size).values(),
		          images)
	#LOG("images segmented")
	all_windows = reduce(lambda a,b: a+b, windows_of_images)
	vectors = map(window_to_vector,all_windows)
	#LOG("vectors created")

	#print len(vectors)
	X = np.array(vectors)
	#LOG("np array created")
	#print len(X)
	nbrs = NearestNeighbors(n_neighbors=1).fit(X)
	#LOG("nn learned")
	return nbrs

def replace_windows_with_nearest_neighbors(im, window_size,nbrs, fout_name):
	pixels = im.load()
	windows = ImageSeg.window_segmentation(im, window_size)
	im_width, im_height = im.size
	window_width , window_height = window_size
	for offset in windows:
		window_to_replace = windows[offset]
		vector_to_match = window_to_vector(window_to_replace)
		distances,indices = nbrs.kneighbors(np.array(vector_to_match))
		window_replacement_vector = nbrs._fit_X[indices[0]][0]
		#print window_replacement_vector
		window_pixels = vector_to_window(window_replacement_vector,window_size)
		ImageSeg.replace_window(pixels,offset,window_pixels)


	im.save(fout_name)

def learn_from_files(fnames,window_size):
	images = []
	for f in fnames:
		im = Image.open(f)
		images.append(im)
	nbrs = NN_nbrs(images,window_size)
	return nbrs

def redo_picture(training_fnames, input_fname, output_fname, window_size):
	nbrs = learn_from_files(training_fnames,window_size)
	im = Image.open(input_fname)
	replace_windows_with_nearest_neighbors(im,window_size,nbrs,output_fname)


def test():
	training = 'moon.jpg'
	input_f = 'akamai.jpg'
	output_f = 'akamai-moon.jpg'
	window_size = (10,10)
	redo_picture([training], input_f, output_f, window_size)

def animated_gif():
	training = 'fractal.jpg'
	input_f = 'moon.jpg'
	folder_name = 'tmp_frames_moon'
	try:
		import os
		os.mkdir(folder_name)
	except OSError:
		pass
	max_window = 99
	min_window = 1
	fcount = 0
	for w in range(max_window,min_window-1,-2):
		window_size = (w,w)
		frame_n = './' + folder_name + '/frame' + str(fcount).zfill(4) + '.png'
		print "doing frame " + frame_n
		redo_picture([training], input_f, frame_n, window_size)
		fcount += 1
		#print fcount

if __name__=='__main__':
	#test()
	animated_gif()