from image_comparison import Images_comparison
import streamlit as st
import matplotlib.image as mpimg
import numpy as np
import cv2
import os


def compare_images(img1, img2):
    comparison = Images_comparison(img1, img2)
    st.write(f"SSIM: {comparison.find_SSIM()}")
    st.write(f"Similarity: {comparison.bin_mask_fullness()}")
    m = comparison.binary_masks(use_m_filt=True)
    mpimg.imsave("out.jpg", m[0])
    st.image("out.jpg")
    # st.write(m[0].shape)


def convert_bytes_to_images(files):
    images = []
    for idx, file in enumerate(files):

        image_np = np.frombuffer(file.read(), np.uint8)
        img_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)  
        
        images.append(img_np)
        cv2.imwrite(f"img{idx}.jpg", img_np)
    return images
    

images = st.file_uploader(label="choose images to compare", accept_multiple_files=True)

if len(images) == 2:
    col1, col2 = st.columns(2)
    img1, img2 = convert_bytes_to_images(images)

    col1.image("img0.jpg")
    col2.image("img1.jpg")
    compare_images("img0.jpg", "img1.jpg")
else:
     os.system("rm -rf img0.jpg img1.jpg")
