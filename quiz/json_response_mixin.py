'''
This module contains a JSON Response Mixin.
'''

from django.http import JsonResponse

class JSONResponseMixin(object):
    '''
    A mixin that can be used to render a JSON response.
    '''
    def render_to_json_response(self, context, **response_kwargs):
        '''
        Returns a JSON response, transforming 'context' to make the payload.
        '''
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        '''
        Returns an object that will be serialized as JSON by json.dumps().
        '''
        return context
