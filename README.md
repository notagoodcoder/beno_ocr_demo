# beno_ocr_demo
simple ocr app takes images of screen, ocr to text, searches for keywords to alert user

Usage Scenario: parental control, raw file backups, interface for smart desktop assistant, etc

Hi beno, here are some instructions for running


should work with any version of python 3...

1.need to install tesseract-ocr before running:
--> see windows install instructions https://github.com/tesseract-ocr/tesseract/wiki

2.once installed open image_to_text.py and edit the path where tesseract is installed if it is different from below
line 2> pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

3. pip is a command line package installer for python... pip comes with most generic python downloads - you need to use it to download third party libraries used in the code

cd to the app directory where requirements.txt is and run the command:

pip install -r requirements.txt


4. search_config.txt contains search items, change the lines to add desired search words

5. run the app with the command: python ./client_instance.py

The app will generate folders in the app directory with screen shot images and parsed image text files... the directory
interest_storage will contain text scrapes containing keywords if the keyword was observed on screen.

The search algorithm isnt perfect and often misses some word instances...

I also wrote a cool flask backend that stores user info in mysql and sends text and email updates with twilio and sendgrid when a keyword alarm is raised.. 
I can add that to github if you want to see it but this version of the client isnt configured to send http requests to the flask api

Still a cool hacked together python app for starting out...If you have any questions or you get runtime errors let me know!
