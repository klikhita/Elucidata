from django.conf.urls import url
from . import views


urlpatterns= [
    url(r'^$',views.index,name='index'),
    url(r'^api1/$',views.api1,name='api1'),
    url(r'^api1/api2/$',views.api2,name='api2'),
    url(r'^api1/api2/api3/$',views.api3,name='api3')


]

