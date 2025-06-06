from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view

class ClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        return FitnessClass.objects.filter(datetime__gte=timezone.now()).order_by('datetime')

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        fitness_class = serializer.validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()
        serializer.save()

class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        return Booking.objects.filter(client_email=email)
@api_view(['POST'])        
def create_fitness_class(request):
    serializer = FitnessClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
