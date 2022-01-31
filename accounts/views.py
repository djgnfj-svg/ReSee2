import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from accounts.form import MemberDelForm, MemberUpdateForm
from accounts.models import MyUser

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        print(request.POST)
        user_email = request.POST.get("user_email")
        user_password = request.POST.get("user_password")
        res_data = {}
        if not (user_email and user_password):
            res_data['error'] = "모든 값을 입력해야 합니다."
        try :
            user = MyUser.objects.get(email=user_email)
        except MyUser.DoesNotExist:
            pass
        else :
            if user.check_password(user_password):
                login(request, user)
                return redirect("home")
    return render(request, "login.html")

def logout_view(request):
    if request.session.get('user'):
        del(request.session['user'])

    logout(request)
    return redirect("home")

@csrf_exempt
def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('user_name',None)
        useremail = request.POST.get('register_email',None)
        password = request.POST.get('register_password',None)
        repasswd = request.POST.get('confirm_password',None)

        res_data ={}
        if not (username and useremail and password and repasswd):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        elif password != repasswd:
            res_data['error'] ='비밀번호가 다릅니다.'

        try:
            user = MyUser.objects.get(email=useremail)
            if user:
                res_data['status'] = '0' # 기존 가입된 회원
                # return JsonResponse(res_data)
                return redirect("home")
        except MyUser.DoesNotExist:
            # 대문자 User 임에 주의
            user = MyUser(
                nickname = username,
                email = useremail,
                password = make_password(password)
            )
            user.save()
            # session 생성
            user = MyUser.objects.get(email=useremail)
            request.session['user'] = user.id
            res_data['status'] = '1' # 회원 가입 완료
            # return JsonResponse(res_data)
            return redirect("home")

        return render(request,'register.html',res_data)

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