from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage
from django.db.models import Count, Avg
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ReputationType

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAdminUser,)

        return super(UserView, self).get_permissions()


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['GET'])
    def get_profile_info(self, request):
        user = get_object_or_404(Profile, user__username=request.user)
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def answers(self, request):
        profile = get_object_or_404(Profile, user__username=request.user)
        answers = Answer.objects.filter(author=profile)
        return Response(AnswerMinSerializer(answers, many=True).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def posts(self, request):
        profile = get_object_or_404(Profile, user__username=request.user)
        posts = Post.objects.filter(author=profile)
        return Response(PostMinSerializer(posts, many=True).data, status=status.HTTP_200_OK)\

    @action(detail=False, methods=['GET'])
    def ranking(self, request):
        profiles = Profile.objects.order_by('-reputation')[:10]
        return Response(ProfileSerializer(profiles, many=True).data, status=status.HTTP_200_OK)


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return AnswerWriteSerializer
        else:
            return AnswerSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(Profile, user__username=self.request.user)
        serializer.validated_data['author'] = user
        user.updateReputation(reputation=ReputationType.REVIEW)
        return super(AnswerView, self).perform_create(serializer)


class PostDetailView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):

        # return pageNumber if next/previous page is not empty
        try:
            next_page = self.page.next_page_number()
        except EmptyPage:
            next_page = None
        try:
            previous_page = self.page.previous_page_number()
        except EmptyPage:
            previous_page = None

        pagination = {
            'next': next_page,
            'previous': previous_page,
            'page_size': self.page_size,
            'current': self.page.number,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
        }
        return Response({
            'pagination': pagination,
            'results': data
        })


class PostView(viewsets.ModelViewSet):
    pagination_class = PostPagination

    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        queryset = Post.objects.all()
        ordering = self.request.query_params.get('ordering')
        filter_category = self.request.query_params.get('category')
        search_text = self.request.query_params.get('search')
        if ordering is not None:
            if ordering == 'date':
                queryset = Post.objects.all().order_by('-created')
            if ordering == 'rank':
                queryset = Post.objects.annotate(
                    rank=Avg('reviewed_categories__rank')).order_by('-rank')
            if ordering == 'visits':
                queryset = Post.objects.all().order_by('-visits')
            if ordering == 'answers':
                queryset = Post.objects.annotate(
                    num_answers=Count('answers')).order_by('-num_answers')
            if ordering == 'noanswer':
                queryset = Post.objects.filter(
                    answers__isnull=True).order_by('-created')
        if filter_category is not None:
            queryset = queryset.filter(categories__name=filter_category)
        if search_text is not None:
            queryset = queryset.filter(
                Q(description__icontains=search_text) |
                Q(title__icontains=search_text) |
                Q(repo_link__icontains=search_text) |
                Q(page_link__icontains=search_text) |
                Q(answers__description__icontains=search_text) |
                Q(reviewed_categories__category_nodes__description__icontains=search_text)
            ).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        if self.action == 'create' or self.action == 'update':
            return PostWriteSerializer
        else:
            return PostDetailSerializer

    # customowa funkcja retrieve zwiększająca ilość wizyt posta po każdym zapytaniu
    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.visits += 1
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = get_object_or_404(Profile, user__username=self.request.user)
        user.updateReputation(reputation=ReputationType.POST)
        serializer.validated_data['author'] = user
        return super(PostView, self).perform_create(serializer)

    # zwwraca wszystkie odpowiedzi udzielone w danym poście

    @action(detail=True, methods=['GET', ])
    def answers(self, request, pk=None):
        post = self.get_object()
        answers = post.answers.all()
        return Response(AnswerSerializer(answers, many=True).data)
