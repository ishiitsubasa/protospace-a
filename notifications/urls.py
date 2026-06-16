from django.urls import path
from . import views
 
app_name = "notifications"
 
urlpatterns = [
    # ポーリング用：未読件数を返す
    path("unread-count/", views.unread_count, name="unread_count"),
    # ベルクリック時：全件既読
    path("mark-all-read/", views.mark_all_read, name="mark_all_read"),
    # 個別既読（任意）
    path("<int:notification_id>/read/", views.mark_one_read, name="mark_one_read"),
]
 