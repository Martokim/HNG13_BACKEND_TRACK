# 1. Use an official Python image as the base
FROM python:3.9-slim

# 2. Set the working directory for the application
# We set this to the folder containing manage.py
WORKDIR /app/task_1

# 3. Copy only the necessary files for the build (dependencies)
# Copy requirements.txt first to leverage Docker caching
COPY task_1/requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY task_1/ .

# 6. Run database migrations during the build process
RUN python manage.py migrate

# 7. Expose the default Django port (8000), though Railway usually uses $PORT
EXPOSE 8000

# 8. Define the command to run the application using Gunicorn
# This is the equivalent of the Custom Start Command
CMD ["gunicorn", "string_analyzer.wsgi:application", "--bind", "0.0.0.0:$PORT", "--log-file", "-"]