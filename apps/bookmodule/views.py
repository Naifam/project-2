from django.shortcuts import render

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

def getProducts(request):
        
    return render(request, 'bookmodule/myproducts.html')