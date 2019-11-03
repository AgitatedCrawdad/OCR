import parametersStudy.Generate_images
import os
import cv2
import json
import enchant
import pandas as pd


def write_text(text):
    file = open('testing.txt', 'w')
    file.write(text)
    file.close()


def read_text():

    with open('testing.txt', 'r') as handle:
        # parses the data by line and by space
        list_of_lines = []
        for line in handle:
            test = line.split()
            if not test:
                continue
            else:
                # makes a list of parsed lines
                list_of_lines.append(test)

    return list_of_lines


def string_count(paragraph):

    ###################################
    #
    #This will be the function to manipulate the actual postprocessing of the text from OCR.
    #Now it is just reading every line from every image that was created.
    #
    ##################################

    accepted_words = []
    count = 0
    if paragraph:
        for line in paragraph:
            for word in line:
                if len(word) > 2 and word_check(word):
                    accepted_words.append(word)
                    count = count+1
                else:
                    continue
    else:
        "The text is empty"


    return count, accepted_words


def word_check(word):
    d = enchant.Dict('en_US')
    is_word = d.check(word)

    return is_word


def write(image,index,type):

    #################################
    #
    #Creates a new directory called 'best_distorted' if not already made
    #and stores the 'best' 10 images along with its OCR read text
    #
    ################################

    path = r'best_distorted/image' + str(index) + '_' + type

    if not os.path.exists('best_distorted'):
        os.mkdir('best_distorted')

    if not os.path.exists(path):
        os.mkdir(path)

    cv2.imwrite(path+r'/image.png', image.image)
    file = open(path+r'/text_' + str(image.string_count) + '.txt', 'w')
    file.write(image.text)
    file.write("\n ---------------------------------------------------------------\n")
    file.write(json.dumps(image.properties))
    file.write("\n ---------------------------------------------------------------\n")
    file.write(json.dumps(image.words))
    file.close()
    print('wrote file')


def stats(images):

    #########################################
    #
    #Function in an attempt to get some numbers.
    #I would really like to see how matching pairs there are but that would be an entire python library
    #in itself so i wont do that. Firstly i'll return how many are scanned vs binarized, then how many
    #scanned and gaussian type or mean and the opposite. This will only be for the accepted list as well(top X)
    #
    #########################################

    prop_list = []

    prop_list = [image.properties for image in images]
    word_count_list = [image.string_count for image in images]

    df = pd.DataFrame(prop_list)
    df['word count'] = word_count_list
    df.to_csv('parameters.csv', index=False)

    def sum_mask_numpy(column, value, scanned=True):

        return ((column == value) & (df.scanned == scanned)).sum()


    scanned_mean = sum_mask_numpy(df.thresh_type, 'mean')
    scanned_gaus = sum_mask_numpy(df.thresh_type, 'gaussian')


    binarized_mean = sum_mask_numpy(df.thresh_type, 'mean', scanned=False)
    binarized_gaus = sum_mask_numpy(df.thresh_type, 'gaussian', scanned=False)


    print('scanned mean: %s' % scanned_mean)
    print('scanned gaus: %s' % scanned_gaus)
    print('binarized mean: %s' % binarized_mean)
    print('binarized gaus: %s' % binarized_gaus)




def main():

    #################################
    #
    #Calls the generate images script to generate a ton of images.
    #Then the text is stored in a text file and then read back in line by line.
    #If the text is not empty then it calls a string count function which needs to be developed
    #more.
    #
    #################################

    images = Generate_images.main('throw_away_dir')
    best_images =[]

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

    test = sorted(range(len(images)), key=lambda i: images[i].string_count)[-15:]

    for index in test:
        write(images[index], index, 'indif')
        best_images.append(images[index])



    return images, best_images


if __name__ == '__main__':

    images, best_images = main()
    stats(best_images)




