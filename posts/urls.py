from django.urls import path
from .views import IndexView, DetailView, PostDetailView, UpdateView
app_name='Posts'

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),
  path('posts/<int:pk>/update', UpdateView.as_view(), name='update'),
]