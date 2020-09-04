from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    params = {
        'title': 'test',
    }
    return render(request, 'posts/index.html', params)
    # return  HttpResponse('a')
