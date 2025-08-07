"""
WebCreator Main Generator
Orchestrates the entire website generation process from description to complete website.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

try:
    from .content_ai import ContentAI
    from .layout_engine import LayoutEngine
    from .style_engine import StyleEngine
    from ..templates.template_manager import TemplateManager
    from ..components.component_library import ComponentLibrary
except ImportError:
    # For direct execution
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from core.content_ai import ContentAI
    from core.layout_engine import LayoutEngine
    from core.style_engine import StyleEngine
    from templates.template_manager import TemplateManager
    from components.component_library import ComponentLibrary

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebsiteRequest:
    """Represents a website generation request with all parameters."""
    
    def __init__(self, description: str, **kwargs):
        self.description = description
        self.website_type = kwargs.get('website_type', 'general')
        self.theme = kwargs.get('theme', 'modern')
        self.color_scheme = kwargs.get('color_scheme', 'auto')
        self.target_audience = kwargs.get('target_audience', 'general')
        self.features = kwargs.get('features', [])
        self.content_tone = kwargs.get('content_tone', 'professional')
        self.responsive = kwargs.get('responsive', True)
        self.accessibility = kwargs.get('accessibility', True)
        self.performance_optimized = kwargs.get('performance_optimized', True)
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'description': self.description,
            'website_type': self.website_type,
            'theme': self.theme,
            'color_scheme': self.color_scheme,
            'target_audience': self.target_audience,
            'features': self.features,
            'content_tone': self.content_tone,
            'responsive': self.responsive,
            'accessibility': self.accessibility,
            'performance_optimized': self.performance_optimized
        }


class GeneratedWebsite:
    """Represents a generated website with all its components."""
    
    def __init__(self):
        self.html_content = ""
        self.css_content = ""
        self.js_content = ""
        self.assets = {}
        self.metadata = {}
        self.structure = {}
        self.generation_time = None
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'html_content': self.html_content,
            'css_content': self.css_content,
            'js_content': self.js_content,
            'assets': self.assets,
            'metadata': self.metadata,
            'structure': self.structure,
            'generation_time': self.generation_time
        }


class WebCreatorGenerator:
    """Main website generator class that orchestrates the creation process."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the WebCreator generator.
        
        Args:
            api_key: OpenAI API key for AI-powered content generation
        """
        self.content_ai = ContentAI(api_key)
        self.layout_engine = LayoutEngine()
        self.style_engine = StyleEngine()
        self.template_manager = TemplateManager()
        self.component_library = ComponentLibrary()
        
        # Generation statistics
        self.stats = {
            'websites_generated': 0,
            'total_generation_time': 0,
            'average_generation_time': 0
        }
        
        logger.info("WebCreator Generator initialized successfully")
    
    def generate_website(self, request: WebsiteRequest) -> GeneratedWebsite:
        """
        Generate a complete website based on the request.
        
        Args:
            request: WebsiteRequest object containing all generation parameters
            
        Returns:
            GeneratedWebsite object containing all generated content
        """
        start_time = datetime.now()
        logger.info(f"Starting website generation: {request.description[:100]}...")
        
        try:
            # Step 1: Analyze request and plan website structure
            logger.info("Step 1: Analyzing request and planning website structure")
            website_plan = self._analyze_and_plan(request)
            logger.info(f"Website plan created with {len(website_plan.get('sections', []))} sections")
            
            # Step 2: Generate content using AI
            logger.info("Step 2: Generating content using AI")
            content_data = self.content_ai.generate_content(request, website_plan)
            logger.info("Content generation completed")
            
            # Step 3: Create layout structure
            logger.info("Step 3: Creating layout structure")
            layout_structure = self.layout_engine.create_layout(website_plan, content_data)
            logger.info("Layout structure created")
            
            # Step 4: Generate styling
            logger.info("Step 4: Generating CSS styles")
            css_content = self.style_engine.generate_styles(request, layout_structure)
            logger.info("CSS styles generated")
            
            # Step 5: Generate HTML
            logger.info("Step 5: Generating HTML content")
            html_content = self._generate_html(layout_structure, content_data, request)
            logger.info("HTML content generated")
            
            # Step 6: Generate JavaScript if needed
            logger.info("Step 6: Generating JavaScript content")
            js_content = self._generate_javascript(request, website_plan)
            logger.info("JavaScript content generated")
            
            # Step 7: Optimize and finalize
            logger.info("Step 7: Optimizing and finalizing website")
            website = self._finalize_website(
                html_content, css_content, js_content, 
                content_data, website_plan, request
            )
            
            # Track generation time
            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()
            website.generation_time = generation_time
            
            # Update statistics
            self._update_stats(generation_time)
            
            logger.info(f"Website generation completed in {generation_time:.2f} seconds")
            return website
            
        except Exception as e:
            logger.error(f"Error during website generation: {str(e)}")
            raise
    
    def _analyze_and_plan(self, request: WebsiteRequest) -> Dict[str, Any]:
        """Analyze the request and create a website plan."""
        # Use AI to analyze the description and determine website structure
        analysis = self.content_ai.analyze_description(request.description)
        
        # Determine website type and appropriate template
        template_type = self._determine_template_type(request, analysis)
        base_template = self.template_manager.get_template(template_type)
        
        # Create website plan
        plan = {
            'website_type': template_type,
            'template': base_template,
            'sections': analysis.get('sections', []),
            'features': analysis.get('features', []) + (request.features if request.features else []),
            'navigation': analysis.get('navigation', {}),
            'pages': analysis.get('pages', ['home']),
            'components_needed': analysis.get('components', []),
            'content_blocks': analysis.get('content_blocks', [])
        }
        
        return plan
    
    def _determine_template_type(self, request: WebsiteRequest, analysis: Dict) -> str:
        """Determine the best template type based on request and analysis."""
        if request.website_type != 'general':
            return request.website_type
            
        # Use AI analysis to determine type
        keywords = analysis.get('keywords', [])
        
        if any(kw in keywords for kw in ['portfolio', 'gallery', 'showcase']):
            return 'portfolio'
        elif any(kw in keywords for kw in ['business', 'company', 'service']):
            return 'business'
        elif any(kw in keywords for kw in ['blog', 'news', 'article']):
            return 'blog'
        elif any(kw in keywords for kw in ['product', 'landing', 'marketing']):
            return 'landing'
        elif any(kw in keywords for kw in ['shop', 'store', 'ecommerce']):
            return 'ecommerce'
        else:
            return 'modern'
    
    def _generate_html(self, layout_structure: Dict, content_data: Dict, request: WebsiteRequest) -> str:
        """Generate the HTML content for the website."""
        template_type = layout_structure.get('template_type', 'modern')
        template = self.template_manager.get_html_template(template_type)
        
        # Prepare template variables
        template_vars = {
            'title': content_data.get('title', 'Generated Website'),
            'description': content_data.get('description', ''),
            'sections': layout_structure.get('sections', []),
            'navigation': layout_structure.get('navigation', {}),
            'content': content_data,
            'theme': request.theme,
            'responsive': request.responsive,
            'accessibility': request.accessibility
        }
        
        # Render template
        html_content = template.render(**template_vars)
        
        # Add components
        components = layout_structure.get('components', [])
        if components:
            for component_name in components:
                component = self.component_library.get_component(component_name)
                if component:
                    html_content = component.inject_into_html(html_content, content_data)
        
        return html_content
    
    def _generate_javascript(self, request: WebsiteRequest, website_plan: Dict) -> str:
        """Generate JavaScript code for interactive features."""
        js_parts = []
        
        # Add basic interactive features
        js_parts.append("""
