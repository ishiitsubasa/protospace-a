from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('create/<int:post_pk>/', views.DiscussionCreateView.as_view(), name='create'),
    
    path('<int:pk>/', views.DiscussionDetailView.as_view(), name='detail'),
    path('posts/<int:post_pk>/discussions/', views.DiscussionIndexView.as_view(), name='index'),
    path('posts/<int:post_pk>/discussions/create/', views.DiscussionCreateView.as_view(), name='create'),
]