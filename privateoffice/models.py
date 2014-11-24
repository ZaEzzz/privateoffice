# -*- coding: utf-8 -*-
from datetime import datetime
from random import choice, randint
from django.conf import settings
from django.db import models
from privateoffice.fields import AutoOneToOneField
from django.contrib.auth.models import User


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^privateoffice\.fields\.AutoOneToOneField',])



class Country(models.Model):
    name = models.CharField('Страна', max_length=60)
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
    def __unicode__(self):
        return self.name

class Resort(models.Model):
    name = models.CharField('Курорт', max_length=120)
    country = models.ForeignKey(Country, related_name='resorts')
    class Meta:
        verbose_name = 'Курорт'
        verbose_name_plural = 'Курорты'
    def __unicode__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField('Отель', max_length=120)
    resort = models.ForeignKey(Resort, related_name='hotels')
    stars = models.IntegerField('Звезды', default=randint(1,5))
    country = models.ForeignKey(Country, related_name='hotels', default=1)
    price = models.IntegerField('Стоимость суток', default=randint(10, 600))
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
    def __unicode__(self):
        return self.name

class Client(models.Model):
    user = AutoOneToOneField(User, related_name='client', primary_key=True)
    tel = models.CharField('Номер телефона', max_length=15)
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    def __unicode__(self):
        return self.tel
        #self.user.get_username()

class Order(models.Model):
    status_choise = (
        ('N',   'Новая'),
        ('W',   'В работе'),
        ('A',   'Принята'),
        ('P',   'Оплачена'),
        ('C',   'Отменена'),
        ('D',   'Выполнена'),
    )
    client = models.ForeignKey(User, related_name='orders')
    hotel = models.ForeignKey(Hotel, related_name='orders')
    manager = models.ForeignKey(User, related_name='manager_orders', blank=True, null=True, default='', on_delete=models.SET_NULL)
    depart = models.DateField('Дата вылета')
    night = models.IntegerField('Количество ночей')
    status = models.CharField('Статус', max_length=1, choices=status_choise, default='N')
    added = models.DateTimeField('Добавлена', auto_now_add=True)
    price = models.IntegerField('Стоимость', default=0)
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    def __unicode__(self):
        return unicode(self.depart)

class People(models.Model):
    order = models.ForeignKey(Order, verbose_name='people')
    firstName = models.CharField('Имя', max_length=100, blank=True, null=True, default='')
    lastName = models.CharField('Фамилия', max_length=100, blank=True, null=True, default='')
    patronymic = models.CharField('Отчество', max_length=100, blank=True, null=True, default='')
    passport = models.CharField('Серия и номер паспорта через пробел', max_length=30, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
    def __unicode__(self):
        return u'%s %s' %(self.firstName, self.lastName)
