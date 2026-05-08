from django.urls import path
from temperature.views import TemperatureViewSet

urlpatterns = [
    path('api/store/', TemperatureViewSet.as_view({'post': 'store'}), name='temperature_store'),
    path('api/table/', TemperatureViewSet.as_view({'get': 'table'}), name='temperature_table'),
    path('api/show/', TemperatureViewSet.as_view({'get': 'show'}), name='temperature_show'),
]
