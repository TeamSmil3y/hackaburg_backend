from django.http import HttpRequest, HttpResponse

def http_get_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method != "GET":
            return
        return func(request=request, *args, **kwargs)
    return wrapper


def http_post_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return
        return func(request=request, *args, **kwargs)
    return wrapper


def http_post_required_params(params: list):
    def inner(func):
        def wrapper(request):
            for param in params:
                if param not in request.POST.keys():
                    return
            return func(request)
        return wrapper
    return inner