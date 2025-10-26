# string_analyzer/urls.py (Reverting to the explicit path() structure)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Explicitly map both slashed and non-slashed prefixes
    path('strings', include('analyzer_app.urls')),
    path('strings/', include('analyzer_app.urls')), 
]