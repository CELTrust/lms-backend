"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from consumer.exceptions import ErrFileNotUploaded

api = NinjaAPI(title="CEL LMS API")

@api.exception_handler(ErrFileNotUploaded)
def file_not_uploaded(request, exc):
    return api.create_response(request=request, data={'error': 'File Not Uploaded Yet. Please Upload file first'},
                               status=422)

api.add_router("p/", "product.api.router", tags=["Product"])
api.add_router("c/", "consumer.api.router")

admin.site.site_header = "CEL. Administration"
admin.site.site_title = "CEL Administration"
admin.site.index_title = "CEL Administration"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls)
]
