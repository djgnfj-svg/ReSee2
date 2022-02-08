from django.urls import path

from reviewer.admins.views import admins_list_view, admins_view

# admins/~
urlpatterns = [
    path("",admins_view,name="admins_home"),
    path("",admins_list_view,name="admins_list"),
]