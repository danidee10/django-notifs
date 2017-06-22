"""Frontend urls."""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.NotificationsView.as_view(),
        name='notifications_view')
]
