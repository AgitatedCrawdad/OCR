'''
Comparing PIL thresholding with OpenCV for
quality and speed




Used only for testing.
'''

import cv2
from PIL import Image
import numpy
import local_image2text as i2p
from datetime import datetime
from scan import scan


img_path = r'receipts/tjoes_1.jpg'
image_threshold = 150
image_width = 700



def run(img_path,image_threshold, image_width):


    startTime = datetime.now()
    image_path, im = binarize_image(img_path, image_threshold)
    image = Image.open(image_path)
    im.save('binarized_pil.jpg')
    im.show()
    scanned_image_name, image_p = scan(image)
    cv2.imwrite('scan_pil.jpg', image_p)

    '''

    image_resize1 = image_resize_pil(image,image_width)
    image_resize1.show()
    finishTime = datetime.now()
    elapsed = finishTime - startTime
    #print(elapsed)
    scanned_image_name, image_p = scan(image_resize1)
    cv2.imshow('scan_2', image_p)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    '''






    #startTime = datetime.now()

    img = cv2.imread(img_path)
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval2, threshold2 = cv2.threshold(grayscaled, image_threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite('binarized_cv2.jpg', threshold2)


    # gaus = cv2.adaptiveThreshold(grayscaled, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 15)
    # retval, img = cv2.threshold(img, image_threshold, 255, cv2.THRESH_BINARY)




    #img = image_resize(img, width=image_width)
    #gaus = image_resize(gaus, width=image_width)
    #threshold2 = image_resize(threshold2, width=image_width)


    #finishTime = (datetime.now() - startTime)

    #cv2.imwrite('normal.jpg', threshold2)
    #cv2.imwrite('gaussian.jpg', gaus)


    #print('opencv binarize: ' + str(finishTime))
    #cv2.imshow('opencv', img)
    #cv2.imshow('gaus', gaus)
    # cv2.imshow('gray', threshold2)
    #
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img = cv2.cvtColor(threshold2, cv2.COLOR_GRAY2RGB)
    im_pil = Image.fromarray(img)


    scanned_image_name, image = scan(im_pil)
    cv2.imwrite('scan_cv2.jpg', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    return image







def image_resize_pil(image, width):
    basewidth = width
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.show()
    return image


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



def binarize_image(img_path, threshold):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    im = Image.fromarray(image)
    im_path = 'binarized.jpg'
    im.save(im_path)

    return im_path, im





def binarize_array(numpy_array, threshold=100):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

if __name__== '__main__':
    '''

    startTime = datetime.now()
    #image_path, image_b = i2p.binarize_image(r'receipts/tjoes_1.jpg', 150)
    #scanned_image_name, image = scan(image_b)
    image_b = run(img_path, image_threshold, image_width)
    #scanned_image_name, image = scan(image_b)

    i2p.run(image_b)
    print(datetime.now() - startTime)

    '''



    run(img_path, image_threshold, image_width)

