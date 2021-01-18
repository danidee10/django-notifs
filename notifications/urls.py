"""Frontend urls."""

from django.urls import path

from . import views


app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationsView.as_view(), name='notifications_view'),
    path('generate-notification/', views.GenerateNotification.as_view())
]
