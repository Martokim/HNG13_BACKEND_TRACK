# Dynamic Profile Endpoint - Stage 0

A simple RESTful GET endpoint built with Django that returns user profile information and a dynamic cat fact fetched from the Cat Facts API.

## API Endpoint

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/me` | Returns profile data, a dynamic UTC timestamp, and a random cat fact. |

## Setup and Local Run Instructions

These instructions assume you have Python 3.x installed.

### 1. Set up Virtual Environment

```bash
# Create and activate the virtual environment
python -m venv my_venv
source venv/bin/activate  
```


### 2. Install Dependencies 
The required dependencies are listed in requirements.txt
``` bash
pip install -r requirements.txt
```
### 3 Environment Variables (Configuration)
create a file named `.env` in the project root directory and define your profile information.Note: This file is intentionally excluded from the repository via .gitignore 

```code 
# .enc file content
MY_EMAIL ="[Your Personal Email]"
MY_NAME="[Your Full Name]"
MY_STACK="Python/Django"
```

### 4.Run the Server 
``` bash
python manage.py runserver 
```
