from django.contrib import admin
from app.models import Answer, Category, Post, Profile, AnswerCategory, AnswerCategoryNode
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

admin.site.register(Answer)
admin.site.register(AnswerCategory)
admin.site.register(AnswerCategoryNode)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)