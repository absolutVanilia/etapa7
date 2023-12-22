from rest_framework import pagination, response
class PostsResultsSetPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return response.Response({
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'total_count': self.page.paginator.count,
            'next_page_url': self.get_next_link(),
            'previous_page_url': self.get_previous_link(),
            'results': data
    })  

    

class LikesResultsSetPagination(PostsResultsSetPagination):
    page_size = 20
