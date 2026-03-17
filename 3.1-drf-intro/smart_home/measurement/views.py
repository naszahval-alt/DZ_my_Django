from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer

class SensorListView(generics.ListCreateAPIView):
    """Получить список датчиков (Read) и создать новый датчик (Create)"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

class SensorDetailView(generics.RetrieveUpdateAPIView):
    """Получить информацию по конкретному датчику (Read) и изменить датчик (Update)"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class MeasurementCreateView(generics.CreateAPIView):
    """Добавить измерение (Create)"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
