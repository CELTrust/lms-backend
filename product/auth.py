from django.http import HttpRequest
from ninja.security import APIKeyHeader

from .models import School


class SchoolAuth(APIKeyHeader):
    param_name = 'X-School-Code'

    def authenticate(self, request: HttpRequest, key: str):
        try:
            return School.objects.get(unique_code=key)
        except:
            pass

school_auth = SchoolAuth()
