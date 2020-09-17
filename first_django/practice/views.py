from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def TellHello(requests):
    html = "<h1> 우리들의 첫번째 장고 App입니다.</h1>"
    return HttpResponse(html)
