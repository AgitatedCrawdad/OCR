'''
This script will
    1) Take an image or multiple images
    2) Loop through a set of parameters to generate a few options for the OCR
    3) Select the 'best' image based on custom criteria
    4) This 'best' image(s) will then be fed to a parsing script

'''


from parametersStudy.image_class import image_ocr
from parametersStudy.Generate_images import image_resize, thresholding, assign_image, erode, dilate
from parametersStudy.postprocessing import write_text, read_text, string_count, word_check
import sys, os
import cv2, enchant, pytesseract
import numpy as numpy


def generate_images(path):
    #parameters to iterate over :)
    widths = range(550, 850, 50)
    blocksizes = range(51, 152, 20)
    constants = range(3, 25, 2)

    images = []
    property_dict = {'erode_kernel':3, 'erode_iter':1, 'dilate_kernel':3, 'dilate_iter':1,
                           'width':5, 'blocksize':6, 'constant':7, 'thresh_type':'gaussian'}

    image = cv2.imread(path)

    try:
        image = erode(property_dict['erode_kernel'], property_dict['erode_iter'], image)
        image = dilate(property_dict['dilate_kernel'], property_dict['dilate_iter'], image)
    except:
        print('image could not be eroded')

    c=0
    for width in widths:
        property_dict['width'] = width
        resized = image_resize(image, width=width)
        for blocksize in blocksizes:
            property_dict['blocksize'] = blocksize
            for constant in constants:
                property_dict['constant'] = constant
                binarized = thresholding(resized, blocksize, property_dict['thresh_type'], constant)
                assigned = assign_image(binarized, property_dict)
                images.append(assigned)
                c=c+1
                print(c)
    
    return images


def analyze(images):


    for image in images:
        write_text(image.text)
        text = read_text()

        if text:
            count, words = string_count(text)
        
        else:
            count = 0
            print('no text in the image')
            image.add_string_count(count)
            image.add_words(words)

    selected = sorted(range(len(images)), key=lambda i: images[i].string_count)[-1]

    
    best_image = images[selected]

    return best_image
        

def main():

    if sys.argv[-1] == 'folder':
        folder = sys.argv[-2]
        for image in os.listdir(folder):
            if image.endswith('.jpg') or image.endswith('.png'):
                images = generate_images(image)
                best = analyze(images)
                print(type(best.text))
            else:
                print('image needs to be jpg or png')


    elif sys.argv[-1] == 'file':
        image = sys.argv[-2]
        if image.endswith('.jpg') or image.endswith('.png'):
            print(image)
            images = generate_images(image)
            best = analyze(images)
            print(type(best.text))
        else:
            print('image needs to be jpg or png')

    else:
        print('run format needs to be "python ocr.py /path/to/file file')
            
        


if __name__ == '__main__':
    main()


