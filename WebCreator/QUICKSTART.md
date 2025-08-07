# 🚀 WebCreator Quick Start Guide

Get up and running with WebCreator in minutes!

## Installation

1. **Clone or download the WebCreator directory**
2. **Install dependencies:**
   ```bash
   # On Ubuntu/Debian
   sudo apt install python3-jinja2
   
   # Or install other requirements if needed
   pip install -r requirements.txt
   ```

## Basic Usage

### 1. Simple Website Generation

```python
from src.core.generator import WebCreatorGenerator, WebsiteRequest

# Initialize the generator
generator = WebCreatorGenerator()

# Create a website request
request = WebsiteRequest(
    description="Create a modern portfolio website for a photographer with dark theme and gallery",
    website_type="portfolio",
    theme="dark"
)

# Generate the website
website = generator.generate_website(request)

# Export to files
generator.export_website(website, "my_awesome_website")
```

### 2. Interactive Demo

```bash
python3 src/demo.py
```

Then open your browser to `http://localhost:7860` to use the web interface.

### 3. Run Examples

```bash
python3 examples/example_usage.py
```

This generates multiple example websites showcasing different types and themes.

## Website Types

- **`portfolio`** - Creative portfolios with galleries
- **`business`** - Professional business websites  
- **`landing`** - High-conversion landing pages
- **`blog`** - Content-focused blog layouts
- **`ecommerce`** - Online store designs

## Themes

- **`modern`** - Clean, contemporary design
- **`dark`** - Dark mode with elegant contrast
- **`minimal`** - Minimalist, clean layouts  
- **`corporate`** - Professional business styling
- **`creative`** - Bold, artistic designs

## Quick Examples

### Photographer Portfolio
```python
request = WebsiteRequest(
    description="Elegant portfolio for wedding photographer",
    website_type="portfolio",
    theme="dark",
    features=["image_gallery", "contact_form"]
)
```

### Startup Landing Page
```python
request = WebsiteRequest(
    description="Landing page for AI productivity app with pricing and testimonials",
    website_type="landing", 
    theme="modern",
    content_tone="persuasive"
)
```

### Restaurant Website
```python
request = WebsiteRequest(
    description="Cozy Italian restaurant with menu and reservations",
    website_type="business",
    theme="creative",
    content_tone="warm"
)
```

## Generated Files

Each website includes:
- **`index.html`** - Complete HTML structure
- **`styles.css`** - Responsive CSS styling
- **`script.js`** - Interactive JavaScript
- **`metadata.json`** - Generation metadata

## Features

✅ **AI-Powered Content** - Automatically generates relevant content  
✅ **Responsive Design** - Works on all devices  
✅ **Modern Styling** - Contemporary design patterns  
✅ **Accessibility** - WCAG compliant  
✅ **Performance** - Optimized for speed  
✅ **Export Ready** - Complete project files  

## Next Steps

1. **Customize Generated Sites** - Edit the HTML/CSS to match your exact needs
2. **Deploy Anywhere** - Upload to any web hosting service
3. **Add Dynamic Features** - Integrate with backend services
4. **Experiment with Themes** - Try different styles and layouts

## Need Help?

- Check the full `README.md` for detailed documentation
- Run the test suite: `python3 test_webcreator.py`
- Explore the examples in the `examples/` directory

Happy website building! 🎨✨