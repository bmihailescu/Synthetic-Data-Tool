from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    # url(r'^(?P<task_id>[\w-]+)/$', views.get_progress, name='task_status')
    path('salesforce', views.salesforce, name="salesforce"),
]