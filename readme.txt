The following package contains the work that has been done as the course project of Multimedia Systems. 

The following package contains the following files and folders+

/final
	|- /emotion=detection : Folder for emotion detection. 
	|- /input : Folder for giving the input.
	|- /output : Folder where output images are saved.
	|- main.py : Main wrapper function that implemens and gets called for the application.
	|- emd.py : Python file for calculating the EMD(Earth Movers Distance)
	|- obj_detect.py : Python file for object detection in image.
	|- get_time.py : Python file that gives the timestamp information.
	|- blur_detection.py : Function that returns the bluriness level of the image.
	|- cv_close_eye_detect.py : Function that returns whether the eyes in the photo are closed or open.

Download and copy resnet50_coco_best_v2.0.1.h5 to the project directory for the object detection.

How to run this package : Open terminal and type "python3 main.py input/"

Output of the package : Output will be written in an output folder.

----------------------------------------------------------------------
