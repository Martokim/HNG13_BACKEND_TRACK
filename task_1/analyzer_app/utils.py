import hashlib
from collections import Counter
import re
from datetime import datetime

def analyze_string(value: str) -> dict:
    """
    Computes all required properties for a given string value.
    """
    
    # 1. SHA-256 Hash (REQUIRED for unique ID and persistence)
    # Must be the lowercase hex digest of the UTF-8 bytes.
    sha256_hash = hashlib.sha256(value.encode('utf-8')).hexdigest()

    # 2. Length (counts all characters, including spaces and punctuation)
    length = len(value)

    # 3. Is Palindrome (case-insensitive, but does NOT strip spaces/punctuation)
    value_lower = value.lower()
    is_palindrome = value_lower == value_lower[::-1]

    # 4. Character Frequency Map (counts ALL characters, including spaces)
    character_frequency_map = dict(Counter(value)) # dict() is required for JSONField

    # 5. Unique Characters (count of distinct characters, includes spaces/punc)
    unique_characters = len(set(value))

    # 6. Word Count (uses standard split, collapsing multiple spaces)
    # The requirement specifies: "number of words using value.split() — multiple spaces collapsed; leading/trailing spaces ignored"
    word_count = len(value.split())
    
    # Final data structure (matches the nested "properties" requirement)
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