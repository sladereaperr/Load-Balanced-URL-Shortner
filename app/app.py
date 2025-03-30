from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
import string
import random
import os
import time

app = Flask(__name__)

# MongoDB connection settings
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('MONGO_DB', 'UrlShortener')
COLLECTION_NAME = 'urls'

# Connect to MongoDB
def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

# Helper function to generate short URL code
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    long_url = data['url']
    
    # Check if URL already exists in database
    db = get_db()
    existing_url = db[COLLECTION_NAME].find_one({'long_url': long_url})
    
    if existing_url:
        short_code = existing_url['short_code']
    else:
        # Generate a unique short code
        short_code = generate_short_code()
        while db[COLLECTION_NAME].find_one({'short_code': short_code}):
            short_code = generate_short_code()
        
        # Store in MongoDB
        db[COLLECTION_NAME].insert_one({
            'long_url': long_url,
            'short_code': short_code,
            'created_at': time.time()
        })
    
    # Construct the full shortened URL
    base_url = request.host_url.rstrip('/')
    short_url = f"{base_url}/{short_code}"
    
    return jsonify({
        'original_url': long_url,
        'short_url': short_url,
        'short_code': short_code
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    # Retrieve the original URL from MongoDB
    db = get_db()
    url_mapping = db[COLLECTION_NAME].find_one({'short_code': short_code})
    
    if not url_mapping:
        return jsonify({'error': 'URL not found'}), 404
    
    # Increment access count (optional)
    db[COLLECTION_NAME].update_one(
        {'short_code': short_code},
        {'$inc': {'access_count': 1}}
    )
    
    return redirect(url_mapping['long_url'])

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check if MongoDB is accessible
        db = get_db()
        db.command('ping')
        return jsonify({'status': 'healthy', 'message': 'MongoDB connection successful'})
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'error': f'MongoDB connection failed: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>URL Shortener API</h1>
    <p>POST to /shorten with {"url": "your-long-url"} to create a short URL</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)