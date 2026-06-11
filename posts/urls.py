from django.urls import path
from .views import IndexView, DetailView, PostDetailView,PostDeleteView

app_name='Posts'

urlpatterns = [
  path('', IndexView.as_view(), name='index'),
  path('detail/int:pk/', DetailView.as_view(), name='detail'),
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),
  path('posts/<int:pk>/delete',PostDeleteView.as_view(),name='delete'),

]