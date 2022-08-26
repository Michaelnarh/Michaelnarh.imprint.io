"""imprint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from myapp.views import index
from myapp.views import remove_dir
from myapp.views import download_file
from myapp.views import guides


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home/', admin.site.urls),
    path('', index, name='home'),
    path('download/', download_file, name='download'),
    path('remove/', remove_dir, name='remove'),
    path('guides/', guides, name='guides'),
    # url(r'home/', index, namehome'),
]
