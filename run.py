import local_image2text as i2p
from scan import scan


if __name__ == '__main__':

    image_path = i2p.binarize_image(r'receipts/tjoes_3.jpg',150)
    scanned_image_name = scan(image_path)
    i2p.run(scanned_image_name)