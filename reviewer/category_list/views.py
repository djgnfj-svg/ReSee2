import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from reviewer.form import CateCreateForm, StudyCreateForm, StudyReviewForm
from reviewer.models import Categories, Statistic, StudyList
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from reviewer.utils import dateCalculation

def category_view(request):
    print(request)
    if request.method == "POST":
        print(request.POST)
        return JsonResponse(request.POST)
    msg = "asdf"
    get_list = Categories.objects.order_by("created_at").filter(creator_id=request.user.id)
    return render(request, "cate_list.html", {"list" : get_list, "msg":msg})


@login_required
def category_create_view(request):
    msg = None
    if request.method == "POST":
        form = CateCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('name')} 생성완료!"
            messages.add_message(request, messages.INFO, msg)
            form.save(request)
            return redirect("cate_list")
        else:
            form =CateCreateForm()
    else:
        form =CateCreateForm()
    return render(request, "cate_create.html", {"form":form})

@login_required
def category_change_view(request, action, category_id):
    if request.method == "POST":
        list_data = Categories.objects.filter(id=category_id)
        if list_data.exists():
            if list_data.first().creator_id != request.user.id:
                msg = "자신이 소유하지 않은 list 입니다리~~"
            else:
                if action == "delete":
                    msg = f"{list_data.first().name} 삭제 완료"
                    list_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{list_data.first().name} 수정 완료"
                    form = CateCreateForm(request.POST)
                    form.update_form(request, category_id)
                    messages.add_message(request, messages.INFO, msg)
    elif request.method == "GET" and action == "update":
        list_data = Categories.objects.filter(pk=category_id).first()
        form = CateCreateForm(instance=list_data)
        return render(request, "cate_create.html", {"form" : form, "is_update":True})
    elif request.method == "GET" and action == "study_list":
        return study_list_view(request, category_id)
    return redirect("cate_list")

def study_list_view(request, category_id):
    form = StudyList.objects.order_by("created_at").filter(creator_id = request.user.id, category_id = category_id)
    return render(request, "study_list.html", {"form" : form, "category_id":category_id})

@login_required
def study_create_view(request, category_id):
    msg = None
    if request.method == "POST":
        form = StudyCreateForm(request.POST)
        if form.is_valid():
            msg = f"{form.cleaned_data.get('name')} 생성완료!"
            messages.add_message(request, messages.INFO, msg)
            temp = Categories.objects.filter(id=category_id).first()
            form.save(request, temp.id)
            return redirect("study_list", category_id)
        else:
            form =StudyCreateForm()
    else:
        form =StudyCreateForm()
    return render(request, "study_create.html", {"form":form})

@login_required
def study_change_view(request, category_id, action, study_id):
    if request.method == "POST":
        list_data = StudyList.objects.filter(id=study_id)
        if list_data.exists():
            if list_data.first().creator_id != request.user.id:
                msg = "자신이 소유하지 않은 list 입니다리~~"
            else:
                if action == "delete":
                    msg = f"{list_data.first().study_topic} 삭제 완료"
                    list_data.delete()
                    messages.add_message(request, messages.INFO, msg)
                elif action == "update":
                    msg = f"{list_data.first().study_topic} 수정 완료"
                    form = StudyCreateForm(request.POST)
                    if form.is_valid():
                        form.update_form(request, study_id)
                    else :
                        msg = f"에메함 "
                    print(form.errors.as_json())
                    messages.add_message(request, messages.INFO, msg)
    elif request.method == "GET" and action == "update":
        list_data = StudyList.objects.filter(pk=study_id).first()
        form = StudyCreateForm(instance=list_data)
        return render(request, "study_create.html", {"form" : form, "is_update":True})
    return redirect("study_list", category_id)

def study_review_view(request, category_id, study_id):
    try:
        base_time = StudyList.objects.filter(category_id=category_id).order_by("-created_at").first().created_at
    except:
        return redirect("cate_list")
    review_list = dateCalculation(base_time, StudyList.objects.filter(category_id = category_id))
    print(review_list)
    prev_button = False
    finish_button = False
    if study_id == 99:
        for object in review_list:
            list_data = StudyList.objects.filter(pk=object.id)
            temp = list_data.get(id=object.id)
            temp.review_count_up()
        # 일단 제목만 저장해도 무방할 거라고 보는데
        # tracking
        category = Categories.objects.filter(id=category_id)
        study = StudyList.objects.filter(id=category_id)
        custom_params = request.GET.dict() if request.GET.dict() else None

        history = Statistic()
        history.record(request, category, study, custom_params)
        return redirect("cate_list")
    try:
        if (study_id-1) >= 0:
            prev_button = True
        if (study_id+1) == len(review_list):
            finish_button = True
        form = StudyReviewForm(instance=review_list[study_id])
    except IndexError:
        messages.add_message(request, messages.INFO, "복습할 껀덕지가 없다 이말이야")
        return redirect("cate_list")
    else:
        return render(request, "study_review.html", {"form" : form, "category_id" : category_id,
        "study_id" : study_id, "prev_button" : prev_button, "finish_button" : finish_button})