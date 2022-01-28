from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout


from accounts.form import LoginForm, RegisterForm
from accounts.models import MyUser
from ReSee.settings import AUTH_USER_MODEL

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
            user = AUTH_USER_MODEL.objects.get(email=email)
        except AUTH_USER_MODEL.DoesNotExist:
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

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			msg = "가입완료"
		return render(request, "home.html", msg)
	return render(request, "register.html", {"form" : form})
