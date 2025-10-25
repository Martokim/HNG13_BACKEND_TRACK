# analyzer_app/utils.py (FINAL FIX)

import hashlib
from collections import Counter
import re
from datetime import datetime

def analyze_string(value: str) -> dict:
    """
    Computes all required properties for a given string value.
    """
    
    # 1. SHA-256 Hash
    sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()

    # 2. Length (counts all characters, including spaces and punctuation)
    length = len(value)

    
    # a. Remove non-alphanumeric characters and convert to lowercase
    cleaned_string = re.sub(r'[^a-zA-Z0-9]', '', value).lower()
    
    # b. Check if the cleaned string equals its reverse
    is_palindrome = cleaned_string == cleaned_string[::-1]

    # 4. Character Frequency Map (counts ALL characters, including spaces)
    character_frequency_map = dict(Counter(value)) # dict() is required for JSONField

    # 5. Unique Characters (count of distinct characters, includes spaces/punc)
    unique_characters = len(set(value))

    # 6. Word Count (uses standard split, collapsing multiple spaces)
    word_count = len(value.split())
    
    # Final data structure
    properties = {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": character_frequency_map,
    }

    # Return the hash (for the primary key) and the properties
    return {
        "id": sha256_hash,
        "value": value,
        "properties": properties,
    }