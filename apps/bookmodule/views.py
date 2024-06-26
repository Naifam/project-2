from django.shortcuts import render,redirect,get_object_or_404
from .models import GeeksModel 
from .forms import GeeksForm
# Create your views here.

def Encrypt(request):
        
    return render(request, 'bookmodule/Encryption.html')

def create_view(request):
    
    context = {}

    form = GeeksForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/Encryption')
        
    context['form'] = form
    return render(request, "bookmodule/index.html", context)
 
def user_list(request):
    users = GeeksModel.objects.all()
    return render(request, 'bookmodule/user_list.html', {'users': users})
        
def create_user(request):
    if request.method == 'POST':
        form = GeeksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = GeeksForm()
    return render(request, 'bookmodule/user_form.html', {'form': form})

def update_user(request, pk):
    user = get_object_or_404(GeeksModel, pk=pk)
    if request.method == 'POST':
        form = GeeksForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = GeeksForm(instance=user)
    return render(request, 'bookmodule/user_form.html', {'form': form})

def delete_user(request, pk):
    user = get_object_or_404(GeeksModel, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'bookmodule/user_confirm_delete.html', {'user': user})


def products(request):
    
    return render(request, 'bookmodule/products.html')



def Cart(request):
    
    return render(request, 'bookmodule/cart.html')
