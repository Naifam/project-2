from django.shortcuts import render
from .models import GeeksModel
from .forms import GeeksForm
 
# Create your views here.


def index(request):
    x = 5
    if x < 5:
        x = x + 2
    else:
        x = x - 1
        
        
    return render(request, 'bookmodule/index.html')


def getBooks(request):
        
    return render(request, 'bookmodule/books.html')

def getBook(request, bookid):
    x = 5
    if x < 5:
        x = x + 2
    else:
        x = x - 1
        
        
    return render(request, 'bookmodule/book.html', {'book_num': bookid})


def getTags(request):
        
    return render(request, 'bookmodule/tags.html')

def Encrypt(request):
        
    return render(request, 'bookmodule/Encryption.html')

def CreateAccount(request):
        
    return render(request, 'bookmodule/Create.html')


# relative import of forms

 
def create_view(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        form.save()
         
    context['form']= form
    return render(request, "create_view.html", context)

 
def home_view(request):
    context ={}
 
    # create object of form
    form = GeeksForm(request.POST or None, request.FILES or None)
     
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        form.save()
 
    context['form']= form
    return render(request, "home.html", context)