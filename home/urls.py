
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('marge/', views.handle_upload, name="handle_upload"),
    path('handle_marge/', views.handle_marge, name="handle_marge"),
    path('compress_pdf/', views.compress_pdf, name="compress_pdf"),
    path('word_to_pdf/', views.word_to_pdf, name="word_to_pdf"),
    path('pdf_to_txt/', views.pdf_to_txt, name="pdf_to_txt"),
    path('rotate_PDF/', views.rotate_handle, name="rotate_handle"),
    path('protect_PDF/', views.protect_PDF, name="protect_PDF"),
    path('img_to_pdf/', views.img_to_pdf, name="img_to_pdf"),
    # path('marge/<slug:data>', views.handle_upload, name="handle_upload"),
    # path('marge_func/', views.handle_marge, name="handle_marge"),

    path('download/', views.download, name="download"),
    path('dlt_file/', views.dlt_uploaded_file, name="dlt_uploaded_file"),
    path('dlt_all_file/', views.dlt_all_file, name="dlt_all_file"),
]
