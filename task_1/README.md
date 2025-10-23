# Task_1:String Analyzer API 
This is the submission for HNG Task 1 on the Backend Track, featuring a Django REST Framework (DRF) application. The application exposes a single API endpoint that analyzes a string provided by the user.
## Request Body 
```JSON
{
    "data":"A sample string to be analyzed"
}
```
## Sample Response (JSON)
``` JSON
{
    "string": "A sample string to be analyzed.",
    "length": 34,
    "word_count": 6,
    "vowel_count": 10,
    "is_palindrome": false,
    "modified_string": "A SAMPLE STRING TO BE ANALYZED."
}
```