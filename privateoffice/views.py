# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseForbidden
from django.core import serializers
from privateoffice.models import *
from privateoffice.forms import *
#from privateoffice.forms import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import authenticate, login
import string
import random
from django.core.mail import send_mail
from privateoffice.settings import *
from django.shortcuts import get_list_or_404, get_object_or_404

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.units import cm
#from reportlab.pdfbase import ttfonts


def gen_pass(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@ensure_csrf_cookie
def index(request):
    tpl = 'privateoffice/index.html'
    return render(request, tpl,{
        'test':     'Pass',
    })

@ensure_csrf_cookie
def orderAdd(request):
    tpl = 'privateoffice/order_add.html'
    countryList = Country.objects.all()
    resortList = Resort.objects.all()[:30]
    hotelList = Hotel.objects.all()[:30]
    return render(request, tpl, {
        'countryList':  countryList,
        'resortList':   resortList,
        'hotelList':    hotelList,
    })

@login_required
def office(request):
    tpl = 'privateoffice/office.html'
    user = request.user
    #try:
    orderList = user.orders.all
    #except:
    #    orderList = ''
    #try:
    orderHistory = user.orders.filter(status__iexact='D')
    #except:
    #    orderHistory = ''
    return render(request, tpl, {
        'user':         user,
        'orderList':    orderList,
        'orderHistory': orderHistory,
    })

def manage(request):
    tpl = 'privateoffice/manage.html'
    return render(request, tpl)

def authLogout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

#@ensure_csrf_cookie
def authLogin(request):
    if request.is_ajax():
        if request.method == 'POST':
            userLogin = request.POST['login']
            userPassword = request.POST['password']
            user = authenticate(username=userLogin, password=userPassword)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('good')
                else:
                    # Return a 'disabled account' error message
                    return HttpResponse('FAIL')
            else:
                # Return an 'invalid login' error message.
                return HttpResponse('Invalid password')
	return HttpResponseForbidden()

def searchGlob(request):
    if request.is_ajax():
        searchString = request.body
        countryList = Country.objects.filter(name__icontains=searchString)
        resortList = Resort.objects.filter(name__icontains=searchString)[:20]
        hotelList = Hotel.objects.filter(name__icontains=searchString)[:20]
        allObjects = list(countryList) + list(resortList) + list(hotelList)
        output = serializers.serialize('json', allObjects)
        return HttpResponse(output, content_type="application/json")
    return HttpResponseForbidden()

def searchChildren(request):
    if request.is_ajax():
        searchString = request.body
        parent = Country.objects.get(pk=searchString)
        resortList = parent.resorts.all()
        hotelList = parent.hotels.all()[:30]
        allObjects = list(resortList) + list(hotelList)
        output = serializers.serialize('json', allObjects)
        return HttpResponse(output, content_type="application/json")
    return HttpResponseForbidden()

def searchOther(request):
    if request.is_ajax():
        searchString = request.body
        selectedObj = Resort.objects.get(pk=searchString)
        parent=Country.objects.filter(pk__iexact=selectedObj.country_id)
        hotelList = selectedObj.hotels.all()
        allObjects = list(parent) + list(hotelList)
        output = serializers.serialize('json', allObjects)
        return HttpResponse(output, content_type="application/json")
    return HttpResponseForbidden()

def searchParent(request):
    if request.is_ajax():
        searchString = request.body
        selectedObj = Hotel.objects.get(pk=searchString)
        hotel = Hotel.objects.filter(pk__iexact=selectedObj.id)
        parent = Resort.objects.filter(pk__iexact=selectedObj.resort_id)
        grandpa = Country.objects.filter(pk__iexact=selectedObj.country_id)
        #hotelList = parent.hotels.all()
        allObjects = list(parent) + list(grandpa) + list(hotel)
        output = serializers.serialize('json', allObjects)
        return HttpResponse(output, content_type="application/json")
    return HttpResponseForbidden()

@ensure_csrf_cookie
def addOrderGetForm(request):
    if request.is_ajax():
        if request.method == 'POST':
            tpl = 'privateoffice/order_add_form.html'
            obj_pk = request.body
            hotel = Hotel.objects.get(pk=obj_pk)
            resort = hotel.resort
            country = hotel.country
            form = addOrderForm(initial={
                'hotel':    hotel,
                'resort':   resort,
                'country':  country,
            })
            return render(request, tpl, {
                'hotel':    hotel,
                'resort':   resort,
                'country':  country,
                'form':     form,
            })
    return HttpResponseForbidden()

def addOrder(request):
    if request.is_ajax():
        if request.method == 'POST':
            hotel = int(request.POST['hotel'])
            firstName = request.POST['firstname']
            lastName = request.POST['lastname']
            email =  request.POST['email']
            date =  request.POST['date']
            #date =  '2006-10-25'
            nights =  int(request.POST['nights'])
            count =  int(request.POST['count'])
            hotel = Hotel.objects.get(pk=hotel)
            resort = hotel.resort
            country = hotel.country
            #form = addOrderForm()
            form = addOrderForm({
                'hotel':    hotel,
                'resort':   resort,
                'country':  country,
                'firstName':firstName,
                'lastName': lastName,
                'email':    email,
                'date':     date,
                'nights':   nights,
                'count':    count,
            })
            if form.is_valid():
                # Create user
                password = gen_pass()
                user = User.objects.create_user(email, email, password)
                user.first_name = firstName
                user.last_name = lastName
                user.save()
                userAuth = authenticate(username=email, password=password)
                if userAuth.is_active:
                    login(request, userAuth)
                    # TODO: Send E-Mail with password
                else:
                    # Return a 'disabled account' error message
                    return HttpResponse('Account is disable')
                # Create client
                client = user.client
                # Create order
                price = count * nights * hotel.price
                order = Order(
                    client = user,
                    hotel = hotel,
                    depart = date,
                    night = nights,
                    price = price,
                )
                order.save()
                # Create passengers
                passenger = People(
                    order = order,
                    firstName = firstName,
                    lastName = lastName,
                    patronymic = '',
                    passport = ''
                )
                passenger.save()
                if count > 1:
                    for i in range(2,count):
                        passenger = People(
                            order = order,
                            firstName = '',
                            lastName = '',
                            patronymic = '',
                            passport = ''
                        )
                        passenger.save()
                # TODO: Get e-mail settings addres from settings
                # TODO: Use mail templates
                subject = 'Письмо с личного кабинета'
                message = u'''
                Добрый день!
                Мы рады привествовать вас в на нашем сайте в нашем личном кабинете!
                Для вас автоматически был создан аккаунт.
                Реквизиты для входа:
                Логин: %s
                Пароль: %s
                Адрес сайта: %s
                ''' % (email, password, ADDRESS_FOR_MAIL)
                send_mail(
                    subject,
                    message,
                    MAIL_FROM,
                    [email],
                    fail_silently=False
                )
                return HttpResponse('good')
            return HttpResponse('Не все поля заполнены')
    return HttpResponse('Epic fail')

@login_required
def orderPDF(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user == order.client:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = u'attachment; filename="договор.pdf"'
        
        font = ttfonts.TTFont('Arial', ARIAL_FILE)
        pdfmetrics.registerFont(font)

        pfile = canvas.Canvas(response)
        pfile.setFont('Arial', 14)
        fstring = u"Договор №%s" % order_id
        pfile.drawString(8.5*cm, 25*cm, fstring)
        fstring = u'Договор №%s составлен между гражданином %s %s и компанией' % (order_id, order.client.first_name, order.client.first_name)
        pfile.drawString(2*cm, 24*cm, fstring)
        fstring = u'КОМПАНИЯ в оказании услуг по путешевствию в страну пребывания'
        pfile.drawString(2*cm, 23*cm, fstring)
        fstring = u'Отель: %s' % (order.hotel)
        pfile.drawString(2*cm, 22*cm, fstring)
        fstring = u'Дата вылета: %s' % (order.depart)
        pfile.drawString(2*cm, 21*cm, fstring)
        fstring = u'Количество ночей проживания: %s' % (order.night)
        pfile.drawString(2*cm, 20*cm, fstring)
        pfile.showPage()
        pfile.save()
        return response
    return HttpResponseForbidden()



def testmail(request):
    pass
    return HttpResponseForbidden()
