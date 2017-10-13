import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
from os import listdir
from os.path import isfile, join
import os
import time
from PIL import Image

def analyze_capture(temp_im_dir,perm_tex_dir,im_dir): ## independant process for scraping images

    while True:
        time.sleep(2)
        onlyfiles = [f for f in listdir(temp_im_dir) if isfile(join(temp_im_dir, f)) and f not in listdir(perm_tex_dir)]
        if len(onlyfiles) > 4:
            work_on = temp_im_dir+onlyfiles[0]
            work_on_file = onlyfiles[0]
            im2 = Image.open(work_on)
            im_string = str(pytesseract.image_to_string(im2).encode('utf-8'))
            with open(perm_tex_dir+work_on_file.replace('.png','.txt'), "a") as image_string_contents:
                image_string_contents.write(im_string)
                try:
                    os.rename(work_on,im_dir+work_on_file)
                except OSError:
                    pass

