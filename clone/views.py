# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from forms import SignUpForm,LoginForm
from models import UserModel,SessionToken
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render,redirect
# Create your views here.
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

def login_user(request):
    print 'loin page called'
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = UserModel.objects.filter(username=username).first()

            if user:
                # Check for the password
                if check_password(password, user.password):
                    print 'User is valid'
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    print 'User is invalid'
                    response_data['message'] = 'Incorrect Password! Please try again!'
    elif request.method == "GET":
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)


def feed_view(request):
    return render(request, 'feed.html')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None

