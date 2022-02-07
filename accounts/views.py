import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from pydantic import Json

from accounts.form import LoginForm, MemberDelForm, MemberUpdateForm, RegisterForm
from accounts.models import MyUser

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        res_data = {}
        if not login_form.is_valid():
            return JsonResponse(login_form.errors.as_json(), safe=False)
        try :
            user = MyUser.objects.get(email=login_form.cleaned_data.get("email"))
        except MyUser.DoesNotExist:
            res_data['error'] = "잘못된 이메일 또는 패스워드 입니다."
            return JsonResponse(res_data)
        else :
            if user.check_password(login_form.cleaned_data.get("password")):
                login(request, user)
                return redirect("home")
        return redirect("home")
    else :
        return render(request, "login.html")

def logout_view(request):
    if request.session.get('user'):
        del(request.session['user'])
    logout(request)
    return redirect("home")

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        register = RegisterForm(request.POST)
        useremail = request.POST.get('useremail',None)
        res_data = {}
        try:
            user = MyUser.objects.get(email=useremail)
            if user:
                res_data['error'] = 'This email is already subscribed.'
                print(type(register.errors.as_json()))
                return JsonResponse(res_data)
        except MyUser.DoesNotExist:
            if register.is_valid():
                login(request, register.save())
                return redirect("home")
            return JsonResponse(register.errors.as_json(), safe=False)
            # session 생성
            # user = MyUser.objects.get(email=useremail)
            # request.session['user'] = user.id
    return render(request,'register.html')

@csrf_exempt
@login_required
def member_update_view(request):
    form_Update = MemberUpdateForm()
    if request.method == "POST":
        form_Update = MemberUpdateForm(request.POST)
        if form_Update.is_valid():
            user = request.user
            user.email = request.POST["useremail"]
            user.save()
    else:
        msg = None
    return render(request, "member_modify.html")

@csrf_exempt
@login_required
def member_del_view(request):
    form_del = MemberDelForm()
    if request.method == "POST":
        form_del = MemberDelForm(request.POST)
        if form_del.is_valid():
            user = request.user
            email = request.POST["useremail"]
            raw_password = request.POST["password1"]
            if user.check_password(raw_password):
                user.delete()
                return redirect("home")
    return render(request, "member_del.html")