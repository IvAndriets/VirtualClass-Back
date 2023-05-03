from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from core.jwt_auth_backend import CustomJWTAuthentication


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    name = 'CustomJWTAuthentication'
    target_class = CustomJWTAuthentication
