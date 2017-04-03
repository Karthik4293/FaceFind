
import cv #Opencv
import Image #Image from PIL
import glob
import os
from sys import argv
import APIConnect

#As the name suggests, this function detects face in the given image
def DetectFace(image, faceCascade, returnImage=False):

    #variables
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Equalize the histogram
    cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.HaarDetectObjects(
            image, faceCascade, cv.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

#To convert a PIL image to Grayscale
def pil2cvGrey(pil_im):
    pil_im = pil_im.convert('L')
    cv_im = cv.CreateImageHeader(pil_im.size, cv.IPL_DEPTH_8U, 1)
    cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0]  )
    return cv_im

# Convert the CV image to a PIL image
def cv2pil(cv_im):
    return Image.fromstring("L", cv.GetSize(cv_im), cv_im.tostring())

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]

    # Calculate scale factors
    xDelta=max(cropBox[2]*(boxScale-1),0)
    yDelta=max(cropBox[3]*(boxScale-1),0)

    # Convert cv box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xDelta, cropBox[1]-yDelta, cropBox[0]+cropBox[2]+xDelta, cropBox[1]+cropBox[3]+yDelta]

    return image.crop(PIL_box)


def faceCrop(img,boxScale=1):
    faceCascade = cv.Load('haarcascade_frontalface_alt.xml')

    if len(img)<=0:
        print 'No Images Found'
        return

    pil_im=Image.open(img)
    cv_im=pil2cvGrey(pil_im)
    faces=DetectFace(cv_im,faceCascade)
    if faces:
        n=1
        for face in faces:
            croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
            fname,ext=os.path.splitext(img)
            croppedImage.save(fname+str(n)+ext)
            n+=1
    else:
        print 'No faces found:', img
    APIConnect.get_data(str(argv[1]))

faceCrop(str(argv[1])+".jpg",boxScale=1)
