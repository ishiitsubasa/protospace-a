from django.urls import path
from . import views
from .views import SignUpView
from django.contrib.auth.views import LoginView,LogoutView

app_name='users'

urlpatterns = [
    path('sign_up/',SignUpView.as_view(),name='sign_up'),
    path('logout/',LogoutView.as_view(next_page='/',),name='logout'),
    path('login/',LoginView.as_view(template_name='users/login.html'),name='login'),
]