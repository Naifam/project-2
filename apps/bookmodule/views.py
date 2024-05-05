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

def book(request,bId):
    obj=book.objects.get(id=bId)
    return render (request, 'bookmodule/book.html', {'book:':obj})
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


from django.shortcuts import redirect
from .models import Task
# Create your views here.

def tasks(request):
# render the appropriate template for this request
    Tasks = Task.objects.all()
    return render(request, 'bookmodule/tasks.html')


def task(request,tId):
# render the appropriate template for this request

    task = Task.objects.get(id = tId)
    return render(request, 'bookmodule/task.html', {'task':task})


def create2(request):
# render the appropriate template for this request
    if request.method == 'POST':
        taskobj = Task(Name = request.POST.get('Name'),
                                password = request.POST.get('password'))
                                     
        taskobj.save()

        return redirect('tasks')
    return render(request, 'bookmodule/create2.html',{})

def edit(request,tId):
# render the appropriate template for this request

    task = Task.objects.get(id = tId)

    if request.method == 'POST':
        task.deadline = request.POST.get('title')
        task.deadline = request.POST.get('deadline')
        task.Priority = request.POST.get('priority')
        task.State = request.POST.get('state')
        task.save()
        return redirect('task', tId = task.id )

    return render(request, 'bookmodule/edit.html', {'task_id': bId})
    return render(request, 'bookmodule/edit.html', {'task':task})

def delete(request,bId):
# render the appropriate template for this request

    return render(request, 'bookmodule/delete.html', {'task_id': bId})
