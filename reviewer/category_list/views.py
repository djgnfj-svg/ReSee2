from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from reviewer.form import CateCreateForm, StudyCreateForm, StudyReviewForm
from reviewer.models import Categories, Statistic, StudyList
from django.contrib.auth.decorators import login_required

from reviewer.utils import Msg_text, dateCalculation

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
def study_detail_view(request, category_id, study_id):
    return render(request, "study_view.html")


@login_required
def study_review_view(request, category_id):
    if request.method == "POST":
        finish = request.POST.get("finish", None)
        print(finish)
        if finish != None:
            temp = StudyList.objects.filter(
                category_id=category_id, creator_id = request.user.id).order_by(
                    "-created_at").first()
            if temp == None:
                raise Http404
            else:
                base_time = temp.created_at
            review_list = dateCalculation(base_time, StudyList.objects.filter(category_id = category_id))
            for l in review_list:
                list_data = StudyList.objects.filter(pk=l.id)
                temp = list_data.get(id=l.id)
                temp.review_count_up()
            category = Categories.objects.filter(id=category_id)
            study = StudyList.objects.filter(id=category_id)
            custom_params = request.GET.dict() if request.GET.dict() else None
            history = Statistic()
            history.record(request, category, study, custom_params)
            return JsonResponse(Msg_text("msg","ok")) 
        else:
            return JsonResponse(Msg_text("error","temp error"))
    return render(request, "study_review.html")