from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mainapp.models import Metka, Std0
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
import datetime
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
	slmp = """Labyrinth-RSSI, SLMF, 1.0, 1.0, Welcome to the RTLS Text Stream interface. (c)2015-2016 OOO NaviTec (http://navi-tec.ru)
LabR,Std0,0000,00000063,39.681625,6.803710,76.457092,2015-12-28T07:29:53:429+3"""
	url = 'http://localhost:8000/receive_slmp'
	r = requests.post(url, data=slmp)
	return redirect('/')


def receive_slmp(request, slmp=1):
	if request.method == 'POST':
		line = request.body.decode('utf-8')
		Metka(text=line).save()
		# line = line.split('\n')
		# line = line[1]
		# line = line.split(',')
		# Std0(LabD=line[0], Std0=line[1], Tag_ID_Format=line[2], Tag_ID=line[3], X=line[4], Y=line[5], Z=line[6], Zone=line[7], DateImport=datetime.datetime.now()).save()
	return HttpResponse('ok')


def landscape(request):
	return render(request, 'landscape.html')

def getxyzvalues(request):
	if request.method == 'POST':
		queryset = list(Std0.objects.raw("""
			select *, max(DateImport) as Date from Std0
			group by Tag_ID
			"""))
		Str = ''
		num = 0
		for tag_id in queryset:
			if num < len(queryset) - 1:
				Str += '(Tag_ID="%s" and DateImport="%s") or ' %(tag_id.Tag_ID, tag_id.Date)
			else:
				Str += '(Tag_ID="%s" and DateImport="%s")' %(tag_id.Tag_ID, tag_id.Date)
			num+=1
		Str = Str.replace('"', "'")
		queryset2 = list(Std0.objects.raw("""
			select * from Std0
			where %s
			""" % Str))
		marks = {}
		num = 0
		for i in queryset2:
			spisok = []
			spisok.append({'tag_id':i.Tag_ID, 'x': i.X, 'y': i.Y, 'z': i.Z})
			marks[num] = spisok
			num+=1
	return JsonResponse(marks)