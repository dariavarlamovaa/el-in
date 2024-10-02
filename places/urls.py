from django.urls import path

from places.views import PlaceView, PlaceFilter, HikingPlaceView, Map

urlpatterns = [
    path('', PlaceView.as_view(), name='places'),
    path('filtered-places/', PlaceFilter.as_view(), name='filter-places'),
    path('place/<pk>', HikingPlaceView.as_view(), name='place'),
    path('map/', Map.as_view(), name='map')
]
