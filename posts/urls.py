from django.urls import path,include
from .views import PostCreateView, IndexView, PostDetailView, PostDeleteView, PostUpdateView, toggle_like, submit_sympathy_vote, submit_pain_score

app_name='Posts'

urlpatterns = [

  path('posts/create/',PostCreateView.as_view(),name='create'),



  path('', IndexView.as_view(), name='index'),
  path('posts/<int:pk>',PostDetailView.as_view(), name='detail'),
  path('posts/<int:pk>/delete',PostDeleteView.as_view(),name='delete'),
  path('posts/<int:pk>/update', PostUpdateView.as_view(), name='update'),
  path('posts/<int:pk>/like', toggle_like, name='like'),
  path('posts/<int:pk>/sympathy-vote', submit_sympathy_vote, name='sympathy_vote'),
  path('posts/<int:pk>/pain-score', submit_pain_score, name='pain_score'),

]
  

