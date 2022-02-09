from django.urls import path

from reviewer.category_list.views import category_view, study_change_view, study_create_view, study_detail_view, study_list_view, study_review_view

from rest_framework import routers
from reviewer.category_list.apis import *

router = routers.DefaultRouter()
router.register(r'category_list', CateViewSet)
router.register(r'category_list/(?P<category_id>\d+)/study_list', CateStudyViewSet, basename="api_study")
router.register(r'category_list/(?P<category_id>\d+)/review', CateReViewSet, basename="api_review")


# category_list/~
urlpatterns = [
    path("",category_view,name="cate_list"),
    path("<int:category_id>/study_list/",study_list_view,name="study_list"),
    path("<int:category_id>/study_list/create/",study_create_view,name="study_create"),
    path("<int:category_id>/study_list/<int:study_id>",
        study_detail_view,name="study_detail_review"),
    path("<int:category_id>/review",
        study_review_view,name="study_review_view"),
]