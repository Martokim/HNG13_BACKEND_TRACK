from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Map all /strings/* requests to the analyzer_app
    path('strings', include('analyzer_app.urls')),
]
