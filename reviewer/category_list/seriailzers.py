from pyexpat import model
from attr import field
from django.contrib.auth.models import User

from accounts.models import MyUser

from rest_framework import serializers

from reviewer.models import Categories

class UserBaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("password",)

class UserSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer(read_only=True)

	class Meta:
		model = MyUser
		fields = ["id", "email",]

class CategoryListSerializer(serializers.ModelSerializer):
	creator = UserSerializer(read_only=True)

	class Meta:
		model = Categories
		fields = ["id", "name",]