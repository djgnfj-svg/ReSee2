from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from accounts.form import LoginForm, MemberDelForm, MemberUpdateForm, RegisterForm
from accounts.models import MyUser

# Create your views here.
@csrf_exempt
def login_view(request):
    login_form = LoginForm()

    #중복됨 계선 필요
    for visible in login_form.visible_fields():
        visible.field.widget.attrs["class"] = "form-control"

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        for visible in login_form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        if login_form.is_valid():
            temp_email = login_form.cleaned_data.get("email")
            temp_password = login_form.cleaned_data.get("password")
            try :
                user = MyUser.objects.get(email=temp_email)
            except MyUser.DoesNotExist:
                pass
            else:
                if user.check_password(temp_password):
                    login(request, user)
                    return redirect("home")
        else:
            msg = f"올바르지 않은 데이터 입니다."
            return render(request, "login.html", {"login_form" :login_form, "msg" : msg})
    else :
        return render(request, "login.html", {"login_form" :login_form})

def logout_view(request):
    if request.session.get('user'):
        del(request.session['user'])
    logout(request)
    return redirect("home")

@csrf_exempt
def register_view(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        for visible in register_form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        if register_form.is_valid():
            useremail = request.POST.get('useremail',None)
            try:
                user = MyUser.objects.get(email=useremail)
                if user:
                    return redirect("login")
            except MyUser.DoesNotExist:
                if register_form.is_valid():
                    login(request, register_form.save())
                    return redirect("home")
        else:
            msg = f"올바르지 않은 데이터 입니다."
            return render(request,'register.html', {"register_form" : register_form, "msg" : msg})
    else:
        for visible in register_form.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        return render(request,'register.html', {"register_form" :register_form})

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