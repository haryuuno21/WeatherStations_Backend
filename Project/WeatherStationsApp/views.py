from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

def hello(request):
    return render(request, 'main_page.html', { 'data' : {
        'stations': [{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1}]
    }})

def description(request):
    return render(request,'description.html')

def orderInfo(request):
    return render(request,'order_page.html', { 'data' : {
        'stations': [{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+28°',
                      'id' : 1},{'img_src' : '/static/images/1.png',
                      'title':'ВДНХ',
                      'temperature' :'+26°',
                      'id' : 1}]
    }})