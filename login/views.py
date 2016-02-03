#!/usr/bin/python
# -*- coding: utf8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf


# Create your views here.
def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/sockjs')
		else:
			args['login_error'] = 'Пользователь не найден или некорректный пароль'
			return render(request, 'login.html', args)
	else:
		return render(request, 'login.html', args)

def logout(request):
	auth.logout(request)
	return redirect('/sockjs')