from django.urls import path,include
from .views import PostCreateView, IndexView, PostDetailView, PostDetailView, PostUpdateView

app_name='Posts'

urlpatterns = [
  path('posts/create/',PostCreateView.as_view(),name='create'),
  path('', IndexView.as_view(), name='index'),
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),
  path('posts/<int:pk>/update', PostUpdateView.as_view(), name='update'),
]
