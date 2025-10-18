# Dynamic Profile Endpoint - Stage 0

A simple RESTful GET endpoint built with Django that returns user profile information and a dynamic cat fact fetched from the Cat Facts API.

## API Endpoint

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/me` | Returns profile data, a dynamic UTC timestamp, and a random cat fact. |

## 🚀 Setup and Local Run Instructions

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
- Dependencies:

Django: Web framework.

requests: Library for making external API calls.

python-dotenv: Library for loading configuration from the .env file
