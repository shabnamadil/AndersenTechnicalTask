from rest_framework.response import Response

from utils.auth.cookies import set_refresh_cookie


class TokenResponseMixin:
    def build_token_response(self, access_token: str, refresh_token: str) -> Response:
        response = Response({"access": access_token}, status=200)
        if refresh_token:
            set_refresh_cookie(response, refresh_token)
        return response
