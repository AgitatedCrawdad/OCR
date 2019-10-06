from PIL import Image
import pytesseract
import cv2
import numpy



#invokes tesseract and saves text to a .txt file
def ocr_core(filename):
    #Function to read the text from an image
    #im = Image.open(filename)
    #im.show()
    # img = cv2.imread(filename,0)
    # retval, img = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
    # img = cv2.resize(img, (0, 0), fx=.5, fy=.5)
    # cv2.imshow('image', img)
    # cv2.waitKey(3000)

    im = binarize_image(filename, 150)
    im.save('binarized.jpg')

    #######im = Image.open(filename)



    basewidth = 400
    wpercent = (basewidth / float(im.size[0]))
    hsize = int((float(im.size[1]) * float(wpercent)))
    im = im.resize((basewidth, hsize), Image.ANTIALIAS)
    im.show()


    text = pytesseract.image_to_string(im)
    # Save text to a text file
    file = open('testing.txt', 'w')
    file.write(text)
    file.close()

    return text




def binarize_image(img_path, threshold):
    """Binarize an image."""
    image_file = Image.open(img_path)
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold)
    im = Image.fromarray(image)

    return im





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



def run(filename):
    list_of_lines = read_text(filename)
    dictionary_i, dictionary_f = list_to_dict(list_of_lines)
    final_dictionary = del_int(dictionary_i, dictionary_f)
    print(final_dictionary)


#run(r'receipts/scanned.jpg')

