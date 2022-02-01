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
		fields = ["id", "email", "user"]

class CateListSerializer(serializers.ModelSerializer):
	creator = UserSerializer(read_only=True)

	class Meta:
		model = Categories
		fields = ["id", "name", "creator", "category_count", "created_at"]

class CateCreateSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=50)
	category_count = serializers.IntegerField(required=False, default=0)

	def create(self, request, data, commit=True):
		instance = Categories()
		instance.name = data.get("name")
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