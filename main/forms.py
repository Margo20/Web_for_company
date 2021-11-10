from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from .models import *
from django import forms


class AccountLoginForm(forms.Form):
    login = forms.CharField(max_length=100, label="Логин")
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=100, label="Пароль"
    )


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput, max_length=75, label="Старый пароль"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, max_length=75, label="Новый пароль"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, max_length=75, label="Повторить пароль"
    )

    class Meta:
        model = ExtendUser
        fields = ["old_password", "new_password1", "new_password2"]


class UserFormRegister(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Повторить пароль",
        help_text="Введите пароль повторно для проверки",
    )

    def clean_password1(self):
        # валидный ли пароль
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Введенные пароли не совпадают", code="password_mismatch"
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.is_activated = False
        if commit:
            user.save()
        return user

    class Meta:
        model = ExtendUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = "__all__"


class AddPositionForm(forms.ModelForm):
    class Meta:
        model = PositionModel
        fields = ("name",)
        labels = {"name": "Название должности"}


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = DepartmentModel
        fields = ("name",)
        labels = {"name": "Название отедела"}


class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        fields = ("department",)
