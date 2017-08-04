# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm
from models import UserModel,SessionToken,PostModel,LikeModel,CommentModel
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render,redirect
from imgurpython import ImgurClient
import os
from datetime import timedelta
from django.utils import timezone
# Create your views here.


CLIENT_ID='e8b96d3df82469'
CLIENT_SECRET= 'f6292d93b81e0f055521eb71084b63b9ccc5329d'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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




def post_view(request):
        user = check_validation(request)
        print "post view called"
        if user:
            print 'Authentic user'
            if request.METHOD == 'GET':
                form = PostForm()
            elif request.method == 'POST':
                form = PostForm(request.POST, request.FILES)
                if form.is_valid():
                    image = form.cleaned_data.get('image')
                    caption = form.cleaned_data.get('caption')

                    post = PostModel(user=user, image=image, caption=caption)
                    post.save()
                    path =   BASE_DIR+'/'+ post.image.url
                    print path
                    client = ImgurClient(CLIENT_ID,CLIENT_SECRET)
                    post.image_url = client.upload_from_path(path, anon=True)['link']
                    post.save()
            return render(request, 'feed.html', {'form': form})

        else:
            return redirect('/login/')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')


def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


# For validating the session
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
    else:
        return None