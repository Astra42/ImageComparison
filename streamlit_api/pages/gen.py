from utils import create_zip, save_images
from over_liner import make_random_images
import streamlit as st
from random import randint
import os


images_count = st.text_input("write a number of image pairs", value=1)

percent = st.slider("choose a percent of identify", min_value=0.0, max_value=1.0)
elem_count = st.text_input("write an elem of images", value=20)
form_count =  st.text_input("write a form count", value=5)

result = st.button("create image pares")

os.system("rm -rf media/*")
if result and elem_count and form_count:
    elem_count = int(elem_count)
    images_count = int(images_count)
    form_count = int(form_count)
    for _ in range(images_count):
        shapes_count = randint(10, 100)

        images = make_random_images(count=elem_count, percent=percent, form_count=form_count)
        # while len(images) != 2:
        #     images = make_random_images((500, 500, 3), shapes_count, percent)
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
