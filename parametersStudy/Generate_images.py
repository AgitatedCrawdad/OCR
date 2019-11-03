#####################################################
'''

This is a direct copy of generate_distortedDOE to test a few things. I will push what i have now, then
i will make the necessary changes to generate_distortedDOE and push again to get a history incase something goes wrong.

Here i was testing the new image_class i made that assigns the image, text, and parameters to each individual image. This
will be helpful in post processing where we can use all this data. I also made the variance in parameters almost unity to reduce  runtime.
Yes i know Spyder would be helpful here, i will download it. But i do like pycharm... ),;

This should probably be cleaned up a little, but i think its fine. The functions to modify an image should probably be in some sort of
user package to clean up this script. Maybe i'll do that during the Rockets game...


'''
#####################################################

import cv2
from Scan.scan import scan
import os
import numpy as np
from parametersStudy.image_class import image_ocr



def erode(kernel_size, iterations, image):

    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded = cv2.erode(image, kernel, iterations=iterations)


    return eroded


def dilate(kernel_size, iterations, image):

    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv2.dilate(image, kernel, iterations=iterations)

    return dilated


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def thresholding(image, blocksize, thresh_type, constant):

    grayscaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if thresh_type == 'gaussian':
        binarized = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, constant)

    else:
        binarized = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize,
                                          constant)

    return binarized


def write_image(out_folder, o_filename, image):
    o_filename = o_filename[:-4]
    file_name = o_filename + '.jpg'
    path = out_folder + '/' + file_name
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    cv2.imwrite(path, image)


def generate_images(image, name):
    #lists to iterate over :)
    kernel_list = range(3, 4, 2)
    iterations = range(1, 3, 1)
    width_list = range(400, 600, 100)
    blocksize_list = range(51, 202, 100)
    constant_list = range(1, 18, 9)
    thresh_type = ['mean']

    #initialize variables
    original_name = name + '_generated_images'
    property_dict = {'erode_kernel':1, 'erode_iter':2, 'dilate_kernel':3, 'dilate_iter':4,
                           'width':5, 'blocksize':6, 'constant':7, 'thresh_type':'temp'}
    images_generated_b = []
    images_generated_s = []



    #start the iterations and assign new image class

    image = cv2.imread(image)
    for kernel in kernel_list:
        property_dict['erode_kernel'] = kernel
        for iteration in iterations:
            try:
                property_dict['erode_iter'] = iteration
                eroded = erode(kernel, iteration, image)

                for kernel_dilate in kernel_list:
                    property_dict['dilate_kernel'] = kernel_dilate
                    for iteration_dilate in iterations:
                        property_dict['dilate_iter'] = iteration_dilate
                        dilated = dilate(kernel_dilate, iteration_dilate, eroded)
                        for width in width_list:
                            property_dict['width'] = width
                            image_resized = image_resize(dilated, width=width)
                            for blocksize in blocksize_list:
                                property_dict['blocksize'] = blocksize
                                for constant in constant_list:
                                    property_dict['constant'] = constant
                                    for thresh in thresh_type:
                                        property_dict['thresh_type'] = thresh
                                        binarized = thresholding(image_resized, blocksize, thresh, constant)
                                        image_b = assign_image(binarized, property_dict)
                                        print('assigning image')
                                        try:
                                            scannedname, scanned_image = scan(binarized)
                                            print('assigning image')
                                            image_s = assign_image(scanned_image, property_dict)
                                        except:
                                            'Could not find the contours...'
                                        images_generated_b.append(image_b)
                                        images_generated_s.append(image_s)
            except:
                print('image could not be eroded')

    images = images_generated_b + images_generated_s

    return images


def assign_image(image, property_dict):

    temp_image = image_ocr()
    temp_image.add_image(image)
    temp_image.add_text()
    for key, value in property_dict.items():
        temp_image.add_property(key, value)
    return temp_image


def main(folder_of_images):


    for filename in os.listdir(folder_of_images):

        path = folder_of_images + '/' + filename
        name = filename[:-4]
        images = generate_images(path, name)


    return images


if __name__ == '__main__':
    main(r'test_images')




