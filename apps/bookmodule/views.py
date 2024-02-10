from django.shortcuts import render

# Create your views here.
def index(request):
# render the appropriate template for this request
    return render(request, 'bookmodule/index.html')