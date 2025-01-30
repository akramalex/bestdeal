from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    path('success/', views.contact_success, name='contact_success'),
]
