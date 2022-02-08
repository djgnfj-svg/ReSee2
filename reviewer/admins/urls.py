from django.urls import path

from reviewer.admins.views import admins_view

# admins/~
urlpatterns = [
    path("",admins_view,name="admins_home"),
]