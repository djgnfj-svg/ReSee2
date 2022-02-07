from pyexpat import model
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import MyUser, PayPlan
from reviewer.form_utils import category_guard

from reviewer.models import Categories, StudyList

class CateCreateForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name"]

    def save(self, request, commit=True):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.name = instance.name.strip()
        if category_guard(instance.category_count, request.user.id):
            return False
        else:
            instance.category_count = (instance.category_count + 1)
        if commit:
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.name = instance.name.strip()
        Categories.objects.filter(pk=list_id, creator_id=request.user.id).update(category_name=instance.category_name)

class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_title",
            "study_content",
        ]
    def save(self, request, category_id, commit=True):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.category_id = category_id
        instance.study_title = instance.study_title.strip()
        instance.study_content = instance.study_content.strip()
        instance.review_count = 0
        if commit:
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.study_title = instance.study_title.strip()
        instance.study_content = instance.study_content.strip()
        StudyList.objects.filter(pk=list_id, creator_id=request.user.id).update(
            study_title=instance.study_title, study_content=instance.study_content)

class StudyReviewForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_title",
            "study_content",
        ]


class PayPlanForm(forms.ModelForm):
    class Meta:
        model = PayPlan
        fields = [
            "name",
        ]
    def save(self, request, User, commit=True):
        instance = super(PayPlanForm, self).save(commit=False)
        instance.name = instance.name.strip()
        for v in PayPlan.Memberships.choices:
            if v[1] == instance.name:
                instance.price = v[0]
                break
        instance.subscribers = MyUser.objects.filter(id=User).first()
        if commit:
            instance.save()
        return instance

    def update_form(self, request, User, commit=True):
        instance = super(PayPlanForm, self).save(commit=False)
        instance.name = instance.name.strip()
        for v in PayPlan.Memberships.choices:
            if v[1] == instance.name:
                instance.price = v[0]
                break
        if commit:
            PayPlan.objects.filter(subscribers_id = request.user.id).update(name=instance.name, price=instance.price)
        return instance
