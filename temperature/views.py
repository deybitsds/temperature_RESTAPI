import json
import traceback

from django.db.models import Min, Max, Avg
from django.db.models import Min, Max, Avg
from django.shortcuts import render
import adrf.viewsets as viewsets
from django.utils import timezone
from channels.layers import get_channel_layer

from temperature.serializer import TemperatureSerializer

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import AllowAny

from temperature.models import Temperature


class TemperatureViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = TemperatureSerializer

    @action(detail=False, methods=['post'])
    async def store(self, request):
        try:
            serializer = TemperatureSerializer(data=request.data)

            if serializer.is_valid():

                temperature = serializer.validated_data.get('temperature')
                humidity = serializer.validated_data.get('humidity')
                heat_index = serializer.validated_data.get('heat_index')

                if temperature is None or humidity is None:
                    return Response(
                            {
                                "status": 400,
                                "msg": "Ingrese temperatura y/o humedad",
                                "error": "Campos nulos"
                            }, status=status.HTTP_400_BAD_REQUEST
                    )

                current_time = timezone.now()

                await Temperature.objects.acreate(
                    temperature=temperature,
                    humidity=humidity,
                    heat_index=heat_index or 0.0,
                    date=current_time
                )

                channel_layer = get_channel_layer()
                await channel_layer.group_send(
                    "temperature_updates",
                    {
                        "type": "temperature_update",
                        "temperature": temperature,
                        "humidity": humidity,
                        "heat_index": heat_index,
                    }
                )

                return Response({
                    "status": 200,
                    "msg": "Temperatura guardada exitosamente"
                    },
                    status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            traceback.print_exc()
            return Response({"Error respondiendo": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def table(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        readings = Temperature.objects.all()

        if start_date and end_date:
            readings = readings.filter(date__date__gte=start_date, date__date__lte=end_date)
        elif start_date:
            readings = readings.filter(date__date__gte=start_date)
        elif end_date:
            readings = readings.filter(date__date__lte=end_date)

        readings = readings.order_by('-date')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = [
                {
                    'id': r.id,
                    'temperature': r.temperature,
                    'humidity': r.humidity,
                    'heat_index': r.heat_index,
                    'date': r.date.isoformat(),
                }
                for r in readings
            ]
            return Response({'readings': data}, status=status.HTTP_200_OK)

        context = {
            'readings': readings,
            'count': readings.count(),
            'start_date': start_date or '',
            'end_date': end_date or '',
        }
        return render(request, 'temperature_table.html', context)

    @action(detail=False, methods=['get'])
    def show(self, request):
        hour = request.GET.get('hour')

        readings = Temperature.objects.all()

        if hour:
            readings = readings.filter(date__hour=hour)

        readings = readings.order_by('-date')

        latest = readings.first()

        stats = readings.aggregate(
            min_temp=Min('temperature'),
            max_temp=Max('temperature'),
            avg_temp=Avg('temperature'),
            min_hum=Min('humidity'),
            max_hum=Max('humidity'),
            avg_hum=Avg('humidity'),
            min_hi=Min('heat_index'),
            max_hi=Max('heat_index'),
            avg_hi=Avg('heat_index'),
        )

        hours_range = range(24)

        # Prepare chart data for last 50 readings (oldest first)
        chart_qs = readings.order_by('date')[:50]
        chart_labels = [r.date.strftime('%H:%M') for r in chart_qs]
        chart_temps = [r.temperature for r in chart_qs]
        chart_hums = [r.humidity for r in chart_qs]

        context = {
            'readings': readings,
            'count': readings.count(),
            'latest': latest,
            'stats': stats,
            'selected_hour': int(hour) if hour else None,
            'hours_range': hours_range,
            'chart_labels': json.dumps(chart_labels),
            'chart_temps': json.dumps(chart_temps),
            'chart_hums': json.dumps(chart_hums),
        }
        return render(request, 'temperature_show.html', context)
