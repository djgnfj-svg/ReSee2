from django.urls import path

from reviewer.category_list.views import category_change_view, category_view, study_change_view, study_list_view, study_review_view

from rest_framework import routers
from reviewer.category_list.apis import *

router = routers.DefaultRouter()
router.register(r'category_list', UserViewSet)
router.register(r'category_list/(?P<category_id>\d+)/study_list', CateStudyViewSet)
router.register(r'study_list', StudyViewSet)


# category_list/~
urlpatterns = [
    path("",category_view,name="cate_list"),
    path("<str:action>/<int:category_id>",category_change_view,name="cate_change"),
    path("<int:category_id>/study_list/",study_list_view,name="study_list"),
    path("<int:category_id>/study_list/reviwe/<int:study_id>",
        study_review_view,name="study_review"),
    path("<int:category_id>/study_list/<str:action>/<int:study_id>",
        study_change_view,name="study_change"),
]