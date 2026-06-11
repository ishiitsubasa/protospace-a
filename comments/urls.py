from django.urls import path
from .views import CreateView,IndexView, DetailView, UpdateView, DeleteView

app_name='Posts'

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('posts/create/',CreateView.as_view(),name='create'),
  path('posts/<int:pk>',DetailView.as_view(), name='detail'),
   path('posts/<int:pk>/update', UpdateView.as_view(), name='update'),
  path('posts/<int:pk>/delete',DeleteView.as_view(),name='delete'),

]
