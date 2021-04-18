from rest_framework import serializers
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    def create(self, validated_data):
        usr = User.objects.create_user(**validated_data)
        Token.objects.create(user=usr)
        Profile.objects.create(user=usr, reputation=0)
        return usr


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'username', 'reputation']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnswerCategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerCategoryNode
        fields = ['id', 'description', 'answer_type']


class AnswerCategorySerializer(serializers.ModelSerializer):
    category_nodes = AnswerCategoryNodeSerializer(many=True, allow_null=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = AnswerCategory
        fields = ['id', 'rank', 'category', 'category_nodes']

# serializer dla POST/PUT


class AnswerCategoryWriteSerializer(WritableNestedModelSerializer):
    category_nodes = AnswerCategoryNodeSerializer(many=True, allow_null=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = AnswerCategory
        fields = ['id', 'rank', 'category', 'category_nodes', 'post']


class AnswerSerializer(serializers.ModelSerializer):
    reviewed_categories = AnswerCategorySerializer(many=True, read_only=True)
    rank = serializers.FloatField(source='get_answer_rank')
    author = ProfileSerializer(many=False)

    class Meta:
        model = Answer
        fields = ['id', 'author', 'created', 'is_top_answer',
                  'description', 'rank', 'reviewed_categories']

# serializer dla POST/PUT


class AnswerWriteSerializer(WritableNestedModelSerializer):
    reviewed_categories = AnswerCategoryWriteSerializer(
        many=True, allow_null=True)

    class Meta:
        model = Answer
        fields = ['id', 'description', 'post', 'reviewed_categories']
        read_only_fields = ['is_top_answer']


class LastActivitySerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.user.username')

    class Meta:
        model = Answer
        fields = ['author', 'created']


# obiekt posta wraz z informacja o odpowiedziach
class PostDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    answers = AnswerSerializer(many=True)
    author = ProfileSerializer(many=False)
    rank = serializers.FloatField(source='get_post_rank')

    class Meta:
        model = Post
        fields = ['id', 'visits', 'rank', 'author', 'created', 'description', 'title',
                  'repo_link', 'page_link', 'has_top_answer', 'categories', 'answers']


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'created', 'description', 'title',
                  'repo_link', 'page_link', 'has_top_answer', 'categories']

# obiekt posta bez dodatkowych informacji


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    number_of_answers = serializers.IntegerField(source="get_answer_count")
    last_activity = LastActivitySerializer(source="get_last_activity")
    author = ProfileSerializer(many=False)
    rank = serializers.FloatField(source='get_post_rank')

    class Meta:
        model = Post
        fields = ['id', 'visits', 'rank', 'last_activity', 'author', 'created', 'description',
                  'title', 'repo_link', 'page_link', 'has_top_answer', 'categories', 'number_of_answers']
