#import urllib2
import re
import time
import datetime
import os
from os import listdir
from os.path import isfile, join

def search_text(keywords,phrases,urls,perm_tex_dir, im_dir, interest_dir,arch_tex_dir): 
    gigabyte = 1073741824
    archive_after_days = 10
    start = time.time()
    #print(keywords)
    while True:
        time.sleep(2)
        add_raw_url_line = []
        onlyfiles = [f for f in listdir(perm_tex_dir) if isfile(join(perm_tex_dir, f))]
        for f in onlyfiles:
            did_break = False
            f1 = open(perm_tex_dir+f).read().split()
            any_words = []
            any_urls = []
            phrase_found = []
            for line in f1:
                holder = percentage_word_match_2(keywords, line, 0.8)
                if len(holder)!= 0:
                    any_words.extend(holder)
                holder_urls = percentage_word_match_2(urls,line, 0.8)
                if len(holder_urls)!= 0:
                    any_urls.extend(holder_urls)
                
                for phrase in phrases:
                    words_in_phrase = phrase.split(' ')
                    report_words = percentage_word_match_2(words_in_phrase,line, 0.8)
                    count = 0
                    for report in report_words:
                        if report in words_in_phrase:
                            count = count + 1
                    if count/len(words_in_phrase) > 0.8:
                        phrase_found.extend(phrase)
                        

            if len(any_words) != 0:
                did_break = True
                print(any_words)
            if len(any_urls) != 0:
                did_break = True
                print(any_urls)
            if len(phrase_found) !=0:
                did_break = True
                    
            if did_break == True:
                try:
                    os.rename(im_dir+f.replace('.txt','.png'),interest_dir+f.replace('.txt','.png'))
                except OSError:
                    pass
                try:
                    os.rename(perm_tex_dir+f,interest_dir+f)
                except OSError:
                    pass

            else:
                try:
                    os.remove(im_dir+f.replace('.txt','.png'))
                except OSError:
                    pass
                try:
                    os.remove(perm_tex_dir+f)
                except OSError:
                    pass

        
        end = time.time()
        if start - end > 60*60:
            #all_search_items = check_for_update(_slk,keywords,phrases,urls)
            if all_search_items != False:
                keywords = all_search_items[0]
                phrases = all_search_items[1]
                urls = all_search_items[2]
            
            archive_text(arch_tex_dir,im_dir)
            start = time.time()
        
