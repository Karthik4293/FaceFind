# FaceFind
 Python Script which takes in Image as an argument and crops faces out of it using OpenCV and passes it through CloudSight API to find the personality in the image 

Install OpenCV and Cloudsight library to use

Steps:
  1. Modify the credentials for Cloudsight API in the APIConnect.py file
  2. Place the image file in the current folder
  3. Run main.py with image name as argument
  
It uses OpenCV for Image processing and locates faces and crops them to create a new image. 
That image is passed to the Cloudsight API which detects the person in it.

This can be used in various applications to find name of personalities when image is available, in some combinational quiz events,etc.
