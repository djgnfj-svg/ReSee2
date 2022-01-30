from django import forms
from django.utils.translation import gettext_lazy as _

from reviewer.models import Categories, StudyList

class CateCreateForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ["name"]
        labels = {
            "name" : _("과목이름"),
        }
        widgets ={
            "name":forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "케테고리 입력하세욥!",
                }),
        }
        
    def save(self, request, commit=True):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.name = instance.name.strip()
        if commit:
            print("Teststsets")
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(CateCreateForm, self).save(commit=False)
        instance.category_name = instance.category_name.strip()
        Categories.objects.filter(pk=list_id, creator_id=request.user.id).update(category_name=instance.category_name)

class StudyCreateForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_topic",
            "study_contect",
        ]
        widgets ={
            "study_topic":forms.Textarea(attrs={
                "class" : "form-control",
                "placeholder" : "학습 주제를 입력하세요! ex.. 접두사",
                "style" : "height : 30px"
                }),
        "study_contect":forms.Textarea(attrs={
            "class": "new-class-name two",
                "placeholder" : "학습 내용을 입력하세요",
                "style" : "height : 500px; width : 90.75rem; outline:none; border:none; overflow: auto;"
                }),
        }
    def save(self, request, category_id, commit=True):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.creator_id = request.user.id
        instance.category_id = category_id
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        instance.review_count = 0
        if commit:
            instance.save()
        return instance

    def update_form(self, request, list_id):
        instance = super(StudyCreateForm, self).save(commit=False)
        instance.study_topic = instance.study_topic.strip()
        instance.study_contect = instance.study_contect.strip()
        StudyList.objects.filter(pk=list_id, creator_id=request.user.id).update(
            study_topic=instance.study_topic, study_contect=instance.study_contect)

class StudyReviewForm(forms.ModelForm):
    class Meta:
        model = StudyList
        fields = [
            "study_topic",
            "study_contect",
        ]
        widgets ={
            "study_topic":forms.TextInput(attrs={"class" : "form-control",
             "disabled" : True,
             "style" : "width : 150px;"

             }),
            "study_contect":forms.Textarea(attrs={"class" : "form-control",
             "disabled" : True,
            "style" : "height : 570px; width : 1440px; overflow : auto;",
             }),
        }