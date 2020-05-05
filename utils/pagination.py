from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 10

    page_size_query_param = 'pagesize'

    page_query_param = 'pagenum'

    def get_paginated_response(self, data):
        from collections import OrderedDict
        count =  len(data)
        return  {'count': count, 'result': data}
