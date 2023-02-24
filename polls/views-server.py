from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from newspaper import Article
from .models import textarticle, Keyword, Film, Genre
from .forms import articleForm, KeywordForm, Genreform, Filmform
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json
from textblob import TextBlob
from bs4 import BeautifulSoup
#seo

import advertools as adv
import pandas as pd
pd.options.display.max_columns = None
import urllib.request
import requests
import csv
cxs ='cxkeys'

keys = 'cseksey'
# def index(request):
#     return HttpResponse('hello world')

dot = '/var/www/subdomain/spellchecker/grammer'
#dot = '/var/www/seo/t'
#dot = '.'
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('keyword_form')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def Plagarism(request):
    return render (request,'plag.html')

@login_required(login_url='login')
def Paraphrasing(request):
    return render (request,'paraphrasing.html')

# @login_required(login_url='login')
def homepage(request):
    return render(request,'homepage.html')

@login_required(login_url='login')
def file_upload(request):
    if request.method == 'POST':
        form = articleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            linkdocuments = textarticle.objects.all()
            for obj in linkdocuments:
                baseurls = obj.url
            print(baseurls)
            article = Article(baseurls)
            article.download()
            article.parse()
            input_text = article.text
            print(input_text)
            with open(dot+"/media/json/test.json", "w") as outfile:
                json.dump(input_text, outfile)
            # Opening JSON file
            f = open(dot+'/media/json/test.json')
            data = json.load(f)
            originaltext = data
            f.close()
            return render(request, 'home.html',{'originaltext': originaltext})
    else:
        form = articleForm()
    return render(request, 'home.html', {
        'form': form
    })

# @login_required(login_url='login')   
# def file_upload(request):
#     if request.method == 'POST':
#         form = articleForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             linkdocuments = textarticle.objects.all()
#             for obj in linkdocuments:
#                 baseurls = obj.url
#             print(baseurls)
#             article = Article(baseurls)
#             article.download()
#             article.parse()
#             input_text = article.text
#             print(input_text)
#             with open("./media/json/test.json", "w") as outfile:
#                 json.dump(input_text, outfile)
#             # Opening JSON file
#             f = open('./media/json/test.json')
#             data = json.load(f)
#             originaltext = data
#             f.close()
#             return render(request, 'home.html',{'originaltext': originaltext})
#     else:
#         form = articleForm()
#     return render(request, 'home.html', {
#         'form': form
#     })

@login_required(login_url='login')
def base(request):
    return render(request,'input.html')

@login_required(login_url='login')
def privacy(request):
    return render(request,'privacy.html')

@login_required(login_url='login')   
def mispell(request):
    word=request.POST['word']
    text=BeautifulSoup(word, features='html.parser').text

    print(text)
    convert_word=TextBlob(text)
    corrected_word=convert_word.correct()
    return render(request,'result.html',{'result':corrected_word})

# import torch
# from gramformer import Gramformer
@login_required(login_url='login')
def result(request):    
    gf_inference = torch.load(r'/content/sample_data/gf.pth')
    aa=str(request.GET['pclass'])
    influent_sentences = []
    op=[]
    op1=[]
    context={}
    influent_sentences.append(aa)  
    for influent_sentence in influent_sentences:
        corrected_sentence = gf_inference.correct(influent_sentence)
        print("[Input] ", influent_sentence)
        op.append(corrected_sentence[0])
        op1.append(influent_sentence)
        
        
        context['h']=influent_sentence
        context['o']=corrected_sentence[0]

        # {'a1':op},{'a2':aa}
    return render(request, 'result.html',context)

