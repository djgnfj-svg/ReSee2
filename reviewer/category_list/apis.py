import time
from django.http import Http404

from rest_framework import viewsets
from rest_framework import permissions

from reviewer.category_list.serializers import CateCreateSerializer, CateListSerializer, StudyCreateSerializer, StudyListSerializer

from reviewer.models import Categories, StudyList
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, action

class UserViewSet(viewsets.ModelViewSet):
	queryset = Categories.objects.filter().order_by("created_at")
	serializer_class = CateListSerializer
	permission_classes = [permissions.IsAuthenticated]

	def create(self, request):
		# POST METHOD
		serializer = CateCreateSerializer(data=request.data)
		if serializer.is_valid():
			rtn = serializer.create(request, serializer.data)
			if rtn:
				return Response(CateListSerializer(rtn).data, status=status.HTTP_201_CREATED)
			else:
				error_msg = "maximun category_count"
		#is_valid 하지 않으면
		# 카테고리 제목값이 너무 길엉
		else:
			error_msg = serializer.errors["name"]
		Resee_data = {
			"status" :400,
			"msg" : error_msg
		}

		return Response(Resee_data)
	
	def retrieve(self, request, pk=None):
		#Detail Get
		queryset = self.get_queryset().filter(pk=pk).first()
		serializer = CateListSerializer(queryset)
		return Response(serializer.data)

	def update(self, request, pk=None):
		# PUT 메소드
		serializer = CateCreateSerializer(data=request.data)
		if serializer.is_valid():
			rtn = serializer.change(request, serializer.data, pk)
			return Response(CateListSerializer(rtn).data, status=status.HTTP_201_CREATED)
		#is_valid 하지 않으면
		Resee_data = {
			"status" :500,
			"msg" : "카테고리 네임을 입력하셔야 합니다."
		}
		return Response(Resee_data)

	def partial_update(self, request, pk=None):
		# PATCH METHOD
		serializer = CateCreateSerializer(data=request.data)
		if serializer.is_valid():
			rtn = serializer.change(request, serializer.data)
			return Response(CateListSerializer(rtn).data, status=status.HTTP_201_CREATED)
		Resee_data = {
			"status" :500,
			"msg" : "카테고리 네임을 입력하셔야 합니다."
		}
		return Response(Resee_data)

	@renderer_classes([JSONRenderer])
	def destroy(self, request, pk=None):
		queryset = self.get_queryset().filter(pk=pk, creator_id = request.user.id)
		if not queryset.exists():
			raise Http404
		queryset.delete()
		return Response({"msg": "ok"})

	def list(self, request):
		# GET ALL
		time.sleep(0.05)
		queryset = self.get_queryset().all().filter(creator_id=request.user.id)
		serializer = CateListSerializer(queryset, many=True)
		return Response(serializer.data)
	
	# @action(detail=True,list=True methods=["get"])
	# def study_list(self, request, pk=None):
	# 	# return redirect("api/category_list/{}/study_list".format(pk))
	# 	return Response("api/category_list/{}/study_list".format(pk))
	# 	return redirect("")


class CateStudyViewSet(viewsets.ModelViewSet):
	queryset = StudyList.objects.filter().order_by("created_at")
	serializer_class = StudyListSerializer
	permission_classes = [permissions.IsAuthenticated]

	def create(self, request, category_id):
		# POST METHOD
		serializer = StudyCreateSerializer(data=request.data)
		if serializer.is_valid():
			rtn = serializer.create(request, serializer.data, category_id)
			return Response(StudyListSerializer(rtn).data, status=status.HTTP_201_CREATED)
		#is_valid 하지 않으면
		Resee_data = {
			"status" :500,
			"msg" : "카테고리 네임을 입력하셔야 합니다."
		}
		return Response(Resee_data)

	def retrieve(self, request, category_id, pk=None):
		#Detail Get
		queryset = self.get_queryset().filter(pk=pk).first()
		serializer = StudyListSerializer(queryset)
		return Response(serializer.data)
	def update(self, request, pk=None):
		# PUT 메소드
		pass

	def partial_update(self, request, pk=None):
		# PATCH METHOD
		pass

	@renderer_classes([JSONRenderer])
	def destroy(self, request, category_id, pk=None):
		queryset = self.get_queryset().filter(category_id = category_id, pk=pk, creator_id = request.user.id)
		if not queryset.exists():
			raise Http404
		queryset.delete()
		return Response({"msg": "ok"})
		
	def list(self, request, category_id):
		# GET ALL
		time.sleep(0.05)
		queryset = self.get_queryset().all().filter(creator_id=request.user.id, category_id = category_id)
		serializer = StudyListSerializer(queryset, many=True)
		return Response(serializer.data)

class StudyViewSet(viewsets.ModelViewSet):
	queryset = StudyList.objects.filter().order_by("created_at")
	serializer_class = StudyListSerializer
	permission_classes = [permissions.IsAuthenticated]

	def create(self, request):
		# POST METHOD
		serializer = StudyCreateSerializer(data=request.data)
		if serializer.is_valid():
			rtn = serializer.create(request, serializer.data)
			return Response(StudyListSerializer(rtn).data, status=status.HTTP_201_CREATED)
		#is_valid 하지 않으면
		Resee_data = {
			"status" :500,
			"msg" : "카테고리 네임을 입력하셔야 합니다."
		}
		return Response(Resee_data)

	def retrieve(self, request, pk=None):
		#Detail Get
		queryset = self.get_queryset().filter(pk=pk).first()
		serializer = StudyListSerializer(queryset)
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
		time.sleep(0.05)
		queryset = self.get_queryset().all().filter(creator_id=request.user.id )
		serializer = StudyListSerializer(queryset, many=True)
		return Response(serializer.data)

	@action(detail=False, list=True, methods=["get"])
	def study_list(self, request, pk=None):
		queryset = self.get_queryset().all().filter(creator_id=request.user.id, category_id = pk)
		serializer = StudyListSerializer(queryset, many=True)
		return Response(serializer.data)
