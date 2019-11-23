#imports
import get_time
import os
import obj_detect
from datetime import datetime
import emd
import blur_detection
import cv_close_eye_detect
import shutil
import sys

#the input folder
dirPath = sys.argv[1]

#filtering out those pics which does not have any person 
#input : image list
#output : image list with "no person images" removed
#This function is using obj_detect.py which is placed in same directory
def filter_persons(imageList):
	for im in imageList:
		imagePath = dirPath + im
		objects = obj_detect.getObjects(imagePath)
		vv = "person"
		if vv not in objects:
			imageList.remove(im)
	return imageList		


#input: time stamps of all images
#output: clusters of images with close time stamps clustered together
def is_close_time_image(timestamp_dictionary, time_info):
	for time_data in timestamp_dictionary.keys():
		d1 = datetime.strptime(time_data, "%Y:%m:%d %H:%M:%S")
		d2 = datetime.strptime(time_info, "%Y:%m:%d %H:%M:%S")
		time_gap = None
		if d1 > d2:
			time_gap = d1-d2
		else:
			time_gap = d2-d1
		if time_gap.seconds < 120:
			return time_data
	return None

#remove the pics which contains even a single person with closed eye
def remove_closed_eyes(clustered_images):
	for im in clustered_images:
		for i in im:
			impath = dirPath+i
			ans = cv_close_eye_detect.are_eyes_open(impath)
			if ans=='no eyes': 
				if len(im)==1:
					clustered_images.remove(im)
				else:	
					im.remove(i)
	return clustered_images				


#modifying clusters so that same person with same environment remains in same cluster
def getClustersAfterRemovingSimilar(clustersImages,threshold):
	distance_list= []
	print(clustersImages)
	for imageList in clustersImages:
		print(imageList)
		new_clusters = []
		for images in imageList:
			for comparision_images in imageList:
				if images in new_clusters:
					continue
				elif comparision_images in new_clusters:
					continue
				elif images == comparision_images:
					continue
				else:
					distance = emd.get_similarity_measure(dirPath + images, dirPath + comparision_images)
				
				if distance > threshold:
					new_clusters.append(comparision_images)

		for new_images in new_clusters:
			print(new_images)
			imageList.remove(new_images)
		if(len(new_clusters)!=0):
			clustersImages.append(new_clusters)

	return clustersImages




#reading images
imageList = os.listdir(dirPath)
not_to_include = ".DS_Store"
if not_to_include in imageList:
	imageList.remove(not_to_include)
imageList = filter_persons(imageList)
print(imageList)

#taking timestamp of every pic into consideration
timestamp_dictionary = {}
for image in imageList:
	imagePath = dirPath + image
	time_info = get_time.get_exif(imagePath)
	nearest_time = is_close_time_image(timestamp_dictionary, time_info)
	if nearest_time == None:
		timestamp_dictionary[time_info] = [image]
	else:
		timestamp_dictionary[nearest_time].append(image)

	# print(get_time.dict['DateTimeOriginal'])
	#obj_detect.getObjects(imagePath)
#print(timestamp_dictionary)
clustersImages = list(timestamp_dictionary.values())
print("similarity check")
clustered_images = getClustersAfterRemovingSimilar(clustersImages,0.001)
print("similarity check done")

final_image_list=list()

clustered_images = remove_closed_eyes(clustered_images)


#finding the blurriness value and for the project purpose the one with minimumm blurriness is preferred.
for im in clustered_images:
	print(im)
	min = 500
	min_path = ""
	for i in im:
		impath = dirPath+i
		blur_value = (blur_detection.find_blurriness(impath))
		if(blur_value<min):
			min = blur_value
			min_path = impath		
	final_image_list.append(min_path)		

print(final_image_list)


for file_name in final_image_list:
	shutil.copy(file_name, './output/')