def archive_text(arch_tex_dir,im_dir):        
    bytes_in_im_dir = sum(os.path.getsize(im_dir) for f in os.listdir('.') if os.path.isfile(f))
    if bytes_in_im_dir > gigabyte: 
        onlyfiles = [f for f in listdir(im_dir) if isfile(join(im_dir, f))]
        pattern = "%Y-%m-%d_%H_%M_%S"
        for f in onlyfiles:
            if '.png' in f:
                date_time = f.replace('.png','')
                epoch_then = int(time.mktime(time.strptime(date_time, pattern)))
                epoch_now = int(time.mktime(time.strptime(datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S"), pattern)))
                if epoch_now - epoch_then > archive_after_days*86400:
                    try:
                        os.remove(im_dir+f)
                    except OSError:
                        pass
            elif '.txt' in f:
                date_time = f.replace('.txt','')
                epoch_then = int(time.mktime(time.strptime(date_time, pattern)))
                epoch_now = int(time.mktime(time.strptime(datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S"), pattern)))
                if epoch_now - epoch_then > archive_after_days*86400:
                    try:
                        os.remove(im_dir+f)
                    except OSError:
                        pass
    bytes_in_arch_tex_dir = sum(os.path.getsize(arch_tex_dir) for f in os.listdir('.') if os.path.isfile(f))
    if bytes_in_arch_tex_dir > gigabyte:
        onlyfiles = [f for f in listdir(arch_tex_dir) if isfile(join(arch_tex_dir, f))]
        pattern = "%Y-%m-%d_%H_%M_%S"
        for f in onlyfiles:
            if '.png' in f:
                date_time = f.replace('.txt','')
                epoch_then = int(time.mktime(time.strptime(date_time, pattern)))
                epoch_now = int(time.mktime(time.strptime(datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S"), pattern)))
                if epoch_now - epoch_then > archive_after_days*86400:
                    try:
                        os.remove(arch_tex_dir+f)
                    except OSError:
                        pass
                        
def percentage_word_match_2(words, search_line, thresh_percentage): 
    alert_words = []
    for word in words:
        if re.search(word,search_line, re.IGNORECASE):
            #print(re.search(word,search_line, re.IGNORECASE))
            alert_words.append(word)
        else:
            i = 0
            letter_info = []
            while i < len(word):
                char_loc = []
                z = 0 
                while z < len(search_line):
                    if word[i] == search_line[z]:
                        char_loc.append(z)
                    z = z + 1
                letter_info.append((word[i],char_loc))
                i = i + 1
  
            i = 0
            track = []
            while i < len(letter_info):
                z = 0
                while z < len(letter_info[i][1]):
                    if i < len(letter_info) - 1:
                        if letter_info[i][1][z] + 1 in letter_info[i+1][1] or letter_info[i][1][z] + 2 in letter_info[i+1][1]:
                            track.append(True)
                        else:
                            track.append(False)
                    z = z + 1
                i = i + 1
            if cascade_search(track,len(word)):
                alert_words.append(word)     
    return(alert_words)
    
def cascade_search(track,len_word):
    i = 0
    count = 0
    max = 0
    while i < len(track):
        if track[i] == True:
            count = count + 1
        else:
            count = 0
        if count > max:
            max = count
        i = i + 1
    if max >= len_word:
        return True
    else:
        return False
def check_for_update(_slk,keywords,phrases,urls):
    dataw =_slk
    files = {'meta':('meta_report.csv', dataw)}
    r = requests.post("http://127.0.0.1:5000/get_search_update", files=files)
    
    if 'keywords' in r.text or 'phrases' in r.text or 'urls' in r.text:
        all_lists = r.text
        for list in all_lists:
            if 'keywords' in list:
                list.remove('keywords')
                nkeywords = list
                for word in nkeywords:
                    if word not in keywords:
                        keywords.append(word)
            if 'phrases' in list:
                list.remove('phrases')
                nphrases = list
                for phrase in nphrases:
                    if phrase not in phrases:
                        phrases.append(phrase)       
            if 'urls' in list:
                list.remove('urls')
                nurls = list
                for url in nurls:
                    if url not in urls:
                        urls.append(url)
    else:
        return False
    return keywords,phrases,urls
def initialize_and_send_message(_slk,_mac,_request_text,_request_data):
    _message_type = False
    dataw =_slk
    files = {'meta':('meta_report.csv', dataw)}
    r = requests.post("http://127.0.0.1:5000/get_message_type", files=files)
    print(r.text)
    print(r.status_code, r.reason)
    _message_type = r.text
    if _message_type == False:
        handle_request_error = True
    else:
        if 'email' in _message_type or 'sms' in _message_type:#email or sms
            dataw =_slk+','+_mac+','+_message_type+','+_request_text+','+_request_data
            files = {'meta':('meta_report.csv', dataw)}
            r = requests.post("http://127.0.0.1:5000/send_screen_event", files=files)
            print(r.text)
            print(r.status_code, r.reason)
        elif 'mms' in _message_type:
            dataw = _slk+','+_mac+','+_message_type+','+_request_text+',Trigger MMS:True'
            with open(_request_data,'rb') as f:
      
                files = {'data':f,'meta':('meta_report.csv', dataw)}
                r = requests.post("http://127.0.0.1:5000/send_screen_event", files=files)##same url or create new route handle
                print(r.text)
                print(r.status_code, r.reason)     
    #try:
        #response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        #return
    #except urllib2.URLError:






