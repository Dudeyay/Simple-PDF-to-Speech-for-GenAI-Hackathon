import easyocr #pip install easyocr
import torch #pip3 install torch torchvision torchaudio (for cpu ***Does not work on python3.12)
#(see the following link for gpu usage: https://www.youtube.com/watch?v=r7Am-ZGMef8&t=3s)
import os
from pdf2image import convert_from_path #pip install pdf2image
import cv2 #pip install opencv-python
from py3langid.langid import LanguageIdentifier, MODEL_FILE #pip3 install py3langid
from gtts import gTTS #pip install gTTS
para = ""
#function that converts a pdf to jpg format
def pdf_to_image(pdf_name):
    images = convert_from_path(pdf_name,500,poppler_path=r'poppler-23.08.0\Library\bin')
    for i in range(len(images)):
        images[i].save('page'+str(i)+'.jpg', 'JPEG')

#reads images and extracts texts, appends to and returns string
def OCR(*lang, image_name, para):
    reader = easyocr.Reader(*lang,gpu = True)
    results = reader.readtext(image_name)
    
    for i in results:
        para += i[1] + " "
    para+="\n\n"
    return para

#dewarps images and returns images in png format
def dewarp(image_path):
    path = "page-dewarp " + image_path
    os.system(path)

#returns 2D list that stores chunks of string with the same language together, as gTTS cannot work with a string containing multiple languages 
def detect_language(text, lang):
    identified_para = text.split(" ")
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE)
    langlist_converter = {"en":"en","ch_tra":"zh"}
    
    converted_lang = [langlist_converter[x] for x in lang]
    identifier.set_languages(converted_lang)
    langlst = []
    langlst.append([identifier.classify(identified_para[0])[0],identified_para[0]])
    for i in range(1,len(identified_para)):
        try:
            curr_lang = identifier.classify(identified_para[i])[0]
            if curr_lang!=langlst[-1][0]:
                langlst.append([curr_lang,identified_para[i]])
            else:
                langlst[-1][1] += " "+identified_para[i]
        except:
            langlst[-1][1] += " "+identified_para[i]
    return langlst

#reads chunks of string generated from detect_language, and writes them all onto the same mp3 file
def output_audio(langlst):
    with open('output.mp3', 'wb') as f:
        for i in range(len(langlst)):
            tts = gTTS(langlst[i][1], lang=langlst[i][0])
            tts.write_to_fp(f)

directory = os.getcwd()
pdf_name = str(input("Enter pdf name: "))
lang = input("Enter language ('en' for english, 'ch_tra' for chinese, separated by comma for multiple languages): ").split(",")
pdf_to_image(pdf_name)
for file in os.listdir(directory): 
     if file.endswith('.jpg'): #reads jpg, extracts text into string "para", and removes images
         dewarp(file)
         dewarp_image = file[0:-4] + "_thresh.png"
         read_dewarp_image = cv2.imread(dewarp_image)
         para += OCR(lang, image_name=read_dewarp_image, para=para)
         os.remove(file)
         print(dewarp_image)
         os.remove(dewarp_image)


langlst = detect_language(para, lang)
output_audio(langlst)

