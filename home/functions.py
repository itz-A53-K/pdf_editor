import os,random,string
from pathlib import Path
from django.conf import settings
from PyPDF2 import *


def dltFile_func(fileList):
    for file in fileList:
            os.remove(file)


def dirPathCreate(path):
    dir=Path(__file__).parent.parent / f"media/{path}"
    return dir

def randomStr(filename):
    letters = string.ascii_letters
    rndStr=''.join(random.choice(letters) for i in range(130))
    return f"rnT={rndStr}&fn={filename}"

def handle_uploaded_pdf_file(file, fpath):  
    #save the uploaded file in the "upload" folder
    if not os.path.isfile(fpath+file.name):
        with open(fpath+file.name, 'wb+') as destination:  
            for chunk in file.chunks():  
                destination.write(chunk)  


def rotate_file(deg, old_filename, new_filename):

    path= settings.MEDIA_ROOT+f"/rotate/{old_filename}"
    path2= settings.MEDIA_ROOT+f"/rotate/{new_filename}"

    reader = PdfReader(path)
    writer = PdfWriter()

    writer.add_page(reader.pages[0])
    writer.pages[0].rotate(deg)

    with open(path2, "wb") as fp:
        writer.write(fp)
    return True


