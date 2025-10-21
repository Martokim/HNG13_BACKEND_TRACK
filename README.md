# HNG13 Backend Track - Stage 0 API

This is the Stage 0 API for the HNG 13 Backend Track.
## Live Endpoint
The successfully deployed API endpoint is available on Render:

`https://hng13-backend-track.onrender.com/me`
## Sample Response Format:

``` json
{
  "status": "success",
  "user": {
    "email": "your-email@example.com",
    "name": "Your Full Name",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-15T12:34:56.789Z",
  "fact": "Cats sleep 70% of their lives."
}
```

## Features
This API endpoint performs the following actions:
1.  Returns user profile details (Name, Email, Stack) from environment variables.
2.  Provides the current timestamp in ISO 8601 format.
3.  Fetches a random cat fact from the `catfact.ninja` external API.