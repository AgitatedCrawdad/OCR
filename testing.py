import os
import sys
import cv2
from PIL import Image
import pytesseract
from image_class import image_ocr


def process_directory(folder):
    for file_name in os.listdir(folder):
        if not file_name.startswith('.'):
            print(file_name)


'''


########################################################################################################
For erode and dilation we can iterate over two parameters: iterations and kernel

Kernel would require maybe 2 options (3x3, or 5x5, maybe 7x7). Once again lack of image processing
knowledge is a hindrance.

Iterations is how much you want to erode/dilate

I would image that we would want to have this fairly low because of how compact and small the characters
already are
########################################################################################################


########################################################################################################
For image resize we can iterate over just one parameter and its just defined as
what we want the width to be and will basically "drag the corner" of the image to reach that width.

Can be pretty flexible here - maybe 10 iterations from small to big.
########################################################################################################

########################################################################################################
For thresholding we can iterate over two variables (maybe 3 if changed the thresholding type)

I'm sticking with Gaussian for now and we can change later. Every example ive seen with adaptive thresholding
has used Gaussian so I'm sticking with that.

Blocksize: Size of a pixel neighborhood that is used to calculate a threshold value. Can be pretty generous
here, especially since we are changing the size of the image from big to small here we can try to have the
largest blocksize be equal to the size of the smallest image. (maybe 10-15 iterations here)

Constant: A constant value that is subtracted from the mean or weighted sum of the neighbourhood pixels.
Has to be an odd number and ive seen them mostly being fairly small but i dont really know. Can be flexible,
maybe 20 iterates from 3 to 43? (or more)
########################################################################################################


'''
def testing_writing(in_folder, out_folder):
    for filename in os.listdir(in_folder):
        name = filename[:-4]
        out_path = out_folder + '/' + name
        print (out_path)
        print (name)


parameters =[['green', 'yellow', 'red'], ['one', 'two', 'three'], ['hot', 'cold', 'neutral']]

'''
class image_ocr:

    def __init__(self):
        self.properties = {'erode_kernel':None, 'erode_iter':None, 'dilate_kernel':None, 'dilate_iter':None,
                           'width':None, 'blocksize':None, 'constant':None, 'thresh_type':None}
        self.text = ''

    def add_property(self, property, value):
        if property in self.properties.keys():
            self.properties[property] = value
        else:
            print('this is not a valid property')

    def add_text(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        im = im_pil
        self.text = pytesseract.image_to_string(im)
'''

'''
dictionary = {'smile':1, 'frown':2, 'indifferent':3}
for key, value in dictionary.items():
    print(key, value)
'''

def string_count(paragraph):
    count = 0
    for line in paragraph:
        for word in line:
            if len(word) > 1:
                count = count+1
            else:
                continue
    return count

if __name__ == '__main__':

    paragraph = [['this', 'is' 'a', 'test'], ['a', 'b', 'c', 'word'],['complete', 'more','no']]

    word_count = string_count(paragraph)
    temp_image = image_ocr()
    temp_image.add_string_count(word_count)
    print(temp_image.string_count)



