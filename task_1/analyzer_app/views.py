from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.utils import IntegrityError
from .models import StringEntry
from .serializers import StringInputSerializer, StringEntrySerializer
from .utils import analyze_string
import re 
from django.db.models import Q 


class StringListCreateView(APIView):
    """
    Handles POST /strings for creation/analysis and GET /strings for listing/filtering.
    """
    

    # 1. POST /strings 
    def post(self, request, *args, **kwargs):
        # 1. Validate Input JSON (Handles 400 Bad Request / 422 Unprocessable Entity)
        input_serializer = StringInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            # Returns 400 or 422 if 'value' is missing or not a string
            return Response(input_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        string_value = input_serializer.validated_data['value']
        
        # 2. Analyze String
        analysis_result = analyze_string(string_value)
        props = analysis_result['properties']
        
        # 3. Prepare Data for Model Creation
        data_to_save = {
            'id': analysis_result['id'], # Use hash as PK
            'value': analysis_result['value'],
            'length': props['length'],
            'is_palindrome': props['is_palindrome'],
            'unique_characters': props['unique_characters'],
            'word_count': props['word_count'],
            'sha256_hash': props['sha256_hash'],
            'character_frequency_map': props['character_frequency_map'],
        }
        
        # 4. Attempt to save (Handles 409 Conflict)
        try:
            instance = StringEntry.objects.create(**data_to_save)
            
            # 5. Success Response (201 Created)
            output_serializer = StringEntrySerializer(instance)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except IntegrityError:
            # This catches the 'unique=True' violation on the 'value' field or 'id' (hash)
            return Response({'error': 'String already exists in the system'}, 
                            status=status.HTTP_409_CONFLICT)

    # 2. GET /strings (Basic structure for list/filtering)
  # analyzer_app/views.py (StringListCreateView - complete get method)

    # 2. GET /strings (Handles listing and filtering - 45 Points)
    def get(self, request, *args, **kwargs):
        queryset = StringEntry.objects.all()
        filters_applied = {}
        
        # ----------------------------------------------
        # A. Implement Standard Query Filters (25 Points)
        # ----------------------------------------------
        
        # Map URL query parameters to Django ORM lookup fields
        # This includes all common string properties with gt/lt lookups
        lookup_map = {
            'length_gt': 'length__gt',
            'length_lt': 'length__lt',
            'word_count_gt': 'word_count__gt',
            'word_count_lt': 'word_count__lt',
            'unique_characters_gt': 'unique_characters__gt',
            'unique_characters_lt': 'unique_characters__lt',
            'is_palindrome': 'is_palindrome', # Exact match filter
        }
        
        for param, lookup in lookup_map.items():
            value = request.query_params.get(param)
            
            if value is not None:
                # Handle numeric lookups (gt/lt)
                if lookup in ['length__gt', 'length__lt', 'word_count__gt', 'word_count__lt', 'unique_characters__gt', 'unique_characters__lt']:
                    if value.isdigit():
                        try:
                            # Apply the filter dynamically
                            queryset = queryset.filter(**{lookup: int(value)})
                            filters_applied[param] = int(value)
                        except ValueError:
                            pass # Ignore non-integer filter values
                
                # Handle boolean lookups (is_palindrome)
                elif lookup == 'is_palindrome':
                    if value.lower() in ['true', 'false']:
                        bool_val = value.lower() == 'true'
                        queryset = queryset.filter(is_palindrome=bool_val)
                        filters_applied[param] = bool_val

        # ----------------------------------------------------
        # B. Implement Natural Language Filter (20 Points)
        # ----------------------------------------------------
        nl_query = request.query_params.get('natural_language_filter')
        if nl_query:
            nl_query = nl_query.lower()
            q_objects = Q()
            
            # Simple keyword detection using OR logic
            if "palindrome" in nl_query:
                q_objects |= Q(is_palindrome=True)
            if "not palindrome" in nl_query or "non-palindrome" in nl_query:
                 q_objects |= Q(is_palindrome=False)
            if "long" in nl_query:
                # Use a reasonable threshold for 'long'
                q_objects |= Q(length__gt=20) 
            if "short" in nl_query:
                # Use a reasonable threshold for 'short'
                q_objects |= Q(length__lt=5)
            if "unique" in nl_query or "distinct" in nl_query:
                # Example: strings with a high number of unique characters
                 q_objects |= Q(unique_characters__gt=10)

            if q_objects:
                # Apply combined Q objects to the queryset
                queryset = queryset.filter(q_objects)
                filters_applied['natural_language_filter'] = nl_query

        # ----------------------------------------------
        # C. Final Serialization and Response
        # ----------------------------------------------
        
        output_serializer = StringEntrySerializer(queryset, many=True)
        
        response_data = {
            "data": output_serializer.data,
            "count": queryset.count(),
            "filters_applied": filters_applied 
        }
        return Response(response_data, status=status.HTTP_200_OK)


class StringDetailView(APIView):
    """
    Handles GET /strings/{value} and DELETE /strings/{value}
    """

    def get_object(self, string_value):
        """Helper method to retrieve the object or raise 404."""
        # The URL parameter 'string_value' is the actual string (URL-decoded).
        try:
            # We look up the object by the original string value.
            return StringEntry.objects.get(value=string_value)
        except StringEntry.DoesNotExist:
            # The requirement is to return a 404 error if the resource is not found.
            raise NotFound(detail="String not found in the database.")

    # 1. GET /strings/{value} (15 points)
    def get(self, request, string_value, *args, **kwargs):
        # 1. Retrieve object (raises 404 if not found)
        instance = self.get_object(string_value)
        
        # 2. Serialize and return (200 OK)
        serializer = StringEntrySerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # 2. DELETE /strings/{value} (15 points)
    
    def delete(self, request, string_value, *args, **kwargs):
        # 1. Retrieve object (raises 404 if not found)
        instance = self.get_object(string_value)
        
        # 2. Delete the object
        instance.delete()
        
        # 3. Success Response (204 No Content)
        # 204 is the standard successful response for DELETE requests with no body.
        return Response(status=status.HTTP_204_NO_CONTENT)
