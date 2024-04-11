from anpr.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", index, name="index"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)