from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def sayHello(request):
    html = """
            <title> 수업 </title>
            <h1> Hello, !! </h1><br>
            <h2> Hello, !! </h2><br>
            <h3> Hello, !! </h3>
            <a href = "https://naver.com">네이버입니다.</a> 
            <p> 테스트입니다. </p>
            """
    return HttpResponse(html)