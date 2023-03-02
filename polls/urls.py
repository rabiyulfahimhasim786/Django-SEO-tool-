from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('home/', views.file_upload, name='file_upload'),
    path('grammerly/',views.base,name='base'),
    path('mispell',views.mispell,name='mispell'),
    path('privacy/',views.privacy,name='privacy'),
    path('keyword/', views.keyword_form, name='keyword_form'),
    path('keyword/<int:id>/',views.delete_keyword, name='delete_keyword'),
    path('keywordoutput/', views.keyword_csv, name='keyword_csv'),
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('plag/',views.Plagarism,name='Plagarism'),
    path('paraphrasing/',views.Paraphrasing,name='Paraphrasing'),
    path('logout/',views.LogoutPage,name='logout'),
    path('homepage/',views.homepage, name='homepage'),
    path('run/', views.run, name='run'),
    path('baseindex/', views.indexhtml, name='indexhtml'),
    # testing with CRUD apps
    path('create',views.createindedxdata,name="createindedxdata"),
    path('retrieve/',views.retrieve,name="retrieve"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('update/<int:id>',views.update,name="update"),
    path('delete/<int:id>',views.delete,name="delete"),

    # path('fileindex/', views.filehtml, name='filehtml'),
    

    path('',views.indexpage,name="indexpage"),

]