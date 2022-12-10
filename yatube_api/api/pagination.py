from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        if self.count < 3:
            return Response(data)
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
