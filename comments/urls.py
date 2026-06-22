# comments/urls.py
from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='create'),
    path('<int:pk>/comment/topic/<int:topic_pk>/', views.CommentCreateView.as_view(), name='create_for_topic'),
]