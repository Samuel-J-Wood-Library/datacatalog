from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'datacatalog'
urlpatterns = [
    # index showing top items and search bar:
    path('', views.IndexView.as_view(), name='index'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


