from flask import Flask, request, jsonify, redirect, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from models import URL, init_db
from utils import generate_short_code, is_valid_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Initialize database
db_session = init_db(os.getenv('DATABASE_URL', 'sqlite:///urls.db'))
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Create a shortened URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    original_url = data['url']
    custom_code = data.get('custom_code', '').strip()
    
    # Validate URL
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Check if custom code is provided
    if custom_code:
        # Validate custom code (alphanumeric only, 3-10 chars)
        if not custom_code.isalnum() or len(custom_code) < 3 or len(custom_code) > 10:
            return jsonify({'error': 'Custom code must be 3-10 alphanumeric characters'}), 400
        
        # Check if custom code already exists
        existing = db_session.query(URL).filter_by(short_code=custom_code).first()
        if existing:
            return jsonify({'error': 'Custom code already taken'}), 409
        
        short_code = custom_code
    else:
        # Check if URL already exists
        existing_url = db_session.query(URL).filter_by(original_url=original_url).first()
        if existing_url:
            return jsonify({
                'short_url': f"{BASE_URL}/{existing_url.short_code}",
                'short_code': existing_url.short_code,
                'original_url': existing_url.original_url,
                'created_at': existing_url.created_at.isoformat(),
                'clicks': existing_url.clicks
            }), 200
        
        # Generate unique short code
        short_code = generate_short_code()
        while db_session.query(URL).filter_by(short_code=short_code).first():
            short_code = generate_short_code()
    
    # Create new URL entry
    new_url = URL(original_url=original_url, short_code=short_code)
    db_session.add(new_url)
    db_session.commit()
    
    return jsonify({
        'short_url': f"{BASE_URL}/{short_code}",
        'short_code': short_code,
        'original_url': original_url,
        'created_at': new_url.created_at.isoformat(),
        'clicks': 0
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to the original URL"""
    url_entry = db_session.query(URL).filter_by(short_code=short_code).first()
    
    if not url_entry:
        return render_template('404.html'), 404
    
    # Increment click count
    url_entry.clicks += 1
    db_session.commit()
    
    return redirect(url_entry.original_url)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a shortened URL"""
    url_entry = db_session.query(URL).filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'Short URL not found'}), 404
    
    return jsonify(url_entry.to_dict()), 200

@app.route('/api/recent', methods=['GET'])
def get_recent_urls():
    """Get recently created URLs"""
    limit = request.args.get('limit', 10, type=int)
    recent_urls = db_session.query(URL).order_by(URL.created_at.desc()).limit(limit).all()
    
    return jsonify([url.to_dict() for url in recent_urls]), 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'inShortUrl'}), 200

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
