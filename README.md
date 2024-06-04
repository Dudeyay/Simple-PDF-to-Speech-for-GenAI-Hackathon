# Simple-PDF-to-Speech-for-GenAI-Hackathon
A simple python program that converts text content on a PDF to a speech output.
Program first uses PDF2Image library to divide a PDF into .jpg's (one page per image). Uses page-dewarp by running page-dewarp command on Terminal to dewarp warped images. Uses EasyOCR to read each of the image and store the obtained text in a string and finally uses Google Text to Speech (gTTS) to convert string into audio file. Since gTTS can process text in only one language at once, given PDFs with multiple languages, a language detector is implemented to divide the entire text into chunks based on languages, and feeds gTTS chunk by chunk. It is then written on one single audio file to give one output.

Several Packages have to be installed before this program is run, commands are shown below:
pip install easyocr
pip3 install torch torchvision torchaudio (for cpu ***Does not work on python3.12) (see the following link for gpu usage: https://www.youtube.com/watch?v=r7Am-ZGMef8&t=3s)
pip install pdf2image
pip install opencv-python
pip3 install py3langid
pip install gTTS
pip install page-dewarp
