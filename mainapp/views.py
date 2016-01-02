from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import Metka
import json
import requests
from django.http import StreamingHttpResponse
try:
	from urllib.request import urlopen
	from urllib.parse import urljoin
except ImportError:
	from urllib2 import urlopen	
	from urlparse import urljoin
import ssl
# Create your views here.
def main(request):
	return render(request, 'metka.html')

def send_json_request(request):
	url = 'http://localhost:8000/recieve_json'
	data = {'data':[{'key1': 'val1'}, {'key2': 'val2'}]}
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data=json.dumps(data), headers=headers)
	return redirect('/')

def recieve_json(request):
	if request.method == 'POST':
		Metka(text=json.loads(request.body)).save()



def send_simple_location_message(request):
	slmp = 'locatemessagedefinition,labd,std0,id_format,tag_id,123.00,100.12,99.2,7,125504.049,online,1,p'
	URL = 'http://localhost:8000/receive_slmp'
	f = urllib.urlopen(URL, urllib.urlencode(slmp))
	return redirect('/')


def receive_slmp(request, slmp=1):
	if request.method == 'POST':
		Metka(text=request.body.decode('utf-8')).save()
	return HttpResponse('ok')

def glmatrix(request):
	return render(request, 'glmatrix.html')

def glmatrix2(request):
	return render(request, 'glmatrix2.html')

def threejs(request):
	return render(request, 'threejs.html')