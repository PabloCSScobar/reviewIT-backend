from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination



class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    def get_serializer_class(self):
        if self.action =='create' or self.action == 'update':
            return AnswerWriteSerializer
        else:
            return AnswerSerializer


class PostDetailView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        if self.action =='create' or self.action == 'update':
            return PostWriteSerializer
        else:
            return PostDetailSerializer

    #customowa funkcja retrieve zwiększająca ilość wizyt posta po każdym zapytaniu
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.visits +=1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    #zwwraca wszystkie odpowiedzi udzielone w danym poście
    @action(detail=True, methods=['GET',])
    def answers(self, request, pk = None):
        post = self.get_object()
        answers = post.answers.all()
        return Response(AnswerSerializer(answers, many=True).data)