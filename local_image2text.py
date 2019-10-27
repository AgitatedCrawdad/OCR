from PIL import Image
import pytesseract
import cv2
import numpy



#invokes tesseract and saves text to a .txt file
def ocr_core(filename):
    #Function to read the text from an image


    #i dont think tesseract can interperate an array so i convert from opencv
    #format to PIL format

    img = cv2.cvtColor(filename, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    im = im_pil

    #resize image because tesseract is picky. this can probably still be tweaked
    im = image_resize_pil(im, 400)

    #invoke tesseract and save text to file
    text = pytesseract.image_to_string(im)
    # Save text to a text file
    file = open('testing.txt', 'w')
    file.write(text)
    file.close()

    return text



#the next two functions binarize an image using numpy and PIL which is indirect and takes too long
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

#Execute tesseract
#text = ocr_core(r'receipts/scanned.jpg')


#Save text to a text file
#file = open('testing.txt', 'w')
#file.write(text)
#file.close()




#list_of_lines = []




#read the text from the text file
#To parse the data correctly i had to read it line by line from a textfile
#reading line by line simply from the tesseract did not return what i wantd
def read_text(filename):
    text = ocr_core(filename)
    with open('testing.txt','r') as handle:
        #parses the data by line and by space
        list_of_lines = []
        for line in handle:
            test = line.split()
            if not test:
                print(" ")
            else:
                #makes a list of parsed lines
                list_of_lines.append(test)

    print(list_of_lines)
    print(list_of_lines)
    return list_of_lines



def list_to_dict(list):
    #function to make a dictionary of based on item and amount
    #ex. "burrito":7.29, "tax":0.95"
    #just one thought i had on being able to parse the correct data
    #this has to be used in conjunction with the del_int function
    dict_i = {}
    dict_f = {}
    for item in list:
        if len(item) > 1:

            price = item[-1]
            purchased = item[-2]
            if '$' in price:
                price = price[1:]
                print(price)
            else:
                price = price

            try:
                dict_f[purchased] = float(price)

            except:
                pass
                #print('not a float')
            try:
                dict_i[purchased] = int(price)
            except:
                pass
                #print('not an integer')
        else:
            print('only one item in line')
    return (dict_i, dict_f)


def del_int(dict_i, dict_f):
    #function to delete any key value pairs that contained an integer and not a float
    #the idea here is that all prices will be in the x.xx form so will be a float.
    #if there is a value that can be an integer then it will not be a price and should
    #be deleted. for ex. the area codes may be included and need to be deleted.
    for (k,v) in dict_i.items():
        dict_f.pop(k, None)
    return (dict_f)


#function to resize an image but keep the same aspect ratio (drag corners) in opencv
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


#same function as above but for PIL
def image_resize_pil(image, width):
    basewidth = width
    wpercent = (basewidth / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(wpercent)))
    image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    image.show()
    return image

#reads in an image and binarizes it. then converts to RGB and then converts to
#PIL format for the scan function (i might be able to get around the reconverting, but i'd
#have to look more into the scan function
def binarize_cv(filename, threshold):

    img = cv2.imread(filename)
    grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval2, threshold2 = cv2.threshold(grayscaled, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.cvtColor(threshold2, cv2.COLOR_GRAY2RGB)
    image_b = Image.fromarray(img)

    return image_b


#calls the necessary functions
def run(filename):
    list_of_lines = read_text(filename)
    dictionary_i, dictionary_f = list_to_dict(list_of_lines)
    final_dictionary = del_int(dictionary_i, dictionary_f)
    print(final_dictionary)


#run(r'receipts/scanned.jpg')

