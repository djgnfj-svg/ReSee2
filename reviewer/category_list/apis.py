from rest_framework import viewsets
from rest_framework import permissions

from reviewer.category_list.seriailzers import CategoryListSerializer

from reviewer.models import Categories

class UserViewSet(viewsets.ModelViewSet):
	queryset = Categories.objects.all().order_by("-created_at")
	serializer_class = CategoryListSerializer
	# permission_classes = [permissions.IsAuthenticated]
