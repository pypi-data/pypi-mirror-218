from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        pages = self.get_pages_number(count)

        return Response({
            'count': count,
            'pages': pages,
            'results': data,
        })

    def get_pages_number(self, count):
        rest = count % self.page_size
        quotient = count // self.page_size

        return quotient if not rest else quotient + 1
