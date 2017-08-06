# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import UserModel,PostModel,LikeModel,CommentModel,SessionToken
admin.site.register(PostModel)
admin.site.register(LikeModel)
admin.site.register(CommentModel)
admin.site.register(SessionToken)


# Register your models here.
