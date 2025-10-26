# analyzer_app/urls.py (CRITICAL: Change order of paths)
from django.urls import path
from .views import StringListCreateView, StringDetailView

urlpatterns = [
    # 1. DETAIL VIEW FIRST: This is more specific and must be checked first
    # This handles /strings/{value}
    path('<str:string_value>', StringDetailView.as_view(), name='string-detail'), 
    
    # 2. LIST VIEW SECOND: This handles the base path /strings or /strings/
    path('', StringListCreateView.as_view(), name='string-list-create'), 
]