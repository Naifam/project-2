from django.shortcuts import render

#from apps.bookmodule.forms import UploadForm

# Create your views here.


def index(request):
  
        
        
    return render(request, 'bookmodule/index.html')


def getBooks(request):
        
    return render(request, 'bookmodule/books.html')

def getBook(request, bookid):
 
        
    return render(request, 'bookmodule/book.html', {'book_num': bookid})


def getTags(request):
        
    return render(request, 'bookmodule/tags.html')

def Encrypt(request):
        
    return render(request, 'bookmodule/Encryption.html')

def Create(request):
        
    return render(request, 'bookmodule/Create.html')

def book(request,bId):
    obj=book.objects.get(id=bId)
    return render (request, 'bookmodule/book.html', {'book:':obj})
# relative import of forms

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from .models import GeeksModel 
from .forms import GeeksForm

def create_view(request): 
    # dictionary for initial data with  
    # field names as keys 
    context ={} 
  
    # add the dictionary during initialization 
    form = GeeksForm(request.POST or None) 
    if form.is_valid(): 
        form.save() 
          
    context['form']= form 
    return render(request, "bookmodule/create_view.html", context) 


def disp(request):
    display = GeeksModel.objects.all()
    return render(request, 'bookmodule/display.html', {'display': display})