// WebCreator Generated JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
});
        """)
        
        # Add feature-specific JavaScript
        features = website_plan.get('features', [])
        
        if 'contact_form' in features:
            js_parts.append(self._get_contact_form_js())
        
        if 'image_gallery' in features:
            js_parts.append(self._get_gallery_js())
        
        if 'animations' in features:
            js_parts.append(self._get_animation_js())
        
        return '\n\n'.join(js_parts)
    
    def _get_contact_form_js(self) -> str:
        """Generate JavaScript for contact form functionality."""
        return """
// Contact Form Handling
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic form validation
        const formData = new FormData(this);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');
        
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
        
        // Show success message (in a real implementation, this would submit to a server)
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
    });
}
        """
    
    def _get_gallery_js(self) -> str:
        """Generate JavaScript for image gallery functionality."""
        return """
// Image Gallery
const galleryImages = document.querySelectorAll('.gallery-image');
if (galleryImages.length > 0) {
    galleryImages.forEach(img => {
        img.addEventListener('click', function() {
            // Create modal for full-size image view
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
            modal.innerHTML = `
                <div class="relative max-w-4xl max-h-full p-4">
                    <img src="${this.src}" alt="${this.alt}" class="max-w-full max-h-full object-contain">
                    <button class="absolute top-4 right-4 text-white text-2xl hover:text-gray-300" onclick="this.closest('.fixed').remove()">×</button>
                </div>
            `;
            document.body.appendChild(modal);
            
            // Close on background click
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.remove();
                }
            });
        });
    });
}
        """
    
    def _get_animation_js(self) -> str:
        """Generate JavaScript for scroll animations."""
        return """
