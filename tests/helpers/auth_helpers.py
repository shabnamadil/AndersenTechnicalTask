from django.conf import settings

import jwt


def decode_jwt(token):
    key = settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY)
    algorithm = settings.SIMPLE_JWT.get("ALGORITHM", "HS256")
    return jwt.decode(token, key, algorithms=[algorithm])
