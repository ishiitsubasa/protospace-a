from django.urls import path
from .views import UpdateView
app_name='Posts'

urlpatterns = [
  path('posts/<int:pk>/update', UpdateView.as_view(), name='update'),

]
