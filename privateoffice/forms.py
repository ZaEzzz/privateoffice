# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.extras.widgets import SelectDateWidget
from privateoffice.models import *


class addOrderForm(forms.Form):
    FORM_NAME = 'AddOrderForm'
    country = forms.CharField(label='Страна')
    resort = forms.CharField(label='Курорт')
    hotel = forms.CharField(label='Отель')
    firstName = forms.CharField(label='Имя')
    lastName = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='E-Mail')
    #date = forms.DateField(label='Дата вылета', widget=CalendarWidget)
    #date = forms.DateField(label='Дата вылета', widget=AdminDateWidget)
    date = forms.DateField(label='Дата вылета', widget=SelectDateWidget)
    nights = forms.IntegerField(label='Кол-во ночей', initial=7)
    count = forms.IntegerField(label='Кол-во человек', initial=1)


