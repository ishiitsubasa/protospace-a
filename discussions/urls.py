from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('posts/<int:post_pk>/discussions/', views.DiscussionIndexView.as_view(), name='index'),
    path('posts/<int:post_pk>/discussions/create/', views.DiscussionCreateView.as_view(), name='create'),
]