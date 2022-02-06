import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from reviewer.form import CateCreateForm, StudyCreateForm, StudyReviewForm
from reviewer.models import Categories, Statistic, StudyList
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from reviewer.utils import dateCalculation

@login_required
def category_view(request):
    if request.method == "POST":
        cate_list = CateCreateForm(request.POST)
        if cate_list.is_valid():
            cate_list.save(request)
            return JsonResponse(request.POST)
    return render(request, "cate_list.html")

@login_required
def study_list_view(request, category_id):
    if request.method == "POST":
        form = StudyCreateForm(request.POST)
        if form.is_valid():
            temp = Categories.objects.filter(id=category_id).first()
            form.save(request, temp.id)
        return redirect("study_list", category_id)
    return render(request, "study_list.html")

@login_required
def study_create_view(request, category_id):
    if request.method == "POST":
        form = StudyCreateForm(request.POST)
        if form.is_valid():
            temp = Categories.objects.filter(id=category_id).first()
            form.save(request, temp.id)
            return redirect("study_list", category_id)
        else:
            form =StudyCreateForm()
    print("Test")
    return render(request, "study_create.html")

@login_required
def study_change_view(request, category_id, action, study_id):
    if request.method == "POST":
        list_data = StudyList.objects.filter(id=study_id)
        if list_data.exists():
            # if list_data.first().creator_id != request.user.id:
            #     msg = "자신이 소유하지 않은 list 입니다리~~"
            # else:
                if action == "delete":
                    list_data.delete()
                elif action == "update":
                    form = StudyCreateForm(request.POST)
                    if form.is_valid():
                        form.update_form(request, study_id)
                return JsonResponse(request.POST)
    return redirect("study_list", category_id)

def study_review_view(request, category_id, study_id):
    try:
        base_time = StudyList.objects.filter(category_id=category_id).order_by("-created_at").first().created_at
    except:
        return redirect("cate_list")
    review_list = dateCalculation(base_time, StudyList.objects.filter(category_id = category_id))
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
        return redirect("cate_list")
    else:
        return render(request, "study_review.html", {"form" : form, "category_id" : category_id,
        "study_id" : study_id, "prev_button" : prev_button, "finish_button" : finish_button})