from django.conf.urls import patterns, include, url
from django.contrib import admin
from privateoffice import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^manage/$', views.manage, name='manage'),
    url(r'^office/$', views.office, name='office'),
    url(r'^office/order/(?P<order_id>\d+)/$', views.orderPDF, name='orderPDF'),
    url(r'^add/$', views.orderAdd, name='orderAdd'),
    url(r'^logout/$', views.authLogout, name='authLogout'),
    url(r'^login/$', views.authLogin, name='authLogin'),
    url(r'^sendmail/$', views.testmail, name='testmail'),
    url(r'^api/search/global/$', views.searchGlob, name='searchGlob'),
    url(r'^api/search/children/$', views.searchChildren, name='searchChildren'),
    url(r'^api/search/other/$', views.searchOther, name='searchOther'),
    url(r'^api/search/parent/$', views.searchParent, name='searchParent'),
    url(r'^api/addorder/$', views.addOrderGetForm, name='addOrderGetForm'),
    url(r'^api/order/confirm/$', views.addOrder, name='addOrder'),

    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),

)
