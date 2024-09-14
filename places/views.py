from django.views.generic import TemplateView

from places.token import make_api_request


class PlaceView(TemplateView):
    def get_context_data(self, **kwargs):
        query = """{
                    product (where: {
                                _and: [
                                    {type:{_eq:attraction}},
                                    {productTags:{tag:{_eq:"hiking_walking_trekking"}}},
                                    {productTargetGroups:{targetGroupId:{_eq:b2c}}}
                                ]
                                }) {
                        type
                        postalAddresses {
                            location
                            postalCode
                            streetName
                            city
                        }
                        productInformations {
                            description
                            name
                            url
                        }
                        productTags {
                            tag
                        }
                    }
                }"""
        api_response = make_api_request(query=query)
        print(api_response)

    template_name = 'places/places.html'
