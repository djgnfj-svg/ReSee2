from rest_framework import viewsets
from rest_framework import permissions

from reviewer.category_list.seriailzers import CateCreateSerializer, CateListSerializer

from reviewer.models import Categories
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
	queryset = Categories.objects.all().order_by("-created_at")
	serializer_class = CateListSerializer
	permission_classes = [permissions.IsAuthenticated]


	def create(self, request):
		# POST METHOD
		serializer = CateCreateSerializer(data=request.data)
		print(serializer.is_valid())
		if serializer.is_valid():
			rtn = serializer.create(request, serializer.data)
			return Response(CateListSerializer(rtn).data, status=status.HTTP_201_CREATED)
		pass