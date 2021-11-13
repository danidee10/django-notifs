import django.dispatch

pre_send = django.dispatch.Signal()
pre_bulk_send = django.dispatch.Signal()

post_send = django.dispatch.Signal()
post_bulk_send = django.dispatch.Signal()
