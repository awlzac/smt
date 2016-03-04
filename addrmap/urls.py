from django.conf.urls import url
from addrmap import views

urlpatterns = [
    url(r'^address/get/', views.address_get, name='address_get'),
    url(r'^address/trunc/', views.address_trunc, name='address_trunc'),
    url(r'^address/add', views.address_add, name='address_add'),
    # any other url -> index page
    url(r'^', views.index, name='index')
]
