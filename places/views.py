from django.views.generic import TemplateView

from places.token import make_api_request


class PlaceView(TemplateView):
    def get_context_data(self, **kwargs):
        query = """{
            city {
                city
            }
        }"""
        api_response = make_api_request(query=query)
        print(api_response)

    template_name = 'places/places.html'
