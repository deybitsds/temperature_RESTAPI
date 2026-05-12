from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from semaphoree.serializer import SemaphoreSerializer
from semaphoree.models import SemaphoreState


class SemaphoreViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def _get_state(self):
        state, _ = SemaphoreState.objects.get_or_create(pk=1)
        return state

    @action(detail=False, methods=['get'])
    def show(self, request):
        state = self._get_state()
        wants_json = (
            request.headers.get('Accept') == 'application/json'
            or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        )
        if wants_json:
            return Response({
                'red': state.red,
                'yellow': state.yellow,
                'green': state.green,
                'updated_at': state.updated_at.isoformat(),
            }, status=status.HTTP_200_OK)
        return render(request, 'semaphore_show.html', {'state': state})

    @action(detail=False, methods=['post'])
    def update(self, request):
        serializer = SemaphoreSerializer(data=request.data)
        if serializer.is_valid():
            state = self._get_state()
            state.red = serializer.validated_data.get('red', state.red)
            state.yellow = serializer.validated_data.get('yellow', state.yellow)
            state.green = serializer.validated_data.get('green', state.green)
            state.save()
            return Response({
                'status': 200,
                'msg': 'Estado guardado',
                'state': {
                    'red': state.red,
                    'yellow': state.yellow,
                    'green': state.green,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
