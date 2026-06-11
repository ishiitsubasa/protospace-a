from django.urls import path
from .views import PostDetailView

app_name='Posts'

urlpatterns = [
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),

]