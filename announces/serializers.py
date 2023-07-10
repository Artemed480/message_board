from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Announce

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class AnnounceSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Announce
        fields = ('id', 'title', 'content', 'author', 'category', 'pub_date', 'get_category')