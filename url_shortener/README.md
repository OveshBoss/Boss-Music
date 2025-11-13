# 🔗 inShortUrl - URL Shortener

A modern, fast, and beautiful URL shortener built with Python Flask and vanilla JavaScript.

## Features

- ⚡ **Lightning Fast** - Shorten URLs in milliseconds
- 🎯 **Custom Short Codes** - Create memorable branded links
- 📊 **Click Tracking** - Monitor link performance with analytics
- 🎨 **Beautiful UI** - Modern, responsive design
- 🔒 **URL Validation** - Ensures only valid URLs are shortened
- 📱 **Mobile Friendly** - Works perfectly on all devices
- 🔄 **Recent URLs** - View recently created short links
- 📋 **One-Click Copy** - Easy clipboard integration

## Tech Stack

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database for storing URLs
- **Flask-CORS** - Cross-Origin Resource Sharing support

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - No frameworks, pure JS
- **Responsive Design** - Mobile-first approach

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd url_shortener
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables (optional):**
   Edit `.env` file to customize settings:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///urls.db
   BASE_URL=http://localhost:5000
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## API Endpoints

### 1. Shorten URL
**POST** `/api/shorten`

Request body:
```json
{
  "url": "https://example.com/very/long/url",
  "custom_code": "mycode" // optional
}
```

Response:
```json
{
  "short_url": "http://localhost:5000/abc123",
  "short_code": "abc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2024-01-01T12:00:00",
  "clicks": 0
}
```

### 2. Redirect to Original URL
**GET** `/<short_code>`

Redirects to the original URL and increments click counter.

### 3. Get URL Statistics
**GET** `/api/stats/<short_code>`

Response:
```json
{
  "id": 1,
  "original_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "created_at": "2024-01-01T12:00:00",
  "clicks": 42
}
```

### 4. Get Recent URLs
**GET** `/api/recent?limit=10`

Returns list of recently created URLs.

### 5. Health Check
**GET** `/health`

Returns service health status.

## Usage Examples

### Using the Web Interface
1. Open the application in your browser
2. Enter a long URL in the input field
3. (Optional) Enter a custom short code
4. Click "Shorten URL"
5. Copy and share your shortened URL!

### Using cURL

**Shorten a URL:**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long/url"}'
```

**With custom code:**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/long/url", "custom_code": "mylink"}'
```

**Get statistics:**
```bash
curl http://localhost:5000/api/stats/abc123
```

## Project Structure

```
url_shortener/
├── app.py              # Main Flask application
├── models.py           # Database models
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── urls.db            # SQLite database (created on first run)
├── static/
│   ├── style.css      # Stylesheet
│   └── script.js      # Frontend JavaScript
└── templates/
    ├── index.html     # Main page
    └── 404.html       # Error page
```

## Features in Detail

### URL Shortening Algorithm
- Uses Base62 encoding (a-z, A-Z, 0-9)
- Generates 6-character random codes
- Collision detection and retry mechanism
- Support for custom short codes (3-10 alphanumeric characters)

### Database Schema
```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY,
    original_url VARCHAR(2048) NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0
);
```

### Security Features
- URL validation before shortening
- SQL injection prevention via ORM
- CORS configuration for API security
- Input sanitization

## Deployment

### Production Considerations
1. Change `SECRET_KEY` in `.env` to a secure random string
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set `FLASK_ENV=production`
4. Consider using PostgreSQL instead of SQLite for better performance
5. Add rate limiting to prevent abuse
6. Implement authentication for admin features
7. Set up proper logging and monitoring

### Example with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Future Enhancements

- [ ] User authentication and accounts
- [ ] QR code generation for short URLs
- [ ] Advanced analytics (geographic data, referrers)
- [ ] Link expiration dates
- [ ] Bulk URL shortening
- [ ] API rate limiting
- [ ] Custom domains
- [ ] Link preview before redirect
- [ ] Password-protected links

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

---

Made with ❤️ by inShortUrl Team
