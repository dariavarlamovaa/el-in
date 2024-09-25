from django.urls import path

from places.views import PlaceView, PlaceFilter

urlpatterns = [
    path('places/', PlaceView.as_view(), name='places'),
    path('filtered-places/', PlaceFilter.as_view(), name='filter-places')
]
