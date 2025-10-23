from django.db import models

class StringEntry(models.Model): 
    # The SHA-256 hash is specified for unique ID and must be the PK for uniqueness.
    # It must be 64 characters long (256 bits * 2 hex chars/bit = 64)
    id = models.CharField(max_length=64, primary_key=True) 
    
    # The original string value
    value = models.TextField(unique=True)
    
    # --- The 6 Computed Properties ---
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True) # Required in properties object
    
    # Character Frequency Map (Use JSONField for dictionary storage)
    character_frequency_map = models.JSONField()
    
    # Required timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value