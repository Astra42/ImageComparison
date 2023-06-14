from image_comparison import Comparer
import streamlit as st
import matplotlib.image as mpimg
import numpy as np
import cv2
import os


def convert_bytes_to_images(files):
    images = []
    for idx, file in enumerate(files):

        image_np = np.frombuffer(file.read(), np.uint8)
        img_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)  

        images.append(img_np)
        cv2.imwrite(f"img{idx}.jpg", img_np)
    return images


def compare(path1, path2):
    c = Comparer(path1=path1, path2=path2)
    c.pad1 = 2
    c.pad2 = 2
    s, d, m, a, sh = c.init_compraision()
    mpimg.imsave("out.jpg", s)
    st.write(m, a, sh)
    st.image("out.jpg")



images = st.file_uploader(label="choose images to compare", accept_multiple_files=True)

if len(images) == 2:
    col1, col2 = st.columns(2)
    img1, img2 = convert_bytes_to_images(images)

    col1.image("img0.jpg")
    col2.image("img1.jpg")

    img1 = "img0.jpg"
    img2 = "img1.jpg"
    compare(img1, img2)
else:
    os.system("rm -rf img0.jpg img1.jpg out.jpg")
