from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('trips/', TripsList.as_view(), name='trips'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('trip/<int:trip_id>/', ShowTrip.as_view(), name='show_trip'),
    path('add/', AddTrip.as_view(), name='add_trip'),
    path('profile/<int:profile_id>/', ShowProfile.as_view(), name='show_profile'),
    path('profileinfo/', AddInfo.as_view(), name='red_info'),
]