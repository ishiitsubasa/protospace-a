from django.urls import path
from .views import DetailView

app_name='Posts'

urlpatterns = [
  path('posts/<int:pk>',DetailView.as_view(), name='detail'),

]