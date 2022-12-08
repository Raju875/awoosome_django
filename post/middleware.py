from django.contrib.sessions.backends import cache

class PostMiddleware:
    # initialize once when start the server
    def __init__(self, get_response):
        self.get_response = get_response
        self.num_requests = 0
        self.num_exceptions = 0
    
     # call every request to the server
    def __call__(self, request):

        self.num_requests += 1
        print(f"Request counts: {self.num_requests}")

        response = self.get_response(request)

        return response

    # call just before the view will call
    def process_view(self, request, view_func, view_args, view_kwargs):
        print('post_middleware_process_view', view_kwargs)
    
    # call when arise any exception
    def process_exception(self, request, exception):
        self.num_exceptions += 1
        print(f"Exceptions counts: {self.num_exceptions}")
