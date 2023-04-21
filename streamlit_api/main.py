from utils import create_zip, save_images
from canvas.utils import make_random_images
import streamlit as st
from random import randint
import os


percent = st.slider("choose a percent of identify", min_value=0.0, max_value=1.0)
images_count = st.text_input("write a number of images")

result = st.button("create image pares")

if result:
    os.system("rm -rf media/*")
    images_count = int(images_count)
    for _ in range(images_count):
        shapes_count = randint(10, 100)
        images = make_random_images((500, 500, 3), shapes_count, percent)
        while len(images) != 2:
            images = make_random_images((500, 500, 3), shapes_count, percent)
        save_images(images=images)
    create_zip("media")
    st.write("ready to download")

if os.path.exists("images.zip"):
    with open("images.zip", "rb") as file:
        btn = st.download_button(
                label="Download image",
                data=file,
                file_name="images.zip",
                mime="application/zip"
                )
