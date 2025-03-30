# URL Shortener

A containerized URL shortener service built with Flask and MongoDB.

## Features

- Shorten long URLs to easy-to-share short links
- Persistent storage with MongoDB
- Containerized with Docker
- Health check endpoint
- Ready for Kubernetes deployment

## Local Development

### Prerequisites

- Docker and Docker Compose

### Running Locally

1. Clone this repository
2. Start the application:
   ```bash
   docker-compose up
   ```
3. The service will be available at http://localhost:8080

## API Endpoints

### Shorten URL

- **URL**: `/shorten`
- **Method**: `POST`
- **Body**: `{"url": "https://long-url-to-shorten.com/path"}`
- **Response**:
  ```json
  {
    "original_url": "https://long-url-to-shorten.com/path",
    "short_url": "http://localhost:8080/AbCdEf",
    "short_code": "AbCdEf"
  }
  ```

### Access Short URL

- **URL**: `/{short_code}`
- **Method**: `GET`
- **Response**: Redirects to the original URL

### Health Check

- **URL**: `/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "healthy",
    "message": "MongoDB connection successful"
  }
  ```
