from django.urls import path

from places.views import PlaceView

urlpatterns = [
    path('/places', PlaceView.as_view(), name='places')
]
