import local_image2text as i2p
from scan import scan
from datetime import datetime
import cv2
from PIL import Image

'''
Binarizes the initial pictures, scans it into a specific format, resizes the image,
then tesseract is called to read the text. The text, scanned, and binarized pictures are all saved
as outputs in the directory. The text parsing here is generally just for me so i can get an idea of
how tesseract is reading. I'll probably move that somewhere else.


Also the 2 commented lines can track the time to execute this script.
'''


if __name__ == '__main__':
    #startTime = datetime.now()


    filename = r'receipts/tjoes_1.jpg'
    threshold = 150


    image_b = i2p.binarize_cv(filename, threshold)
    scanned_image_name, image = scan(image_b)
    i2p.run(image)

    #print(datetime.now()-startTime)