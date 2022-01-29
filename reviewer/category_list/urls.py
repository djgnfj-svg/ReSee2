from django.urls import path

from reviewer.category_list.views import category_change_view, category_create_view, category_view, study_change_view, study_create_view, study_list_view, study_review_view

# category_list/~
urlpatterns = [
    path("",category_view,name="cate_list"),
    path("create/",category_create_view,name="cate_create"),
    path("<str:action>/<int:category_id>",category_change_view,name="cate_change"),
    path("<int:category_id>/study_list/",study_list_view,name="study_list"),
    path("<int:category_id>/study_list/create/",study_create_view,name="study_create"),
    path("<int:category_id>/study_list/reviwe/<int:study_id>",
        study_review_view,name="study_review"),
    path("<int:category_id>/study_list/<str:action>/<int:study_id>",
        study_change_view,name="study_change"),
]