from rest_framework import pagination


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    page_size = 100
    page_query_param = 'page'
    max_page_size = 1000