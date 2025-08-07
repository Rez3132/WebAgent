"""
WebCreator Style Engine
Generates modern CSS styling with responsive design and theme support.
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class StyleEngine:
    """Generates CSS styles for websites with theme support and responsive design."""
    
    def __init__(self):
        """Initialize the style engine."""
        self.themes = {
            'modern': self._get_modern_theme(),
            'dark': self._get_dark_theme(),
            'minimal': self._get_minimal_theme(),
            'corporate': self._get_corporate_theme(),
            'creative': self._get_creative_theme()
        }
        
        logger.info("StyleEngine initialized")
    
    def generate_styles(self, request, layout_structure: Dict[str, Any]) -> str:
        """
        Generate CSS styles for the website.
        
        Args:
            request: WebsiteRequest object
            layout_structure: Layout structure from LayoutEngine
            
        Returns:
            Complete CSS stylesheet as string
        """
        theme = self.themes.get(request.theme, self.themes['modern'])
        
        css_parts = [
            self._generate_reset_styles(),
            self._generate_base_styles(theme),
            self._generate_layout_styles(layout_structure, theme),
            self._generate_component_styles(layout_structure, theme),
            self._generate_responsive_styles(layout_structure, theme),
            self._generate_utility_styles()
        ]
        
        if request.accessibility:
            css_parts.append(self._generate_accessibility_styles())
        
        css_content = '\n\n'.join(css_parts)
        logger.info("CSS styles generated successfully")
        return css_content
    
    def _get_modern_theme(self) -> Dict[str, Any]:
        """Get modern theme configuration."""
        return {
            'name': 'modern',
            'colors': {
                'primary': '#3B82F6',
                'primary_dark': '#1D4ED8',
                'secondary': '#10B981',
                'accent': '#F59E0B',
                'text': '#111827',
                'text_light': '#6B7280',
                'background': '#FFFFFF',
                'background_alt': '#F9FAFB',
                'border': '#E5E7EB',
                'success': '#10B981',
                'warning': '#F59E0B',
                'error': '#EF4444'
            },
            'typography': {
                'font_family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                'font_size_base': '16px',
                'font_weight_normal': '400',
                'font_weight_medium': '500',
                'font_weight_semibold': '600',
                'font_weight_bold': '700',
                'line_height': '1.6',
                'heading_line_height': '1.2'
            },
            'spacing': {
                'xs': '0.25rem',
                'sm': '0.5rem',
                'md': '1rem',
                'lg': '1.5rem',
                'xl': '2rem',
                'xxl': '3rem'
            },
            'borders': {
                'radius': '0.5rem',
                'radius_sm': '0.25rem',
                'radius_lg': '0.75rem',
                'width': '1px'
            },
            'shadows': {
                'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
            }
        }
    
    def _get_dark_theme(self) -> Dict[str, Any]:
        """Get dark theme configuration."""
        theme = self._get_modern_theme()
        theme['name'] = 'dark'
        theme['colors'].update({
            'primary': '#60A5FA',
            'text': '#F9FAFB',
            'text_light': '#D1D5DB',
            'background': '#111827',
            'background_alt': '#1F2937',
            'border': '#374151'
        })
        return theme
    
    def _get_minimal_theme(self) -> Dict[str, Any]:
        """Get minimal theme configuration."""
        theme = self._get_modern_theme()
        theme['name'] = 'minimal'
        theme['colors'].update({
            'primary': '#000000',
            'secondary': '#666666',
            'accent': '#000000'
        })
        return theme
    
    def _get_corporate_theme(self) -> Dict[str, Any]:
        """Get corporate theme configuration."""
        theme = self._get_modern_theme()
        theme['name'] = 'corporate'
        theme['colors'].update({
            'primary': '#1E40AF',
            'secondary': '#059669',
            'accent': '#DC2626'
        })
        return theme
    
    def _get_creative_theme(self) -> Dict[str, Any]:
        """Get creative theme configuration."""
        theme = self._get_modern_theme()
        theme['name'] = 'creative'
        theme['colors'].update({
            'primary': '#8B5CF6',
            'secondary': '#EC4899',
            'accent': '#F59E0B'
        })
        return theme
    
    def _generate_reset_styles(self) -> str:
        """Generate CSS reset styles."""
        return """/* CSS Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

img {
    max-width: 100%;
    height: auto;
}

button {
    border: none;
    background: none;
    cursor: pointer;
}

a {
    text-decoration: none;
    color: inherit;
}

ul, ol {
    list-style: none;
}"""
    
    def _generate_base_styles(self, theme: Dict[str, Any]) -> str:
        """Generate base styles with theme variables."""
        colors = theme['colors']
        typography = theme['typography']
        
        return f"""/* Base Styles */
