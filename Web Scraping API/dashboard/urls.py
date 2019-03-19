"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from webscrap.views import image_scraper, image_list, image_downloader, text_scraper, download_csv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('scrape/', image_scraper, name='image_scraper'),
    path('home/', image_list, name='home'),
    path('download/', image_downloader, name='image_downloader'),
    path('text/', text_scraper, name='text_scraper'),
    path('csv_saved/', download_csv, name='download_csv'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)