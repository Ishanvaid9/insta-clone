# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.core import validators

# Create your models here.

#user model info
class UserModel(models.Model):
  email = models.EmailField()
  name = models.CharField(max_length=120)
  username = models.CharField(max_length=120)
  password = models.CharField(max_length=400)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

  def __str__(self):
       return self.username


# post model


class PostModel(models.Model):
  user = models.ForeignKey(UserModel)
  image = models.FileField(upload_to='user_images')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=240)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

  @property
  def like_count(self):
      return len(LikeModel.objects.filter(post=self))
  @property
  def comment_like(self):
      return CommentModel.objects.filter(post=self)


 # session tokken
class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token = uuid.uuid4()

#like model

class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


# comment model


class CommentModel(models.Model):
  user = models.ForeignKey(UserModel)
  post = models.ForeignKey(PostModel)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.user.name +" has commented " +self.comment_text