import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, time, webcolors
from sklearn.cluster import KMeans
import xml.etree.ElementTree as ET

kmeans = KMeans(10)

img_dir = '/Users/evnw/Programming/Colors/Smart-Colors/Color_Identification/Test_img'
img_path = os.path.join(img_dir, 'test.jpg')

res_dir = '/Users/evnw/Programming/Colors/Smart-Colors/Color_Identification/Test_img'

class Color:
	
	def __init__(self, num, BGR):
		self.BGR = BGR
		self.num = num
		self.dist = np.sqrt(BGR[0]**2 + BGR[1]**2 + BGR[2]**2)
		self.Blue = BGR[0]
		self.Green = BGR[1]
		self.Red = BGR[2]

	def calc_dist(self, Color):
		dist = np.sqrt((int(self.Blue)-int(Color.Blue))**2 + (int(self.Green)-int(Color.Green))**2 + (int(self.Red)-int(Color.Red))**2)
		return dist

def color_recognition(im):

	# RGB2BGR
	im = im[...,::-1]
	im_s = cv2.resize(im, (15, 15))

	background = find_background(im_s)

	#print(background)

	# KMeans
	im_arr = im_s.reshape((im_s.shape[0] * im_s.shape[1], 3))
	kmeans.fit(im_arr)
	colors = kmeans.cluster_centers_.astype(np.uint8)                                 #BGR
	labels = kmeans.labels_

	# Create color class
	color_array = []
	for i in range(10):
		color_temp = Color(len(np.where(labels==i)[0]), colors[i])
		color_array.append(color_temp)

	# find number of significant colors
	color_res, color_num = color_filter(color_array)

	kmeans_res = KMeans(color_num)
	kmeans_res.fit(im_arr)
	colors_final = kmeans_res.cluster_centers_.astype(np.uint8)

	#plt.imshow([colors_final]);plt.show()

	min_dist = 999999
	closest_BGR_index = None

	for i in range(len(colors_final)):
		color_BGR = colors_final[i]
		dist = np.sqrt((int(color_BGR[0] - int(background[0])))**2 + (int(color_BGR[1] - int(background[1])))**2 + (int(color_BGR[2] - int(background[2])))**2)
		if dist < min_dist:
			min_dist = dist
			closest_BGR_index = i

	colors_final = np.delete(colors_final, closest_BGR_index, 0)


	#plt.imshow([colors_final]);plt.show()

	#print(colors_final)

	return colors_final

def color_filter(color_array):

	distant_color_num = 0
	res = []
	current = Color(500, [0,0,0])

	while len(color_array) > 0:

		closest_color = None
		min_dist = 9999999

		for color in color_array:
			dist = current.calc_dist(color)
			#dist = current.calc_dist(color)
			if (dist < min_dist):
				min_dist = dist
				closest_color = color

		if min_dist >= 50:
			distant_color_num += 1
		if current.num == 500 and min_dist < 50:
			distant_color_num += 1


		res.append(closest_color)
		current = closest_color
		color_array.remove(closest_color)

	return res, max(distant_color_num - 1, 1)



def find_background(im):
	edge_BGRs = im[0,:]+im[:,0]

	kmeans_background = KMeans(2)
	kmeans_background.fit(edge_BGRs)
	labels = kmeans_background.labels_
	if len(np.where(labels == 0)[0]) > len(np.where(labels == 1)[0]):
		index = 0
	else:
		index = 1

	return kmeans_background.cluster_centers_[index]


def create_xml(colors, url):
	root = ET.Element("Outfit")
	link = ET.SubElement(root, 'link')
	dom_colors = ET.SubElement(root, 'dom_colors')
	ET.SubElement(link, "url").text = "{}".format(url)
	for color_BGR in colors:
		color = ET.SubElement(dom_colors, "color")
		ET.SubElement(color, "blue").text = "{}".format(color_BGR[0])
		ET.SubElement(color, "green").text = "{}".format(color_BGR[1])
		ET.SubElement(color, "red").text = "{}".format(color_BGR[2])
	tree = ET.ElementTree(root)

	xml_path = os.path.join(res_dir, 'test.xml')
	tree.write(xml_path)


if __name__ == '__main__':
	main()
'''
	url = img_path                                              # need change
	im = cv2.imread(img_path)

	tm = time.time() #---------------------------------------------------------

	dominant_colors = color_rec(im)
	create_xml(dominant_colors, url)

	print(time.time() - tm) #--------------------------------------------------'''

	