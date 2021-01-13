import logging
from collections import OrderedDict

from django.conf import settings
from drf_yasg import openapi
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

from drf_yasg.inspectors import PaginatorInspector


class PageNumberPaginatorInspectorClass(PaginatorInspector):
    def get_paginated_response(self, paginator, response_schema):
        paged_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('page_size', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('next', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('prev', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('results', response_schema),
            )),
            required=['results']
        )

        return paged_schema


class StandardResultSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


def paginated_queryset(
        queryset, request, pagination_class=PageNumberPagination()
):
    """
        Return a paginated result for a queryset
    """
    paginator = pagination_class
    paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
    result_page = paginator.paginate_queryset(queryset, request)
    return tuple([paginator, result_page])


def team_paginated_queryset(
        queryset, request, pagination_class=PageNumberPagination()
):
    """
        Return a paginated result for a queryset
    """
    paginator = pagination_class
    paginator.page_size = settings.REST_FRAMEWORK["TEAM_PAGE_SIZE"]
    result_page = paginator.paginate_queryset(queryset, request)
    return tuple([paginator, result_page])


def get_model_object(model_name):
    def get_model_by_pk(pk):
        try:
            model_object = model_name.objects.get(pk=pk)
            return model_object
        except model_name.DoesNotExist:
            raise NotFound(
                "{} {} does not exist".format(model_name.__name__, pk)
            )

    get_model_by_pk.__name__ = "get_{}_object".format(
        model_name.__name__.lower()
    )
    return get_model_by_pk
