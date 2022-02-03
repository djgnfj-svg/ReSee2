from django import forms
from django.utils.translation import gettext_lazy as _

from reviewer.models import Categories, StudyList

class CateCreateForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name"]

    def save(self, request, commit=True):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.name = instance.name.strip()
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
        widgets ={
            "study_title":forms.Textarea(attrs={
                "class" : "form-control",
                "placeholder" : "학습 주제를 입력하세요! ex.. 접두사",
                "style" : "height : 30px"
                }),
        "study_content":forms.Textarea(attrs={
            "class": "new-class-name two",
                "placeholder" : "학습 내용을 입력하세요",
                "style" : "height : 500px; width : 90.75rem; outline:none; border:none; overflow: auto;"
                }),
        }
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
        widgets ={
            "study_title":forms.TextInput(attrs={"class" : "form-control",
             "disabled" : True,
             "style" : "width : 150px;"

             }),
            "study_content":forms.Textarea(attrs={"class" : "form-control",
             "disabled" : True,
            "style" : "height : 570px; width : 1440px; overflow : auto;",
             }),
        }