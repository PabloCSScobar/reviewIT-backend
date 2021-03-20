from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class PostDetailView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        if self.action =='create':
            return PostCreateSerializer
        else:
            return PostDetailSerializer

    #customowa funkcja retrieve zwiększająca ilość wizyt posta po każdym zapytaniu
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.visits +=1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
