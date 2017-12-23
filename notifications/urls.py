"""Frontend urls."""

from django.conf.urls import url

from . import views


app_name = 'notifications'

urlpatterns = [
    url(r'^$', views.NotificationsView.as_view(),
        name='notifications_view'),
    url(r'^generate-notification/$', views.GenerateNotification.as_view())
]
