import os
import cv2
from zipfile import ZipFile
from os.path import basename

def save_images(images, folder_name="media"):
    if not os.path.exists(path=folder_name):
        os.mkdir(path=folder_name)

    f_name = f"{folder_name}/count_of_same_sample.txt"
    if not os.path.exists(f_name):
        with open(f_name, 'w') as f:
            f.write("0")
    
    count_of_same_images = int(open(f_name, 'r').readline().rstrip('\n'))
    for idx, image in enumerate(images):
        cv2.imwrite(f"{folder_name}/{count_of_same_images}_{idx}.jpg", image)

    open(f_name, 'w').write(str(count_of_same_images + 1))

def create_zip(dirName):
    with ZipFile('images.zip', 'w') as zipObj:
        for folderName, _, filenames in os.walk(dirName):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
