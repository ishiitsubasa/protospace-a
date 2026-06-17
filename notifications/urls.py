from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("unread-count/", views.unread_count, name="unread_count"),
    path("mark-all-read/", views.mark_all_read, name="mark_all_read"),
    path("<int:notification_id>/read/", views.mark_one_read, name="mark_one_read"),
    path("", views.notification_list, name="list"),      # ← 追加
]