:root {{
    --color-primary: {colors['primary']};
    --color-primary-dark: {colors['primary_dark']};
    --color-secondary: {colors['secondary']};
    --color-accent: {colors['accent']};
    --color-text: {colors['text']};
    --color-text-light: {colors['text_light']};
    --color-background: {colors['background']};
    --color-background-alt: {colors['background_alt']};
    --color-border: {colors['border']};
    --color-success: {colors['success']};
    --color-warning: {colors['warning']};
    --color-error: {colors['error']};
    
    --font-family: {typography['font_family']};
    --font-size-base: {typography['font_size_base']};
    --font-weight-normal: {typography['font_weight_normal']};
    --font-weight-medium: {typography['font_weight_medium']};
    --font-weight-semibold: {typography['font_weight_semibold']};
    --font-weight-bold: {typography['font_weight_bold']};
    --line-height: {typography['line_height']};
    --line-height-heading: {typography['heading_line_height']};
    
    --spacing-xs: {theme['spacing']['xs']};
    --spacing-sm: {theme['spacing']['sm']};
    --spacing-md: {theme['spacing']['md']};
    --spacing-lg: {theme['spacing']['lg']};
    --spacing-xl: {theme['spacing']['xl']};
    --spacing-xxl: {theme['spacing']['xxl']};
    
    --border-radius: {theme['borders']['radius']};
    --border-radius-sm: {theme['borders']['radius_sm']};
    --border-radius-lg: {theme['borders']['radius_lg']};
    --border-width: {theme['borders']['width']};
    
    --shadow-sm: {theme['shadows']['sm']};
    --shadow-md: {theme['shadows']['md']};
    --shadow-lg: {theme['shadows']['lg']};
    --shadow-xl: {theme['shadows']['xl']};
}}

body {{
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-normal);
    line-height: var(--line-height);
    color: var(--color-text);
    background-color: var(--color-background);
}}

.container {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}}

@media (min-width: 768px) {{
    .container {{
        padding: 0 var(--spacing-lg);
    }}
}}

@media (min-width: 1024px) {{
    .container {{
        padding: 0 var(--spacing-xl);
    }}
}}"""
    
    def _generate_layout_styles(self, layout_structure: Dict[str, Any], theme: Dict[str, Any]) -> str:
        """Generate layout-specific styles."""
        grid_system = layout_structure.get('grid_system', 'css-grid')
        
        styles = ["""/* Layout Styles */
.section {
    padding: var(--spacing-xxl) 0;
}

.section-title {
    font-size: 2.5rem;
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-heading);
    margin-bottom: var(--spacing-lg);
    text-align: center;
}

.section-content {
    font-size: 1.125rem;
    color: var(--color-text-light);
    text-align: center;
    margin-bottom: var(--spacing-xl);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}"""]
        
        if grid_system == 'css-grid':
            styles.append("""
/* CSS Grid Layout */
.grid {
    display: grid;
    gap: var(--spacing-lg);
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

@media (min-width: 768px) {
    .md\\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
    .md\\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
    .lg\\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
    .lg\\:grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
}""")
        
        return '\n'.join(styles)
    
    def _generate_component_styles(self, layout_structure: Dict[str, Any], theme: Dict[str, Any]) -> str:
        """Generate component-specific styles."""
        components = []
        
        # Header and Navigation
        components.append("""/* Header & Navigation */
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: var(--color-background);
    border-bottom: var(--border-width) solid var(--color-border);
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: all 0.3s ease;
}

.nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md) 0;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: var(--font-weight-bold);
    color: var(--color-primary);
}

.nav-menu {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
}

.nav-link {
    font-weight: var(--font-weight-medium);
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: var(--color-primary);
}

.mobile-menu-button {
    display: none;
    flex-direction: column;
    gap: 4px;
    padding: var(--spacing-sm);
}

.mobile-menu-button span {
    width: 24px;
    height: 2px;
    background: var(--color-text);
    transition: all 0.3s ease;
}

@media (max-width: 767px) {
    .nav-menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: var(--color-background);
        border-top: var(--border-width) solid var(--color-border);
        flex-direction: column;
        padding: var(--spacing-md);
        gap: var(--spacing-md);
    }
    
    .nav-menu.active {
        display: flex;
    }
    
    .mobile-menu-button {
        display: flex;
    }
}""")
        
        # Hero Section
        components.append("""/* Hero Section */
.hero {
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    position: relative;
    margin-top: 80px;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 800px;
    padding: 0 var(--spacing-md);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: var(--font-weight-bold);
    line-height: var(--line-height-heading);
    margin-bottom: var(--spacing-lg);
}

.hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-xl);
    opacity: 0.9;
}

@media (max-width: 767px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
    }
}""")
        
        # Buttons
        components.append("""/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-md) var(--spacing-xl);
    font-weight: var(--font-weight-medium);
    border-radius: var(--border-radius);
    transition: all 0.3s ease;
    cursor: pointer;
    text-decoration: none;
    border: var(--border-width) solid transparent;
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
    border-color: var(--color-primary);
}

.btn-secondary:hover {
    background: var(--color-primary);
    color: white;
}

.btn-large {
    padding: var(--spacing-lg) var(--spacing-xxl);
    font-size: 1.125rem;
}""")
        
        # Cards
        components.append("""/* Cards */
