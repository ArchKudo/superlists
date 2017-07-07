from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new_list/$', views.new_list_page, name='new_list_page'),
    url(r'^(\d+)/$', views.list_page, name='list_page'),
]
