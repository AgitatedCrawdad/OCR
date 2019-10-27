import os
import sys
import cv2
from PIL import Image
import pytesseract


class image_ocr:

    def __init__(self):
        self.properties = {'erode_kernel':None, 'erode_iter':None, 'dilate_kernel':None, 'dilate_iter':None,
                           'width':None, 'blocksize':None, 'constant':None, 'thresh_type':None}
        self.text = ''
        self.image = None
        self.string_count = 0

    def add_property(self, property, value):
        if property in self.properties.keys():
            self.properties[property] = value
        else:
            print('this is not a valid property')

    def add_text(self):
        if self.image is not None:
            img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            im = im_pil
            self.text = pytesseract.image_to_string(im)
        else:
            print('First add an image with .add_image(image)')

    def add_image(self, image):
        self.image = image

    def add_string_count(self, count):
        self.string_count = count


if __name__ == '__main__':
    image = cv2.imread(r'receipts/tjoes_1.jpg')
    y = image_ocr()
    y.add_image(image)
    y.add_text()
    print(y.text)