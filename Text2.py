import pytesseract
import cv2
import numpy as np
import urllib
import requests
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

url = 'https://live.staticflickr.com/3432/3716692151_c5a162551d_b.jpg'

img = url_to_image(url)


#This line alters the original image to be binarized according to a certain threshold.
retval, img = cv2.threshold(img,110,255, cv2.THRESH_BINARY)
#This line resizes the image, resizing makes a big impact on readability, want big but not too big
img = cv2.resize(img,(0,0),fx=4,fy=4)
#This line blurs edges
#img = cv2.GaussianBlur(img,(11,11),0)
#Im not entirely sure what this what does, but believe it also blurs edges
#img = cv2.medianBlur(img,9)

cv2.imshow('asd',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
txt = pytesseract.image_to_string(img)
print(txt)