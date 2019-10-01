from PIL import Image
import pytesseract



def ocr_core(filename):
    #Function to read the text from an image
    text = pytesseract.image_to_string(Image.open(filename))
    return text

#Execute tesseract
text = ocr_core('chipotle.png')


#Save text to a text file
file = open('testing.txt', 'w')
file.write(text)
file.close()


list_of_lines = []

print(text)


#read the text from the text file
#To parse the data correctly i had to read it line by line from a textfile
#reading line by line simply from the tesseract did not return what i wantd
with open('testing.txt','r') as handle:
    #parses the data by line and by space
    for line in handle:
        test = line.split()
        if not test:
            print(" ")
        else:
            #makes a list of parsed lines
            list_of_lines.append(test)


def list_to_dict(list):
    #function to make a dictionary of baed on item and amount
    #ex. "burrito":7.29, "tax":0.95"
    #just one thought i had on being able to parse the correct data
    #this has to be ised in conjection with the del_int function
    dict_i = {}
    dict_f = {}
    for item in list:
        try:
            dict_f[item[-2]] = float(item[-1])

        except:
            pass
            #print('not a float')
        try:
            dict_i[item[-2]] = int(item[-1])
        except:
            pass
            #print('not an integer')
    return (dict_i, dict_f)


def del_int(dict_i, dict_f):
    #function to delete any key value pairs that contained an integer and not a float
    #the idea here is that all prices will be in the x.xx form so will be a float.
    #if there is a value that can be an integer then it will not be a price and should
    #be deleted. for ex. the area codes may be included and need to be deleted.
    for (k,v) in dict_i.items():
        dict_f.pop(k, None)
    return (dict_f)



dictionary_i, dictionary_f = list_to_dict(list_of_lines)

final_dictionary = del_int(dictionary_i, dictionary_f)
print(final_dictionary)




