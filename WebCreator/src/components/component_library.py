"""
WebCreator Component Library
Manages reusable UI components for website generation.
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class Component:
    """Base class for UI components."""
    
    def __init__(self, name: str, template: str, styles: str = "", scripts: str = ""):
        self.name = name
        self.template = template
        self.styles = styles
        self.scripts = scripts
    
    def render(self, **kwargs) -> str:
        """Render the component with given data."""
        try:
            # Simple template replacement (could be enhanced with Jinja2)
            rendered = self.template
            for key, value in kwargs.items():
                rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
            return rendered
        except Exception as e:
            logger.error(f"Error rendering component {self.name}: {str(e)}")
            return f"<!-- Error rendering {self.name} -->"
    
    def inject_into_html(self, html_content: str, data: Dict[str, Any]) -> str:
        """Inject this component into HTML content."""
        # Simple injection - could be more sophisticated
        return html_content


class ComponentLibrary:
    """Library of reusable UI components."""
    
    def __init__(self):
        """Initialize the component library."""
        self.components = self._load_components()
        logger.info("ComponentLibrary initialized")
    
    def get_component(self, component_name: str) -> Optional[Component]:
        """Get a component by name."""
        return self.components.get(component_name)
    
    def list_components(self) -> List[str]:
        """Get list of available component names."""
        return list(self.components.keys())
    
    def _load_components(self) -> Dict[str, Component]:
        """Load all available components."""
        components = {}
        
        # Header component
        components['header'] = Component(
            name='header',
            template=self._get_header_template(),
            styles=self._get_header_styles()
        )
        
        # Navigation component
        components['navigation'] = Component(
            name='navigation',
            template=self._get_navigation_template(),
            styles=self._get_navigation_styles(),
            scripts=self._get_navigation_scripts()
        )
        
        # Hero section component
        components['hero'] = Component(
            name='hero',
            template=self._get_hero_template(),
            styles=self._get_hero_styles()
        )
        
        # Card component
        components['card'] = Component(
            name='card',
            template=self._get_card_template(),
            styles=self._get_card_styles()
        )
        
        # Button component
        components['button'] = Component(
            name='button',
            template=self._get_button_template(),
            styles=self._get_button_styles()
        )
        
        # Contact form component
        components['contact_form'] = Component(
            name='contact_form',
            template=self._get_contact_form_template(),
            styles=self._get_contact_form_styles(),
            scripts=self._get_contact_form_scripts()
        )
        
        # Image gallery component
        components['image_gallery'] = Component(
            name='image_gallery',
            template=self._get_image_gallery_template(),
            styles=self._get_image_gallery_styles(),
            scripts=self._get_image_gallery_scripts()
        )
        
        # Testimonial component
        components['testimonial'] = Component(
            name='testimonial',
            template=self._get_testimonial_template(),
            styles=self._get_testimonial_styles()
        )
        
        # Footer component
        components['footer'] = Component(
            name='footer',
            template=self._get_footer_template(),
            styles=self._get_footer_styles()
        )
        
        return components
    
    def _get_header_template(self) -> str:
        """Get header component template."""
        return """
        <header class="header">
            <div class="container">
                <div class="header-content">
                    <div class="logo">{{brand_name}}</div>
                    <nav class="main-nav">{{navigation_items}}</nav>
                    <div class="header-actions">{{header_actions}}</div>
                </div>
            </div>
        </header>
        """
    
    def _get_header_styles(self) -> str:
        """Get header component styles."""
        return """
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--color-border);
            z-index: 1000;
        }
        
        .header-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 0;
        }
        """
    
    def _get_navigation_template(self) -> str:
        """Get navigation component template."""
        return """
        <nav class="navigation" role="navigation" aria-label="Main navigation">
            <ul class="nav-list">
                {{nav_items}}
            </ul>
        </nav>
        """
    
    def _get_navigation_styles(self) -> str:
        """Get navigation component styles."""
        return """
        .navigation {
            display: flex;
            align-items: center;
        }
        
        .nav-list {
            display: flex;
            list-style: none;
            margin: 0;
            padding: 0;
            gap: 2rem;
        }
        
        .nav-item {
            position: relative;
        }
        
        .nav-link {
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }
        
        .nav-link:hover {
            color: var(--color-primary);
        }
        """
    
    def _get_navigation_scripts(self) -> str:
        """Get navigation component scripts."""
        return """
        // Mobile navigation toggle
        document.addEventListener('DOMContentLoaded', function() {
            const mobileToggle = document.querySelector('.mobile-nav-toggle');
            const navigation = document.querySelector('.navigation');
            
            if (mobileToggle && navigation) {
                mobileToggle.addEventListener('click', function() {
                    navigation.classList.toggle('active');
                });
            }
        });
        """
    
    def _get_hero_template(self) -> str:
        """Get hero section component template."""
        return """
        <section class="hero">
            <div class="hero-content">
                <h1 class="hero-title">{{title}}</h1>
                <p class="hero-subtitle">{{subtitle}}</p>
                <div class="hero-actions">
                    {{cta_buttons}}
                </div>
            </div>
            <div class="hero-visual">
                {{hero_visual}}
            </div>
        </section>
        """
    
    def _get_hero_styles(self) -> str:
        """Get hero section component styles."""
        return """
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
            color: white;
            position: relative;
            overflow: hidden;
        }
        
        .hero-content {
            flex: 1;
            max-width: 600px;
            z-index: 2;
            position: relative;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 1.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.125rem;
            }
        }
        """
    
    def _get_card_template(self) -> str:
        """Get card component template."""
        return """
        <div class="card {{card_class}}">
            {{card_image}}
            <div class="card-content">
                <h3 class="card-title">{{title}}</h3>
                <p class="card-text">{{text}}</p>
                {{card_actions}}
            </div>
        </div>
        """
    
    def _get_card_styles(self) -> str:
        """Get card component styles."""
        return """
        .card {
            background: var(--color-background);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-md);
            overflow: hidden;
            transition: all 0.3s ease;
            border: 1px solid var(--color-border);
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .card-content {
            padding: 1.5rem;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        .card-text {
            color: var(--color-text-light);
            line-height: 1.6;
        }
        """
    
    def _get_button_template(self) -> str:
        """Get button component template."""
        return """
        <button class="btn {{button_class}}" {{button_attributes}}>
            {{button_icon}}
            <span>{{button_text}}</span>
        </button>
        """
    
    def _get_button_styles(self) -> str:
        """Get button component styles."""
        return """
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            border-radius: var(--border-radius);
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background: var(--color-primary);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--color-primary-dark);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .btn-secondary {
            background: transparent;
            color: var(--color-primary);
            border: 1px solid var(--color-primary);
        }
        
        .btn-secondary:hover {
            background: var(--color-primary);
            color: white;
        }
        
        .btn-large {
            padding: 1rem 2rem;
            font-size: 1.125rem;
        }
        """
    
    def _get_contact_form_template(self) -> str:
        """Get contact form component template."""
        return """
        <form class="contact-form" id="contact-form">
            <div class="form-row">
                <div class="form-group">
                    <label for="name" class="form-label">Name *</label>
                    <input type="text" id="name" name="name" class="form-input" required>
                </div>
                <div class="form-group">
                    <label for="email" class="form-label">Email *</label>
                    <input type="email" id="email" name="email" class="form-input" required>
                </div>
            </div>
            <div class="form-group">
                <label for="subject" class="form-label">Subject</label>
                <input type="text" id="subject" name="subject" class="form-input">
            </div>
            <div class="form-group">
                <label for="message" class="form-label">Message *</label>
                <textarea id="message" name="message" class="form-input form-textarea" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Send Message</button>
        </form>
        """
    
    def _get_contact_form_styles(self) -> str:
        """Get contact form component styles."""
        return """
        .contact-form {
            max-width: 600px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .form-label {
            display: block;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: var(--color-text);
        }
        
        .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--color-border);
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        .form-textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
        """
    
    def _get_contact_form_scripts(self) -> str:
        """Get contact form component scripts."""
        return """
        document.addEventListener('DOMContentLoaded', function() {
            const contactForm = document.getElementById('contact-form');
            
            if (contactForm) {
                contactForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    // Get form data
                    const formData = new FormData(this);
                    const name = formData.get('name');
                    const email = formData.get('email');
                    const message = formData.get('message');
                    
                    // Basic validation
                    if (!name || !email || !message) {
                        alert('Please fill in all required fields.');
                        return;
                    }
                    
                    // Email validation
                                         const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
                    if (!emailRegex.test(email)) {
                        alert('Please enter a valid email address.');
                        return;
                    }
                    
                    // Success message (replace with actual form submission)
                    alert('Thank you for your message! We will get back to you soon.');
                    this.reset();
                });
            }
        });
        """
    
    def _get_image_gallery_template(self) -> str:
        """Get image gallery component template."""
        return """
        <div class="image-gallery">
            <div class="gallery-grid">
                {{gallery_items}}
            </div>
        </div>
        """
    
    def _get_image_gallery_styles(self) -> str:
        """Get image gallery component styles."""
        return """
        .image-gallery {
            width: 100%;
        }
        
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        
        .gallery-item {
            position: relative;
            overflow: hidden;
            border-radius: var(--border-radius-lg);
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .gallery-item:hover {
            transform: scale(1.05);
        }
        
        .gallery-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .gallery-item:hover .gallery-image {
            transform: scale(1.1);
        }
        
        .gallery-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .gallery-item:hover .gallery-overlay {
            opacity: 1;
        }
        """
    
    def _get_image_gallery_scripts(self) -> str:
        """Get image gallery component scripts."""
        return """
        document.addEventListener('DOMContentLoaded', function() {
            const galleryImages = document.querySelectorAll('.gallery-image');
            
            galleryImages.forEach(function(img) {
                img.addEventListener('click', function() {
                    // Create modal for full-size image
                    const modal = document.createElement('div');
                    modal.className = 'gallery-modal';
                    modal.innerHTML = `
                        <div class="modal-backdrop" onclick="this.parentElement.remove()"></div>
                        <div class="modal-content">
                            <img src="${this.src}" alt="${this.alt}" class="modal-image">
                            <button class="modal-close" onclick="this.closest('.gallery-modal').remove()">×</button>
                        </div>
                    `;
                    
                    document.body.appendChild(modal);
                    document.body.style.overflow = 'hidden';
                    
                    // Close modal on escape
                    document.addEventListener('keydown', function(e) {
                        if (e.key === 'Escape') {
                            modal.remove();
                            document.body.style.overflow = '';
                        }
                    });
                });
            });
        });
        """
    
    def _get_testimonial_template(self) -> str:
        """Get testimonial component template."""
        return """
        <div class="testimonial {{testimonial_class}}">
            <div class="testimonial-content">
                <blockquote class="testimonial-quote">
                    "{{quote}}"
                </blockquote>
                <div class="testimonial-author">
                    {{author_image}}
                    <div class="author-info">
                        <div class="author-name">{{author_name}}</div>
                        <div class="author-position">{{author_position}}</div>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _get_testimonial_styles(self) -> str:
        """Get testimonial component styles."""
        return """
        .testimonial {
            background: var(--color-background);
            border-radius: var(--border-radius-lg);
            padding: 2rem;
            box-shadow: var(--shadow-md);
            text-align: center;
        }
        
        .testimonial-quote {
            font-size: 1.125rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            font-style: italic;
            color: var(--color-text-light);
        }
        
        .testimonial-author {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }
        
        .author-image {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .author-name {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .author-position {
            color: var(--color-text-light);
            font-size: 0.875rem;
        }
        """
    
    def _get_footer_template(self) -> str:
        """Get footer component template."""
        return """
        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    {{footer_sections}}
                </div>
                <div class="footer-bottom">
                    <div class="footer-copyright">{{copyright_text}}</div>
                    <div class="footer-social">{{social_links}}</div>
                </div>
            </div>
        </footer>
        """
    
    def _get_footer_styles(self) -> str:
        """Get footer component styles."""
        return """
        .footer {
            background: var(--color-background-alt);
            border-top: 1px solid var(--color-border);
            padding: 3rem 0 1.5rem;
        }
        
        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .footer-section h3 {
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .footer-section ul {
            list-style: none;
        }
        
        .footer-section ul li {
            margin-bottom: 0.5rem;
        }
        
        .footer-section ul li a {
            color: var(--color-text-light);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .footer-section ul li a:hover {
            color: var(--color-primary);
        }
        
        .footer-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 1.5rem;
            border-top: 1px solid var(--color-border);
            color: var(--color-text-light);
        }
        
        @media (max-width: 768px) {
            .footer-bottom {
                flex-direction: column;
                gap: 1rem;
                text-align: center;
            }
        }
        """