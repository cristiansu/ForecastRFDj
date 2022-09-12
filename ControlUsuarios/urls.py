from django.urls import path, include
from .views import home, login_attemp, register_attemp, success, token_send, verify, error_page
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home', home, name='home'),
    path('register', register_attemp, name='register'),
    path('login', login_attemp, name='login'),
    path('logout', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('token', token_send, name='token'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error_page, name='error'),
]