from rest_framework import serializers
from .models import StringEntry

class StringInputSerializer(serializers.Serializer):
    """
    Serializer used only for validating the input JSON {"value": "string"}
    """
    value = serializers.CharField(required=True, max_length=10000) 
    
    def validate_value(self, value):
        # 422 Unprocessable Entity for invalid data type (handled by CharField)
        if not value:
            raise serializers.ValidationError("The 'value' field cannot be empty.")
        return value

class StringEntrySerializer(serializers.ModelSerializer):
    """
    Serializer used for outputting the saved data (201, 200 responses)
    """
    # Define a properties field that will contain the full computed properties object
    properties = serializers.SerializerMethodField()

    class Meta:
        model = StringEntry
        # Fields to expose in the response JSON
        fields = ['id', 'value', 'properties', 'created_at']
        # Read-only fields (set automatically or by the analysis)
        read_only_fields = ('id', 'created_at', 'length', 'is_palindrome', 
                            'unique_characters', 'word_count', 
                            'sha256_hash', 'character_frequency_map')
    
    def get_properties(self, obj):
        """
        Constructs the nested 'properties' object required by the schema.
        """
        return {
            "length": obj.length,
            "is_palindrome": obj.is_palindrome,
            "unique_characters": obj.unique_characters,
            "word_count": obj.word_count,
            "sha256_hash": obj.sha256_hash,
            "character_frequency_map": obj.character_frequency_map,
        }