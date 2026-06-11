from django.urls import path,include
from .views import PostCreateView,PostDeleteView

app_name='Posts'

urlpatterns = [
  
  path('posts/create/',PostCreateView.as_view(),name='create'),
   path('posts/<int:pk>/delete',PostDeleteView.as_view(),name='delete'),


]
