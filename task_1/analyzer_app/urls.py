from django.urls import path
from .views import StringListCreateView, StringDetailView

urlpatterns = [
    # POST /strings and GET /strings (list)
    path('', StringListCreateView.as_view(), name='string-list-create'), 
    
    # GET /strings/{value} and DELETE /strings/{value}
    # This uses a path converter that requires the path parameter to be a string
    path('<str:string_value>/', StringDetailView.as_view(), name='string-detail'), 
]