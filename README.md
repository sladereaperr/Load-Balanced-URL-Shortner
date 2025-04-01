# URL Shortener

A containerized URL shortener service built with FastAPI and PostgreSQL.

## Features

- Shorten long URLs to easy-to-share short links
- Persistent storage with PostgreSQL
- Containerized with Docker
- Health check endpoint
- Ready for Kubernetes deployment

## Local Development

### Prerequisites

- Docker and Docker Compose

### Running Locally

1. Clone this repository
   ```bash
   git clone https://github.com/your-username/url-shortener.git
   cd url-shortener
   ```

### Start the application using Docker Compose:

- docker-compose up

The service will be available at http://localhost:8000.

## API Endpoints

### Shorten URL

URL: /shorten/

Method: POST

Response:

{
"original_url": "https://long-url-to-shorten.com/path",
"short_url": "AbCdEf",
"short_url_link": "http://localhost:8000/AbCdEf"
}

### Access Short URL

URL: /{short_url}

Method: GET

Response: Redirects to the original URL.

### Get All Shortened URLs

URL: /urls/

Method: GET

Response: Returns a list of all shortened URLs.

### Delete Short URL

URL: /delete/{short_url}

Method: DELETE

Response: Deletes the shortened URL.
{
"message": "URL with short URL AbCdEf has been deleted successfully"
}

### Update Short URL

URL: /update/{short_url}

Method: PUT

Response:
{
"original_url": "https://new-url.com/path",
"short_url": "AbCdEf",
"short_url_link": "http://localhost:8000/AbCdEf"
}
