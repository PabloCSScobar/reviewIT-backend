from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator

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

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="created_posts")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    visits = models.PositiveIntegerField(default=0)
    description = models.TextField()
    title = models.CharField(max_length=255)
    repo_link = models.CharField(max_length=255)
    page_link = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)


    #zwraca True jeśli jedna z odpowiedzi przypisana do posta ma flagę is_top_answer=True
    @property
    def has_top_answer(self):
        return self.answers.filter(is_top_answer=True).exists()

    #zwraca liczbe udzielonych odzpowiedzi w danym poście
    def get_answer_count(self):
        return self.answers.count()

    #zwraca ostatnią dodana odpowiedz lub null jesli nie ma jeszcze żadnych odpowiedzi
    def get_last_activity(self):
        try:
            answer = self.answers.latest('id')
        except ObjectDoesNotExist:
            answer = None
        return answer

    #zwraca średnią ocenę dla każdej zrecenzowanej kategorii w poście
    def get_categories_rank(self):
        categories = self.reviewed_categories.values('category').annotate(avg=Avg('rank')).order_by('-avg')

    #zwraca ocene główną posta
    def get_post_rank(self):
        return self.reviewed_categories.all().aggregate(Avg('rank'))['rank__avg']


    def __str__(self):
        return self.title
    


#udzielona odpowiedz
class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="provided_answers")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="answers")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_top_answer =  models.BooleanField(default=False)
    description = models.TextField()


    def get_answer_rank(self):
        return self.reviewed_categories.all().aggregate(Avg('rank'))['rank__avg']

    def __str__(self):
        return str(self.id) + ' ' + self.author.user.username + ': ' + self.post.title
    

#oceniona kategoria w odpowiedzi (Answer)
class AnswerCategory(models.Model):
    class Meta:
        verbose_name_plural = "Answer Categories"

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="reviewed_categories")
    rank = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="reviewed_categories")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reviewed_categories")



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
