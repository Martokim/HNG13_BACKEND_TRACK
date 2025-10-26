from django.contrib import admin
# CRITICAL: Import re_path along with path and include
from django.urls import path, re_path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # It aggressively matches 'strings' with zero or one trailing slash, 
    # ensuring the POST request finds the route.
    re_path(r'^strings/?$', include('analyzer_app.urls')), 
]