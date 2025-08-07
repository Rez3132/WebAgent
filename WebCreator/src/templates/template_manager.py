"""
WebCreator Template Manager
Manages website templates and HTML generation.
"""

import logging
from typing import Dict, List, Optional, Any
from jinja2 import Template, Environment, DictLoader

logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages website templates and HTML generation."""
    
    def __init__(self):
        """Initialize the template manager."""
        self.templates = self._load_templates()
        self.jinja_env = Environment(loader=DictLoader(self.templates))
        
        logger.info("TemplateManager initialized")
    
    def get_template(self, template_type: str) -> Dict[str, Any]:
        """Get template configuration for a specific type."""
        template_configs = {
            'modern': {
                'name': 'modern',
                'description': 'Modern, clean design with contemporary elements',
                'sections': ['hero', 'about', 'services', 'contact'],
                'layout': 'single-page',
                'navigation': 'horizontal'
            },
            'portfolio': {
                'name': 'portfolio',
                'description': 'Creative portfolio layout with gallery focus',
                'sections': ['hero', 'about', 'portfolio', 'contact'],
                'layout': 'single-page',
                'navigation': 'horizontal'
            },
            'business': {
                'name': 'business',
                'description': 'Professional business website layout',
                'sections': ['hero', 'about', 'services', 'testimonials', 'contact'],
                'layout': 'single-page',
                'navigation': 'horizontal'
            },
            'landing': {
                'name': 'landing',
                'description': 'High-conversion landing page layout',
                'sections': ['hero', 'features', 'testimonials', 'contact'],
                'layout': 'single-page',
                'navigation': 'minimal'
            },
            'blog': {
                'name': 'blog',
                'description': 'Content-focused blog layout',
                'sections': ['hero', 'about', 'recent-posts', 'contact'],
                'layout': 'multi-page',
                'navigation': 'horizontal'
            },
            'ecommerce': {
                'name': 'ecommerce',
                'description': 'Online store layout with product focus',
                'sections': ['hero', 'featured-products', 'about', 'contact'],
                'layout': 'multi-page',
                'navigation': 'horizontal'
            }
        }
        
        return template_configs.get(template_type, template_configs['modern'])
    
    def get_html_template(self, template_type: str) -> Template:
        """Get Jinja2 template for HTML generation."""
        template_name = f"{template_type}_template.html"
        return self.jinja_env.get_template(template_name)
    
    def _load_templates(self) -> Dict[str, str]:
        """Load all HTML templates."""
        return {
            'modern_template.html': self._get_modern_template(),
            'portfolio_template.html': self._get_portfolio_template(),
            'business_template.html': self._get_business_template(),
            'landing_template.html': self._get_landing_template(),
            'blog_template.html': self._get_blog_template(),
            'ecommerce_template.html': self._get_ecommerce_template(),
            'base_template.html': self._get_base_template()
        }
    
    def _get_base_template(self) -> str:
        """Get base HTML template structure."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <title>{{ title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* CSS will be injected here */
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav-brand">{{ navigation.brand }}</div>
            <div class="nav-menu" id="nav-menu">
                {% for item in navigation.items %}
                <a href="{{ item.href }}" class="nav-link">{{ item.name }}</a>
                {% endfor %}
                <a href="#contact" class="btn btn-primary">Get Started</a>
            </div>
            <button class="mobile-menu-button" id="mobile-menu-button">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </nav>
    </header>

    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                {% for column in footer.columns %}
                <div class="footer-section">
                    <h3>{{ column.title }}</h3>
                    <ul>
                        {% for item in column.items %}
                        <li><a href="{{ item.href if item.href else '#' }}">{{ item.name if item.name else item.value }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
                {% endfor %}
            </div>
            <div class="footer-bottom">
                <p>{{ footer.copyright }}</p>
            </div>
        </div>
    </footer>

    <script>
        /* JavaScript will be injected here */
    </script>
</body>
</html>"""
    
    def _get_modern_template(self) -> str:
        """Get modern website template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <title>{{ title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav-brand">{{ content.navigation.brand }}</div>
                         <div class="nav-menu" id="nav-menu">
                 {% for item in content.navigation.nav_items %}
                 <a href="{{ item.href }}" class="nav-link">{{ item.name }}</a>
                 {% endfor %}
                 <a href="#contact" class="btn btn-primary">Get Started</a>
            </div>
            <button class="mobile-menu-button" id="mobile-menu-button">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="hero">
        <div class="hero-content">
            <h1 class="hero-title">{{ content.hero.headline }}</h1>
            <p class="hero-subtitle">{{ content.hero.subheadline }}</p>
            <a href="#contact" class="btn btn-primary btn-large">{{ content.hero.cta_text }}</a>
        </div>
    </section>

    {% for section in sections %}
    {% if section.name == 'about' %}
    <!-- About Section -->
    <section class="section" id="about">
        <div class="container">
            <div class="grid grid-cols-1 lg:grid-cols-2 items-center">
                <div>
                    <h2 class="section-title text-left">{{ section.content.title }}</h2>
                    <p class="section-content text-left">{{ section.content.content }}</p>
                    {% if section.content.points %}
                    <ul class="mb-lg">
                        {% for point in section.content.points %}
                        <li class="mb-sm">✓ {{ point }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
                <div>
                    <img src="{{ section.image.src }}" alt="{{ section.image.alt }}" class="rounded-lg shadow-lg">
                </div>
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'services' %}
    <!-- Services Section -->
    <section class="section bg-alt" id="services">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {% for service in section.content.services %}
                <div class="card">
                    <h3 class="card-title">{{ service.name }}</h3>
                    <p class="card-content">{{ service.description }}</p>
                    <ul class="card-features">
                        {% for feature in service.features %}
                        <li>{{ feature }}</li>
                        {% endfor %}
                    </ul>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'contact' %}
    <!-- Contact Section -->
    <section class="section" id="contact">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="grid grid-cols-1 lg:grid-cols-2">
                <div>
                    <form id="contact-form" class="mb-lg">
                        {% for field in section.content.form_fields %}
                        <div class="form-group">
                            <label for="{{ field.name }}" class="form-label">{{ field.label }}</label>
                            {% if field.type == 'textarea' %}
                            <textarea id="{{ field.name }}" name="{{ field.name }}" class="form-input form-textarea" {% if field.required %}required{% endif %}></textarea>
                            {% else %}
                            <input type="{{ field.type }}" id="{{ field.name }}" name="{{ field.name }}" class="form-input" {% if field.required %}required{% endif %}>
                            {% endif %}
                        </div>
                        {% endfor %}
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
                <div>
                    <div class="card">
                        <h3 class="card-title">Contact Information</h3>
                        <div class="card-content">
                            <p><strong>Email:</strong> {{ section.content.contact_info.email }}</p>
                            <p><strong>Phone:</strong> {{ section.content.contact_info.phone }}</p>
                            <p><strong>Address:</strong> {{ section.content.contact_info.address }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    {% endif %}
    {% endfor %}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        {% for item in content.footer.links %}
                        <li><a href="{{ item.href }}">{{ item.name }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact</h3>
                    <ul>
                        <li>Email: hello@example.com</li>
                        <li>Phone: +1 (555) 123-4567</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>{{ content.footer.copyright }}</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""
    
    def _get_portfolio_template(self) -> str:
        """Get portfolio website template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <title>{{ title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav-brand">{{ content.navigation.brand }}</div>
                         <div class="nav-menu" id="nav-menu">
                 {% for item in content.navigation.nav_items %}
                 <a href="{{ item.href }}" class="nav-link">{{ item.name }}</a>
                 {% endfor %}
                 <a href="#contact" class="btn btn-primary">Contact Me</a>
            </div>
            <button class="mobile-menu-button" id="mobile-menu-button">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="hero">
        <div class="hero-content">
            <h1 class="hero-title">{{ content.hero.headline }}</h1>
            <p class="hero-subtitle">{{ content.hero.subheadline }}</p>
            <a href="#portfolio" class="btn btn-primary btn-large">{{ content.hero.cta_text }}</a>
        </div>
    </section>

    {% for section in sections %}
    {% if section.name == 'about' %}
    <!-- About Section -->
    <section class="section" id="about">
        <div class="container">
            <div class="grid grid-cols-1 lg:grid-cols-2 items-center">
                <div>
                    <h2 class="section-title text-left">{{ section.content.title }}</h2>
                    <p class="section-content text-left">{{ section.content.content }}</p>
                    {% if section.content.points %}
                    <ul class="mb-lg">
                        {% for point in section.content.points %}
                        <li class="mb-sm">✓ {{ point }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
                <div>
                    <img src="{{ section.image.src }}" alt="{{ section.image.alt }}" class="rounded-lg shadow-lg">
                </div>
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'portfolio' %}
    <!-- Portfolio Section -->
    <section class="section bg-alt" id="portfolio">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {% for project in section.content.projects %}
                <div class="card">
                    <img src="{{ project.image }}" alt="{{ project.name }}" class="gallery-image rounded-lg mb-md">
                    <h3 class="card-title">{{ project.name }}</h3>
                    <p class="card-content">{{ project.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'contact' %}
    <!-- Contact Section -->
    <section class="section" id="contact">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="grid grid-cols-1 lg:grid-cols-2">
                <div>
                    <form id="contact-form" class="mb-lg">
                        {% for field in section.content.form_fields %}
                        <div class="form-group">
                            <label for="{{ field.name }}" class="form-label">{{ field.label }}</label>
                            {% if field.type == 'textarea' %}
                            <textarea id="{{ field.name }}" name="{{ field.name }}" class="form-input form-textarea" {% if field.required %}required{% endif %}></textarea>
                            {% else %}
                            <input type="{{ field.type }}" id="{{ field.name }}" name="{{ field.name }}" class="form-input" {% if field.required %}required{% endif %}>
                            {% endif %}
                        </div>
                        {% endfor %}
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                </div>
                <div>
                    <div class="card">
                        <h3 class="card-title">Contact Information</h3>
                        <div class="card-content">
                            <p><strong>Email:</strong> {{ section.content.contact_info.email }}</p>
                            <p><strong>Phone:</strong> {{ section.content.contact_info.phone }}</p>
                            <p><strong>Address:</strong> {{ section.content.contact_info.address }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    {% endif %}
    {% endfor %}

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        {% for item in content.footer.links %}
                        <li><a href="{{ item.href }}">{{ item.name }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact</h3>
                    <ul>
                        <li>Email: hello@example.com</li>
                        <li>Phone: +1 (555) 123-4567</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>{{ content.footer.copyright }}</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""
    
    def _get_business_template(self) -> str:
        """Get business website template."""
        return self._get_modern_template()  # Use modern template as base for business
    
    def _get_landing_template(self) -> str:
        """Get landing page template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{ description }}">
    <title>{{ title }}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Minimal Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav-brand">{{ content.navigation.brand }}</div>
            <div class="nav-menu">
                <a href="#contact" class="btn btn-primary">Get Started</a>
            </div>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="hero">
        <div class="hero-content">
            <h1 class="hero-title">{{ content.hero.headline }}</h1>
            <p class="hero-subtitle">{{ content.hero.subheadline }}</p>
            <a href="#contact" class="btn btn-primary btn-large">{{ content.hero.cta_text }}</a>
        </div>
    </section>

    {% for section in sections %}
    {% if section.name == 'features' %}
    <!-- Features Section -->
    <section class="section" id="features">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="grid grid-cols-1 md:grid-cols-3">
                {% for service in section.content.services %}
                <div class="card text-center">
                    <h3 class="card-title">{{ service.name }}</h3>
                    <p class="card-content">{{ service.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'testimonials' %}
    <!-- Testimonials Section -->
    <section class="section bg-alt" id="testimonials">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {% for testimonial in section.content.testimonials %}
                <div class="card text-center">
                    <p class="card-content">"{{ testimonial.text }}"</p>
                    <div class="font-semibold">{{ testimonial.author }}</div>
                    <div class="text-light">{{ testimonial.position }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    {% endif %}

    {% if section.name == 'contact' %}
    <!-- Contact Section -->
    <section class="section" id="contact">
        <div class="container">
            <h2 class="section-title">{{ section.content.title }}</h2>
            <p class="section-content">{{ section.content.content }}</p>
            <div class="max-w-md mx-auto">
                <form id="contact-form">
                    {% for field in section.content.form_fields %}
                    <div class="form-group">
                        <label for="{{ field.name }}" class="form-label">{{ field.label }}</label>
                        {% if field.type == 'textarea' %}
                        <textarea id="{{ field.name }}" name="{{ field.name }}" class="form-input form-textarea" {% if field.required %}required{% endif %}></textarea>
                        {% else %}
                        <input type="{{ field.type }}" id="{{ field.name }}" name="{{ field.name }}" class="form-input" {% if field.required %}required{% endif %}>
                        {% endif %}
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-primary w-full">{{ content.hero.cta_text }}</button>
                </form>
            </div>
        </div>
    </section>
    {% endif %}
    {% endfor %}

    <!-- Minimal Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-bottom">
                <p>{{ content.footer.copyright }}</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>"""
    
    def _get_blog_template(self) -> str:
        """Get blog website template."""
        return self._get_modern_template()  # Use modern template as base for blog
    
    def _get_ecommerce_template(self) -> str:
        """Get ecommerce website template."""
        return self._get_modern_template()  # Use modern template as base for ecommerce