import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import ShopUser
from authapp.validators import check_name, check_size_file


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ['username', 'password']

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class ShopUserRegistrationForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл. почты'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_first_name(self):
        check_name(self.cleaned_data['first_name'])
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        check_name(self.cleaned_data['last_name'])
        return self.cleaned_data['last_name']

    def save(self, commit=True):
        user = super().save(commit)
        user.is_active = False
        solt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email+solt).encode()).hexdigest()
        user.save()
        return user


class UserProfileForm(UserChangeForm):
    avatar = forms.FileField(widget=forms.FileInput, required=False, validators=[check_size_file])
    age = forms.IntegerField(widget=forms.NumberInput, required=False, label='Возраст')

    class Meta:
        model = ShopUser
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['aria-describedby'] = 'usernameHelp'
        self.fields['username'].widget.attrs['readonly'] = True

        self.fields['email'].widget.attrs['aria-describedby'] = 'emailHelp'
        self.fields['email'].widget.attrs['readonly'] = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['avatar'].widget.attrs['class'] = 'custom-file-input'
        self.fields['avatar'].widget.attrs['size'] = 50

    def clean_first_name(self):
        check_name(self.cleaned_data['first_name'])
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        check_name(self.cleaned_data['last_name'], field_name='Фамилия')
        return self.cleaned_data['last_name']
