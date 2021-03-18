from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, status


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
        else:
            return PostDetailSerializer

