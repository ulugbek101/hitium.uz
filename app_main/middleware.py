class NoIndexAdminMiddleware:
    """Keeps every admin page, the login page included, out of search engines."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/admin/"):
            response["X-Robots-Tag"] = "noindex, nofollow"
        return response
