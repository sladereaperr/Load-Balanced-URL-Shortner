from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import models, utils
from .models import URL, get_db
from .config import BASE_URL
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI(title="URL Shortener Service")

# Create database tables on startup
@app.on_event("startup")
async def startup():
    models.create_tables()

# Pydantic model for URL creation requests
class URLCreate(BaseModel):
    url: str

# Pydantic model for URL responses
class URLResponse(BaseModel):
    original_url: str
    short_url: str
    short_url_link: str

@app.post("/shorten/", response_model=URLResponse)
def create_short_url(url_data: URLCreate, db: Session = Depends(get_db)):
    # Check if the URL already exists in the database
    existing_url = db.query(URL).filter(URL.original_url == url_data.url).first()
    
    # If URL already exists, return the existing short URL
    if existing_url:
        return {
            "original_url": existing_url.original_url,
            "short_url": existing_url.short_url,
            "short_url_link": f"{BASE_URL}/{existing_url.short_url}"
        }
    
    # If URL doesn't exist, generate a new short URL
    short_id = utils.generate_short_url()
    
    # Create a new URL entry
    db_url = URL(
        short_url=short_id,
        original_url=url_data.url
    )
    
    # Save to database
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    # Return the shortened URL
    return {
        "original_url": db_url.original_url,
        "short_url": db_url.short_url,
        "short_url_link": f"{BASE_URL}/{db_url.short_url}"
    }

@app.put("/update/{short_url}", response_model=URLResponse)
def update_url(short_url: str, url_data: URLCreate, db: Session = Depends(get_db)):
    # Find the URL entry by short_url
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Update the original URL
    db_url.original_url = url_data.url
    db.commit()
    db.refresh(db_url)
    
    return {
        "original_url": db_url.original_url,
        "short_url": db_url.short_url,
        "short_url_link": f"{BASE_URL}/{db_url.short_url}"
    }

@app.delete("/delete/{short_url}")
def delete_short_url(short_url: str, db: Session = Depends(get_db)):
    # Lookup the URL entry by short URL
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    
    # If URL doesn't exist, raise 404
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Delete the URL entry
    db.delete(db_url)
    db.commit()
    
    # Return a success message
    return {"detail": f"URL with short URL {short_url} has been deleted"}


@app.get("/{short_url}")
def redirect_to_original(short_url: str, db: Session = Depends(get_db)):
    # Lookup the original URL
    db_url = db.query(URL).filter(URL.short_url == short_url).first()
    
    # If URL doesn't exist, raise 404
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Redirect to the original URL
    return RedirectResponse(url=db_url.original_url)


@app.get("/urls/", response_model=list[URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URL).all()
    return [
        {
            "original_url": url.original_url,
            "short_url": url.short_url,
            "short_url_link": f"{BASE_URL}/{url.short_url}"
        } for url in urls
    ]

@app.get("/")
def read_root():
    return {"message": "URL Shortener API. Use /shorten/ to create a short URL"}