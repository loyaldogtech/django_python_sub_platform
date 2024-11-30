from django.urls import path
from . import views


urlpatterns = [
   
    path('software_engineer-dashboard', views.software_engineer_dashboard, name='software_engineer-dashboard'),
    path('create-article', views.create_article, name='create-article'),
]