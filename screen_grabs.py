from PIL import Image
from desktopmagic.screengrab_win32 import getDisplaysAsImages
import time
import datetime
import os
def spawn_capture(temp_im_dir,perm_tex_dir): ## independant process for taking screen captures
    #print('screen capture')
    original = 10
    seconds_between = original
    end = 'GO'
    gigabyte = 1073741824
    while True:
        enlarge_factor = 4
        now = datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S")
        im_name = temp_im_dir+now
        ############get im
        im_names = []
        start = time.time()
        if end == 'GO' or start - end > seconds_between -5 :
            for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
                enlarge_factor = 4
                #print(displayNumber)
                width, height = im.size
                if int(width*enlarge_factor) < 5600 or int(height*enlarge_factor) < 3200:
                    enlarge_factor = enlarge_factor + 1
                width = int(width*enlarge_factor)
                height = int(height*enlarge_factor)
                new_size = width, height
                im_resized = im.resize(new_size, Image.ANTIALIAS)
                im_resized.save(im_name+'_'+str(displayNumber)+'.png')
                im_names.append(im_name+'_'+str(displayNumber)+'.png')
                end = time.time()
		############
        bytes_in_temp_im_dir = sum(os.path.getsize(temp_im_dir) for f in os.listdir('.') if os.path.isfile(f))
        if bytes_in_temp_im_dir > gigabyte:
            seconds_between = seconds_between + 5
        else:
            seconds_between = original
    
    
    
    
    '''
    #print('screen capture')
    original = 10
    seconds_between = original
    end = 'GO'
    gigabyte = 1073741824
    while True:
        enlarge_factor = 4
        now = datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S")
        im_name = temp_im_dir+now
        ############get im
        im_names = []
        start = time.time()
        if end == 'GO' or start - end > seconds_between -5 :
            for displayNumber, im in enumerate(getDisplaysAsImages(), 1):
                should_enlarge = True
                enlarge_factor = 4
                #print(displayNumber)
                width, height = im.size
                while should_enlarge == True:
                    if int(width*enlarge_factor) < 5600 or int(height*enlarge_factor) < 3200:
                        enlarge_factor = enlarge_factor + 1
                    else:
                        should_enlarge = False
                    width = int(width*enlarge_factor)
                    height = int(height*enlarge_factor)
                    
                        
                new_size = width, height
                im_resized = im.resize(new_size, Image.ANTIALIAS)
                im_resized.save(im_name+'_'+str(displayNumber)+'.png')
                im_names.append(im_name+'_'+str(displayNumber)+'.png')
                end = time.time()
		############
        bytes_in_temp_im_dir = sum(os.path.getsize(temp_im_dir) for f in os.listdir('.') if os.path.isfile(f))
        if bytes_in_temp_im_dir > gigabyte:
            seconds_between = seconds_between + 5
        else:
            seconds_between = original
        '''