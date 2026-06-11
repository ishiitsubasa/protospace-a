from django.urls import path,include
from .views import PostCreateView
from .views import IndexView, DetailView, PostDetailView

app_name='Posts'

urlpatterns = [
  
  path('posts/create/',PostCreateView.as_view(),name='create'),



  path('', IndexView.as_view(), name='index'),
  path('detail/int:pk/', DetailView.as_view(), name='detail'),
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),

]
