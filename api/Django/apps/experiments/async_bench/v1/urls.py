from django.urls import path

from apps.experiments.async_bench.v1.views import (
    NotifySyncView,
    NotifyOffloadedView,
    notify_async_view,
)

urlpatterns = [
    path("notify-sync/", NotifySyncView.as_view(), name="notify-sync"),
    path("notify-async/", notify_async_view, name="notify-async"),
    path(
        "notify-offloaded/",
        NotifyOffloadedView.as_view(),
        name="notify-offloaded",
    ),
]

