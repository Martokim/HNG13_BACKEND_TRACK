from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.utils import IntegrityError
from .models import StringEntry
from .serializers import StringInputSerializer, StringEntrySerializer
from .utils import analyze_string

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
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def get(self, request, *args, **kwargs):
        # This will be updated later for filtering (Day 2 plan)
        queryset = StringEntry.objects.all()
        
        # Basic response format for listing (needed to verify structure)
        output_serializer = StringEntrySerializer(queryset, many=True)
        
        response_data = {
            "data": output_serializer.data,
            "count": queryset.count(),
            "filters_applied": {}
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
