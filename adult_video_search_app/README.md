# Adult Video Search Application

A comprehensive Flask web application for searching adult videos across multiple platforms including Eporner, RedGifs, and more. This application provides a modern, responsive interface for discovering adult content with advanced filtering and sorting capabilities.

## 🚀 Features

- **Multi-Platform Search**: Search across Eporner, RedGifs, and demo APIs simultaneously
- **Advanced Filtering**: Filter by categories, keywords, and content metadata
- **Multiple Sort Options**: Sort by views, rating, upload date, or title
- **Responsive Design**: Modern Bootstrap-based UI that works on all devices
- **Real-time Results**: Fast API integration with loading indicators
- **Age Verification**: Built-in 18+ content warnings and compliance features
- **API Health Monitoring**: Check the status of connected APIs
- **Rate Limiting**: Respectful API usage with built-in rate limiting
- **Configuration Management**: Flexible environment-based configuration

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Available APIs](#available-apis)
- [Legal Considerations](#legal-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🔧 Requirements

- Python 3.8 or higher
- Internet connection for API access
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 📦 Installation

### 1. Clone or Download the Application

```bash
# If you have the files, navigate to the directory
cd adult_video_search_app
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred settings
nano .env  # or use your preferred editor
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000` by default.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root to customize the application:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development

# API Configuration
PORNHUB_API_KEY=your-api-key-if-available

# Security Settings
AGE_VERIFICATION_REQUIRED=True
MAX_REQUESTS_PER_MINUTE=60
```

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `FLASK_SECRET_KEY` | Random | Secret key for Flask sessions |
| `FLASK_DEBUG` | `True` | Enable debug mode |
| `FLASK_PORT` | `5000` | Port to run the application |
| `AGE_VERIFICATION_REQUIRED` | `True` | Show age verification warning |
| `MAX_REQUESTS_PER_MINUTE` | `60` | Rate limiting for API calls |

## 🎯 Usage

### Basic Search

1. Open your web browser and navigate to `http://localhost:5000`
2. Enter search keywords (default: "footjob wife")
3. Select which platforms to search (Eporner, RedGifs, Demo)
4. Choose sorting preference (Most Views, Highest Rated, Newest, A-Z)
5. Click "Search Videos"

### Advanced Features

- **Multi-Platform Selection**: Choose which APIs to search simultaneously
- **Category Filtering**: Add category filters for more specific results
- **Sorting Options**: Sort results by popularity, rating, or recency
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### Search Tips

- Use specific keywords for better results (e.g., "amateur wife", "footjob fetish")
- Combine multiple platforms for comprehensive results
- Try different categories: "amateur", "milf", "fetish", "homemade"
- Use sorting to find the most popular or newest content

## 📡 API Documentation

### REST API Endpoints

#### POST `/api/search`

Programmatic search endpoint for developers.

**Request Body:**
```json
{
  "query": "footjob wife",
  "category": "amateur",
  "apis": ["eporner", "redgifs"],
  "limit_per_api": 10,
  "sort_by": "views"
}
```

**Response:**
```json
{
  "success": true,
  "query": "footjob wife",
  "total_results": 15,
  "api_stats": {
    "eporner": 8,
    "redgifs": 7
  },
  "videos": [
    {
      "source": "Eporner",
      "title": "Hot Wife Footjob",
      "url": "https://eporner.com/...",
      "thumbnail": "https://...",
      "duration": "5:23",
      "views": 50000,
      "rating": 4.2,
      "keywords": "footjob, wife, amateur"
    }
  ]
}
```

#### GET `/health`

Check API status and application health.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "available_apis": ["eporner", "redgifs", "pornhub_demo"]
}
```

## 🌐 Available APIs

### 1. Eporner API
- **Type**: Official API
- **Rate Limit**: 1 request per second
- **Features**: Search, categories, sorting, metadata
- **Content**: Full-length videos
- **Documentation**: https://www.eporner.com/api/

### 2. RedGifs API
- **Type**: Official API
- **Rate Limit**: 1 request per second
- **Features**: GIF/short video search, tags
- **Content**: Short clips and GIFs
- **Authentication**: Temporary tokens (automatic)

### 3. Demo API
- **Type**: Demonstration/Testing
- **Features**: Placeholder data for testing
- **Content**: Sample metadata (no real videos)
- **Purpose**: Development and demonstration

### Future API Integrations

The application is designed to easily add new APIs:

- **PornHub API**: Official webmaster API (requires approval)
- **xHamster API**: Third-party integrations possible
- **Custom APIs**: Add your own API integrations

## ⚖️ Legal Considerations

### Age Verification
- This application searches 18+ adult content
- Users must be 18 years or older
- Comply with local laws regarding adult content access

### API Terms of Service
- **Eporner**: Review their API terms at eporner.com
- **RedGifs**: Follow RedGifs API guidelines
- **Rate Limiting**: All APIs are accessed respectfully with rate limiting

### Content Responsibility
- The application only provides links to content hosted by third parties
- No content is downloaded or stored locally
- Users are responsible for their content consumption

### Privacy
- No user data is collected or stored
- Search queries are not logged
- All requests are made directly to third-party APIs

## 🔧 Troubleshooting

### Common Issues

#### No Videos Found
- **Solution**: Try broader search terms or different APIs
- **Check**: Internet connection and API availability
- **Tip**: Use categories like "amateur" or "milf" for more results

#### API Errors
- **Solution**: Check the `/health` endpoint for API status
- **Wait**: Some APIs have rate limits - wait and try again
- **Alternative**: Try different API combinations

#### Installation Problems
```bash
# If pip install fails:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# If Python version issues:
python --version  # Should be 3.8+
```

#### Port Already in Use
```bash
# Change port in .env file:
FLASK_PORT=5001

# Or run with custom port:
python app.py --port 5001
```

### Debug Mode

Enable detailed error logging:

```bash
# Set in .env file:
FLASK_DEBUG=True
FLASK_ENV=development
```

### API Rate Limits

If you encounter rate limiting:

1. Wait 60 seconds between searches
2. Reduce the number of results per API
3. Use fewer APIs simultaneously
4. Check API status at `/health`

## 🛡️ Security Features

- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Prevents API abuse
- **HTTPS Ready**: SSL/TLS support for production deployment
- **Session Security**: Secure session management
- **Content Warnings**: Clear 18+ warnings and age verification

## 🚀 Production Deployment

### Using Gunicorn (Recommended)

```bash
# Install gunicorn (included in requirements.txt)
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Configuration

```bash
# Set production environment
export FLASK_ENV=production
export FLASK_SECRET_KEY=your-secure-production-key
export SESSION_COOKIE_SECURE=True
```

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Contributing

### Adding New APIs

1. Create a new API class in `app.py`:

```python
class YourAPIClass:
    @staticmethod
    def fetch_videos(query, limit=10):
        # Your implementation
        return videos
```

2. Add the API to the `VideoSearcher.search_all_apis()` method
3. Update the HTML template to include the new API option
4. Test thoroughly and submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Set development environment
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run with auto-reload
python app.py
```

## 📄 License

This project is provided for educational and personal use. Please ensure compliance with:

- Local laws regarding adult content
- API terms of service for all integrated platforms
- Age verification requirements in your jurisdiction

## ⚠️ Disclaimer

- This application is for adults 18+ only
- Content is provided by third-party platforms
- No content is hosted or stored by this application
- Users are responsible for their own compliance with local laws
- The developers assume no responsibility for content accessed through this application

## 📞 Support

For technical issues:

1. Check this README for troubleshooting steps
2. Verify your configuration in `.env`
3. Check API status at `/health`
4. Review application logs for error details

## 🔄 Version History

- **v1.0.0**: Initial release with Eporner and RedGifs integration
- Multi-platform search functionality
- Responsive web interface
- Configuration management system
- API health monitoring

---

**Remember**: This application is intended for legal adult use only. Always comply with local laws and platform terms of service.