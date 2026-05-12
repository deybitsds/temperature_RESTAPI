from django.urls import path
from semaphoree.views import SemaphoreViewSet

urlpatterns = [
    path('api/semaphore/', SemaphoreViewSet.as_view({'get': 'show', 'post': 'update'}), name='semaphore_show'),
]
