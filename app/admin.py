from django.contrib import admin
from app.models import Answer, Category, Post, Profile, AnswerCategory, AnswerCategoryNode


admin.site.register(Answer)
admin.site.register(AnswerCategory)
admin.site.register(AnswerCategoryNode)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
