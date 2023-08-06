from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 8

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        pages = self.get_pages_number(count)

        return Response({
            'count': count,
            'pages': pages,
            'results': data,
        })

    def get_pages_number(self, count):
        page_size = self.get_page_size(self.request)
        rest = count % page_size
        quotient = count // page_size

        return quotient if not rest else quotient + 1
