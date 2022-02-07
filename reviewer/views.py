from django.shortcuts import redirect, render

from accounts.models import PayPlan
from reviewer.form import PayPlanForm

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home_view(request):
	return render(request, "home.html")

@csrf_exempt
def payplan_view(request):
	if request.method == "POST":
		form = PayPlanForm(request.POST)
		if form.is_valid():
			form.save(request, request.user.id)
			return redirect("home")
	return render(request,"payplan.html")