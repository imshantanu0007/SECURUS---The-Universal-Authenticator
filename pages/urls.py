from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('About/', views.about, name='about'),
        path('Register_form',views.Register_form, name='Register_form'),
        path('Enter_otp/', views.Enter_otp, name='Enter_otp'),
        path('Otp_validation',views.Otp_validation, name='Otp_validation'),
        path('Otp_validation1',views.Otp_validation1, name='Otp_validation1'),
        path('Enter_otp1/', views.Enter_otp1, name='Enter_otp1'),
        path('home1/', views.home1, name='home1'),
        path('loading/', views.loading, name='loading'),
]
