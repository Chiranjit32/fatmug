"""
URL configuration for fatmug project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from . import views

urlpatterns = [
    path('', include('superuser.urls')),
    
    path('admin/', admin.site.urls),

    path('message-store', csrf_exempt(views.messageStore), name='messageStore'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),

    path('api/', include('api.urls')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]


handler404 = 'fatmug.views.custom_page_not_found_view'
handler500 = 'fatmug.views.custom_error_view'
handler403 = 'fatmug.views.custom_permission_denied_view'
handler400 = 'fatmug.views.custom_bad_request_view'
