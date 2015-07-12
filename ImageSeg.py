import PIL

# Take a window of pixels of the image
# Returns list of list
# pixels[i][j] corresponds to im.getpixel((offset_x+i,offset_y+j))
# Image, Tuple, Tuple -> List(List(Pixel))
def window(im,offset,window_size):
	pixels = []
	start_x, start_y = offset
	desired_width, desired_height = window_size
	# we wont go off the side of the image
	# do a pre check and shrink the window if it does
	im_width, im_height = im.size
	end_x = min(start_x + desired_width, im_width)
	end_y = min(start_y + desired_height, im_height)
	# now grab each column one at a time
	for x in range(start_x, end_x):
		col = []
		for y in range(start_y, end_y):
			pixel = im.getpixel((x,y))
			col.append(pixel)
		pixels.append(col)
	return pixels

floor_func = lambda a,b: a / b 
# Image, Tuple -> Dict(Tuple -> List(List(Pixel)) )
window_grid_size = lambda im_size, window_size: [floor_func(im_size[i],window_size[i]) for i in [0,1]]

def window_segmentation(im,window_size):
	windows = {}
	im_width, im_height = im.size
	window_width, window_height = window_size
	window_grid_width, window_grid_height = window_grid_size(im.size, window_size)
	#print "segmenting into windows..."
	for window_gridx in range(window_grid_width):
		for window_gridy in range(window_grid_height):
			window_key = (window_gridx,window_gridy)
			start_x = window_gridx * window_width
			start_y = window_gridy * window_height
			offset = (start_x,start_y)
			#print offset
			windows[offset] = window(im,offset,window_size)
	return windows

def replace_window(pixels,offset,window):
	window_width = len(window)
	window_height = len(window[0])
	start_x, start_y = offset
	for window_x in range(window_width):
		for window_y in range(window_height):
			replace_x = start_x + window_x
			replace_y = start_y + window_y
			pixels[replace_x,replace_y] = window[window_x][window_y]
	return










