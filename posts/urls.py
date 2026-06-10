from django.urls import path,include
from .views import CreateView

app_name='Posts'

urlpatterns = [
  
  path('posts/create/',CreateView.as_view(),name='create'),


]