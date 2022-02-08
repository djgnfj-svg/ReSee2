

from django.shortcuts import render
from reviewer.decorators import admin_only
from django.contrib.auth.decorators import login_required


@admin_only
@login_required
def admins_view(request):
	return render(request, "admins/admins_home.html")

@admin_only
@login_required
def admins_list_view(request):
	return render(request, "admins/admins_list.html")