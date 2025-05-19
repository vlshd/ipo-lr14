from django.shortcuts import render

def hello_world(request):
    return render(request,'myapp/index.html')

def about(request):
    return render(request, 'myapp/aboutAuthor.html')

def aboutShop(request):
    return render(request, 'myapp/aboutShop.html')
    