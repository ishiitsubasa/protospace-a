from django.urls import path,include
from .views import CreateView,IndexView, DetailView, UpdateView, DeleteView

app_name='Posts'

urlpatterns = [
  
  path('posts/create/',CreateView.as_view(),name='create'),


]