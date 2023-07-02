from django.contrib import admin
from django.urls import path, include #we import 'include' to include base.urls 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')), #It just directs all the routings of our core project to base.urls
    path('api/',include('base.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)