from django.db import models
from django.contrib.auth.models import User

#profil uzytkownika bazujacy da wbudowanym modelu User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.user.username
    

#dziedzina, w ktorej oceniany bedzie projekt
class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


#oceniona kategoria w odpowiedzi (Answer)
class AnswerCategory(models.Model):
    class Meta:
        verbose_name_plural = "Answer Categories"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="reviewed_categories")
    rank = models.IntegerField()
    def __str__(self):
        return self.category.name
    

#pojedynczy element ocenionej kategorii (wada lub zaleta)
class AnswerCategoryNode(models.Model):
    class Meta:
        verbose_name_plural = "Answer Category Nodes"

    STATUS_CHOICES = (
        ('advantage', 'Advantage'),
        ('disadvantage', 'Disadvantage')
    )
    answer_category = models.ForeignKey(AnswerCategory, on_delete=models.CASCADE, related_name="category_nodes")
    description = models.TextField()
    answer_type = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.answer_type + ': ' + self.description


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="created_posts")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    description = models.TextField()
    title = models.CharField(max_length=255)
    repo_link = models.CharField(max_length=255)
    page_link = models.CharField(max_length=255)
    has_top_answer = models.BooleanField(default=False)



#udzielona odpowiedz
class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="provided_answers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="answers")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_top_answer =  models.BooleanField()
    description = models.TextField()
