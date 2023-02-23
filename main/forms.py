from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class AddTripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['driver', 'from_city', 'to_city', 'info', 'date', 'time', 'capacity', 'price']
        widgets = {
            'date': forms.SelectDateWidget(),
            'time': forms.TimeInput(format='%H:%M'),
            'info': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'capacity': forms.Select(choices=[(1, 1), (2, 2), (3, 3), (4, 4)]),
            'driver': forms.HiddenInput(),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=10)
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }


class SearchTripForm(forms.Form):
    FROM_CITIES = Trip.objects.values('from_city')
    SET_FROM = set(list(map(lambda x: list(x.values())[0], list(FROM_CITIES))))
    FROM_CHOICES = list(zip([x for x in range(1, len(SET_FROM) + 1)], SET_FROM))

    from_city = forms.ChoiceField(choices=FROM_CHOICES, label='Откуда')


    TO_CITIES = Trip.objects.values('to_city')
    SET_TO = set(list(map(lambda x: list(x.values())[0], list(TO_CITIES))))
    TO_CHOICES = list(zip([x for x in range(1, len(SET_TO) + 1)], SET_TO))

    to_city = forms.ChoiceField(choices=TO_CHOICES, label='Куда')

    DATE = Trip.objects.values('date')
    SET_DATE = set(list(map(lambda x: list(x.values())[0], list(DATE))))
    DATE_CHOICES = list(zip([x for x in range(1, len(SET_DATE) + 1)], SET_DATE))
    date = forms.ChoiceField(choices=DATE_CHOICES, label='Дата')


class RedInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['info', 'photo']
        widgets = {
            'info': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = []