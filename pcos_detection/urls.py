"""
URL configuration for pcos_detection project.

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
# get the admin panel and URL tools
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# this is where we tell Django what URLs to use
urlpatterns = [
    # the admin panel URL
    path('admin/', admin.site.urls),
    # all our PCOS app URLs
    path('pcos/', include('pcos.urls')),
    # if someone goes to the root URL, send them to the PCOS app
    path('', RedirectView.as_view(url='pcos/', permanent=True)),
]
