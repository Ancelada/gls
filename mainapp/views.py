from django.shortcuts import render, redirect
from django.http import HttpResponse
from mainapp.models import Metka
# Create your views here.
def main(request):
	return render(request, 'metka.html')

def inputquery(request, query=1):
	Metka(text=query).save()
	return HttpResponse(query)

def getkoors(request):
	a = Metka.objects.all()
	return HttpResponse(a)