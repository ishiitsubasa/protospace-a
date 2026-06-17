from django.urls import path
from .views import IndexView, toggle_like

app_name = 'posts'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:post_id>/like/', toggle_like, name='toggle_like'),
]
