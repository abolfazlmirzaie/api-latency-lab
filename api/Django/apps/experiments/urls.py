from django.urls import path , include


urlpatterns = [
       path('async/', include('apps.experiments.async_bench.v1.urls'))
]
