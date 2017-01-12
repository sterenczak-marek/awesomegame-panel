from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DatatablePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'length'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        self.queryset = queryset
        return super(DatatablePagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'recordsTotal': self.queryset.count(),
            'recordsFiltered': self.queryset.count(),
            'results': data
        })
