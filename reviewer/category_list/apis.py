from tkinter.tix import Tree
from django.http import Http404
from rest_framework import viewsets
from rest_framework import permissions

from reviewer.category_list.serializers import CateCreateSerializer, CateListSerializer

from reviewer.models import Categories
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action, renderer_classes

class UserViewSet(viewsets.ModelViewSet):
	queryset = Categories.objects.order_by("-created_at")
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
	
	def retrieve(self, request, pk=None):
		#Detail Get
		# 내용보기를 눌렀을때임
		queryset = self.get_queryset().filter(pk=pk).first()
		serializer = CateListSerializer(queryset)
		return Response(serializer.data)

	def update(self, request, pk=None):
		# PUT 메소드
		pass

	def partial_update(self, request, pk=None):
		# PATCH METHOD
		pass

	@renderer_classes([JSONRenderer])
	def destroy(self, request, pk=None):
		queryset = self.get_queryset().filter(pk=pk, creator_id = request.user.id)
		if not queryset.exists():
			raise Http404
		queryset.delete()
		return Response({"msg": "ok"})

	def list(self, request):
		# GET ALL
		queryset = self.get_queryset().all()
		serializer = CateListSerializer(queryset, many=True)
		return Response(serializer.data)
	
	@action(detail=True, methods=["get"])
	def add_cate(self, request, pk=None):
		print("test")