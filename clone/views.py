# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from forms import SignUpForm
from models import UserModel
from django.contrib.auth.hashers import make_password

from django.shortcuts import render
def singnup_view(request):
        print ' view called'
        if request.method == "POST":
            print ' post called'
            form = SignUpForm(request.POST)
            if form.is_valid():
                print ' form is valid'
                username = form.cleaned_data['username']
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = UserModel(name=name, password=make_password(password), email=email, username=username)
                user.save()
                print ' user saved'
                return render(request,'sucess.html')
            else:
                print ' form invalid'
        elif request.method == "GET":
            print ' get called'
            form = SignUpForm()
        return render(request, 'instalogin.html',{'form':form})

# Create your views here.
