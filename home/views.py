from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.http import Http404, JsonResponse
from django.contrib import messages
from .forms import *
from PyPDF2 import *
from django.core.files.storage import FileSystemStorage
from .functions import*
from pathlib import Path
from django.conf import settings
import json
import requests
import glob
import os,random,string
from docx2pdf import convert
from django.views.static import serve
import img2pdf
from PIL import Image
import os



def home(request):
    params={}
    return render(request, "home/home.html", params)

     
def handle_upload(request):
    if request.method == "POST":
        form = fileInp_frm(request.POST, request.FILES)
        success= False
        if form.is_valid():
            inp_file= request.FILES["file"]
            if (inp_file.name).endswith('.pdf') or (inp_file.name).endswith('.PDF') :

                handle_uploaded_file(inp_file, 'media/upload/mrg_pdf/')
                success=True
            else:
                messages.error(request, "Invalid file type")
                print("Invalid file type")
        
        W_filesList = list( dirPathCreate('upload/mrg_pdf').glob("*.pdf"))

        return JsonResponse( {"success": success,"pdf_files": files_list(W_filesList),"fileCount": len(W_filesList) } )
    else:
        W_filesList = list( dirPathCreate('upload/mrg_pdf').glob("*.pdf"))

        return render( request, "home/margeBody.html", {"pdf_files": files_list(W_filesList),"fileCount": len(W_filesList)})

def handle_marge(request):

    pdf_files=list(dirPathCreate('upload/mrg_pdf').glob("*.pdf")) #getting all pdf files        
    pdf_files.sort(key=lambda x: os.path.getmtime(x)) # short

    merger = PdfMerger()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write("media/output/siteName_marged.pdf")
    merger.close()
    return redirect(f"/download/?{randomStr('/output/siteName_marged.pdf')}")


def download(request):
    
    if request.method== "POST":
    #     if handle_marge("margeBtn"):
            
        path=request.POST.get("path")
        file_path = settings.MEDIA_ROOT+path
        # return serve(request, os.path.basename(file_path), os.path.dirname(file_path)) #from django.views.static import serve #to show the pdf file in browser (not download)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

        # request.session['download_visited'] = True
    return render(request, "home/downloadPage.html")

 

def dlt_uploaded_file(request ):
    if request.method =="POST":
        b_dir= request.POST.get("b_dir")
        f_name=request.POST.get("f_name")

        file_path_asList=list(dirPathCreate('upload/'+b_dir).glob(f_name))

        dltFile_func(file_path_asList)

        pdf_files=list(os.listdir(settings.MEDIA_ROOT+f"/upload/{b_dir}/"))
        print(pdf_files)
        print(len(pdf_files))
        
        return JsonResponse( {"success": True,"pdf_files": pdf_files,"fileCount": len(pdf_files) } )
    
    else:
        return redirect("/")


def img_to_pdf(request):
    if request.method =="POST":
            
        if request.POST.get("mkPDF") == "mkPdF":

            dirname = settings.MEDIA_ROOT+"/upload/img/"
            imgs = []
            for fname in os.listdir(dirname):
                path = os.path.join(dirname, fname)
                imgs.append(path)

            out_path=settings.MEDIA_ROOT+f"/output/image-to-pdf.pdf"

            with open(out_path,"wb") as f:
                f.write(img2pdf.convert(imgs))

            return redirect(f"/download/?{randomStr('/output/image-to-pdf.pdf')}")

        else:
            success= True
            form = fileInp_frm(request.POST, request.FILES)
            if form.is_valid():
                inp_file= request.FILES["file"]
                
                f_ext=[".PNG", ".png",".JPG",".jpg", ".JPEG", ".jpeg"]

                if (inp_file.name).endswith(tuple(f_ext)) == True:

                    handle_uploaded_file(inp_file, "media/upload/img/")
                
                else:
                    messages.error(request, "Invalid file type")
                    print("Invalid file type")
                    success= False
                    
                W_filesList = list( dirPathCreate('upload/img').glob("*"))
                
                return JsonResponse( {"success": success,"pdf_files": files_list(W_filesList),"fileCount": len(W_filesList) } )
                    
            

    W_filesList = list( dirPathCreate('upload/img').glob("*"))

    params={"fn":files_list(W_filesList), "fileCount":len(W_filesList)}
    return render( request, "home/img-to-PDF.html",params)


def compress_pdf(request):
    
    reader = PdfReader("Input.pdf")

    # page = reader.pages[0]
    # count = 0

    # for image_file_object in page.images:
    #     with open(str(count) + image_file_object.name, "wb") as fp:
    #         fp.write(image_file_object.data)
    #         count += 1
    return render( request, "home/pdfCompress.html")
    pass


