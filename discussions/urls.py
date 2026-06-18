from django.urls import path
from . import views
from views import DiscussionIndexView,DiscussionCreateView

app_name='discussions'

urlpatterns = [
    path('discussions/create',DiscussionCreateView.as_view(),name='create'),
]
