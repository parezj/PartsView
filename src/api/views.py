from django.shortcuts import render
from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, api_view
from rest_framework import authentication, permissions, status
from ajax.views import query
from django.http import JsonResponse
import json
import urllib
from urllib.parse import unquote, quote
from drf_yasg import openapi
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework_api_key.permissions import HasAPIKey

class NameValue:   
    def __init__(self, name, value):
        self.name = name
        self.value = value

class SearchView(APIView):
    """
    View to return SearchResult OctoPart object.

    * Requires API key authentication.
    """
    #authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = []
    permission_classes = [HasAPIKey]
 
    param_q = openapi.Parameter('q', openapi.IN_QUERY, required=False, description="search word(s)", type=openapi.TYPE_STRING)
    resp_200 = openapi.Response(description='Successfully retrieved data stored at **success** root key.')
    resp_201 = openapi.Response(description='Successfully retrieved data - cached mode.')
    resp_404 = openapi.Response(description='Search query parameter *q* is missing or empty.')
    resp_500 = openapi.Response(description='Server exception specified by **error** root key.')
    resp_501 = openapi.Response(description='Offline mode. Server is in maintenance mode.')

    # 'method' can be used to customize a single HTTP method of a view
    @swagger_auto_schema(responses={200: resp_200, 201: resp_201, 404: resp_404, 500: resp_500, 501: resp_501}) # manual_parameters=[param_q]
    def get(self, request, q):
        """
        If there is no error, object **'success'** is returend with value of **SearchResult** object specified by *OctoPart API* (https://octopart.com/api/docs/v3/overview).
        If error happens, object **'error'** is returned, with string description value.
        """

        if q and len(q) > 0:
            #q2 = unquote(q)
            ret = query(q)
            try:   
                if ret.status_code == 200 or ret.status_code == 201:
                    with open(settings.CACHE_QUERY_PATH + q + '.json', 'r') as f:
                        search_response = json.load(f)
                        return Response({'success': search_response})
                else:
                    return Response({'error1': ret["error"]})
            except Exception as e:
                return Response({'error2': str(e)})
        else:
            return Response({'error': 'q param missing'})