@login_required(login_url='login')
def keyword_csv(request):
    documents = Keyword.objects.all()
    for obj in documents:
        n = obj.Keywords
    print(n)
    #dot = '/var/www/seo/t'
    #dot = '.'
    dot = '/var/www/subdomain/spellchecker/grammer'
    search = adv.serp_goog(q=n, cx=cxs, key=keys)
    search.to_csv(dot+'/media/json/keyword.csv')
    datasets = pd.read_csv(dot+'/media/json/keyword.csv',  encoding= 'unicode_escape')
    d1 = {'Searchterms': datasets['searchTerms'].tolist(), 'Title': datasets['title'].tolist(), 'Snippet':datasets['snippet'].tolist()  , 'Link': datasets['link'].tolist(), }
    dfdata = pd.DataFrame(data=d1)
    #display(df)
    dfdata.to_csv(dot+'/media/json/pixar.csv',  index=False)
    with open(dot+'/media/json/pixar.csv', 'r', encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Advance past the header
                for row in reader:
                    print(row)

            # genre, _ = Genre.objects.get_or_create(name=row[0])

                    film, _ = Film.objects.get_or_create(title=row[1],
                      year=row[2],
                      filmurl = row[3],
                      genre=row[0])
                    # film, _ = Film.objects.get_or_create(title=row[3],
                    #   year=row[4],
                    #   filmurl = row[6],
                    #   genre=row[2])
                    film.save()
    filedata = dot+'/media/json/keyword.csv'
    dfjson = pd.read_csv(filedata , index_col=None, header=0,  encoding= 'unicode_escape')
    #geeks = df.to_html()
    json_records = dfjson.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    return render(request, 'keyword.html', {'data': data })

@login_required(login_url='login')
def keyword_form(request):
    if request.method == 'POST':
        form = KeywordForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # documents = Keyword.objects.all()
            # for obj in documents:
            #     n = obj.Keywords
            # print(n)
            # #dot = '/var/www/seo/t'
            # dot = '.'
            # search = adv.serp_goog(q=n, cx=cxs, key=keys)
            # search.to_csv(dot+'/media/input/keyword.csv')
            # filedata = dot+'/media/input/keyword.csv'
            # dfjson = pd.read_csv(filedata , index_col=None, header=0)
            # #geeks = df.to_html()
            # json_records = dfjson.reset_index().to_json(orient ='records')
            # data = []
            # data = json.loads(json_records)
            # return render(request, 'keyword.html', {'data': data })
            return redirect('keyword_csv')
    else:
        form = KeywordForm()
        documents =Keyword.objects.all().order_by('-id')
    return render(request, 'keywordform.html', {
        'form': form, 'documents1':documents
    })

@login_required(login_url='login')
def delete_keyword(request,id):
    if request.method == 'POST':
        document = Keyword.objects.get(id=id)
        document.delete()
        return redirect('keyword_form')


# #dot = '/var/www/seo/t'
# dot = '.'
@login_required(login_url='login')
def run(request):
    with open(dot+'/media/csv/pixar.csv', 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        #Film.objects.all().delete()
        #Genre.objects.all().delete()

        for row in reader:
            print(row)

            # genre, _ = Genre.objects.get_or_create(name=row[0])

            film, _ = Film.objects.get_or_create(title=row[1],
                        year=row[2],
                        filmurl = row[3],
                        genre=row[0])
            film.save()
    #return render('base.html')
    return HttpResponse("Hello, world !")

@login_required(login_url='login')
def indexhtml(request):
    filmes = Film.objects.all()
    return render(request, 'films.html', { 'filmes': filmes })


# def create(request):
#     if request.method=="POST":
#         name=request.POST['name']
#         age=request.POST['age']
#         phone=request.POST['phone']
#         obj=Film.objects.create(name=name,age=age,phone=phone)
#         obj.save()
#         return redirect('/')

@login_required(login_url='login')
def retrieve(request):
    details=Film.objects.all().order_by('-id')
    return render(request,'retrieve.html',{'details':details})


@login_required(login_url='login')
def edit(request,id):
    object=Film.objects.get(id=id)
    return render(request,'edit.html',{'object':object})

@login_required(login_url='login')
def update(request,id):
    object=Film.objects.get(id=id)
    form=Filmform(request.POST,instance=object)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # object=Film.objects.all()
            return redirect('retrieve')
    return redirect('retrieve')

# def delete(request,id):
#     Film.objects.filter(id=id).delete()
#     return redirect('retrieve')


@login_required(login_url='login')
def delete(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Film, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        # return HttpResponseRedirect("/")
        return redirect('retrieve')
 
    return render(request, "delete_view.html", context)