.card {
    background: var(--color-background);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
    padding: var(--spacing-xl);
    transition: all 0.3s ease;
    border: var(--border-width) solid var(--color-border);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-xl);
}

.card-title {
    font-size: 1.5rem;
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--spacing-md);
}

.card-content {
    color: var(--color-text-light);
    margin-bottom: var(--spacing-lg);
}

.card-features {
    list-style: none;
}

.card-features li {
    padding: var(--spacing-sm) 0;
    border-bottom: var(--border-width) solid var(--color-border);
}

.card-features li:last-child {
    border-bottom: none;
}""")
        
        # Forms
        components.append("""/* Forms */
.form-group {
    margin-bottom: var(--spacing-lg);
}

.form-label {
    display: block;
    font-weight: var(--font-weight-medium);
    margin-bottom: var(--spacing-sm);
    color: var(--color-text);
}

.form-input {
    width: 100%;
    padding: var(--spacing-md);
    border: var(--border-width) solid var(--color-border);
    border-radius: var(--border-radius);
    font-size: var(--font-size-base);
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
}""")
        
        # Footer
        components.append("""/* Footer */
.footer {
    background: var(--color-background-alt);
    border-top: var(--border-width) solid var(--color-border);
    padding: var(--spacing-xxl) 0 var(--spacing-xl);
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-xl);
    margin-bottom: var(--spacing-xl);
}

.footer-section h3 {
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--spacing-md);
}

.footer-section ul li {
    padding: var(--spacing-sm) 0;
}

.footer-section a {
    color: var(--color-text-light);
    transition: color 0.3s ease;
}

.footer-section a:hover {
    color: var(--color-primary);
}

.footer-bottom {
    text-align: center;
    padding-top: var(--spacing-lg);
    border-top: var(--border-width) solid var(--color-border);
    color: var(--color-text-light);
}""")
        
        return '\n\n'.join(components)
    
    def _generate_responsive_styles(self, layout_structure: Dict[str, Any], theme: Dict[str, Any]) -> str:
        """Generate responsive styles for different screen sizes."""
        return """/* Responsive Styles */
@media (max-width: 767px) {
    .section {
        padding: var(--spacing-xl) 0;
    }
    
    .section-title {
        font-size: 2rem;
    }
    
    .container {
        padding: 0 var(--spacing-md);
    }
    
    .hero {
        min-height: 70vh;
    }
    
    .card {
        padding: var(--spacing-lg);
    }
}

@media (min-width: 768px) and (max-width: 1023px) {
    .section-title {
        font-size: 2.25rem;
    }
}

@media (min-width: 1024px) {
    .section {
        padding: 4rem 0;
    }
    
    .section-title {
        font-size: 3rem;
    }
}"""
    
    def _generate_utility_styles(self) -> str:
        """Generate utility CSS classes."""
        return """/* Utility Classes */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.font-bold { font-weight: var(--font-weight-bold); }
.font-semibold { font-weight: var(--font-weight-semibold); }
.font-medium { font-weight: var(--font-weight-medium); }

.text-primary { color: var(--color-primary); }
.text-secondary { color: var(--color-secondary); }
.text-light { color: var(--color-text-light); }

.bg-primary { background-color: var(--color-primary); }
.bg-secondary { background-color: var(--color-secondary); }
.bg-alt { background-color: var(--color-background-alt); }

.mb-0 { margin-bottom: 0; }
.mb-sm { margin-bottom: var(--spacing-sm); }
.mb-md { margin-bottom: var(--spacing-md); }
.mb-lg { margin-bottom: var(--spacing-lg); }
.mb-xl { margin-bottom: var(--spacing-xl); }

.mt-0 { margin-top: 0; }
.mt-sm { margin-top: var(--spacing-sm); }
.mt-md { margin-top: var(--spacing-md); }
.mt-lg { margin-top: var(--spacing-lg); }
.mt-xl { margin-top: var(--spacing-xl); }

.hidden { display: none; }
.block { display: block; }
.inline-block { display: inline-block; }
.flex { display: flex; }
.grid { display: grid; }

.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.rounded { border-radius: var(--border-radius); }
.rounded-lg { border-radius: var(--border-radius-lg); }

.shadow-sm { box-shadow: var(--shadow-sm); }
.shadow-md { box-shadow: var(--shadow-md); }
.shadow-lg { box-shadow: var(--shadow-lg); }

.animate-fade-in {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-on-scroll {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease-in-out;
}"""
    
    def _generate_accessibility_styles(self) -> str:
        """Generate accessibility-focused styles."""
        return """/* Accessibility Styles */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

.focus\\:not-sr-only:focus {
    position: static;
    width: auto;
    height: auto;
    padding: 0;
    margin: 0;
    overflow: visible;
    clip: auto;
    white-space: normal;
}

*:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

button:focus,
a:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

@media (prefers-color-scheme: dark) {
    /* Dark mode styles will be handled by theme selection */
}"""