// Scroll Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
});
        """
    
    def _finalize_website(self, html: str, css: str, js: str, 
                         content_data: Dict, website_plan: Dict, 
                         request: WebsiteRequest) -> GeneratedWebsite:
        """Finalize the website with optimization and metadata."""
        website = GeneratedWebsite()
        
        # Optimize content if requested
        if request.performance_optimized:
            html = self._optimize_html(html)
            css = self._optimize_css(css)
            js = self._optimize_js(js)
        
        # Set content
        website.html_content = html
        website.css_content = css
        website.js_content = js
        
        # Set metadata
        website.metadata = {
            'title': content_data.get('title', 'Generated Website'),
            'description': content_data.get('description', ''),
            'keywords': content_data.get('keywords', []),
            'generated_at': datetime.now().isoformat(),
            'generator_version': '1.0.0',
            'request_parameters': request.to_dict()
        }
        
        # Set structure info
        website.structure = {
            'template_type': website_plan.get('website_type'),
            'sections': website_plan.get('sections', []),
            'features': website_plan.get('features', []),
            'pages': website_plan.get('pages', ['home'])
        }
        
        return website
    
    def _optimize_html(self, html: str) -> str:
        """Optimize HTML for performance."""
        # Remove extra whitespace while preserving structure
        lines = html.split('\n')
        optimized_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:
                optimized_lines.append(stripped)
        return '\n'.join(optimized_lines)
    
    def _optimize_css(self, css: str) -> str:
        """Optimize CSS for performance."""
        # Remove comments and unnecessary whitespace
        import re
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = re.sub(r'\s+', ' ', css)
        css = css.replace(' {', '{').replace('{ ', '{')
        css = css.replace(' }', '}').replace('} ', '}')
        return css.strip()
    
    def _optimize_js(self, js: str) -> str:
        """Optimize JavaScript for performance."""
        # Basic minification - remove comments and extra whitespace
        import re
        js = re.sub(r'//.*?\n', '\n', js)
        js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
        js = re.sub(r'\s+', ' ', js)
        return js.strip()
    
    def _update_stats(self, generation_time: float):
        """Update generation statistics."""
        self.stats['websites_generated'] += 1
        self.stats['total_generation_time'] += generation_time
        self.stats['average_generation_time'] = (
            self.stats['total_generation_time'] / self.stats['websites_generated']
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get generation statistics."""
        return self.stats.copy()
    
    def export_website(self, website: GeneratedWebsite, output_dir: str) -> str:
        """
        Export the generated website to a directory.
        
        Args:
            website: GeneratedWebsite object to export
            output_dir: Directory to export to
            
        Returns:
            Path to the exported website
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Write HTML file
        with open(output_path / 'index.html', 'w', encoding='utf-8') as f:
            f.write(website.html_content)
        
        # Write CSS file
        with open(output_path / 'styles.css', 'w', encoding='utf-8') as f:
            f.write(website.css_content)
        
        # Write JS file
        if website.js_content:
            with open(output_path / 'script.js', 'w', encoding='utf-8') as f:
                f.write(website.js_content)
        
        # Write metadata
        with open(output_path / 'metadata.json', 'w', encoding='utf-8') as f:
            json.dump(website.metadata, f, indent=2)
        
        # Copy assets if any
        if website.assets:
            assets_dir = output_path / 'assets'
            assets_dir.mkdir(exist_ok=True)
            for asset_name, asset_content in website.assets.items():
                with open(assets_dir / asset_name, 'wb') as f:
                    f.write(asset_content)
        
        logger.info(f"Website exported to {output_path}")
        return str(output_path)