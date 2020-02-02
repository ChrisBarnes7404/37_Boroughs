from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from Boroughs.views import *

urlpatterns = [
    path('', Index, name='index'),
    path('About/', About, name='about'),
    path('image_upload', hotel_image_view, name='image_upload'),
    path('success', success, name='success'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
