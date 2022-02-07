from django.http import JsonResponse
from django.shortcuts import redirect, render
from reviewer.form import CateCreateForm, StudyCreateForm, StudyReviewForm
from reviewer.models import Categories, Statistic, StudyList
from django.contrib.auth.decorators import login_required

from reviewer.utils import dateCalculation

@login_required
def category_view(request):
    if request.method == "POST":
        cate_list = CateCreateForm(request.POST)
        if cate_list.is_valid():
            if cate_list.save(request):
                return JsonResponse(request.POST)
            else:
                res_data = {
                    # 나중에 좀더 자세히 보네야되겠다.
                    "error" : "please subscribe ReSee"
                }
                return JsonResponse(res_data)
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
    return render(request, "study_create.html")

@login_required
def study_change_view(request, category_id):
    return render(request, "study_change.html")

@login_required
def study_review_view(request, category_id, study_id):
    return render(request, "study_review.html")