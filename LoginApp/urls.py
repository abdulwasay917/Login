from django.urls import path
from .views import signup, user_login, forgot_password,user_logout,dashboard,reset_password

urlpatterns = [
    path('', user_login, name='login'),          # default page
    path('signup/', signup, name='signup'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/',dashboard , name='dashboard'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
]
