from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import MyUser

class LoginForm(forms.Form):
	email = forms.EmailField(
			max_length=100, required=True, widget=forms.EmailInput(attrs={
             "class" : "input-field",
             "style" : "width:90%; height: 36.5px; padding : 9.75px 13px; margin-bottom: 2%;",
             })
	)
	password = forms.CharField(
		max_length=30, required=True,
		widget=forms.PasswordInput(attrs={
            "class" : "input-field",
            "style" : "width:90%; height: 36.5px; padding : 9.75px 13px;",
             })
	)

class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields=(
        "username",
        "password1",
        "password2",
        "useremail",
        )

        
    username = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={"class" : "input-field", "placeholder": "유저이름"})
    )
    password1 = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )
    password2 = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드 확인"})
    )
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일"})
    )
    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(RegisterForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["useremail"]
        if commit:
            user.save()
        return user

class MemberUpdateForm(forms.Form):
    class Meta:
        model = MyUser
        fields = (
            "useremail"
        )
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일수정"})
    )

class MemberDelForm(forms.Form):
    class Meta:
        model = MyUser
        fields = (
            "useremail",
            "password",
        )
    useremail = forms.EmailField(
        max_length=30, required=True, widget=forms.EmailInput(attrs={"class" : "input-field", "placeholder": "이메일수정"})
    )
    password1 = forms.CharField(
        max_length=30, required=True, 
        widget=forms.PasswordInput(attrs={"class" : "input-field", "placeholder": "패스워드"})
    )