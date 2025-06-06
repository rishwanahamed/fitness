from django.urls import path
from .views import ClassListView, BookingCreateView, BookingListView
from . import views


urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('book/', BookingCreateView.as_view(), name='book-class'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('fitness-classes/create/', views.create_fitness_class, name='create_fitness_class'),
]