def rotate_handle(request):
    global count
    count = 0
    if request.method=="POST":
        if request.POST.get("down")== "download":
            fn= request.POST.get("fnm")
            deg= request.POST.get("rotation")

            out_fileName=f"{os.path.splitext(fn)[0]}_rotated.pdf"

            rotate_file(int(deg)*90,fn,out_fileName)

            return redirect(f"/download/?{randomStr('/rotate/'+out_fileName)}")
        
        else:           
            form = fileInp_frm(request.POST, request.FILES)
            if form.is_valid():
                inp_file= request.FILES["file"]
                if (inp_file.name).endswith('.pdf') or (inp_file.name).endswith('.PDF') :

                    handle_uploaded_file(inp_file, "media/rotate/")
                    return JsonResponse({"success":True,"fn":inp_file.name})
                else:
                    # messages.error(request, "Invalid file type")
                    print("Invalid file type")
        
    fLoc_list=list(dirPathCreate("/rotate").glob("*"))

    fn_list=[]
    if len(fLoc_list) != 0:
        fn_list.append(os.path.basename(fLoc_list[0]))

    params={"fn":fn_list}
    return render(request, "home/pdfRotate.html", params)


def word_to_pdf(request):
    if request.method == "POST":
        form = fileInp_frm(request.POST, request.FILES)
        if form.is_valid():
            inp_file= request.FILES["file"]

            if (inp_file.name).endswith('.docx') or (inp_file.name).endswith('.doc') :

                handle_uploaded_file(inp_file, "media/upload/word_pdf/")
                inputFile=settings.MEDIA_ROOT+f"/upload/word_pdf/{inp_file.name}"

                out_pdf_fileName=f"{os.path.splitext(inp_file.name)[0]}.pdf"

                outputFile=settings.MEDIA_ROOT+f"/output/{out_pdf_fileName}"
                
                convert(inputFile,outputFile)
                return redirect(f"/download/?{randomStr('/output/'+out_pdf_fileName)}")
            else:
                # messages.error(request, "Invalid file type")
                print("Invalid file type")
    
    
    return render(request, "home/word_to_pdf.html")


def pdf_to_txt(request):

    if request.method == "POST":
        form = fileInp_frm(request.POST, request.FILES)
        if form.is_valid():
            inp_file= request.FILES["file"]

            if (inp_file.name).endswith('.pdf') or (inp_file.name).endswith('.PDF') :

                handle_uploaded_file(inp_file, "media/upload/pdf_txt/")
                
                reader = PdfReader(settings.MEDIA_ROOT+f"/upload/pdf_txt/{inp_file.name}")
    
                page = reader.pages[0]
                txtFileName=f'{os.path.splitext(inp_file.name)[0]}.txt'
                out_path=settings.MEDIA_ROOT+f"/output/{txtFileName}"
                with open(out_path, 'w') as f:
                    f.write(page.extract_text())
                return redirect(f"/download/?{randomStr('/output/'+txtFileName)}")
            else:
                messages.error(request, "Invalid file type")
                print("Invalid file type")
    
    return render(request, "home/pdfToTXT.html")

    
def protect_PDF(request):

    if request.method == "POST":
        form = fileInp_frm(request.POST, request.FILES)
        if form.is_valid():
            inp_file= request.FILES["file"]

            if (inp_file.name).endswith('.pdf') or (inp_file.name).endswith('.PDF') :
                
                handle_uploaded_file(inp_file, "media/upload/enc_pdf/")
                return JsonResponse({"success":True,"fn":inp_file.name})
                
            else:
                # messages.error(request, "Invalid file type")
                print("Invalid file type")
        
        if request.POST.get("psw172") == "psw172":
            fn=request.POST.get("fn")
            password=request.POST.get("protect_pass")
            reader = PdfReader(settings.MEDIA_ROOT+f"/upload/enc_pdf/{fn}")
            writer = PdfWriter()

            # Add all pages to the writer
            for page in reader.pages:
                writer.add_page(page)

            # Add a password to the new PDF
            writer.encrypt(password)

            # Save the new PDF to a file
            out_path=settings.MEDIA_ROOT+f"/output/{os.path.splitext(fn)[0]}-protected.pdf"
            with open(out_path, "wb") as f:
                writer.write(f)
            # return redirect(f"/download/?{randomStr('/output/'+out_path)}")
            return serve(request, os.path.basename(out_path), os.path.dirname(out_path))

    fLoc_list=list(dirPathCreate("/upload/enc_pdf").glob("*"))

    fn_list=[]
    if len(fLoc_list) != 0:
        fn_list.append(os.path.basename(fLoc_list[0]))

    params={"fn":fn_list}
    return render(request, "home/protect_PDF.html", params)










def dlt_all_file(request):
    success=False
    if request.method=="POST":
        mrg_pdf=list(dirPathCreate('upload/mrg_pdf').glob("*.pdf"))   #getting all files
        pdf_to_txt=list(dirPathCreate('upload/pdf_txt').glob("*.pdf"))   
        word_to_pdf=list(dirPathCreate('upload/word_pdf').glob("*"))   
        output=list(dirPathCreate('output').glob("*"))  
        rotate=list(dirPathCreate('rotate').glob("*"))  
        protect=list(dirPathCreate('upload/enc_pdf').glob("*"))  
        img_to_pdf=list(dirPathCreate('upload/img').glob("*"))  

        dltFile_func(mrg_pdf)
        dltFile_func(pdf_to_txt)
        dltFile_func(word_to_pdf)
        dltFile_func(output)
        dltFile_func(rotate)
        dltFile_func(protect)
        dltFile_func(img_to_pdf)
        
        success=True
    return JsonResponse({"success":success})


