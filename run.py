import local_image2text as i2p
from scan import scan


if __name__ == '__main__':

    scanned_image_name = scan(r'receipts/thai.jpg')
    i2p.run(scanned_image_name)