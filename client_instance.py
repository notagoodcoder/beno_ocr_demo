###third
import os
from multiprocessing import Process
from os import listdir
from os.path import isfile, join
#import urllib2
###first
from screen_grabs import *
from image_to_text import *
from text_search import *
from key_scrape import *
###

def make_storage_dirs(all_dirs):
    for dir in all_dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
            
def clear_all_dirs(all_dirs):#test function for cleanup
    for folder in all_dirs:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)	
            except Exception as e:
                pass 
def getMacAddress(): 
    if sys.platform == 'win32': 
        for line in os.popen("ipconfig /all"): 
            if line.lstrip().startswith('Physical Address'): 
                mac = line.split(':')[1].strip().replace('-',':') 
                break 
    else: 
        for line in os.popen("/sbin/ifconfig"): 
            if line.find('Ether') > -1: 
                mac = line.split()[4] 
                break 
    return mac
    
def parse_licenses():#should be in same dir as app running
    cur_dir = os.getcwd()
    #print()

    with open(cur_dir+'\\search_config.txt') as f:
        for line in f:
            line = line.strip().split(',')
            if 'keywords' in line:
                line.remove('keywords')
                keywords = line
            if 'phrases' in line:
                line.remove('phrases')
                phrases = line
            if 'urls' in line:
                line.remove('urls')
                urls = line
    return keywords,phrases,urls
    
def main():
    search_info = parse_licenses()
    keywords = search_info[0]
    phrases = search_info[1]
    urls = search_info[2]
    cur_dir = os.getcwd()
	##dev_sec rem prod
    arch_tex_dir = cur_dir+'\\arch_text_storage\\'#### change in write strokes as well --> exception
    temp_im_dir = cur_dir+'\\temporary_image_storage\\'
    perm_tex_dir = cur_dir+'\\permanent_text_storage\\'
    interest_dir = cur_dir+'\\interest_storage\\'
    im_dir = cur_dir+'\\image_storage\\'
    all_dirs = [temp_im_dir,perm_tex_dir,interest_dir,im_dir,arch_tex_dir]
    make_storage_dirs(all_dirs)
    clear_all_dirs(all_dirs)
    
    


	
    
    while True:
        p1 = Process(target = spawn_capture , args = (temp_im_dir,perm_tex_dir))
        p1.start()
        p2 = Process(target= analyze_capture,args = (temp_im_dir,perm_tex_dir,im_dir))
        p2.start()
        p3 = Process(target= search_text,args = (keywords,phrases,urls,perm_tex_dir, im_dir, interest_dir,arch_tex_dir))
        p3.start()
        #p4 = Process(target= get_strokes,args = ())
        #p4.start()
        p1.join()
        p2.join()
        p3.join()
        #p4.join()
        

if __name__ == "__main__":
	main()
	
