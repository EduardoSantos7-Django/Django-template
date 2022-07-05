from django.http import HttpRequest
from rest_framework.serializers import Serializer


def serialize_query_params(request: HttpRequest, serializer_class: Serializer) -> dict:
    """Retrieve query parameter and serializer them to dict."""
    query_params = request.query_params
    query_serializer = serializer_class(data=query_params)
    query_serializer.is_valid(raise_exception=True)

    return query_serializer.data
