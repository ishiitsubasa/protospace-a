from django.urls import path
from . import views

app_name = 'discussions'

urlpatterns = [
    path('create/<int:post_pk>/', views.DiscussionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.DiscussionDetailView.as_view(), name='detail'),
]