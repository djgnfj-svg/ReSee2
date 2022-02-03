from tkinter.tix import Tree
from unicodedata import category
from xml.etree.ElementInclude import default_loader
from django.contrib.auth.models import User

from accounts.models import MyUser

from rest_framework import serializers

from reviewer.models import Categories, StudyList

class UserBaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ("password",)

class UserSerializer(serializers.ModelSerializer):
	user = UserBaseSerializer(read_only=True)

	class Meta:
		model = MyUser
		fields = ["id", "email", "user"]

class CateListSerializer(serializers.ModelSerializer):
	creator = UserSerializer(read_only=True)

	class Meta:
		model = Categories
		fields = ["id", "name", "creator", "category_count", "created_at"]

class StudyListSerializer(serializers.ModelSerializer):
	creator = UserSerializer(read_only=True)

	class Meta:
		model = StudyList
		fields = "__all__"


class CateCreateSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=50)
	category_count = serializers.IntegerField(required=False, default=0)

	def create(self, request, data, commit=True):
		instance = Categories()
		instance.name = data.get("name", None)
		instance.creator_id = request.user.id
		instance.category_count = data.get("category_count") + 1
		if commit:
				try:
						instance.save()
				except Exception as e:
						print(e)
				else:
						pass
		return instance

class StudyCreateSerializer(serializers.Serializer):
	study_title = serializers.CharField(max_length=50)
	study_content = serializers.CharField(max_length=100)
	review_count = serializers.IntegerField(default=0)


	def create(self, request, data, category_id, commit=True):
		instance = StudyList()
		instance.study_title = data.get("study_title", None)
		instance.study_content = data.get("study_content", None)
		instance.review_count = data.get("review_count")
		instance.category = Categories.objects.filter(id=category_id).first()
		instance.creator_id = request.user.id
		print(data)
		print(request.POST)
		if commit:
				try:
						instance.save()
				except Exception as e:
						print(e)
				else:
						pass
		return instance