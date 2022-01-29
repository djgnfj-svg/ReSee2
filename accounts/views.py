from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from accounts.form import LoginForm, MemberDelForm, MemberUpdateForm, RegisterForm
from accounts.models import MyUser

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            email = form_login.cleaned_data.get("email")
            raw_password = form_login.cleaned_data.get("password")
            msg = "가입되있지 않습니다."
        try :
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            pass
        else :
            if user.check_password(raw_password):
                msg = "성공"
                login(request, user)
                return render(request,"home.html")
    else:
        msg = None
        form_login = LoginForm()
    return render(request, "login.html", {"form_login" : form_login, "msg" : msg})

def logout_view(request):
    logout(request)
    return redirect("home")

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			msg = "가입완료"
		return render(request, "home.html", msg)
	return render(request, "register.html", {"form" : form})

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
    return render(request, "member_modify.html", {"form_Update" : form_Update})

@csrf_exempt
@login_required
def member_del_view(request):
    form_del = MemberDelForm()
    if request.method == "POST":
        form_del = MemberDelForm(request.POST)
        print(form_del.errors.as_json())
        if form_del.is_valid():
            user = request.user
            email = request.POST["useremail"]
            raw_password = request.POST["password1"]
            if user.check_password(raw_password):
                user.delete()
                return redirect("home")
    return render(request, "member_del.html", {"form_del" : form_del})