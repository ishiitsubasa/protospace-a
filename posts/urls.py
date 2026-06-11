from django.urls import path,include
from .views import PostCreateView

app_name='Posts'

urlpatterns = [
  
  path('posts/create/',PostCreateView.as_view(),name='create'),


]